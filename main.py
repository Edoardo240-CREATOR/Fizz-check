import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from telegram import Bot
import os

# CONFIG
URL = 'https://short.rent/the-fizz-utrecht'  # esempio, sostituiscilo con l'URL corretto
CHECK_INTERVAL = 300  # 5 minuti

# EMAIL CONFIG
EMAIL_SENDER = 'monitor@fizz-checker.com'
EMAIL_RECEIVER = 'edomonte2001@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# TELEGRAM CONFIG
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# MESSAGGIO
def notify_all(msg):
    print(f"[INFO] Notifica inviata: {msg}")
    send_telegram(msg)
    send_email(msg)

def send_telegram(message):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"[ERROR] Telegram: {e}")

def send_email(message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'THE FIZZ Utrecht - Notifica Disponibilità'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[ERROR] Email: {e}")

def check_availability():
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        if "not available" not in r.text.lower():
            notify_all("🚨 Una stanza potrebbe essere disponibile su THE FIZZ Utrecht!")
        else:
            print("[INFO] Nessuna novità.")
    except Exception as e:
        print(f"[ERROR] Durante il controllo: {e}")

if __name__ == '__main__':
    notify_all("🔍 Monitoraggio THE FIZZ Utrecht avviato con successo.")
    while True:
        check_availability()
        time.sleep(CHECK_INTERVAL)
