# -*- coding: utf-8 -*-
import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phuoc Son Landslide Susceptibility System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }
    iframe { border: none !important; width: 100% !important; height: 100vh !important; }
</style>
""", unsafe_allow_html=True)

base_dir = os.path.dirname(os.path.abspath(__file__))

def to_b64_uri(rel_path):
    p = os.path.join(base_dir, rel_path)
    if not os.path.exists(p):
        return rel_path
    mime = "image/png" if p.endswith(".png") else "application/json"
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

manifest = json.load(open(os.path.join(base_dir, "cache", "manifest.json"), "r", encoding="utf-8"))
for k, v in manifest.items():
    if "url" in v:
        v["url"] = to_b64_uri(v["url"])
boundary = json.load(open(os.path.join(base_dir, "cache", "phuoc_son_boundary.geojson"), "r", encoding="utf-8"))
inventory = json.load(open(os.path.join(base_dir, "cache", "inventory_polygons.json"), "r", encoding="utf-8"))
static_bundle = json.load(open(os.path.join(base_dir, "cache", "static_bundle.json"), "r", encoding="utf-8"))

for rel_img in [
    "ketqua_img/ROC_3_Models_In_One.png",
    "ketqua_img/PhuocLoc/BieuDo_CapDoSatLo_13_5.png",
    "ketqua_img/PhuocLoc/Fig14/a_VeTinh.png",
    "ketqua_img/PhuocLoc/Fig14/b_DuDoan.png",
    "ketqua_img/PhuocLoc/Fig14/c_SauSK_SatLo.png",
    "ketqua_img/PhuocLoc/Fig15/a_VeTinh.png",
    "ketqua_img/PhuocLoc/Fig15/b_DuDoan.png",
    "ketqua_img/PhuocLoc/Fig15/c_SauSK_SatLo.png",
]:
    html = html.replace(f'src="{rel_img}"', f'src="{to_b64_uri(rel_img)}"')

inject_js = f"""
window.__INLINE_DATA__ = {{
    manifest: {json.dumps(manifest)},
    boundary: {json.dumps(boundary)},
    inventory: {json.dumps(inventory)},
    static_bundle: {json.dumps(static_bundle)}
}};
"""
html = html.replace("<script>", "<script>" + inject_js, 1)
html = html.replace(
    "const res = await fetch('/api/init');",
    "if (window.__INLINE_DATA__) { IS_STATIC_MODE = true; STATIC_BUNDLE = window.__INLINE_DATA__.static_bundle; data = { manifest: window.__INLINE_DATA__.manifest, boundary: window.__INLINE_DATA__.boundary, inventory: window.__INLINE_DATA__.inventory, samples: STATIC_BUNDLE.samples || [] }; } else { const res = await fetch('/api/init');"
).replace(
    "data = await res.json();",
    "data = await res.json(); }",
    1
)

components.html(html, height=920, scrolling=True)
