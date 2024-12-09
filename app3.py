import streamlit as st
import smtplib
from email.message import EmailMessage
import plotly.graph_objects as go

# Customizing the app title and header
st.set_page_config(page_title="Pump Cloud Savings", layout="wide")

# Add Custom Title and Subtitle
st.title("Pump Cloud Savings Opportunity Notification System")
st.markdown("""
    This tool helps businesses optimize their cloud costs by providing tailored recommendations for reducing
    cloud service utilization. Let's start optimizing your cloud service costs today!
""")

# Styling the form with custom headers
st.subheader("Enter Cloud Configuration to Analyze Savings")

# Input Form for Service Type
service_type = st.selectbox("Select Cloud Service Type", ["Compute (EC2)", "Storage (S3)", "Database (RDS)"],
                            help="Choose the type of cloud service you are using.")

# Service type-specific instance selection
if service_type == "Compute (EC2)":
    instance_type = st.selectbox("Select EC2 Instance Type", ["t2.micro", "t2.small", "t2.medium", "m5.large", "m5.xlarge", "c5.xlarge", "r5.large", "r5.xlarge"],
                                 help="Select the EC2 instance you're using.")
elif service_type == "Storage (S3)":
    instance_type = None  # S3 does not have instance types, so none is selected
elif service_type == "Database (RDS)":
    instance_type = st.selectbox("Select RDS Instance Type", ["db.t3.micro", "db.t3.small", "db.m5.large", "db.m5.xlarge", "db.r5.large", "db.r5.xlarge"],
                                 help="Select the RDS instance you're using.")

# Input for Utilization and Billing
utilization = st.slider("Utilization (%)", min_value=0, max_value=100, value=50,
                        help="How much are you utilizing your cloud resources?")
billing_frequency = st.selectbox("Billing Frequency", ["Hourly", "Monthly"],
                                help="How do you get billed for your cloud services?")
current_cost = st.number_input("Current Cost ($)", min_value=0.0, step=0.01,
                              help="Enter your current cloud service cost.")

# Rule-based logic to analyze savings
def analyze_savings(service_type, utilization, billing_frequency, current_cost, instance_type=None):
    recommendations = []

    # EC2 Recommendations
    if service_type == "Compute (EC2)":
        if instance_type == "t2.micro":
            recommendations.append("Consider upgrading to t2.small or t2.medium if performance requirements increase.")
        elif instance_type == "m5.xlarge":
            recommendations.append("Consider downsizing to m5.large if usage is lower than expected.")
        elif instance_type == "c5.xlarge":
            recommendations.append("Consider switching to m5.xlarge or lower if compute needs decrease.")
        
        if utilization < 40:
            recommendations.append("Consider downsizing the EC2 instance to reduce costs.")
        if billing_frequency == "Hourly":
            recommendations.append("Switch to Reserved Instances or Savings Plans for better rates.")
        elif billing_frequency == "Monthly":
            recommendations.append("Consider switching to an EC2 Spot Instance to reduce costs.")
    
    # S3 Recommendations
    elif service_type == "Storage (S3)":
        if utilization < 20:
            recommendations.append("Move unused data to S3 Glacier or Glacier Deep Archive for reduced costs.")
        if utilization < 40:
            recommendations.append("Consider moving data to S3 Infrequent Access for lower storage costs.")
        if billing_frequency == "Hourly":
            recommendations.append("Use S3 Intelligent-Tiering to automatically move data between access tiers.")
        elif billing_frequency == "Monthly":
            recommendations.append("Switch to S3 Glacier for long-term storage to reduce costs.")

    # RDS Recommendations
    elif service_type == "Database (RDS)":
        if instance_type == "db.m5.large":
            recommendations.append("Consider switching to db.m5.medium or db.t3.medium to save costs if utilization is low.")
        elif instance_type == "db.r5.xlarge":
            recommendations.append("Consider downsizing to db.r5.large if memory requirements are lower.")
        elif instance_type == "db.t3.micro":
            recommendations.append("Consider upgrading to db.t3.small or db.m5.large if performance needs increase.")
        
        if utilization < 50:
            recommendations.append("Consider scaling down your RDS instance.")
        if billing_frequency == "Hourly":
            recommendations.append("Switch to Reserved Instances or Savings Plans for long-term cost savings.")
        elif billing_frequency == "Monthly":
            recommendations.append("Consider using a multi-AZ deployment for high availability if needed.")

    potential_savings = current_cost * 0.6  # Assume 60% savings
    return recommendations, potential_savings

# Analyze savings when button is pressed
if st.button("Analyze Savings"):
    recommendations, potential_savings = analyze_savings(service_type, utilization, billing_frequency, current_cost, instance_type)
    
    # Display Recommendations and Potential Savings
    st.write("### Recommendations:")
    for rec in recommendations:
        st.write(f"- {rec}")
    st.write(f"### Potential Savings: ${potential_savings:.2f}")

def send_email(user_email, recommendations, potential_savings):
    email = EmailMessage()
    email.set_content(f"Recommendations: {', '.join(recommendations)}\nPotential Savings: ${potential_savings:.2f}")
    email["Subject"] = "Cloud Cost Savings Recommendations"
    email["From"] = "your-email@gmail.com"  # Your Gmail address
    email["To"] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Gmail's SMTP server and port for SSL
            server.login("deshpandeatharva188@gmail.com", "wjiv oduf nwoe sjxe")  # Replace with Gmail credentials
            server.send_message(email)
        st.success(f"Email sent to {user_email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Email Input and Button
st.subheader("Send Savings Report")
user_email = st.text_input("Enter recipient email:")
if st.button("Send Notification"):
    if user_email:
        recommendations, potential_savings = analyze_savings(service_type, utilization, billing_frequency, current_cost)
        send_email(user_email, recommendations, potential_savings)
    else:
        st.warning("Please enter a valid email address.")

# Visualization
if st.button("Visualize Savings"):
    recommendations, potential_savings = analyze_savings(service_type, utilization, billing_frequency, current_cost)
    fig = go.Figure(data=[
        go.Bar(name='Current Cost', x=['Cost'], y=[current_cost]),
        go.Bar(name='Optimized Cost', x=['Cost'], y=[current_cost - potential_savings])
    ])
    fig.update_layout(barmode='group', title="Savings Visualization")
    st.plotly_chart(fig)
    
