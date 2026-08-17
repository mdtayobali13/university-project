from app.tasks.celery_app import celery_app
import time

@celery_app.task
def send_welcome_email(email: str, name: str):
    # Mock sending email
    print(f"Sending welcome email to {name} <{email}>...")
    time.sleep(2)
    print("Email sent successfully!")
    return True

@celery_app.task
def send_order_confirmation_email(email: str, order_id: str):
    # Mock sending email
    print(f"Sending order confirmation to {email} for Order #{order_id}...")
    time.sleep(2)
    print("Email sent successfully!")
    return True

@celery_app.task
def process_low_stock_alerts():
    # Mock processing low stock
    print("Checking for low stock products...")
    time.sleep(2)
    print("Alerts dispatched to vendors.")
    return True
