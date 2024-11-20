import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    initial_investment = st.number_input("Initial Investment (₹):", min_value=0, value=100000)
    annual_return = st.number_input("Annual Return (%):", min_value=0.0, value=8.0, format="%f") / 100.0
    inflation_rate = st.number_input("Estimated Inflation Rate (%):", min_value=0.0, value=5.0, format="%f") / 100.0

with col2:
    annual_income = st.number_input("Annual Income (₹):", min_value=0, value=600000)
    investment_type = st.radio("Choose Investment Type:", ["Percentage of Income", "Fixed Monthly Contribution"])
    if investment_type == "Percentage of Income":
        investment_percentage = st.number_input("Investment Percentage (%):", min_value=0.0, value=20.0, format="%f") / 100.0
        monthly_contribution = (annual_income * investment_percentage) / 12
    else:
        monthly_contribution = st.number_input("Monthly Contribution (₹):", min_value=0, value=10000)

target_amount = st.number_input("Target Portfolio Value (₹):", min_value=1000000, value=10000000)  # Default ₹1 crore

if st.button("Calculate"):
    years_to_target, data, final_adjusted_target = calculate_growth(
        initial_investment,
        monthly_contribution,
        annual_return,
        target_amount,
        inflation_rate
    )

    if years_to_target < 50:
        st.write(f"You'll reach ₹{target_amount:,.0f} in {years_to_target} years.")
        st.write(f"By age {current_age + years_to_target}.")
        st.write(f"Adjusted for inflation, ₹{target_amount:,.0f} will be worth approximately ₹{final_adjusted_target:,.0f} in {years_to_target} years.")
    else:
        st.write("It will take over 50 years to reach your target amount.")

    # Create a DataFrame for the chart
    df = pd.DataFrame(data, columns=['Year', 'Portfolio Value (₹)', 'Adjusted Target (₹)'])
    df['Year'] = df['Year'].apply(lambda x: f"Year {x}")

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(df['Year'], df['Portfolio Value (₹)'], marker='o', linestyle='-', color='b', label='Portfolio Value')
    ax.plot(df['Year'], df['Adjusted Target (₹)'], marker='x', linestyle='--', color='r', label='Adjusted Target (Inflation)')
    ax.set_title('Portfolio Growth vs Adjusted Target Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Value (₹)')
    ax.legend()
    ax.grid(True)

    # Improve x-axis readability
    ax.set_xticks(range(0, len(df['Year']), max(1, len(df['Year']) // 10)))
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # Add download option for data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='portfolio_growth_with_inflation.csv',
        mime='text/csv'
    )
