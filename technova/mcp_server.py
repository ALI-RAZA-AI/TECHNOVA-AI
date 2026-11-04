"""TECHNOVA MCP server exposing the tested dashboard functions."""
from mcp.server.fastmcp import FastMCP
from technova.logic import recommend_pc_budget, estimate_psu, check_compatibility, compare_specs, build_plan, load_catalog

mcp = FastMCP("TECHNOVA Gaming & Workstation Intelligence")

@mcp.tool()
def pc_budget_planner(budget_pkr: float, purpose: str, include_monitor: bool = False) -> dict:
    """Allocate a PC budget in PKR for a gaming PC or professional workstation."""
    return recommend_pc_budget(budget_pkr, purpose, include_monitor)

@mcp.tool()
def psu_calculator(cpu_tdp_w: float, gpu_tdp_w: float, other_components_w: float = 100, headroom_percent: float = 30) -> dict:
    """Estimate system power draw and a sensible PSU wattage target."""
    return estimate_psu(cpu_tdp_w, gpu_tdp_w, other_components_w, headroom_percent)

@mcp.tool()
def pc_compatibility_checker(cpu_socket: str, motherboard_socket: str, ram_type: str, motherboard_ram_type: str, gpu_length_mm: float, case_gpu_clearance_mm: float) -> dict:
    """Check CPU socket, RAM generation and graphics-card physical clearance."""
    return check_compatibility(cpu_socket, motherboard_socket, ram_type, motherboard_ram_type, gpu_length_mm, case_gpu_clearance_mm)

@mcp.tool()
def compare_hardware_specs(product_a: str, specs_a_json: str, product_b: str, specs_b_json: str) -> dict:
    """Compare two products using JSON specs supplied by the user."""
    import json
    try:
        a, b = json.loads(specs_a_json), json.loads(specs_b_json)
    except json.JSONDecodeError:
        return {"error": "Specifications must be valid JSON."}
    return compare_specs(product_a, a, product_b, b)

@mcp.tool()
def recommend_workload_build(budget_pkr: float, workload: str, priority: str = "Balanced") -> dict:
    """Create a component budget plan for gaming, AI/ML, 3D, video editing or workstation use."""
    return build_plan(budget_pkr, workload, priority)

@mcp.tool()
def search_sample_catalog(query: str = "", category: str = "All") -> dict:
    """Search the included illustrative sample catalogue; prices are not live market prices."""
    products = load_catalog(); q = query.casefold().strip()
    items = [p for p in products if (not q or q in (p["name"] + " " + p["brand"] + " " + p["category"]).casefold()) and (category == "All" or p["category"] == category)]
    return {"count": len(items), "products": items, "notice": "Illustrative sample data only. No live price, stock or retailer data is claimed."}

if __name__ == "__main__":
    mcp.run(transport="stdio")
