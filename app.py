import streamlit as st
import pandas as pd
import numpy as np
import math

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dökme Malzeme Hesaplayıcı",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0f1117;
    --surface: #1a1d2e;
    --surface2: #252840;
    --accent: #6c8cff;
    --accent2: #ff6c6c;
    --accent3: #6cffb4;
    --text: #e8eaf6;
    --muted: #8890b5;
    --border: #2d3154;
    --radius: 12px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

h1, h2, h3 { font-family: 'Space Mono', monospace; }

/* HEADER */
.app-header {
    background: linear-gradient(135deg, #1a1d2e 0%, #252840 50%, #1a1d2e 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(108,140,255,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.app-header h1 {
    font-size: 1.8rem;
    margin: 0 0 0.3rem 0;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-header p {
    color: var(--muted);
    margin: 0;
    font-size: 0.95rem;
}

/* CARDS */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    position: relative;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent); }
.card-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.4rem;
}
.card-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    color: var(--text);
    line-height: 1.1;
}
.card-unit {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.2rem;
}

/* METRIC GRID */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    text-align: center;
}
.metric-card.accent-blue { border-color: var(--accent); }
.metric-card.accent-green { border-color: var(--accent3); }
.metric-card.accent-red { border-color: var(--accent2); }

/* SHAPE ITEM */
.shape-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.shape-badge {
    background: var(--accent);
    color: #fff;
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    white-space: nowrap;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* INPUTS */
.stSelectbox > div > div, .stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stSelectbox > div > div:hover, .stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #4a6cf7) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(108,140,255,0.4) !important;
}

/* DIVIDER */
hr { border-color: var(--border); }

/* TABLE */
.stDataFrame {
    border-radius: var(--radius);
    border: 1px solid var(--border) !important;
}

