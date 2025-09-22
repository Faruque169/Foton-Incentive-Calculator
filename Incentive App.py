# module
from congratsAnimation import animate_confetti
from calculations import calculate_incentive
import base64
from streamlit_extras.metric_cards import style_metric_cards
import streamlit as st
st.set_page_config(
    page_title="Foton Incentive Calculator", layout="wide",
    page_icon="🧮",
    initial_sidebar_state="collapsed")

st.title("Foton Incentive Calculator 2025-26")
st.markdown("""---""")

# Path to your PDF inside the resources folder
pdf_path = "resources/Detailed Incentive Scheme for FY25-26.pdf"

# Session state init
if "show_pdf" not in st.session_state:
    st.session_state.show_pdf = False

# Toggle button
if st.button("👁️ Show Incentive Circular"):
    st.session_state.show_pdf = not st.session_state.show_pdf

# Show/hide PDF + Eye in box
if st.session_state.show_pdf:
    # PDF viewer
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


designation = st.selectbox("Select your Designation",
                           ["Territory officer", "Area Head"])

# Number of territories supervised
num_territories = 1
if designation != "Territory officer":
    num_territories = st.number_input(
        "Number of Territories Supervised", min_value=1, value=1)

# --- Inputs
st.subheader("Basic Inputs")
with st.expander("🔧 Enter Input Details", expanded=True):
    for i in range(num_territories):
        st.markdown(
            f"### Territory {i+1 if i+1 > 1 else (i+1 if designation == 'Area Head' else '')}")
        # hide responsibility for TO
        if designation != "Territory officer":
            responsibility = st.selectbox("Select Supervision Type", [
                "Complete Responsibility", "Direct Supervised Responsibility", "Additional Supervised Responsibility"], key=f"responsibility_{i}")
        else:
            # initialize_key for responsibility"
            if f"responsibility_{i}" not in st.session_state:
                st.session_state[f"responsibility_{i}"] = "Direct Responsibility"
            responsibility = "Direct Responsibility"

        col1, col2, col3 = st.columns(3)

        with col1:
            budget = st.number_input(
                f"Monthly Budget (Units) - ", min_value=0, value=0, key=f"budget_{i}")
            achieved = st.number_input(
                f"Units Achieved (Units) - ", min_value=0, value=0, key=f"achieved_{i}")

            dp_30 = st.number_input(
                f"Units with 30% Down Payment - ", min_value=0, value=0, key=f"dp30_{i}")
            dp_50 = st.number_input(
                f"Units with 50% Down Payment - ", min_value=0, value=0, key=f"dp50_{i}")
            cash_sales = st.number_input(
                f"Cash Sales Units - ", min_value=0, value=0, key=f"cash_{i}")

        with col2:
            resale_budget = st.number_input(
                f"Resale Budget  (Units) - ", min_value=0, value=0, key=f"resale_budget_{i}")
            resale_achieved = st.number_input(
                f"Resale Achieved (Units) - ", min_value=0, value=0, key=f"resale_achieved_{i}")

            Resale_dp_30 = st.number_input(
                f"Resale Units with 30% Down Payment - ", min_value=0, value=0, key=f"Resale_dp30_{i}")
            Resale_dp_50 = st.number_input(
                f"Resale Units with 50% Down Payment - ", min_value=0, value=0, key=f"Resale_dp50_{i}")
            Resale_cash_sales = st.number_input(
                f"Cash Resale Units - ", min_value=0, value=0, key=f"Resale_cash_{i}")

        with col3:
            installment_collection = st.number_input(
                f"No. of MRO Files - 1st & 2nd Installments Collected - ", min_value=0, value=0, key=f"installment_{i}")
            credit_note_units = st.number_input(
                f"Credit Note Units - ", min_value=0, value=0, key=f"credit_{i}")
            zero_sales_upazila = st.number_input(
                f"Sales Units in Previous Year Zero-Sales Upazilas - ", min_value=0, value=0, key=f"zero_sales_{i}")
            inquiry_project_units = st.number_input(
                f"Inquiry/Project Units (New Sales) - ", min_value=0, value=0, key=f"new_inquiry_{i}")
            inquiry_project_units = st.number_input(
                f"Inquiry Units (ReSales) - ", min_value=0, value=0, key=f"resale_inquiry_{i}")


# --- Results

st.header("Incentive Summary")
total_final_incentive = 0
achieved_list = []
budget_list = []
achieved_re_list = []
budget_re_list = []

for i in range(num_territories):
    inputs = {
        "achieved": st.session_state[f"achieved_{i}"],
        "budget": st.session_state[f"budget_{i}"],
        "resale_budget": st.session_state[f"resale_budget_{i}"],
        "resale_achieved": st.session_state[f"resale_achieved_{i}"],
        "responsibility": st.session_state[f"responsibility_{i}"],
        "zero_sales": st.session_state[f"zero_sales_{i}"],
        "dp30": st.session_state[f"dp30_{i}"],
        "dp50": st.session_state[f"dp50_{i}"],
        "cash": st.session_state[f"cash_{i}"],

        "Resale_dp30": st.session_state[f"Resale_dp30_{i}"],
        "Resale_dp50": st.session_state[f"Resale_dp50_{i}"],
        "Resale_cash": st.session_state[f"Resale_cash_{i}"],

        "installment": st.session_state[f"installment_{i}"],
        "credit": st.session_state[f"credit_{i}"],
        "new_inquiry": st.session_state[f"new_inquiry_{i}"],
        "resale_inquiry": st.session_state[f"resale_inquiry_{i}"]
    }
    result = calculate_incentive(inputs, designation, responsibility)

    total_final_incentive += result['final']

    st.markdown(f"""
    #### 📍 Territory {i+1 if i+1 > 1 else (i+1 if designation == 'Area Head' else '')} Summary:
    - Sales Unit Incentive: TK {result['unit_incentive']:,.0f}
    - Resale Unit Incentive: Tk {result['resale_incentive']:,.0f}
    - Base Incentive: Tk {result['base_incentive']:,.0f}
    - Add-ons: Tk {result['add_ons']:,.0f}
    - Penalty: Tk {result['penalty']:,.0f}
    - Multiplier Applied: x{result['multiplier']}
    - Final Incentive: **Tk {result['final']:,.0f}**
    """)


# ✅ Build all 4 lists AFTER loop (no blank lists needed)
achieved_list = [st.session_state.get(
    f"achieved_{i}", 0) for i in range(num_territories)]
budget_list = [st.session_state.get(
    f"budget_{i}", 0) for i in range(num_territories)]

yearly_sales = st.checkbox(
    "Check this box if these are your Fiscal Year Sales.", key=f"yearly_target")

if designation != "Territory officer":
    if yearly_sales:
        if sum(achieved_list) / sum(budget_list) >= 1.25:
            st.success(
                f"🎉 Congratulations! You have achieved Foreign Trip within TK 80,000")
        else:
            st.warning(
                "You need to achieve 25% more than your yearly budget to get the Foreign Trip.")

else:
    if yearly_sales:
        if inputs['achieved'] / inputs['budget'] >= 1.25:
            st.success(
                f"🎉 Congratulations! You have achieved Foreign Trip within 80,000")
        else:
            st.warning(
                "You need to achieve 25% more than your yearly budget to get the Foreign Trip.")


# st.success(
#     f"🎉 Total Incentive across all Territories: Tk {total_final_incentive:,.0f}")
animate_confetti(total_final_incentive)


style_metric_cards()
