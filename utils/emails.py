from fastapi import FastAPI, HTTPException
import requests
from src.models import Land , User 
from src.database import SessionLocal   
from src.models import Land, User


app = FastAPI()


BREVO_API_KEY = "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"  
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_welcome_mail(to_email: str, to_name: str):
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "sender": {"name": "IRRIGO Platform", "email": "smart.agriculture.999@gmail.com"},  # Change this to your verified sender email
        "to": [{"email": to_email, "name": to_name}],
        "subject": "Welcome to IRRIGO Platform - Transforming Farming with Technology! 🌱🚀",
        "htmlContent": f"""
            <html>
            <body>
                <h2>Dear {to_name},</h2>
                <p>Welcome to <b>IRRIGO Platform</b>! We're thrilled to have you on board as we revolutionize modern farming with data-driven insights and automation.</p>

                <h3>What is IRRIGO Platform?</h3>
                <p>Our platform empowers farmers and agricultural professionals with real-time data monitoring, AI-powered recommendations, and smart irrigation control to enhance productivity and sustainability.</p>

                <h3>Key Features You’ll Love:</h3>
                <ul>
                    <li>🌍 <b>Real-time Environmental Monitoring</b> – Track soil moisture, temperature, humidity, wind speed, and more through IoT-powered sensors.</li>
                    <li>📊 <b>Data Analytics & Visualization</b> – Get insightful reports and trend analysis to make informed decisions.</li>
                    <li>🤖 <b>AI-Powered Irrigation Recommendations</b> – Our system analyzes soil and weather data to suggest optimal irrigation schedules.</li>
                    <li>📡 <b>Remote Access & Notifications</b> – Receive alerts and updates via email or mobile notifications for critical changes in farm conditions.</li>
                    <li>⚡ <b>User-Friendly Dashboard</b> – Access your farm data anytime, anywhere through our interactive mobile and web apps.</li>
                </ul>

                <h3>Getting Started:</h3>
                <ol>
                    <li>1️⃣ <b>Log in to your account.</b></li>
                    <li>2️⃣ <b>Set up your farm profile</b> and connect your sensors.</li>
                    <li>3️⃣ <b>Start receiving real-time insights</b> and recommendations!</li>
                </ol>

                <p>Let's cultivate a smarter future together! 🌾</p>

                <p>Best regards,<br><b>IRRIGO Platform Team</b></p>
            </body>
            </html>
        """
    }

    try:
        response = requests.post(BREVO_API_URL, json=data, headers=headers)
        response.raise_for_status() 

        return {"message": f"Welcome email sent to {to_email}."}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def send_irrigation_decision_email(to_email: str, to_name: str, land_id: int):
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "sender": {"name": "IRRIGO Platform", "email": "smart.agriculture.999@gmail.com"},
        "to": [{"email": to_email, "name": to_name}],
        "subject": "New Soil and Weather Data Available – Irrigation Decision Needed",
        "htmlContent": f"""
            <html>
            <body>
                <h2>Dear {to_name},</h2>
                <p>We hope you're doing well.</p>
                
                <p>New data regarding your land <b>ID: {land_id}</b> soil and weather conditions has just been recorded in the system. Based on this update, we kindly remind you to review the latest readings and determine if irrigation is necessary.</p>

                <p>You can check the details and make your decision through your dashboard.</p>

                <p>If you have enabled automatic irrigation, the system will proceed based on the recommended settings. Otherwise, please review the data and take action accordingly.</p>

                <p>If you have any questions, feel free to reach out.</p>

                <p>Best regards,<br><b>IRRIGO Platform Team</b></p>
            </body>
            </html>
        """
    }

    try:
        response = requests.post(BREVO_API_URL, json=data, headers=headers)
        response.raise_for_status() 

        return {"message": f"Irrigation decision email sent to {to_email}."}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


def send_irrigation_emails_to_all():  
    db = SessionLocal()

    land_owners = db.query(
        User.user_id, 
        User.firstname, 
        User.lastname, 
        User.email, 
        Land.land_id
    ).join(Land, User.user_id == Land.user_id).all()

    if not land_owners:
        return {"message": "No landowners found."}

    for owner in land_owners:
        user_id, firstname, lastname, email, land_id = owner  
        full_name = f"{firstname} {lastname}" 
        send_irrigation_decision_email(to_email=email, to_name=full_name, land_id=land_id)

    return {"message": "Irrigation decision emails sent to all landowners."}