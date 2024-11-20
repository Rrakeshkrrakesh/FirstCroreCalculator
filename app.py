import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to calculate inflation-adjusted target
def inflation_adjusted_target(target_amount, inflation_rate, years):
    return target_amount * ((1 + inflation_rate) ** years)


# Function to calculate portfolio growth
def calculate_growth(initial_investment, monthly_contribution, annual_return, years):
    balance = initial_investment
    for _ in range(years):
        balance = balance * (1 + annual_return) + (monthly_contribution * 12)
    return balance


# Streamlit app
st.title("Inflation-Adjusted Portfolio Calculator")

# Input Fields (Three Column Layout)
col1, col2, col3 = st.columns(3)

with col1:
    current_age = st.number_input("Current Age:", min_value=1, value=30, step=1)
    initial_investment = st.number_input("Initial Investment (₹ Lakhs):", min_value=0.0, value=1.0, step=0.5) * 1e5
    annual_return = st.number_input("Annual Return (%):", min_value=0.0, value=8.0, step=0.5) / 100.0

with col2:
    annual_income = st.number_input("Annual Income (₹ Lakhs):", min_value=0.0, value=6.0, step=0.5) * 1e5
    inflation_rate = st.number_input("Inflation Rate (%):", min_value=0.0, value=5.0, step=0.5) / 100.0
    investment_type = st.radio("Investment Type:", ["Percentage of Income", "Fixed Monthly Contribution"])

with col3:
    if investment_type == "Percentage of Income":
        investment_percentage = st.number_input("Investment Percentage (%):", min_value=0.0, value=20.0, step=0.5) / 100.0
        monthly_contribution = (annual_income * investment_percentage) / 12
    else:
        monthly_contribution = st.number_input("Monthly Contribution (₹ Lakhs):", min_value=0.0, value=1.0, step=0.5) * 1e5

target_amount = 1e7  # Target ₹1 crore

# Calculate and display results
if st.button("Calculate"):
    total_years = 50  # Maximum time frame
    portfolio = calculate_growth(initial_investment, monthly_contribution, annual_return, total_years)
    equivalent_target = inflation_adjusted_target(target_amount, inflation_rate, total_years)

    st.subheader("Results:")

    if portfolio >= equivalent_target:
        st.write(
            f"Your portfolio value will be ₹{portfolio:,.0f} in {total_years} years, "
            f"which is more than the equivalent of ₹{equivalent_target:,.0f} considering an inflation rate of {inflation_rate * 100:.2f}%."
        )
    else:
        st.write(
            f"Even after {total_years} years, your portfolio will only grow to ₹{portfolio:,.0f}, "
            f"which is less than the inflation-adjusted target of ₹{equivalent_target:,.0f}."
        )

    st.markdown("### Inflation Adjustment Logic:")
    st.write(
        f"The inflation-adjusted equivalent is calculated using the formula: "
        f"`Adjusted Target = Target Amount × (1 + Inflation Rate) ^ Years`"
    )
    st.write(
        "This means the real value of ₹1 crore reduces significantly over time if inflation is high."
        " Would you like to adjust your target value?"
    )
    user_comment = st.text_area("Your thoughts or adjustments:", placeholder="Share your comments or revised target...")

    # Create data for visualization
    years = list(range(1, total_years + 1))
    balances = []
    adjusted_targets = []

    for year in years:
        balance_at_year = calculate_growth(initial_investment, monthly_contribution, annual_return, year)
        equivalent_target_at_year = inflation_adjusted_target(target_amount, inflation_rate, year)
        balances.append(balance_at_year)
        adjusted_targets.append(equivalent_target_at_year)

    df = pd.DataFrame({
        'Year': [current_age + y for y in years],
        'Portfolio Value (₹)': balances,
        'Inflation-Adjusted Target (₹)': adjusted_targets
    })

    # Visualization
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

    st.markdown("## Visualization:")
    st.pyplot(fig)

    # CSV download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='portfolio_growth_with_inflation.csv',
        mime='text/csv'
    )
