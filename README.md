# TECHNOVA AI — Gaming & Workstation Hardware Intelligence

**Designed & developed by ALI RAZA**

A Streamlit dashboard and Python MCP server for gaming PC planning, workstation budget planning, sample hardware exploration, basic compatibility checks, PSU estimation, and MCP tool exposure.

## Deploy the dashboard free with Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Select repository `ALI-RAZA-AI/TECHNOVA-AI`, branch `main`, and main file `app.py`.
3. Select **Deploy**. Streamlit installs dependencies from `requirements.txt`.

The dashboard is hosted separately from the MCP STDIO server. Streamlit Community Cloud does not expose the MCP server as a web endpoint.

## Run locally (Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Run the MCP server

```powershell
python -m technova.mcp_server
```

The MCP server uses STDIO transport and is intended for an MCP-compatible host/client.

## Run tests

```powershell
pytest -q
```

## Features

- Overview dashboard with component budget visualization.
- Gaming PC Builder for budget planning.
- Workstation Planner for AI/ML, 3D rendering, video editing and general workstation workloads.
- Hardware Explorer with search and category filtering.
- Compatibility Lab for CPU socket, RAM generation and GPU clearance.
- PSU wattage calculator.
- MCP Tools & Demo page and six MCP server tools.
- Dark / Light interface theme switch.

## MCP tools

- `pc_budget_planner`
- `psu_calculator`
- `pc_compatibility_checker`
- `compare_hardware_specs`
- `recommend_workload_build`
- `search_sample_catalog`

## Data and limitations

The included hardware catalogue is illustrative sample data. Product profiles and PKR prices are placeholders, not current retail listings. The app does not claim live pricing, stock, benchmark FPS or retailer integrations. Build allocations are heuristics, not verified parts lists. Validate exact models, BIOS support, RAM QVL, PSU connectors, cooling, dimensions and vendor documentation before purchase.

No paid API key is required. An LLM-backed autonomous agent, live retailer adapters and live market feeds are not included in this demonstrator.
