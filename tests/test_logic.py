from technova.logic import recommend_pc_budget, estimate_psu, check_compatibility, build_plan

def test_budget_total():
    assert sum(recommend_pc_budget(300000, "gaming")["allocation"].values()) == 300000

def test_psu():
    assert estimate_psu(170, 450, 100)["suggested_psu_w"] >= 936

def test_compatibility_flags_three_mismatches():
    result = check_compatibility("AM5", "AM4", "DDR5", "DDR4", 320, 300)
    assert not result["compatible"] and len(result["issues"]) == 3

def test_ai_plan():
    assert sum(build_plan(500000, "AI / ML")["allocation"].values()) == 500000
