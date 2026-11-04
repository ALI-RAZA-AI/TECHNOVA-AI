import streamlit as st
import pandas as pd
import plotly.express as px

from technova.logic import (
    load_catalog,
    recommend_pc_budget,
    estimate_psu,
    check_compatibility,
    compare_specs,
    build_plan,
    load_gaming_laptops,
    recommend_gaming_laptops,
)

st.set_page_config(
    page_title="TECHNOVA AI | Hardware Intelligence",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Theme -----------------------------------------
if "tech_theme" not in st.session_state:
    st.session_state.tech_theme = "Dark"

with st.sidebar:
    st.markdown("## 🖥️ TECHNOVA AI")
    st.caption("HARDWARE INTELLIGENCE")
    st.radio("Appearance", ["Dark", "Light"], key="tech_theme", horizontal=True)

dark = st.session_state.tech_theme == "Dark"
theme = {
    "bg": "#080d17" if dark else "#f2f6fc",
    "surface": "#111d30" if dark else "#ffffff",
    "surface2": "#17263b" if dark else "#f7faff",
    "text": "#edf4ff" if dark else "#17283f",
    "muted": "#a7b6ca" if dark else "#5c6f87",
    "line": "#293c56" if dark else "#c5d3e2",
    "accent": "#61d5ff" if dark else "#087eae",
    "sidebar": "#0b1321" if dark else "#ffffff",
    "input": "#17263b" if dark else "#ffffff",
}
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
  --bg: %(bg)s; --surface: %(surface)s; --surface2: %(surface2)s;
  --text: %(text)s; --muted: %(muted)s; --line: %(line)s;
  --accent: %(accent)s; --sidebar: %(sidebar)s; --input: %(input)s;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: var(--sidebar); border-right: 1px solid var(--line); }
[data-testid="stSidebar"] * { color: var(--text); }
h1, h2, h3, h4, p, label, span, div { }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--text); }
p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }
.hero {
  padding: 30px 34px; border: 1px solid var(--line); border-radius: 22px;
  background: linear-gradient(120deg, var(--surface), var(--surface2));
  margin: 4px 0 22px 0;
}
.hero small { color: var(--accent); font-weight: 700; letter-spacing: 2px; }
.hero h1 { margin: 12px 0 4px 0; }
.hero p { margin: 0; color: var(--muted); }
.panel, [data-testid="stMetric"] {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 14px; padding: 16px;
}
[data-testid="stMetric"] label, [data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div { color: var(--text) !important; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
  color: var(--text) !important; font-weight: 600;
}
div[data-baseweb="select"] > div, [data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
  background: var(--input) !important; color: var(--text) !important;
  border-color: var(--line) !important; border-radius: 10px !important;
}
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
  background: var(--surface) !important; color: var(--text) !important;
}
[data-baseweb="menu"] *, [role="option"] { color: var(--text) !important; }
[data-testid="stCheckbox"] label, [data-testid="stToggle"] label,
[data-testid="stRadio"] label { color: var(--text) !important; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
  width: 100%; min-height: 44px; border: 0; border-radius: 11px;
  color: #ffffff !important; font-weight: 700;
  background: linear-gradient(110deg, #087eae, #6558d9);
  transition: filter .15s ease, transform .15s ease;
}
div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
  filter: brightness(1.12); transform: translateY(-1px);
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--line); border-radius: 12px; overflow: hidden;
}

/* Consistent borders and readable surfaces in both themes */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stExpander"],
[data-testid="stPopover"],
[data-testid="stAlert"],
[data-testid="stDataFrame"],
[data-testid="stTable"],
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  border-color: var(--line) !important;
}
[data-testid="stExpander"], [data-testid="stPopover"] {
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
}
[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-testid="stNumberInput"] button,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  border: 1px solid var(--line) !important;
  outline-color: var(--line) !important;
  box-shadow: none !important;
}
[data-testid="stMetric"], .panel, .hero {
  border-color: var(--line) !important;
}
hr { border-top: 1px solid var(--line) !important; }