/* SECTION TITLE */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* TAG */
.tag {
    display: inline-block;
    background: rgba(108,140,255,0.15);
    border: 1px solid rgba(108,140,255,0.3);
    color: var(--accent);
    border-radius: 20px;
    padding: 0.1rem 0.6rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
UNIT_FACTORS = {"m": 1.0, "cm": 0.01, "mm": 0.001, "ft": 0.3048, "in": 0.0254}

DENSITY_PRESETS = {
    "Özel giriş": None,
    "── Tahıllar ──": None,
    "Buğday": 780,
    "Mısır": 720,
    "Arpa": 620,
    "Pirinç (ham)": 580,
    "Soya fasulyesi": 750,
    "── İnşaat ──": None,
    "Kum (kuru)": 1600,
    "Kum (ıslak)": 1900,
    "Çakıl": 1800,
    "Çimento": 1500,
    "Beton": 2400,
    "Toprak (kuru)": 1200,
    "Toprak (ıslak)": 1800,
    "Kireçtaşı (kırılmış)": 1550,
    "── Maden / Kimya ──": None,
    "Kömür (antrasit)": 1000,
    "Kömür (bitümlü)": 850,
    "Demir cevheri": 2200,
    "Sodyum klorür (tuz)": 1200,
    "Gübre (amonyum nitrat)": 800,
}

SHAPE_ICONS = {
    "Silindir": "⬤",
    "Koni": "▲",
    "Yarım Koni": "◐",
    "Dikdörtgen Prizma": "▬",
    "Üçgen Prizma": "△",
    "Genel Prizma": "⬡",
    "Küre": "●",
}

# ─────────────────────────────────────────────
# VOLUME CALCULATION FUNCTIONS
# ─────────────────────────────────────────────
def to_meters(val, unit):
    return val * UNIT_FACTORS[unit]

def vol_cylinder(r, h):
    return math.pi * r**2 * h

def vol_cone(r, h):
    return (1/3) * math.pi * r**2 * h

def vol_half_cone(r, h):
    return vol_cone(r, h) / 2

def vol_rect_prism(l, w, h):
    return l * w * h

def vol_tri_prism(b, tri_h, length):
    return 0.5 * b * tri_h * length

def vol_general_prism(area, h):
    return area * h

def vol_sphere(r):
    return (4/3) * math.pi * r**3

def calculate_volume(shape, params, unit):
    f = lambda v: to_meters(v, unit)
    if shape == "Silindir":
        return vol_cylinder(f(params["r"]), f(params["h"]))
    elif shape == "Koni":
        return vol_cone(f(params["r"]), f(params["h"]))
    elif shape == "Yarım Koni":
        return vol_half_cone(f(params["r"]), f(params["h"]))
    elif shape == "Dikdörtgen Prizma":
        return vol_rect_prism(f(params["l"]), f(params["w"]), f(params["h"]))
    elif shape == "Üçgen Prizma":
        return vol_tri_prism(f(params["b"]), f(params["tri_h"]), f(params["length"]))
    elif shape == "Genel Prizma":
        return vol_general_prism(params["area"] * (UNIT_FACTORS[unit]**2), f(params["h"]))
    elif shape == "Küre":
        return vol_sphere(f(params["r"]))
    return 0.0

# ─────────────────────────────────────────────
# 3D VISUALIZATION
# ─────────────────────────────────────────────
def make_cylinder_mesh(r, h, color, opacity=0.6):
    theta = np.linspace(0, 2*np.pi, 40)
    z = np.linspace(0, h, 20)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x = r * np.cos(theta_grid)
    y = r * np.sin(theta_grid)
    return go.Surface(x=x, y=y, z=z_grid, colorscale=[[0, color],[1, color]],
                      opacity=opacity, showscale=False, name="Silindir")

def make_cone_mesh(r, h, color, opacity=0.6):
    theta = np.linspace(0, 2*np.pi, 40)
    z_vals = np.linspace(0, h, 20)
    theta_grid, z_grid = np.meshgrid(theta, z_vals)
    r_grid = r * (1 - z_grid/h)
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    return go.Surface(x=x, y=y, z=z_grid, colorscale=[[0, color],[1, color]],
                      opacity=opacity, showscale=False, name="Koni")

def make_box_mesh(l, w, h, color, opacity=0.6):
    verts = np.array([
        [0,0,0],[l,0,0],[l,w,0],[0,w,0],
        [0,0,h],[l,0,h],[l,w,h],[0,w,h],
    ])
    i = [0,0,0,0,4,4,6,6]
    j = [1,2,3,4,5,6,5,7]
    k = [2,3,1,5,6,7,7,5]
    return go.Mesh3d(x=verts[:,0], y=verts[:,1], z=verts[:,2],
                     i=i, j=j, k=k, color=color, opacity=opacity, name="Dikdörtgen")

def make_sphere_mesh(r, color, opacity=0.6):
    theta = np.linspace(0, np.pi, 30)
    phi = np.linspace(0, 2*np.pi, 40)
    theta_g, phi_g = np.meshgrid(theta, phi)
    x = r * np.sin(theta_g) * np.cos(phi_g)
    y = r * np.sin(theta_g) * np.sin(phi_g)
    z = r * np.cos(theta_g)
    return go.Surface(x=x, y=y, z=z, colorscale=[[0, color],[1, color]],
                      opacity=opacity, showscale=False, name="Küre")

COLORS_3D = [
    "#6c8cff","#ff6c6c","#6cffb4","#ffd66c","#d66cff",
    "#6cd4ff","#ff9f6c","#6cffd4","#ff6ccc","#c4ff6c",
]

def build_3d_figure(shapes_list):
    if not PLOTLY_OK:
        return None
    fig = go.Figure()
    has_trace = False
    all_pts = []

    for idx, item in enumerate(shapes_list):
        color = COLORS_3D[idx % len(COLORS_3D)]
        shape = item["shape"]
        p = item["params"]
        u = item["unit"]
        f = lambda v: to_meters(v, u)
        trace = None
        try:
            if shape == "Silindir":
                trace = make_cylinder_mesh(f(p["r"]), f(p["h"]), color)
                all_pts += [[f(p["r"]), f(p["r"]), f(p["h"])]]
            elif shape in ("Koni", "Yarım Koni"):
                trace = make_cone_mesh(f(p["r"]), f(p["h"]), color)
                all_pts += [[f(p["r"]), f(p["r"]), f(p["h"])]]
            elif shape == "Dikdörtgen Prizma":
                trace = make_box_mesh(f(p["l"]), f(p["w"]), f(p["h"]), color)
                all_pts += [[f(p["l"]), f(p["w"]), f(p["h"])]]
            elif shape == "Küre":
                trace = make_sphere_mesh(f(p["r"]), color)
                all_pts += [[f(p["r"]), f(p["r"]), f(p["r"])*2]]
            else:  # prisms without easy 3D → show a box approximation
                if shape == "Üçgen Prizma":
                    equiv_side = math.sqrt(p["b"] * p["tri_h"])
                    trace = make_box_mesh(f(p["length"]), f(equiv_side), f(equiv_side), color)
                    all_pts += [[f(p["length"]), f(equiv_side), f(equiv_side)]]
                else:
                    side = math.sqrt(p.get("area", 1))
                    trace = make_box_mesh(f(side), f(side), f(p["h"]), color)
                    all_pts += [[f(side), f(side), f(p["h"])]]
        except Exception:
            pass
        if trace:
            fig.add_trace(trace)
            has_trace = True

    if not has_trace:
        fig.add_annotation(text="Henüz şekil eklenmedi", showarrow=False,
                           font=dict(color="#8890b5", size=14))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(15,17,23,0.9)",
            xaxis=dict(showbackground=False, color="#8890b5", title="X (m)"),
            yaxis=dict(showbackground=False, color="#8890b5", title="Y (m)"),
            zaxis=dict(showbackground=False, color="#8890b5", title="Z (m)"),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
        font=dict(family="DM Sans", color="#e8eaf6"),
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "shapes" not in st.session_state:
    st.session_state.shapes = []

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>⚖️ Dökme Malzeme Hesaplayıcı</h1>
    <p>Geometrik şekiller ekleyerek toplam hacim ve kütle hesaplayın — tek veya birleşik yapılar için.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — SHAPE INPUT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-title">🔧 Şekil Ekle</div>', unsafe_allow_html=True)

    shape_choice = st.selectbox("Geometrik Şekil", list(SHAPE_ICONS.keys()),
                                format_func=lambda s: f"{SHAPE_ICONS[s]} {s}")
    unit_choice = st.selectbox("Ölçü Birimi", list(UNIT_FACTORS.keys()))

    st.markdown("**📐 Boyutlar**")
    params = {}

    if shape_choice == "Silindir":
        params["r"] = st.number_input("Yarıçap (r)", min_value=0.001, value=2.0, step=0.1, format="%.3f")
        params["h"] = st.number_input("Yükseklik (h)", min_value=0.001, value=5.0, step=0.1, format="%.3f")
    elif shape_choice == "Koni":
        params["r"] = st.number_input("Taban Yarıçapı (r)", min_value=0.001, value=2.0, step=0.1, format="%.3f")
        params["h"] = st.number_input("Yükseklik (h)", min_value=0.001, value=4.0, step=0.1, format="%.3f")
    elif shape_choice == "Yarım Koni":
        params["r"] = st.number_input("Taban Yarıçapı (r)", min_value=0.001, value=2.0, step=0.1, format="%.3f")
        params["h"] = st.number_input("Yükseklik (h)", min_value=0.001, value=4.0, step=0.1, format="%.3f")
    elif shape_choice == "Dikdörtgen Prizma":
        params["l"] = st.number_input("Uzunluk (l)", min_value=0.001, value=4.0, step=0.1, format="%.3f")
        params["w"] = st.number_input("Genişlik (w)", min_value=0.001, value=3.0, step=0.1, format="%.3f")
        params["h"] = st.number_input("Yükseklik (h)", min_value=0.001, value=2.0, step=0.1, format="%.3f")
    elif shape_choice == "Üçgen Prizma":
        params["b"] = st.number_input("Taban Kenarı (b)", min_value=0.001, value=3.0, step=0.1, format="%.3f")
        params["tri_h"] = st.number_input("Üçgen Yüksekliği (h₁)", min_value=0.001, value=2.0, step=0.1, format="%.3f")
        params["length"] = st.number_input("Prizma Uzunluğu (L)", min_value=0.001, value=5.0, step=0.1, format="%.3f")
    elif shape_choice == "Genel Prizma":
        params["area"] = st.number_input(f"Taban Alanı ({unit_choice}²)", min_value=0.001, value=10.0, step=0.1, format="%.3f")
        params["h"] = st.number_input("Yükseklik (h)", min_value=0.001, value=3.0, step=0.1, format="%.3f")
    elif shape_choice == "Küre":
        params["r"] = st.number_input("Yarıçap (r)", min_value=0.001, value=2.0, step=0.1, format="%.3f")

    # Preview volume
    try:
        preview_vol = calculate_volume(shape_choice, params, unit_choice)
        st.markdown(f"""
        <div style="background:rgba(108,140,255,0.1);border:1px solid rgba(108,140,255,0.3);
                    border-radius:8px;padding:0.6rem 1rem;margin:0.75rem 0;">
            <div style="font-size:0.7rem;color:#8890b5;font-family:'Space Mono';letter-spacing:1px;">ÖNIZLEME HACİM</div>
            <div style="font-size:1.3rem;font-family:'Space Mono';font-weight:700;color:#6c8cff;">
                {preview_vol:,.4f} m³
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    st.markdown('<div class="section-title">🧪 Yoğunluk</div>', unsafe_allow_html=True)
    density_label = st.selectbox("Malzeme Seçimi", [k for k in DENSITY_PRESETS.keys()],
                                  format_func=lambda x: x)
    density_val = DENSITY_PRESETS.get(density_label)

    if density_val is None:
        density = st.number_input("Yoğunluk (kg/m³)", min_value=1.0, value=800.0, step=10.0, format="%.1f")
    else:
        density = float(density_val)
        st.markdown(f'<span class="tag">🔒 {density:.0f} kg/m³</span>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📝 İsim (opsiyonel)</div>', unsafe_allow_html=True)
    shape_name = st.text_input("Şekil Adı / Notu", placeholder="örn: Silo A - Alt Koni")

    st.markdown("---")
    if st.button("➕ Şekil Ekle", use_container_width=True):
        vol = calculate_volume(shape_choice, params, unit_choice)
        mass_kg = vol * density
        st.session_state.shapes.append({
            "id": len(st.session_state.shapes),
            "name": shape_name if shape_name else f"{shape_choice} #{len(st.session_state.shapes)+1}",
            "shape": shape_choice,
            "params": params.copy(),
            "unit": unit_choice,
            "density": density,
            "density_label": density_label if density_val else "Özel",
            "volume_m3": vol,
            "mass_kg": mass_kg,
        })
        st.success(f"✓ {shape_choice} eklendi! ({vol:.4f} m³)")
        st.rerun()

    if st.session_state.shapes:
        st.markdown("---")
        if st.button("🗑️ Tümünü Temizle", use_container_width=True):
            st.session_state.shapes = []
            st.rerun()

# ─────────────────────────────────────────────
# MAIN — METRICS
# ─────────────────────────────────────────────
shapes = st.session_state.shapes

total_vol = sum(s["volume_m3"] for s in shapes)
total_mass_kg = sum(s["mass_kg"] for s in shapes)
total_mass_ton = total_mass_kg / 1000

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card" style="border-color:var(--accent);">
        <div class="card-label">⬡ Toplam Hacim</div>
        <div class="card-value">{total_vol:,.4f}</div>
        <div class="card-unit">m³</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="border-color:var(--accent3);">
        <div class="card-label">⚖️ Toplam Kütle (Ton)</div>
        <div class="card-value">{total_mass_ton:,.3f}</div>
        <div class="card-unit">ton</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card" style="border-color:var(--accent2);">
        <div class="card-label">⚖️ Toplam Kütle (kg)</div>
        <div class="card-value">{total_mass_kg:,.1f}</div>
        <div class="card-unit">kg · {len(shapes)} şekil</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN — SHAPE LIST + 3D
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown('<div class="section-title">📋 Eklenen Şekiller</div>', unsafe_allow_html=True)
    if not shapes:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem;color:#8890b5;
                    border:1px dashed #2d3154;border-radius:12px;">
            <div style="font-size:2.5rem;margin-bottom:0.5rem;">🧊</div>
            <div style="font-family:'Space Mono';font-size:0.85rem;">Henüz şekil eklenmedi</div>
            <div style="font-size:0.8rem;margin-top:0.3rem;">Sol panelden şekil ekleyin</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, s in enumerate(shapes):
            icon = SHAPE_ICONS.get(s["shape"], "◆")
            pct = (s["volume_m3"] / total_vol * 100) if total_vol > 0 else 0
            color = COLORS_3D[i % len(COLORS_3D)]
            st.markdown(f"""
            <div class="card" style="border-left:4px solid {color}; padding:0.85rem 1.25rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="font-weight:600;font-size:1rem;">{icon} {s['name']}</div>
                        <div style="color:#8890b5;font-size:0.8rem;margin-top:0.2rem;">
                            {s['shape']} · {s['density_label']} ({s['density']:.0f} kg/m³) · birim: {s['unit']}
                        </div>
                    </div>
                    <div style="text-align:right;flex-shrink:0;">
                        <div style="font-family:'Space Mono';font-weight:700;color:{color};">{s['volume_m3']:,.4f} m³</div>
                        <div style="font-size:0.8rem;color:#8890b5;">{s['mass_kg']:,.1f} kg</div>
                        <div style="font-size:0.72rem;color:#8890b5;">%{pct:.1f}</div>
                    </div>
                </div>
                <div style="margin-top:0.6rem;background:#2d3154;border-radius:4px;height:4px;overflow:hidden;">
                    <div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🗑 Kaldır", key=f"del_{i}"):
                st.session_state.shapes.pop(i)
                st.rerun()

with right_col:
    st.markdown('<div class="section-title">🔬 3D Görselleştirme</div>', unsafe_allow_html=True)
    if PLOTLY_OK:
        fig3d = build_3d_figure(shapes)
        st.plotly_chart(fig3d, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("3D görselleştirme için plotly paketi gereklidir.")

# ─────────────────────────────────────────────
# RESULTS TABLE
# ─────────────────────────────────────────────
if shapes:
    st.markdown('<div class="section-title">📊 Detaylı Sonuç Tablosu</div>', unsafe_allow_html=True)
    rows = []
    for i, s in enumerate(shapes):
        pct = (s["volume_m3"] / total_vol * 100) if total_vol > 0 else 0
        rows.append({
            "#": i + 1,
            "Ad": s["name"],
            "Şekil": f"{SHAPE_ICONS.get(s['shape'],'')} {s['shape']}",
            "Birim": s["unit"],
            "Hacim (m³)": round(s["volume_m3"], 5),
            "Yoğunluk (kg/m³)": s["density"],
            "Kütle (kg)": round(s["mass_kg"], 2),
            "Kütle (ton)": round(s["mass_kg"] / 1000, 4),
            "Pay (%)": round(pct, 2),
        })

    rows.append({
        "#": "TOPLAM",
        "Ad": "—",
        "Şekil": f"— ({len(shapes)} şekil)",
        "Birim": "—",
        "Hacim (m³)": round(total_vol, 5),
        "Yoğunluk (kg/m³)": "—",
        "Kütle (kg)": round(total_mass_kg, 2),
        "Kütle (ton)": round(total_mass_ton, 4),
        "Pay (%)": 100.0,
    })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Pie chart
    if len(shapes) > 1 and PLOTLY_OK:
        st.markdown('<div class="section-title">🥧 Hacim Dağılımı</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=[s["name"] for s in shapes],
            values=[s["volume_m3"] for s in shapes],
            marker_colors=COLORS_3D[:len(shapes)],
            hole=0.45,
            textinfo="label+percent",
            textfont=dict(family="DM Sans", color="#e8eaf6"),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#e8eaf6"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8eaf6")),
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            annotations=[dict(text=f"{total_vol:,.2f}<br>m³", x=0.5, y=0.5,
                              font=dict(size=14, family="Space Mono", color="#e8eaf6"),
                              showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    elif len(shapes) > 1:
        st.markdown('<div class="section-title">🥧 Hacim Dağılımı</div>', unsafe_allow_html=True)
        for s in shapes:
            pct = s["volume_m3"] / total_vol * 100 if total_vol > 0 else 0
            st.markdown(f"**{s['name']}**: {s['volume_m3']:,.4f} m³ ({pct:.1f}%)")
            st.progress(pct / 100)

    # CSV Export
    st.markdown('<div class="section-title">💾 Dışa Aktar</div>', unsafe_allow_html=True)
    export_df = pd.DataFrame([{k: v for k, v in r.items()} for r in rows])
    csv_bytes = export_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="⬇️ CSV Olarak İndir",
        data=csv_bytes,
        file_name="dokme_malzeme_hesaplama.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr>
<div style="text-align:center;color:#8890b5;font-size:0.78rem;padding:0.75rem 0;font-family:'Space Mono';">
    Dökme Malzeme Hesaplayıcı — Tüm hacimler m³, kütleler kg/ton cinsinden hesaplanır
</div>
""", unsafe_allow_html=True)
