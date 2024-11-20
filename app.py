import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Function to calculate inflation-adjusted value of the target
def inflation_adjusted_target(target_amount, inflation_rate, years):
    return target_amount / ((1 + inflation_rate) ** years)

# Function to calculate growth
def calculate_growth(initial_investment, monthly_contribution, annual_return, years):
    balance = initial_investment
    for _ in range(years):
        balance = balance * (1 + annual_return) + (monthly_contribution * 12)
    return balance

# Streamlit app
st.title("Inflation-Adjusted First Crore Calculator")

# Inputs section (three-column layout)
col1, col2, col3 = st.columns(3)

with col1:
    current_age = st.number_input("Current Age:", min_value=1, value=30, step=1)
    initial_investment = st.number_input("Initial Investment (₹ Lakhs):", min_value=0.0, value=1.0, step=0.5) * 1e5
    annual_return = st.number_input("Annual Return (%):", min_value=0.0, value=8.0, step=0.5, format="%f") / 100.0

with col2:
    annual_income = st.number_input("Annual Income (₹ Lakhs):", min_value=0.0, value=6.0, step=0.5) * 1e5
    inflation_rate = st.number_input("Estimated Inflation Rate (%):", min_value=0.0, value=5.0, step=0.5, format="%f") / 100.0
    investment_type = st.radio("Choose Investment Type:", ["Percentage of Income", "Fixed Monthly Contribution"])

with col3:
    if investment_type == "Percentage of Income":
        investment_percentage = st.number_input("Investment Percentage (%):", min_value=0.0, value=20.0, step=0.5, format="%f") / 100.0
        monthly_contribution = (annual_income * investment_percentage) / 12
    else:
        monthly_contribution = st.number_input("Monthly Contribution (₹ Lakhs):", min_value=0.0, value=1.0, step=0.5) * 1e5

target_amount = 1e7  # Target ₹1 crore

# Calculate and display results
if st.button("Calculate"):
    # Calculations
    total_years = 50  # Max time frame
    portfolio = calculate_growth(initial_investment, monthly_contribution, annual_return, total_years)
    equivalent_target = inflation_adjusted_target(target_amount, inflation_rate, total_years)

    # Show Results and Logic
    st.subheader("Results:")
    if portfolio >= target_amount:
        st.write(f"Your portfolio will reach ₹{target_amount:,.0f} in 50 years.")
        st.write(f"However, considering an inflation rate of {inflation_rate * 100:.2f}%,")
        st.write(f"₹1 crore in today's terms will be equivalent to ₹{equivalent_target:,.0f} after 50 years.")
    else:
        st.write(f"Even after fifty."""
        st.write(f"Even after 50 years, your portfolio will not reach ₹1 crore. The projected portfolio value is ₹{portfolio:,.0f}.")
        st.write(f"Considering inflation, ₹1 crore today would need to be ₹{equivalent_target:,.0f} in 50 years to maintain the same purchasing power.")

    # Explain logic and request user comments
    st.markdown("### Inflation Adjustment Logic:")
    st.write("The inflation-adjusted equivalent is calculated as:")
    st.latex(r"Adjusted\ Target = \frac{Target}{(1 + Inflation\ Rate)^{Years}}")
    st.write(
        "This means that if inflation is high, the real value of ₹1 crore reduces significantly over time. "
        "Would you like to adjust your target value?"
    )
    user_comment = st.text_area("Your thoughts or adjustments:", placeholder="Share your comments or revised target...")

    # Create a DataFrame for the chart
    years = range(1, total_years + 1)
    balances = [calculate_growth(initial_investment, monthly_contribution, annual_return, y) for y in years]
    adjusted_targets = [inflation_adjusted_target(target_amount, inflation_rate, y) for y in years]

    df = pd.DataFrame({
        'Year': [current_age + y for y in years],
        'Portfolio Value (₹)': balances,
        'Inflation-Adjusted Target (₹)': adjusted_targets
    })

    # Enhanced graph with better visuals
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Year', y='Portfolio Value (₹)', data=df, label='Portfolio Value', color='blue', marker='o')
    sns.lineplot(x='Year', y='Inflation-Adjusted Target (₹)', data=df, label='Inflation-Adjusted Target', color='red', marker='x')
    ax.set_title('Portfolio Growth vs Inflation-Adjusted Target', fontsize=16, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Value (₹)', fontsize=12)
    ax.legend(fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Dynamically move graph above inputs when calculated
    st.markdown("## Visualization:")
    st.pyplot(fig)

    # Add download option for data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='portfolio_growth_with_inflation.csv',
        mime='text/csv'
    )
