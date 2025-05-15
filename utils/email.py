# utils/email.py

import smtplib
from email.mime.text import MIMEText

from core.config import get_settings
from utils.logging import logger
from fastapi.concurrency import run_in_threadpool

settings = get_settings()


def _send_email_sync(to_email: str, subject: str, body: str, from_email: str = None):
    sender_email = from_email or settings.SMTP_FROM

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        if settings.SMTP_SSL:
            server = smtplib.SMTP_SSL(
                settings.SMTP_HOST, settings.SMTP_PORT, timeout=10
            )
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
            server.ehlo()
            if settings.SMTP_TLS:
                server.starttls()
                server.ehlo()

        # Only attempt login if credentials are set
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(
            f"Failed to send email to {to_email}, from {sender_email} on {server}: {e}"
        )


async def send_email(to_email: str, subject: str, body: str, from_email: str = None):
    await run_in_threadpool(_send_email_sync, to_email, subject, body, from_email)


def send_verification_email(to_email: str, token: str):
    verification_url = f"https://127.0.0.1:8000/v1/auth/verify?token={token}"
    subject = "[pywjs] Verify your email for your account"
    body = f"Hi,\n\nPlease verify your email address by clicking the link below:\n\n{verification_url}\n\nIf you did not sign up, ignore this email."
    _send_email_sync(
        to_email=to_email,
        subject=subject,
        body=body,
        from_email=settings.SMTP_FROM,
    )
