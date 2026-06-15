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

st.info(
    "This dashboard is a conceptual model exploring how changes in cell membrane potential "
    "may influence ion channel activity and downstream cellular state, including metabolism, "
    "methylation status, and regenerative gene expression. All readouts below are conceptual "
    "predictions, not measured data."
)

vm = st.slider("Cell Membrane Potential (mV)", min_value=-90, max_value=0, value=-70, step=1)

st.caption(
    "Resting / Stable: -90 to -60 mV   |   Transition / Signaling-sensitive: -60 to -40 mV   |   "
    "Activated / Plastic: -40 to -20 mV   |   High activation / Stress-remodeling: -20 to 0 mV"
)

st.markdown(
    "**Model logic:** membrane potential is converted into ion channel open probability using a "
    "simplified Boltzmann activation function, then mapped onto conceptual downstream cellular-state predictions."
)

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

import altair as alt

line = (
    alt.Chart(curve_df)
    .mark_line(color="#00e0ff")
    .encode(x="Membrane Potential (mV)", y="Open Probability")
)
point_df = pd.DataFrame({"Membrane Potential (mV)": [vm], "Open Probability": [open_prob]})
point = (
    alt.Chart(point_df)
    .mark_circle(color="red", size=100)
    .encode(x="Membrane Potential (mV)", y="Open Probability")
)
st.altair_chart((line + point).properties(height=350), use_container_width=True)

st.markdown(f"Current operating point marked at **Vm = {vm} mV**, open probability = **{open_prob:.3f}**")

# Bioelectric state zones
if vm <= -60:
    zone_label = "Resting / Stable / Quiescent (-90 to -60 mV)"
elif vm <= -40:
    zone_label = "Transition / Signaling-Sensitive (-60 to -40 mV)"
elif vm <= -20:
    zone_label = "Activated / Plastic / Remodeling (-40 to -20 mV)"
else:
    zone_label = "High Activation / Stress or Regeneration, Context-Dependent (-20 to 0 mV)"

st.markdown(f"**Bioelectric State Zone:** {zone_label}")

st.subheader("Cellular State Readout (Conceptual Predictions)")

if vm <= -60:
    state_data = {
        "Parameter": [
            "Ion Channel State",
            "Metabolic Activity",
            "Epigenetic Methylation",
            "TET Enzyme Activity",
            "Cell Water / Cytoplasmic Organization",
            "Regenerative Gene Output",
        ],
        "Status": [
            "Closed / Resting",
            "Standard Maintenance",
            "Associated with Stable / Repressed Expression",
            "Low Predicted Activity",
            "High - Structured (Conceptual)",
            "Baseline / Quiescent",
        ],
        "Description": [
            "Voltage-gated channels are predicted to remain closed at hyperpolarized resting potential.",
            "Cell is modeled as maintaining homeostasis with standard ATP turnover.",
            "Conceptual prediction: methylation patterns associated with stable, repressed gene expression.",
            "Conceptual prediction: TET demethylation enzymes are not strongly active in this regime.",
            "Conceptual prediction, inspired partly by structured-water and cytoplasmic organization theories.",
            "Conceptual prediction: may correlate with reduced regenerative signaling.",
        ],
    }
else:
    state_data = {
        "Parameter": [
            "Ion Channel State",
            "Metabolic Activity",
            "Epigenetic Methylation",
            "TET Enzyme Activity",
            "Cell Water / Cytoplasmic Organization",
            "Regenerative Gene Output",
        ],
        "Status": [
            "Open / Activated",
            "Elevated / Shifted",
            "Associated with Active Demethylation",
            "Higher Predicted Activity",
            "Reduced Structure - Disordered (Conceptual)",
            "Activated / Upregulated (Conceptual)",
        ],
        "Description": [
            "Depolarization is predicted to open voltage-gated ion channels, allowing ion flux.",
            "Increased ionic flux is modeled as driving elevated metabolic and signaling activity.",
            "Conceptual prediction: methylation marks associated with more dynamic, demethylated states.",
            "Conceptual prediction: TET enzyme activity may increase, exposing regulatory regions.",
            "Conceptual prediction, inspired partly by structured-water and cytoplasmic organization theories.",
            "Conceptual prediction: may correlate with increased regenerative signaling (e.g. dedifferentiation/proliferation markers), depending on context.",
        ],
    }

df = pd.DataFrame(state_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Why This Matters")
st.markdown(
    "The purpose of this prototype is to explore whether bioelectric state could act as an "
    "upstream control layer that influences gene expression, cellular identity, and regenerative "
    "potential — and to generate better questions for further research, not to assert settled conclusions."
)

st.divider()
st.caption(
    "Note: This is a conceptual prototype dashboard for illustrative purposes only. "
    "The Boltzmann activation curve, state zones, and table thresholds are simplified representations "
    "intended to organize and communicate a proposed bioelectric-to-epigenetic signaling concept, "
    "not validated experimental results."
)
