import streamlit as st
import pandas as pd
import numpy as np
import io

# --- BANKING GRADE CALCULATION ENGINE ---
def calculate_vehicle_loan(principal, tenure_val, tenure_type, rate_pa, method):
    if principal <= 0 or tenure_val <= 0 or rate_pa <= 0:
        return None
    
    # Convert tenure to total months
    if tenure_type == "Years":
        tenure_months = int(tenure_val * 12)
        years_for_flat = tenure_val
    else:
        tenure_months = int(tenure_val)
        years_for_flat = tenure_val / 12
        
    schedule = []
    
    if method == "Diminishing":
        monthly_rate = (rate_pa / 100) / 12
        emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
        
        total_payment = emi * tenure_months
        total_interest = total_payment - principal
        
        remaining_balance = principal
        for month in range(1, tenure_months + 1):
            opening_balance = remaining_balance
            interest_m = remaining_balance * monthly_rate
            principal_m = emi - interest_m
            remaining_balance -= principal_m
            
            schedule.append({
                "Month": month,
                "Opening Balance": round(opening_balance),
                "Monthly EMI": round(emi),
                "Interest Paid": round(interest_m),
                "Principal Paid": round(principal_m),
                "Closing Balance": round(max(0, remaining_balance))
            })
            
    else: # Flat Rate
        total_interest = (principal * rate_pa * years_for_flat) / 100
        total_payment = principal + total_interest
        emi = total_payment / tenure_months
        
        monthly_interest_fixed = total_interest / tenure_months
        monthly_principal_fixed = principal / tenure_months
        
        remaining_balance = principal
        for month in range(1, tenure_months + 1):
            opening_balance = remaining_balance
            remaining_balance -= monthly_principal_fixed
            
            schedule.append({
                "Month": month,
                "Opening Balance": round(opening_balance),
                "Monthly EMI": round(emi),
                "Interest Paid": round(monthly_interest_fixed),
                "Principal Paid": round(monthly_principal_fixed),
                "Closing Balance": round(max(0, remaining_balance))
            })

    return {
        "monthly_emi": round(emi),
        "total_interest": round(total_interest),
        "total_payment": round(total_payment),
        "schedule": schedule,
        "tenure_months": tenure_months
    }

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Vehicle Loan Pro - Calculator", layout="wide")

