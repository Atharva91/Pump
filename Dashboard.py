import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import numpy as np

# Dashboard Title
st.title("Cloud Savings Opportunity Dashboard")
st.markdown("---")

# Sidebar: Data Input
st.sidebar.header("Input Lead Data")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload Lead Data (CSV)", type="csv")
if uploaded_file:
    leads_data = pd.read_csv(uploaded_file)
    st.sidebar.success("Data Uploaded Successfully!")
else:
    st.sidebar.warning("Awaiting CSV file upload.")

# Manual Input Form
if st.sidebar.checkbox("Add Lead Manually"):
    st.sidebar.subheader("Manual Lead Entry")
    company_name = st.sidebar.text_input("Company Name")
    industry = st.sidebar.selectbox("Industry", ["SaaS", "FinTech", "E-Commerce", "Gaming", "Other"])
    cloud_provider = st.sidebar.selectbox("Cloud Provider", ["AWS", "Azure", "GCP", "Other"])
    company_size = st.sidebar.number_input("Company Size (Employees)", min_value=1)
    estimated_spend = st.sidebar.number_input("Estimated Cloud Spend ($M/year)", min_value=0.0)
    growth_rate = st.sidebar.slider("Growth Rate (%)", min_value=0, max_value=100, value=10)
    churn_risk = st.sidebar.slider("Churn Risk (%)", min_value=0, max_value=100, value=50)

    if st.sidebar.button("Add Lead"):
        new_lead = {
            "Company Name": company_name,
            "Industry": industry,
            "Cloud Provider": cloud_provider,
            "Company Size (Employees)": company_size,
            "Estimated Spend ($M/year)": estimated_spend,
            "Growth Rate (%)": growth_rate,
            "Churn Risk (%)": churn_risk
        }
        if 'leads_data' in locals():
            leads_data = pd.concat([leads_data, pd.DataFrame([new_lead])], ignore_index=True)
        else:
            leads_data = pd.DataFrame([new_lead])
        st.sidebar.success(f"Lead {company_name} added successfully!")

# Section: Lead Scoring Algorithm
def calculate_lead_score(row):
    score = 0

    # Base score for cloud spend
    if row['Estimated Spend ($M/year)'] > 1:
        score += 40
    elif row['Estimated Spend ($M/year)'] > 0.5:
        score += 30
    else:
        score += 10

    # Industry multiplier
    industry_weights = {"SaaS": 1.2, "FinTech": 1.1, "E-Commerce": 1.0, "Gaming": 1.0, "Other": 0.8}
    score *= industry_weights.get(row['Industry'], 1.0)

    # Growth rate bonus
    if row['Growth Rate (%)'] > 20:
        score += 20
    elif row['Growth Rate (%)'] > 10:
        score += 10

    # Churn risk deduction
    if row['Churn Risk (%)'] > 50:
        score -= 10

    return score

if uploaded_file or 'leads_data' in locals():
    leads_data['Lead Score'] = leads_data.apply(calculate_lead_score, axis=1)

# Section: Data Insights
if 'leads_data' in locals():
    st.subheader("Leads Table")
    st.dataframe(leads_data)

    st.subheader("Top 5 Prioritized Leads")
    top_leads = leads_data.sort_values(
        by=["Lead Score", "Estimated Spend ($M/year)", "Growth Rate (%)"], 
        ascending=[False, False, False]
    ).head(5)
    st.write(top_leads)

    st.subheader("Key Metrics")
    st.metric("Total Leads", len(leads_data))
    avg_score = np.round(leads_data['Lead Score'].mean(), 2)
    st.metric("Average Lead Score", avg_score)

    st.subheader("Industry Distribution")
    fig = px.pie(leads_data, names='Industry', title='Leads by Industry')
    st.plotly_chart(fig)

    st.subheader("Cloud Provider Usage")
    fig_provider = px.bar(leads_data, x='Cloud Provider', title='Cloud Provider Distribution', color='Cloud Provider')
    st.plotly_chart(fig_provider)

# Section: Advanced Analytics
if 'leads_data' in locals():
    st.subheader("Churn Risk Analysis")
    churn_fig = px.histogram(leads_data, x='Churn Risk (%)', title='Churn Risk Distribution')
    st.plotly_chart(churn_fig)

    st.subheader("Cloud Spend vs. Growth Rate")
    scatter_fig = px.scatter(leads_data, x='Estimated Spend ($M/year)', y='Growth Rate (%)', 
                              size='Lead Score', color='Industry', 
                              title='Cloud Spend vs. Growth Rate')
    st.plotly_chart(scatter_fig)

# Section: Export Options
st.sidebar.header("Export Options")
if 'leads_data' in locals():
    if st.sidebar.button("Download Prioritized Leads"):
        csv = leads_data.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(label="Download CSV", data=csv, file_name="prioritized_leads.csv", mime="text/csv")

# Integration Placeholder
st.subheader("CRM Integration")
st.write("Integrate with Salesforce, HubSpot, or other CRM tools for real-time lead tracking and updates.")

# Footer
st.markdown("---")
st.caption("Dashboard by Atharva Deshpande")
