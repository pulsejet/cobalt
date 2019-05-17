"""Function to send mail using smtplib"""
import smtplib
import ssl
from email.mime.text import MIMEText

def get_connection(address: str, port: str, username: str, password: str) -> smtplib.SMTP:
    """Get a connection to an SMTP server."""
    context = ssl.create_default_context()
    server = smtplib.SMTP(address, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(username, password)
    return server

def close_connection(server: smtplib.SMTP) -> None:
    """Close the connection to the SMTP server cleanly."""
    server.quit()

def send_html_mail(server: smtplib.SMTP, body: str, addr_from: str, addr_to: str, subject: str) -> None:
    """Ugly helper for sending a single email"""

    msg = MIMEText(body, 'html')

    msg['Subject'] = subject
    msg['From'] = addr_from
    msg['To'] = addr_to

    server.sendmail(addr_from, [addr_to], msg.as_string())

def test_auth(server: str, port: str, username: str, password: str) -> str:
    """Test if authentication succeeds."""

    try:
        conn = get_connection(server, port, username, password)
        close_connection(conn)
        return None
    except smtplib.SMTPException as smtp_exception:
        return str(smtp_exception)
