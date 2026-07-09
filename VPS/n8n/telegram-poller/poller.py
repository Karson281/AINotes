import time
import os
import requests
import json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
N8N_URL = os.environ.get("N8N_URL", "http://n8n:5678/webhook/telegram-local")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
offset = 0

print(f"🟢 Starting Telegram Poller")
print(f"📡 BOT_TOKEN set: {'Yes' if BOT_TOKEN else 'No'}")
print(f"🔐 WEBHOOK_SECRET set: {'Yes' if WEBHOOK_SECRET else 'No'}")
print(f"🌐 n8n URL: {N8N_URL}\n")

while True:
    try:
        res = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
            params={"offset": offset + 1, "timeout": 10}
        )
        res.raise_for_status()
        updates = res.json()

        if updates.get("result"):
            print(f"📥 Received {len(updates['result'])} update(s)")

        for update in updates.get("result", []):
            offset = update["update_id"]
            print(f"\n➡️ Sending update to n8n:")
            print(f"POST {N8N_URL}")

            try:
                headers = {"Content-Type": "application/json"}
                if WEBHOOK_SECRET:
                    headers["X-Webhook-Secret"] = WEBHOOK_SECRET
                webhook_response = requests.post(N8N_URL, json=update, headers=headers)
                print(f"✅ Webhook response: {webhook_response.status_code}")
            except Exception as we:
                print(f"❌ Error posting to webhook: {we}")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Polling error: {e}")
        time.sleep(5)
