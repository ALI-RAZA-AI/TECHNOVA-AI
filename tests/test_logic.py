from technova.logic import recommend_pc_budget, estimate_psu, check_compatibility, build_plan, load_gaming_laptops, recommend_gaming_laptops

def test_budget_total():
    assert sum(recommend_pc_budget(300000, "gaming")["allocation"].values()) == 300000

def test_psu():
    assert estimate_psu(170, 450, 100)["suggested_psu_w"] >= 936

def test_compatibility_flags_three_mismatches():
    result = check_compatibility("AM5", "AM4", "DDR5", "DDR4", 320, 300)
    assert not result["compatible"] and len(result["issues"]) == 3

def test_ai_plan():
    assert sum(build_plan(500000, "AI / ML")["allocation"].values()) == 500000


def test_gaming_laptop_dataset_loads():
    df = load_gaming_laptops()
    assert len(df) == 346
    assert df["price"].min() > 0
    assert df["specs_score"].between(0, 100).all()

def test_gaming_laptop_recommendations_respect_budget_and_ram():
    rows = recommend_gaming_laptops(150000, "Gaming", 16, 0, "Any", 8)
    assert rows
    assert len(rows) <= 8
    assert all(row["price"] <= 150000 and row["ram(GB)"] >= 16 for row in rows)
