import streamlit as st
import pandas as pd

st.title("First Crore Calculator")

# Styling (Optional - include if you want the custom styles)
st.markdown("""
<style>
div[data-testid="stNumberInput"] {
    margin-bottom: 10px;
    width: 200px;
}
</style>
""", unsafe_allow_html=True)


# Input form in two columns
col1, col2 = st.columns(2)

with col1:
    current_age = st.number_input("Current Age:", min_value=0, value=30)
    current_corpus = st.number_input("Current Corpus:", min_value=0, value=75000)
    current_income = st.number_input("Current Annual Income:", min_value=0, value=400000)

with col2:
    annual_increase = st.number_input("Annual Increase in Salary (%):", min_value=0.0, value=0.05, format="%f")
    investment_proportion = st.number_input("Proportion of Income Invested (%):", min_value=0.0, value=0.80, format="%f")
    investment_return = st.number_input("Expected Investment Return (%):", min_value=0.0, value=0.12, format="%f")
    target_corpus = st.number_input("Target Corpus (e.g., 10000000 for 1 crore):", min_value=0, value=10000000)


# Calculation
if st.button("Calculate"):
    year = 0
    fund_start = current_corpus
    data = []

    while True:
        year += 1
        age = current_age + year - 1
        annual_income = current_income * (1 + annual_increase)**(year - 1)
        amount_invested = annual_income * investment_proportion
        investment_return_amount = (fund_start + amount_invested) * investment_return  # Corrected calculation

        fund_end = fund_start + amount_invested + investment_return_amount

        if fund_end >= target_corpus:
            data.append([year, age, fund_start, annual_income, amount_invested, investment_return_amount, fund_end])
            break  # Exit loop once target is reached

        data.append([year, age, fund_start, annual_income, amount_invested, investment_return_amount, fund_end])
        fund_start = fund_end

    df = pd.DataFrame(data, columns=['Year', 'Age', 'Fund at Start', 'Annual Income', 'Amount Invested', 'Investment Return', 'Fund at End'])
    st.write(f"You will achieve your target at the age of {age}")
    st.dataframe(df)
