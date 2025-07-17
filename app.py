import streamlit as st  
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

# Title
st.title("📊 AI-Powered Personal Finance Tracker")

# Sidebar: User Input
st.sidebar.header("🔹 Enter Your Transactions")

# Data storage
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# User Inputs
date = st.sidebar.date_input("Date")
amount = st.sidebar.number_input("Amount", min_value=0.01, step=0.01)
category = st.sidebar.selectbox("Category", ["Income", "Food", "Rent", "Shopping", "Transport", "Bills", "Others"])
description = st.sidebar.text_input("Description")

# Add transaction
if st.sidebar.button("➕ Add Transaction"):
    st.session_state.transactions.append({"Date": date, "Amount": amount, "Category": category, "Description": description})
    st.success("Transaction added successfully!")

# Convert data to DataFrame
df = pd.DataFrame(st.session_state.transactions)

# Display transactions
st.subheader("📜 Transaction History")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No transactions added yet.")

# Expense Analysis
if not df.empty:
    st.subheader("📊 Expense Breakdown")

    # Income & Expense Calculation
    total_income = df[df["Category"] == "Income"]["Amount"].sum()
    total_expense = df[df["Category"] != "Income"]["Amount"].sum()
    savings = total_income - total_expense

    # Display Summary
    st.write(f"💰 **Total Income:** ${total_income:.2f}")
    st.write(f"💸 **Total Expenses:** ${total_expense:.2f}")
    st.write(f"💾 **Savings:** ${savings:.2f}")

    # Expense Pie Chart
    expense_data = df[df["Category"] != "Income"].groupby("Category")["Amount"].sum()
    if not expense_data.empty:
        fig, ax = plt.subplots()
        ax.pie(expense_data, labels=expense_data.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    # Income vs Expense Bar Chart
    fig, ax = plt.subplots()
    ax.bar(["Income", "Expenses", "Savings"], [total_income, total_expense, savings], color=["green", "red", "blue"])
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)