footer { visibility: hidden; }
</style>
"""
css = css.replace("%(bg)s", theme["bg"]).replace("%(surface)s", theme["surface"]).replace("%(surface2)s", theme["surface2"])
css = css.replace("%(text)s", theme["text"]).replace("%(muted)s", theme["muted"]).replace("%(line)s", theme["line"])
css = css.replace("%(accent)s", theme["accent"]).replace("%(sidebar)s", theme["sidebar"]).replace("%(input)s", theme["input"])
st.markdown(css, unsafe_allow_html=True)

# ----------------------------- Shared helpers -------------------------------
catalog = load_catalog()
pages = [
    "Overview", "Gaming PC Builder", "Workstation Planner",
    "Hardware Explorer", "Gaming Laptop Intelligence", "Compatibility Lab", "MCP Tools & Demo",
]
with st.sidebar:
    st.divider()
    page = st.radio("NAVIGATION", pages, label_visibility="collapsed", key="tech_page")
    st.divider()
    st.success("Application ready")
    st.caption("Designed & developed by **ALI RAZA**")


def hero(title, subtitle):
    st.markdown(
        f'<section class="hero"><small>TECHNOVA INTELLIGENCE SUITE</small>'
        f'<h1>{title}</h1><p>{subtitle}</p></section>',
        unsafe_allow_html=True,
    )


def money(value):
    return f"PKR {value:,.0f}"


def show_plan(result, chart_key):
    if not result or "error" in result:
        st.error((result or {}).get("error", "No result available."))
        return
    st.metric("Planned budget", money(result["budget_pkr"]))
    df = pd.DataFrame(
        {"Component": list(result["allocation"]),
         "Allocation (PKR)": list(result["allocation"].values())}
    )
    st.dataframe(df, width="stretch", hide_index=True)
    fig = px.pie(df, names="Component", values="Allocation (PKR)", hole=0.48)
    fig.update_layout(
        template="plotly_dark" if dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=theme["text"],
        legend_title_text="Components",
        margin=dict(l=8, r=8, t=24, b=8),
    )
    st.plotly_chart(fig, width="stretch", key=chart_key)


# ----------------------------- Overview -------------------------------------
if page == "Overview":
    hero("Build smarter. Compute faster.",
         "Your command center for gaming rigs, AI workstations and PC hardware decisions.")
    cols = st.columns(4)
    for col, label, value in zip(
        cols, ["Hardware profiles", "MCP tools", "Build domains", "Currency"],
        [len(catalog), "8", "7", "PKR"]
    ):
        with col:
            st.metric(label, value)

    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Explore the platform")
        st.markdown(
            '<div class="panel"><h3>🎮 Gaming systems</h3>'
            '<p>Plan balanced builds for 1080p, 1440p and 4K gaming.</p>'
            '<h3>⚡ AI & creator workstations</h3>'
            '<p>Plan GPU-heavy systems for machine learning, 3D rendering and editing.</p>'
            '<h3>🧩 Hardware intelligence</h3>'
            '<p>Explore sample profiles, compare specifications and estimate power needs.</p></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.subheader("Sample gaming allocation")
        sample = recommend_pc_budget(350000, "gaming")
        df = pd.DataFrame(
            {"Component": list(sample["allocation"]),
             "PKR": list(sample["allocation"].values())}
        )
        fig = px.pie(df, names="Component", values="PKR", hole=0.55)
        fig.update_layout(
            template="plotly_dark" if dark else "plotly_white",
            paper_bgcolor="rgba(0,0,0,0)", font_color=theme["text"],
        )
        st.plotly_chart(fig, width="stretch", key="overview_chart")
    st.info("Catalogue prices are illustrative placeholders, not live retailer prices.")

# ----------------------------- Gaming builder -------------------------------
elif page == "Gaming PC Builder":
    hero("Gaming PC Builder", "Turn your budget into a component allocation.")
    form_col, result_col = st.columns([1, 1])
    with form_col:
        with st.form("gaming_build_form"):
            budget = st.number_input("Total budget (PKR)", 50000, 5000000, 350000, 10000)
            resolution = st.selectbox("Gaming target", ["1080p Gaming", "1440p Gaming", "4K Gaming"])
            include = st.checkbox("Include monitor & peripherals")
            submitted = st.form_submit_button("Generate gaming build")
        st.caption("Target: " + resolution)
        if submitted:
            st.session_state.gaming_result = recommend_pc_budget(budget, "gaming", include)
            st.session_state.gaming_target = resolution
    with result_col:
        st.subheader("Your build allocation")
        show_plan(
            st.session_state.get("gaming_result", recommend_pc_budget(350000, "gaming")),
            "gaming_allocation_chart",
        )
    st.caption("This is a budget allocation estimate, not a verified list of currently available parts.")

# ----------------------------- Workstation planner --------------------------
elif page == "Workstation Planner":
    hero("Workstation Planner", "Budget planning for AI/ML, rendering, editing and professional workloads.")
    form_col, result_col = st.columns([1, 1])
    with form_col:
        with st.form("workstation_form"):
            budget = st.number_input("Workstation budget (PKR)", 80000, 10000000, 600000, 25000)
            workload = st.selectbox("Workload", ["AI / ML", "3D Rendering", "Video Editing", "General Workstation"])
            priority = st.selectbox("Priority", ["Balanced", "GPU first", "CPU first"])
            submitted = st.form_submit_button("Create workstation plan")
        if submitted:
            st.session_state.ws_result = build_plan(budget, workload, priority)
    with result_col:
        st.subheader("Your workstation allocation")
        show_plan(
            st.session_state.get("ws_result", build_plan(600000, "AI / ML")),
            "workstation_allocation_chart",
        )

# ----------------------------- Hardware explorer ---------------------------
elif page == "Hardware Explorer":
    hero("Hardware Explorer", "Browse the included sample component catalogue.")
    st.warning("Sample profiles and placeholder prices only; no live retailer inventory.")
    search_col, category_col = st.columns([2, 1])
    with search_col:
        query = st.text_input("Search hardware", placeholder="NVIDIA, Ryzen, DDR5...")
    with category_col:
        category = st.selectbox("Category", ["All", "gpu", "cpu", "ram", "storage"])
    found = [
        item for item in catalog
        if (not query or query.casefold() in
            (item["name"] + " " + item["brand"] + " " + item["category"]).casefold())
        and (category == "All" or item["category"] == category)
    ]
    st.caption(f"{len(found)} matching profiles")
    if not found:
        st.info("No matching hardware profiles. Try another search or category.")
    for item in found:
        with st.expander(item["brand"] + " · " + item["name"]):
            st.metric("Sample price", money(item["sample_price_pkr"]))
            st.json(item["specs"])


# ----------------------------- Gaming laptop intelligence -------------------
elif page == "Gaming Laptop Intelligence":
    hero("Gaming Laptop Intelligence", "Explore 346 cleaned laptop records, discover price/specification patterns and get transparent shortlist recommendations.")
    try:
        laptops = load_gaming_laptops()
    except Exception as exc:
        st.error(f"Could not load the bundled laptop dataset: {exc}")
        st.stop()

    st.caption("Dataset source: uploaded cleaned gaming-laptop CSV · 346 records · Prices shown in Indian rupees (INR ₹), as supplied. Not live retailer prices.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Laptop records", f"{len(laptops):,}")
    m2.metric("Average listed price", f"₹{laptops['price'].mean():,.0f}")
    m3.metric("Median spec score", f"{laptops['specs_score'].median():.0f}/100")
    m4.metric("GPU profiles", f"{laptops['graphics_card'].nunique():,}")

    tab1, tab2, tab3 = st.tabs(["Explore & analyse", "Smart recommendations", "Compare laptops"])
    with tab1:
        st.subheader("Filter the laptop catalogue")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            max_price = st.slider("Maximum price (INR ₹)", int(laptops.price.min()), int(laptops.price.max()), int(laptops.price.max()), step=5000)
        with f2:
            gpu_options = ["All"] + sorted(laptops.graphics_card.dropna().unique().tolist())
            gpu_filter = st.selectbox("Graphics card", gpu_options)
        with f3:
            ram_filter = st.selectbox("Minimum RAM", [0, 8, 16, 24, 32, 64], index=2, format_func=lambda x: "Any" if x == 0 else f"{x} GB")
        with f4:
            score_filter = st.slider("Minimum spec score", 0, 100, 0)
        search_text = st.text_input("Search model, processor or GPU", placeholder="e.g. Lenovo LOQ, Ryzen, RTX 4060")
        filtered = laptops[laptops.price <= max_price].copy()
        filtered = filtered[filtered["ram(GB)"] >= ram_filter]
        filtered = filtered[filtered.specs_score >= score_filter]
        if gpu_filter != "All":
            filtered = filtered[filtered.graphics_card == gpu_filter]
        if search_text.strip():
            mask = (
                filtered["name"].str.contains(search_text, case=False, na=False) |
                filtered["processor"].str.contains(search_text, case=False, na=False) |
                filtered["graphics_card"].str.contains(search_text, case=False, na=False)
            )
            filtered = filtered[mask]
        st.caption(f"{len(filtered)} laptops match your filters.")
        display_cols = ["name","price","specs_score","processor","graphics_card","VRAM(GB)","ram(GB)","ram_version","storage_size","display_size","display_resolution"]
        st.dataframe(filtered[display_cols].sort_values("specs_score", ascending=False), width="stretch", hide_index=True)
        left, right = st.columns(2)
        with left:
            st.subheader("Price distribution")
            fig = px.histogram(filtered, x="price", nbins=20, labels={"price":"Price (INR ₹)"}, template="plotly_dark" if dark else "plotly_white")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color=theme["text"])
            st.plotly_chart(fig, width="stretch", key="laptop_price_hist")
        with right:
            st.subheader("Specification score vs price")
            fig = px.scatter(filtered, x="price", y="specs_score", color="graphics_card", hover_name="name", labels={"price":"Price (INR ₹)","specs_score":"Dataset spec score"}, template="plotly_dark" if dark else "plotly_white")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color=theme["text"], legend_title_text="GPU")
            st.plotly_chart(fig, width="stretch", key="laptop_score_scatter")
        st.subheader("Most common graphics cards")
        gpu_counts = filtered["graphics_card"].value_counts().head(10).rename_axis("Graphics card").reset_index(name="Laptop count")
        if not gpu_counts.empty:
            fig = px.bar(gpu_counts, x="Laptop count", y="Graphics card", orientation="h", template="plotly_dark" if dark else "plotly_white")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color=theme["text"], yaxis={"categoryorder":"total ascending"})
            st.plotly_chart(fig, width="stretch", key="laptop_gpu_bar")

    with tab2:
        st.subheader("Find laptops for your budget and workload")
        st.caption("Recommendations rank matching records with transparent weighted heuristics based on the dataset's spec score, GPU VRAM, RAM, CPU threads and display size. This is not a trained ML prediction.")
        with st.form("laptop_recommend_form"):
            budget = st.number_input("Your maximum budget (INR ₹)", min_value=10000, max_value=2000000, value=150000, step=5000)
            purpose = st.selectbox("Main workload", ["Gaming", "AI/ML", "3D Rendering", "Video Editing", "General use"])
            min_ram = st.selectbox("Minimum RAM", [8,16,24,32,64], index=1)
            min_vram = st.selectbox("Minimum dedicated GPU VRAM", [0,4,6,8,12,16,24], index=0)
            gpu_pref = st.selectbox("GPU preference", ["Any","NVIDIA","AMD","Intel"])
            count = st.slider("Number of recommendations", 3, 15, 8)
            go = st.form_submit_button("Recommend laptops")
        if go:
            st.session_state.laptop_recs = recommend_gaming_laptops(budget, purpose, min_ram, min_vram, gpu_pref, count)
        recs = st.session_state.get("laptop_recs", [])
        if recs:
            rec_df = pd.DataFrame(recs)
            st.success(f"Found {len(rec_df)} matching recommendations.")
            st.dataframe(rec_df[["name","price","specs_score","processor","graphics_card","VRAM(GB)","ram(GB)","display_resolution","recommendation_score"]], width="stretch", hide_index=True)
            best = rec_df.iloc[0]
            st.markdown("**Top ranked match:** " + str(best["name"]))
            st.metric("Listed dataset price", f"₹{best['price']:,.0f}")
        elif "laptop_recs" in st.session_state:
            st.warning("No laptops match those constraints. Increase the budget or relax RAM/VRAM/GPU filters.")

    with tab3:
        st.subheader("Side-by-side laptop comparison")
        options = laptops["name"].drop_duplicates().sort_values().tolist()
        selected = st.multiselect("Choose up to four laptop models", options, max_selections=4)
        if selected:
            comp = laptops[laptops.name.isin(selected)].copy()
            comp = comp[["name","price","specs_score","processor","graphics_card","VRAM(GB)","cores","thread","ram(GB)","ram_version","storage_size","storage_type","display_size","display_resolution","warranty"]]
            st.dataframe(comp.set_index("name").T, width="stretch")
            fig = px.bar(comp, x="name", y="specs_score", color="graphics_card", title="Dataset specification score comparison", template="plotly_dark" if dark else "plotly_white")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color=theme["text"], xaxis_tickangle=-25)
            st.plotly_chart(fig, width="stretch", key="laptop_compare_chart")
        else:
            st.info("Select two to four laptop models to compare their specifications.")
    st.info("Data quality note: this is the supplied cleaned dataset. A specification score is reproduced as provided by the source; it is not independently benchmarked. Prices, availability and configurations may change.")

# ----------------------------- Compatibility lab ---------------------------
elif page == "Compatibility Lab":
    hero("Compatibility Lab", "Run basic component checks and estimate PSU capacity.")
    form_col, result_col = st.columns([1, 1])
    with form_col:
        with st.form("compatibility_form"):
            cpu_socket = st.selectbox("CPU socket", ["AM5", "AM4", "LGA1700", "LGA1851"])
            board_socket = st.selectbox("Motherboard socket", ["AM5", "AM4", "LGA1700", "LGA1851"])
            ram_type = st.selectbox("RAM type", ["DDR4", "DDR5"])
            board_ram = st.selectbox("Board memory support", ["DDR4", "DDR5"])
            gpu_length = st.number_input("GPU length (mm)", 100, 500, 320)
            case_clearance = st.number_input("Case GPU clearance (mm)", 100, 600, 350)
            cpu_tdp = st.number_input("CPU TDP (W)", 0, 600, 170)
            gpu_tdp = st.number_input("GPU TDP (W)", 0, 1000, 300)
            submitted = st.form_submit_button("Run compatibility & PSU checks")
        if submitted:
            st.session_state.compat_result = check_compatibility(
                cpu_socket, board_socket, ram_type, board_ram,
                gpu_length, case_clearance,
            )
            st.session_state.psu_result = estimate_psu(cpu_tdp, gpu_tdp, 100, 30)
    with result_col:
        st.subheader("Compatibility results")
        result = st.session_state.get("compat_result")
        if result:
            if result["compatible"]:
                st.success("Basic compatibility checks passed.")
            else:
                st.error("Potential compatibility issues found.")
            for item in result["checks"]:
                st.write(("✅ " if item["passed"] else "❌ ") + item["name"])
            psu = st.session_state.get("psu_result", {})
            if "error" not in psu:
                a, b, c = st.columns(3)
                a.metric("Estimated load", f'{psu["estimated_load_w"]} W')
                b.metric("Calculated target", f'{psu["calculated_capacity_w"]} W')
                c.metric("Suggested PSU", f'{psu["suggested_psu_w"]} W')
        else:
            st.info("Choose your components and run the checks to see results.")
    st.caption("Basic screening only. Confirm exact model support, connectors, cooling and case dimensions.")

# ----------------------------- MCP demo -------------------------------------
elif page == "MCP Tools & Demo":
    hero("MCP Tools & Demo", "Explore six hardware-planning functions exposed through Model Context Protocol.")
    descriptions = {
        "pc_budget_planner": "Gaming/workstation budget allocation",
        "psu_calculator": "System load and PSU wattage estimate",
        "pc_compatibility_checker": "Socket, RAM and GPU clearance checks",
        "compare_hardware_specs": "Compare two user-supplied specification sets",
        "recommend_workload_build": "Workload-specific build planning",
        "search_sample_catalog": "Search the illustrative sample catalogue",
        "gaming_laptop_recommender": "Recommend laptops from the uploaded dataset (INR)",
        "gaming_laptop_dataset_summary": "Summarize the 346-record laptop dataset",
    }
    for name, description in descriptions.items():
        st.markdown(
            f'<div class="panel"><b>{name}</b><p>{description}</p></div>',
            unsafe_allow_html=True,
        )
    tool = st.selectbox(
        "Try a tool",
        ["PC budget planner", "PSU calculator", "Compatibility checker",
         "Compare specifications", "Workload build", "Search catalogue", "Gaming laptop recommender", "Laptop dataset summary"],
    )
    if tool == "PC budget planner":
        with st.form("mcp_budget_form"):
            amount = st.number_input("Budget (PKR)", 50000, 5000000, 300000, 10000)
            purpose = st.selectbox("Purpose", ["gaming", "workstation"])
            run = st.form_submit_button("Execute budget tool")
        if run:
            st.json(recommend_pc_budget(amount, purpose))
    elif tool == "PSU calculator":
        with st.form("mcp_psu_form"):
            cpu = st.number_input("CPU TDP (W)", 0, 600, 170)
            gpu = st.number_input("GPU TDP (W)", 0, 1000, 450)
            run = st.form_submit_button("Execute PSU tool")
        if run:
            st.json(estimate_psu(cpu, gpu))
    elif tool == "Compatibility checker":
        with st.form("mcp_compat_form"):
            cpu = st.selectbox("CPU socket", ["AM5", "AM4", "LGA1700"])
            board = st.selectbox("Board socket", ["AM5", "AM4", "LGA1700"])
            run = st.form_submit_button("Execute compatibility tool")
        if run:
            st.json(check_compatibility(cpu, board, "DDR5", "DDR5", 320, 350))
    elif tool == "Compare specifications":
        with st.form("mcp_compare_form"):
            name_a = st.text_input("First component name", "Component A")
            name_b = st.text_input("Second component name", "Component B")
            specs_a = st.text_area("First specs (JSON)", '{"cores": 8, "memory_gb": 16}')
            specs_b = st.text_area("Second specs (JSON)", '{"cores": 12, "memory_gb": 24}')
            run = st.form_submit_button("Compare components")
        if run:
            import json
            try:
                st.json(compare_specs(name_a, json.loads(specs_a), name_b, json.loads(specs_b)))
            except (ValueError, TypeError) as exc:
                st.error(f"Invalid JSON: {exc}")
    elif tool == "Workload build":
        with st.form("mcp_workload_form"):
            amount = st.number_input("Workload budget (PKR)", 80000, 10000000, 600000, 25000)
            workload = st.selectbox("Workload", ["AI / ML", "3D Rendering", "Video Editing", "General Workstation", "1080p Gaming", "1440p Gaming", "4K Gaming"])
            priority = st.selectbox("Priority", ["Balanced", "GPU first", "CPU first"])
            run = st.form_submit_button("Recommend workload build")
        if run:
            st.json(build_plan(amount, workload, priority))
    elif tool == "Search catalogue":
        with st.form("mcp_search_form"):
            term = st.text_input("Search catalogue", "NVIDIA")
            run = st.form_submit_button("Search hardware")
        if run:
            matches = [p for p in catalog if term.casefold() in (p["name"] + " " + p["brand"] + " " + p["category"]).casefold()]
            st.json(matches if matches else {"message": "No matching sample hardware."})
    elif tool == "Gaming laptop recommender":
        with st.form("mcp_laptop_form"):
            laptop_budget = st.number_input("Maximum laptop budget (INR ₹)", 10000, 2000000, 150000, 5000)
            laptop_workload = st.selectbox("Workload", ["Gaming", "AI/ML", "3D Rendering", "Video Editing"])
            laptop_ram = st.selectbox("Minimum RAM (GB)", [8, 16, 24, 32, 64], index=1)
            laptop_vram = st.selectbox("Minimum VRAM (GB)", [0, 4, 6, 8, 12, 16, 24])
            run = st.form_submit_button("Recommend from dataset")
        if run:
            st.json({"currency": "INR", "recommendations": recommend_gaming_laptops(laptop_budget, laptop_workload, laptop_ram, laptop_vram), "method": "Weighted heuristic, not ML prediction."})
    else:
        laptops_data = load_gaming_laptops()
        st.json({"records": len(laptops_data), "currency": "INR", "average_price": round(float(laptops_data.price.mean()), 2), "median_price": int(laptops_data.price.median()), "gpu_profiles": int(laptops_data.graphics_card.nunique()), "median_spec_score": float(laptops_data.specs_score.median())})
    st.divider()
    st.markdown("**Run the MCP server locally**")
    st.code("python -m technova.mcp_server", language="bash")
    st.caption("The MCP server uses STDIO. Streamlit hosting does not publish it as a public web endpoint.")

st.divider()
st.caption("TECHNOVA AI · Designed & Developed by ALI RAZA")
