import streamlit as st
import pandas as pd
import plotly.express as px
from technova.logic import load_catalog, recommend_pc_budget, estimate_psu, check_compatibility, compare_specs, build_plan

st.set_page_config(page_title="TECHNOVA AI | Hardware Intelligence", page_icon="🖥️", layout="wide")
if "tech_theme" not in st.session_state: st.session_state.tech_theme = "Dark"
st.sidebar.markdown("## 🖥️ TECHNOVA **AI**")
st.sidebar.caption("HARDWARE INTELLIGENCE")
st.sidebar.radio("Appearance", ["Dark", "Light"], key="tech_theme", horizontal=True)
dark = st.session_state.tech_theme == "Dark"
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{{--bg:{'#080d17' if dark else '#f3f6fb'};--surface:{'#111d30' if dark else '#fff'};--surface2:{'#15243a' if dark else '#f7f9fd'};--text:{'#edf4ff' if dark else '#17283f'};--muted:{'#91a4bf' if dark else '#60738c'};--line:{'#263954' if dark else '#dce5f0'};--accent:{'#61d5ff' if dark else '#087eae'};--sidebar:{'#0b1321' if dark else '#fff'};--input:{'#101c2d' if dark else '#fff'};}}
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif}}
.stApp{{background:radial-gradient(circle at 85% 0%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 35%),var(--bg);color:var(--text)}}
[data-testid="stSidebar"]{{background:var(--sidebar);border-right:1px solid var(--line)}} [data-testid="stSidebar"] *{{color:var(--text)}}
h1,h2,h3{{font-family:'Space Grotesk',sans-serif!important;color:var(--text)!important}}
.hero{{padding:32px 36px;border:1px solid var(--line);border-radius:22px;background:linear-gradient(120deg,var(--surface),var(--surface2));margin-bottom:22px}}
.hero small{{color:var(--accent);font-weight:700;letter-spacing:2px}} .hero p,.muted{{color:var(--muted)}}
.panel{{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;margin:8px 0}}
div.stButton>button{{border-radius:10px;background:linear-gradient(110deg,#087eae,#6558d9);color:white;border:0;font-weight:700}}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input{{background:var(--input);color:var(--text)}}
div[data-testid="stMetric"]{{background:var(--surface);border:1px solid var(--line);padding:14px;border-radius:12px}}
</style>""", unsafe_allow_html=True)

catalog=load_catalog()
pages=["Overview","Gaming PC Builder","Workstation Planner","Hardware Explorer","Compatibility Lab","MCP Tools & Demo"]
with st.sidebar:
    page=st.radio("NAVIGATION",pages,label_visibility="collapsed")
    st.divider()
    st.success("Application ready")
    st.caption("Designed & developed by **ALI RAZA**")

def hero(title,subtitle):
    st.markdown(f'<div class="hero"><small>TECHNOVA INTELLIGENCE SUITE</small><h1>{title}</h1><p>{subtitle}</p></div>',unsafe_allow_html=True)
def money(n): return f"PKR {n:,.0f}"
def show_plan(result):
    if "error" in result: st.error(result["error"]); return
    st.metric("Planned budget",money(result["budget_pkr"]))
    df=pd.DataFrame({"Component":list(result["allocation"]),"Allocation (PKR)":list(result["allocation"].values())})
    st.dataframe(df,use_container_width=True,hide_index=True)
    fig=px.pie(df,names="Component",values="Allocation (PKR)",hole=.48)
    fig.update_layout(template="plotly_dark" if dark else "plotly_white",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,use_container_width=True)

if page=="Overview":
    hero("Build smarter. Compute faster.","Your command center for gaming rigs, AI workstations and PC hardware decisions.")
    a,b,c,d=st.columns(4)
    for col,label,value in zip((a,b,c,d),("Hardware profiles","MCP tools","Build domains","Currency"),(len(catalog),"6","7","PKR")):
        with col: st.metric(label,value)
    left,right=st.columns([1.2,1])
    with left:
        st.markdown("### Explore the platform")
        st.markdown('<div class="panel"><h3>🎮 Gaming systems</h3><p class="muted">Plan balanced builds for 1080p, 1440p and 4K gaming.</p><h3>⚡ AI & creator workstations</h3><p class="muted">Plan GPU-heavy systems for machine learning, 3D rendering and editing.</p><h3>🧩 Hardware intelligence</h3><p class="muted">Explore sample profiles, compare specifications and estimate power requirements.</p></div>',unsafe_allow_html=True)
    with right:
        st.markdown("### Sample budget allocation")
        df=pd.DataFrame({"Component":list(recommend_pc_budget(350000,"gaming")["allocation"]),"PKR":list(recommend_pc_budget(350000,"gaming")["allocation"].values())})
        fig=px.pie(df,names="Component",values="PKR",hole=.55)
        fig.update_layout(template="plotly_dark" if dark else "plotly_white",paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig,use_container_width=True)
    st.info("Catalogue prices are illustrative placeholders, not live retailer prices.")
elif page=="Gaming PC Builder":
    hero("Gaming PC Builder","Turn your budget into a component allocation.")
    x,y=st.columns(2)
    with x:
        budget=st.number_input("Total budget (PKR)",50000,5000000,350000,10000)
        resolution=st.selectbox("Gaming target",["1080p Gaming","1440p Gaming","4K Gaming"])
        include=st.toggle("Include monitor & peripherals")
        st.caption("Target: "+resolution)
        if st.button("Generate gaming build",use_container_width=True): st.session_state.gaming_result=recommend_pc_budget(budget,"gaming",include)
    with y: show_plan(st.session_state.get("gaming_result",recommend_pc_budget(350000,"gaming")))
elif page=="Workstation Planner":
    hero("Workstation Planner","Budget planning for AI/ML, rendering, editing and professional workloads.")
    x,y=st.columns(2)
    with x:
        budget=st.number_input("Workstation budget (PKR)",80000,10000000,600000,25000)
        workload=st.selectbox("Workload",["AI / ML","3D Rendering","Video Editing","General Workstation"])
        priority=st.selectbox("Priority",["Balanced","GPU first","CPU first"])
        if st.button("Create workstation plan",use_container_width=True): st.session_state.ws_result=build_plan(budget,workload,priority)
    with y: show_plan(st.session_state.get("ws_result",build_plan(600000,"AI / ML")))
elif page=="Hardware Explorer":
    hero("Hardware Explorer","Browse the included sample component catalogue.")
    st.warning("Sample class-level profiles and placeholder prices only.")
    q=st.text_input("Search hardware",placeholder="NVIDIA, Ryzen, DDR5...")
    cat=st.selectbox("Category",["All","gpu","cpu","ram","storage"])
    found=[p for p in catalog if (not q or q.casefold() in (p["name"]+" "+p["brand"]+" "+p["category"]).casefold()) and (cat=="All" or p["category"]==cat)]
    st.caption(f"{len(found)} matching profiles")
    for p in found:
        with st.expander(p["brand"]+" · "+p["name"]):
            st.metric("Sample price",money(p["sample_price_pkr"])); st.json(p["specs"])
elif page=="Compatibility Lab":
    hero("Compatibility Lab","Run basic component checks and estimate PSU capacity.")
    l,r=st.columns(2)
    with l:
        cpu=st.selectbox("CPU socket",["AM5","AM4","LGA1700","LGA1851"])
        board=st.selectbox("Motherboard socket",["AM5","AM4","LGA1700","LGA1851"])
        ram=st.selectbox("RAM type",["DDR4","DDR5"])
        boardram=st.selectbox("Board memory support",["DDR4","DDR5"])
    with r:
        gpu=st.number_input("GPU length (mm)",100,500,320)
        clearance=st.number_input("Case GPU clearance (mm)",100,600,350)
        cpuw=st.number_input("CPU TDP (W)",0,600,170)
        gpuw=st.number_input("GPU TDP (W)",0,1000,300)
    if st.button("Run compatibility & PSU checks",use_container_width=True):
        result=check_compatibility(cpu,board,ram,boardram,gpu,clearance)
        (st.success if result["compatible"] else st.error)("Basic compatibility checks passed." if result["compatible"] else "Potential compatibility issues found.")
        for item in result["checks"]: st.write(("✅ " if item["passed"] else "❌ ")+item["name"])
        psu=estimate_psu(cpuw,gpuw,100,30)
        a,b,c=st.columns(3)
        a.metric("Estimated load",f'{psu["estimated_load_w"]} W'); b.metric("Calculated target",f'{psu["calculated_capacity_w"]} W'); c.metric("Suggested PSU",f'{psu["suggested_psu_w"]} W')
        st.caption("Basic screening only. Confirm exact model support, connectors, cooling and case dimensions.")
elif page=="MCP Tools & Demo":
    hero("MCP Tools & Demo","Six hardware-planning functions exposed through Model Context Protocol.")
    descriptions={"pc_budget_planner":"Gaming/workstation budget allocation","psu_calculator":"System load and PSU wattage estimate","pc_compatibility_checker":"Socket, RAM and GPU clearance checks","compare_hardware_specs":"Compare user-supplied specifications","recommend_workload_build":"Workload-specific build planning","search_sample_catalog":"Search the illustrative sample catalogue"}
    for name,desc in descriptions.items(): st.markdown(f'<div class="panel"><b>{name}</b><p class="muted">{desc}</p></div>',unsafe_allow_html=True)
    choice=st.selectbox("Try a tool",["PC budget planner","PSU calculator","Compatibility checker"])
    if choice=="PC budget planner":
        budget=st.number_input("Budget (PKR)",50000,5000000,300000,10000); purpose=st.selectbox("Purpose",["gaming","workstation"])
        if st.button("Execute budget tool"): st.json(recommend_pc_budget(budget,purpose))
    elif choice=="PSU calculator":
        cpu=st.number_input("CPU TDP",0,600,170); gpu=st.number_input("GPU TDP",0,1000,450)
        if st.button("Execute PSU tool"): st.json(estimate_psu(cpu,gpu))
    else:
        cpu=st.selectbox("CPU socket",["AM5","AM4","LGA1700"]); board=st.selectbox("Board socket",["AM5","AM4","LGA1700"])
        if st.button("Execute compatibility tool"): st.json(check_compatibility(cpu,board,"DDR5","DDR5",320,350))
    st.markdown("**Start MCP server**")
    st.code("python -m technova.mcp_server",language="bash")
    st.caption("MCP server uses STDIO. Streamlit hosting does not publish this as a web endpoint.")
st.divider()
st.caption("TECHNOVA AI · Designed & Developed by ALI RAZA")
