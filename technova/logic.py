from __future__ import annotations
import json, math
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "hardware_catalog.json"

def load_catalog():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))["products"]

def recommend_pc_budget(budget_pkr: float, purpose: str, include_monitor: bool = False) -> dict:
    if not math.isfinite(budget_pkr) or budget_pkr <= 0:
        return {"error": "Budget must be a positive number."}
    purpose = purpose.casefold().strip()
    if purpose not in {"gaming", "workstation"}:
        return {"error": "Purpose must be gaming or workstation."}
    ratios = ({"GPU": .38, "CPU": .18, "Motherboard": .10, "RAM": .08, "Storage": .08, "PSU": .07, "Case & cooling": .06, "Contingency": .05} if purpose == "gaming" else {"GPU": .32, "CPU": .23, "Motherboard": .10, "RAM": .13, "Storage": .10, "PSU": .07, "Case & cooling": .05})
    if include_monitor:
        ratios = {k: v * .88 for k, v in ratios.items()}
        ratios["Monitor & peripherals"] = .12
    result = {k: round(budget_pkr * v) for k, v in ratios.items()}
    drift = round(budget_pkr) - sum(result.values())
    result["Contingency" if "Contingency" in result else "Case & cooling"] += drift
    return {"purpose": purpose, "budget_pkr": round(budget_pkr), "allocation": result}

def estimate_psu(cpu_tdp_w: float, gpu_tdp_w: float, other_w: float = 100, headroom: float = 30) -> dict:
    vals = [cpu_tdp_w, gpu_tdp_w, other_w, headroom]
    if any(not math.isfinite(v) for v in vals) or min(vals) < 0 or headroom > 100:
        return {"error": "Enter finite non-negative values; headroom must be between 0 and 100%."}
    load = cpu_tdp_w + gpu_tdp_w + other_w
    target = load * (1 + headroom / 100)
    standards = [450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1200, 1300, 1500, 1600]
    return {"estimated_load_w": round(load), "calculated_capacity_w": math.ceil(target), "suggested_psu_w": next((x for x in standards if x >= target), math.ceil(target / 100) * 100)}

def check_compatibility(cpu_socket, board_socket, ram_type, board_ram, gpu_length, case_clearance, board_form="", supported_forms=""):
    checks = [("CPU socket", cpu_socket.strip().casefold() == board_socket.strip().casefold()), ("Memory generation", ram_type.strip().casefold() == board_ram.strip().casefold()), ("GPU clearance", float(gpu_length) <= float(case_clearance))]
    if board_form and supported_forms:
        supported = [x.strip().casefold() for x in supported_forms.split(",")]
        checks.append(("Motherboard form factor", board_form.strip().casefold() in supported))
    issues = [name + " check failed" for name, ok in checks if not ok]
    return {"compatible": not issues, "checks": [{"name": n, "passed": ok} for n, ok in checks], "issues": issues}

def compare_specs(name_a, specs_a, name_b, specs_b):
    if not isinstance(specs_a, dict) or not isinstance(specs_b, dict):
        return {"error": "Both specification sets must be JSON objects."}
    keys = sorted(set(specs_a) | set(specs_b))
    return {"comparison": [{"specification": k, name_a: specs_a.get(k, "Not supplied"), name_b: specs_b.get(k, "Not supplied")} for k in keys]}