st.markdown("""
    <style>
    :root {
        --primary-blue: #1E40AF;
        --text-dark: #111827;
        --label-grey: #374151;
        --bg-white: #FFFFFF;
        --vehicle-accent: #E53E3E;
    }
    
    .main-title {
        text-align: center;
        color: #FFFFFF !important;
        background: linear-gradient(90deg, #1A365D 0%, #2D3748 100%);
        padding: 20px;
        border-radius: 10px;
        font-weight: 800 !important;
        font-size: 42px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0px;
        border-bottom: 5px solid var(--vehicle-accent);
    }

    .stNumberInput label, .stSlider label, .stRadio label {
        color: var(--label-grey) !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: var(--label-grey) !important;
        font-weight: 600 !important;
    }

    .stNumberInput input {
        color: var(--text-dark) !important;
        background-color: var(--bg-white) !important;
        font-weight: bold !important;
    }
    
    .stNumberInput, .stSlider, .stRadio {
        background: #F8FAFC !important;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin-bottom: 10px;
    }
    
    .emi-box {
        background-color: #1A365D !important;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        border-left: 10px solid var(--vehicle-accent);
    }
    
    .emi-box h1, .emi-box p {
        color: #FFFFFF !important;
        margin: 0;
    }
    
    .result-card {
        background: #FFFFFF !important;
        padding: 15px 5px;
        border-radius: 10px;
        border-top: 5px solid var(--vehicle-accent);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .result-card small {
        color: #64748b !important;
        text-transform: uppercase;
        font-weight: 700;
        font-size: 11px;
        margin-bottom: 5px;
    }

    .result-card b {
        color: #1A365D !important;
        font-size: 18px !important; 
        white-space: nowrap; 
    }
    
    div.stButton > button:first-child {
        background-color: var(--vehicle-accent) !important;
        color: #FFFFFF !important;
        width: 100%;
        height: 60px;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        font-size: 20px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>VEHICLE LOAN EMI CALCULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #cbd5e1; margin-bottom: 5px;'>Drive Your Dream - Professional Finance Planner</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFFFFF; font-weight: bold; margin-bottom: 10px;'>Developed by: Shamsudeen Abdulla</p>", unsafe_allow_html=True)

sc1, sc2, sc3, sc4, sc5 = st.columns([1, 1, 1, 1, 1])
with sc2:
    st.link_button("💬 WhatsApp", "https://wa.me/qr/IOBUQDQMM2X3D1", use_container_width=True)
with sc4:
    st.link_button("🔵 Facebook", "https://www.facebook.com/shamsudeen.abdulla.2025/", use_container_width=True)

st.write("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("<h3 style='color:#FFFFFF;'>Vehicle Loan Requirements</h3>", unsafe_allow_html=True)
    p_amount = st.number_input("Vehicle Loan Amount (₹)", min_value=10000, value=500000, step=10000)
    
    tenure_type = st.radio("Select Tenure Type", ["Years", "Months"], horizontal=True)
    
    if tenure_type == "Years":
        tenure_val = st.slider("Tenure (Years)", min_value=1, max_value=10, value=5)
    else:
        tenure_val = st.slider("Tenure (Months)", min_value=1, max_value=120, value=60)
    
    # --- പലിശ നിരക്ക് പരിധി 50% ആക്കി മാറ്റി ---
    int_rate = st.number_input("Interest Rate (% P.A.)", min_value=1.0, max_value=50.0, value=9.0, step=0.1)
    
    calc_method = st.radio("Interest Calculation Method", ["Diminishing", "Flat"], horizontal=True)
    
    st.write("<br>", unsafe_allow_html=True)
    calculate_btn = st.button("Calculate Vehicle EMI")

if calculate_btn:
    res = calculate_vehicle_loan(p_amount, tenure_val, tenure_type, int_rate, calc_method)
    
    if res:
        with col2:
            st.markdown(f"""
                <div class="emi-box">
                    <p style='font-size: 18px;'>Your Monthly Vehicle Loan EMI</p>
                    <h1 style='font-size: 58px;'>₹ {res['monthly_emi']:,}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"<div class='result-card'><small>Principal</small><b>₹ {p_amount:,}</b></div>", unsafe_allow_html=True)
            with r2:
                st.markdown(f"<div class='result-card'><small>Total Interest</small><b>₹ {res['total_interest']:,}</b></div>", unsafe_allow_html=True)
            with r3:
                st.markdown(f"<div class='result-card'><small>Total Payable</small><b>₹ {res['total_payment']:,}</b></div>", unsafe_allow_html=True)

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#FFFFFF;'>Vehicle Loan Amortization Schedule (Monthly - {calc_method})</h3>", unsafe_allow_html=True)
        df_schedule = pd.DataFrame(res['schedule'])
        st.dataframe(df_schedule.style.format("{:,}"), use_container_width=True, hide_index=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_data = {
                "LOAN SUMMARY PARAMETERS": ["Loan Amount", f"Tenure ({tenure_type})", "Interest Rate (%)", "Interest Type", "Monthly EMI", "Total Interest Paid", "Total Payable Amount"],
                "VALUE": [p_amount, tenure_val, int_rate, calc_method, res['monthly_emi'], res['total_interest'], res['total_payment']]
            }
            df_sum = pd.DataFrame(summary_data)
            df_sum.to_excel(writer, sheet_name='Vehicle Loan Report', index=False, startrow=1)
            
            start_row_schedule = len(df_sum) + 4
            df_schedule.to_excel(writer, sheet_name='Vehicle Loan Report', index=False, startrow=start_row_schedule)
            
            workbook = writer.book
            worksheet = writer.sheets['Vehicle Loan Report']
            fmt_header = workbook.add_format({'bold': True, 'bg_color': '#1A365D', 'font_color': 'white', 'border': 1, 'align': 'center'})
            fmt_cell = workbook.add_format({'border': 1, 'align': 'center'})
            fmt_money = workbook.add_format({'border': 1, 'num_format': '#,##,##0', 'align': 'center'})
            
            for col_num, value in enumerate(df_sum.columns.values):
                worksheet.write(1, col_num, value, fmt_header)
            
            for i in range(len(summary_data["VALUE"])):
                worksheet.write(2+i, 0, summary_data["LOAN SUMMARY PARAMETERS"][i], fmt_cell)
                val = summary_data["VALUE"][i]
                if isinstance(val, (int, float)) and i not in [1, 2]:
                    worksheet.write(2+i, 1, val, fmt_money)
                else:
                    worksheet.write(2+i, 1, val, fmt_cell)

            for col_num, value in enumerate(df_schedule.columns.values):
                worksheet.write(start_row_schedule, col_num, value, fmt_header)
            
            for i, row in df_schedule.iterrows():
                for j, val in enumerate(row):
                    if j == 0:
                        worksheet.write(start_row_schedule + i + 1, j, val, fmt_cell)
                    else:
                        worksheet.write(start_row_schedule + i + 1, j, val, fmt_money)

            worksheet.set_column('A:F', 25)
            
        excel_data = output.getvalue()
        st.download_button(
            label="📥 Download Vehicle Loan Report (Excel)",
            data=excel_data,
            file_name=f"Vehicle_Loan_Report_{p_amount}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.error("Please provide valid input values.")
else:
    with col2:
        st.info("Adjust the loan parameters and click 'Calculate Vehicle EMI' to see your plan.")
