import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Bioelectric Epigenetics Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00e0ff; }
    .stDataFrame { background-color: #161a23; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚡ Bioelectric Control of Epigenetic Expression")
st.caption("Prototype: Modulating Vm to bypass chemical signaling bottlenecks")

vm = st.slider("Cell Membrane Potential (mV)", min_value=-90, max_value=0, value=-70, step=1)

# Boltzmann curve for voltage-gated channel open probability
V_half = -40.0   # half-activation voltage (mV)
k = 6.0          # slope factor (mV)
open_prob = 1 / (1 + np.exp(-(vm - V_half) / k))

col1, col2 = st.columns(2)
with col1:
    st.metric("Membrane Potential", f"{vm} mV")
with col2:
    st.metric("Ion Channel Open Probability", f"{open_prob*100:.1f}%")

st.subheader("Voltage-Gated Channel Activation Curve")
v_range = np.linspace(-90, 0, 200)
p_range = 1 / (1 + np.exp(-(v_range - V_half) / k))
curve_df = pd.DataFrame({"Membrane Potential (mV)": v_range, "Open Probability": p_range})
st.line_chart(curve_df.set_index("Membrane Potential (mV)"))

st.markdown(f"Current operating point marked at **Vm = {vm} mV**, open probability = **{open_prob:.3f}**")

st.subheader("Cellular State Readout")

if vm <= -60:
    state_data = {
        "Parameter": [
            "Ion Channel State",
            "Metabolic Activity",
            "Epigenetic Methylation",
            "TET Enzyme Activity",
            "Cell Water Structure (Gilbert Ling)",
            "Regenerative Gene Output",
        ],
        "Status": [
            "Closed / Resting",
            "Standard Maintenance",
            "Locked / Stable",
            "Inactive",
            "High - Structured (EZ Water)",
            "Baseline / Quiescent",
        ],
        "Description": [
            "Voltage-gated channels remain closed at hyperpolarized resting potential.",
            "Cell maintains homeostasis with standard ATP turnover.",
            "DNA methylation patterns remain locked, gene expression suppressed.",
            "TET demethylation enzymes are not significantly active.",
            "High degree of exclusion-zone (EZ) water ordering supports stable resting state.",
            "Regenerative and proliferative gene programs remain dormant.",
        ],
    }
else:
    state_data = {
        "Parameter": [
            "Ion Channel State",
            "Metabolic Activity",
            "Epigenetic Methylation",
            "TET Enzyme Activity",
            "Cell Water Structure (Gilbert Ling)",
            "Regenerative Gene Output",
        ],
        "Status": [
            "Open / Activated",
            "Elevated / Shifted",
            "Active Demethylation",
            "Active",
            "Reduced Structure - Disordered",
            "Activated / Upregulated",
        ],
        "Description": [
            "Depolarization opens voltage-gated ion channels, allowing ion flux.",
            "Increased ionic flux drives elevated metabolic and signaling activity.",
            "Epigenetic methylation marks become dynamically removed.",
            "TET enzymes actively catalyze demethylation, exposing regulatory regions.",
            "EZ water structuring is reduced as ionic flux disrupts cell-water organization.",
            "Regenerative gene programs (e.g. dedifferentiation/proliferation markers) are upregulated.",
        ],
    }

df = pd.DataFrame(state_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Note: This is a conceptual prototype dashboard for illustrative purposes only. "
    "The Boltzmann activation curve and table thresholds are simplified representations "
    "intended to demonstrate the proposed bioelectric-to-epigenetic signaling concept."
)