def build_plan(budget, workload, priority="balanced"):
    if budget <= 0:
        return {"error": "Budget must be positive."}
    if workload not in {"1080p Gaming", "1440p Gaming", "4K Gaming", "AI / ML", "3D Rendering", "Video Editing", "General Workstation"}:
        return {"error": "Unsupported workload."}
    workstation = workload in {"AI / ML", "3D Rendering", "Video Editing", "General Workstation"}
    ratios = ({"GPU": .40, "CPU": .17, "RAM": .08, "Motherboard": .09, "Storage": .08, "PSU": .07, "Case & cooling": .06, "Reserve": .05} if not workstation else {"GPU": .30, "CPU": .23, "RAM": .14, "Motherboard": .09, "Storage": .10, "PSU": .07, "Case & cooling": .07})
    if workload == "AI / ML":
        ratios = {"GPU": .38, "CPU": .20, "RAM": .12, "Motherboard": .09, "Storage": .10, "PSU": .06, "Case & cooling": .05}
    if priority == "GPU first":
        shift = min(.05, ratios["CPU"] - .01); ratios["CPU"] -= shift; ratios["GPU"] += shift
    elif priority == "CPU first":
        shift = min(.05, ratios["GPU"] - .01); ratios["GPU"] -= shift; ratios["CPU"] += shift
    values = {k: round(budget * v) for k, v in ratios.items()}
    key = "Reserve" if "Reserve" in values else "Case & cooling"
    values[key] += round(budget) - sum(values.values())
    return {"workload": workload, "budget_pkr": round(budget), "allocation": values}


# ---------------------- Gaming laptop dataset intelligence ------------------
import base64
import gzip
import io
import pandas as pd

LAPTOP_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gaming_laptops.csv.gz.b64"

def load_gaming_laptops() -> pd.DataFrame:
    """Load the cleaned 346-row laptop dataset bundled as gzip+base64 text."""
    encoded = LAPTOP_DATA_PATH.read_text(encoding="utf-8").strip()
    raw = gzip.decompress(base64.b64decode(encoded))
    frame = pd.read_csv(io.BytesIO(raw))
    for col in frame.select_dtypes(include="object").columns:
        frame[col] = frame[col].astype(str).str.strip()
    return frame

def recommend_gaming_laptops(budget_inr: float, purpose: str = "Gaming", min_ram_gb: int = 8,
                             min_vram_gb: int = 0, preferred_gpu: str = "Any",
                             limit: int = 10) -> list[dict]:
    """Rank dataset laptops within an INR budget using transparent specification heuristics."""
    df = load_gaming_laptops()
    if budget_inr <= 0:
        return []
    candidates = df[df["price"] <= budget_inr].copy()
    candidates = candidates[(candidates["ram(GB)"] >= min_ram_gb) & (candidates["VRAM(GB)"] >= min_vram_gb)]
    if preferred_gpu != "Any":
        candidates = candidates[candidates["graphics_card"].str.contains(preferred_gpu, case=False, na=False)]
    if candidates.empty:
        return []
    purpose = purpose.casefold()
    if purpose in {"ai/ml", "machine learning", "3d rendering"}:
        candidates["recommendation_score"] = (
            candidates["specs_score"] * 0.25 + candidates["VRAM(GB)"] * 3.0 +
            candidates["ram(GB)"] * 0.55 + candidates["thread"] * 0.35
        )
    elif purpose in {"editing", "content creation", "video editing"}:
        candidates["recommendation_score"] = (
            candidates["specs_score"] * 0.45 + candidates["ram(GB)"] * 0.75 +
            candidates["display_size"] * 0.8 + candidates["thread"] * 0.25
        )
    else:
        candidates["recommendation_score"] = (
            candidates["specs_score"] * 0.65 + candidates["VRAM(GB)"] * 2.0 +
            candidates["ram(GB)"] * 0.45
        )
    candidates["value_score"] = candidates["specs_score"] / (candidates["price"] / 100000)
    candidates = candidates.sort_values(["recommendation_score", "value_score"], ascending=False)
    cols = ["name","price","specs_score","processor","graphics_card","VRAM(GB)","ram(GB)",
            "ram_version","storage_size","storage_type","display_size","display_resolution",
            "warranty","recommendation_score","value_score"]
    return candidates[cols].head(max(1, min(int(limit), 50))).to_dict("records")

def compare_gaming_laptops(names: list[str]) -> list[dict]:
    """Return exact or partial name matches for laptop comparison."""
    df = load_gaming_laptops()
    chosen = []
    for name in names[:4]:
        match = df[df["name"].str.casefold() == str(name).casefold()]
        if match.empty:
            match = df[df["name"].str.contains(str(name), case=False, na=False)].head(1)
        if not match.empty:
            chosen.append(match.iloc[0].to_dict())
    return chosen
