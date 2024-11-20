import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate growth
def calculate_growth(initial_investment, monthly_contribution, annual_return, target_amount):
    balance = initial_investment
    years = 0
    data_points = []

    while balance < target_amount and years < 50:
        data_points.append(balance)
        balance = balance * (1 + annual_return) + (monthly_contribution * 12)
        years += 1

    data_points.append(balance)  # Append the final balance
    return years, data_points

# Streamlit app
st.title("First Crore Calculator (₹)")

# Input form
current_age = st.number_input("Current Age:", min_value=1, value=30)
initial_investment = st.number_input("Initial Investment (₹):", min_value=0, value=100000)
monthly_contribution = st.number_input("Monthly Contribution (₹):", min_value=0, value=10000)
annual_return = st.number_input("Annual Return (%):", min_value=0.0, value=8.0, format="%f") / 100.0
target_amount = st.number_input("Target Portfolio Value (₹):", min_value=1000000, value=10000000)  # Default ₹1 crore

if st.button("Calculate"):
    years_to_target, data_points = calculate_growth(
        initial_investment, monthly_contribution, annual_return, target_amount
    )

    if years_to_target < 50:
        st.write(f"You'll reach ₹{target_amount:,.0f} in {years_to_target} years.")
        st.write(f"By age {current_age + years_to_target}.")
    else:
        st.write("It will take over 50 years to reach your target amount.")

    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Year': range(current_age, current_age + years_to_target + 1),
        'Portfolio Value (₹)': data_points
    })

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(df['Year'], df['Portfolio Value (₹)'], marker='o', linestyle='-', color='b')
    ax.set_title('Portfolio Growth Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Portfolio Value (₹)')
    ax.grid(True)

    # Improve x-axis readability
    ax.set_xticks(np.arange(current_age, current_age + years_to_target + 1, max(1, years_to_target // 10)))

    st.pyplot(fig)

    # Add download option for data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='portfolio_growth.csv',
        mime='text/csv'
    )
