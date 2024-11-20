import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to format numbers into lakhs and crores for display
def format_amount(amount):
    if amount >= 1e7:
        return f"{amount / 1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"{amount / 1e5:.2f} L"
    else:
        return f"{amount:,.0f} ₹"

# Function to calculate growth with inflation adjustment
def calculate_growth(initial_investment, monthly_contribution, annual_return, target_amount, inflation_rate):
    balance = initial_investment
    years = 0
    data = []

    adjusted_target = target_amount  # Initialize adjusted target

    while balance < adjusted_target and years < 50:
        years += 1
        balance = balance * (1 + annual_return) + (monthly_contribution * 12)
        data.append([years, balance, adjusted_target])  # Store year, balance, and adjusted target
        adjusted_target *= (1 + inflation_rate)  # Adjust target for next year

    return years, data, adjusted_target

# Streamlit app
st.title("First Crore Calculator (₹)")

# User input form split into two columns
col1, col2 = st.columns(2)

with col1:
    current_age = st.number_input("Current Age:", min_value=1, value=30)
    initial_investment = st.number_input("Initial Investment (₹ in Lakhs):", min_value=0.0, value=1.0) * 1e5
    annual_return = st.number_input("Annual Return (%):", min_value=0.0, value=8.0, format="%f") / 100.0
    inflation_rate = st.number_input("Estimated Inflation Rate (%):", min_value=0.0, value=5.0, format="%f") / 100.0

with col2:
    annual_income = st.number_input("Annual Income (₹ in Lakhs):", min_value=0.0, value=6.0) * 1e5
    investment_type = st.radio("Choose Investment Type:", ["Percentage of Income", "Fixed Monthly Contribution"])
    if investment_type == "Percentage of Income":
        investment_percentage = st.number_input("Investment Percentage (%):", min_value=0.0, value=20.0, format="%f") / 100.0
        monthly_contribution = (annual_income * investment_percentage) / 12
    else:
        monthly_contribution = st.number_input("Monthly Contribution (₹ in Lakhs):", min_value=0.0, value=1.0) * 1e5

target_amount = st.number_input("Target Portfolio Value (₹ in Crores):", min_value=0.1, value=1.0) * 1e7  # Default ₹1 crore

if st.button("Calculate"):
    years_to_target, data, final_adjusted_target = calculate_growth(
        initial_investment,
        monthly_contribution,
        annual_return,
        target_amount,
        inflation_rate
    )

    if years_to_target < 50:
        st.write(f"You'll reach **₹{format_amount(target_amount)}** in **{years_to_target} years**.")
        st.write(f"By age **{current_age + years_to_target}**.")
        st.write(f"Adjusted for inflation, ₹{format_amount(target_amount)} will be worth approximately **₹{format_amount(final_adjusted_target)}** in **{years_to_target} years**.")
    else:
        st.write("It will take over 50 years to reach your target amount.")

    # Create a DataFrame for the chart
    df = pd.DataFrame(data, columns=['Year', 'Portfolio Value (₹)', 'Adjusted Target (₹)'])
    df['Year'] = df['Year'].apply(lambda x: f"Year {x}")

    # Enhanced graph with better visuals
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df['Year'], y=df['Portfolio Value (₹)'], marker='o', label='Portfolio Value', color='blue', ax=ax)
    sns.lineplot(x=df['Year'], y=df['Adjusted Target (₹)'], marker='x', label='Adjusted Target (Inflation)', color='red', ax=ax)
    ax.set_title('Portfolio Growth vs Adjusted Target Over Time', fontsize=16, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Value (₹)', fontsize=12)
    ax.legend(fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    # Add download option for data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='portfolio_growth_with_inflation.csv',
        mime='text/csv'
    )
