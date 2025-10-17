import firebase_admin
from firebase_admin import messaging, credentials
import os

if not firebase_admin._apps:
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        try:
            firebase_admin.initialize_app()
        except Exception:
            pass

def send_push_for_alert(message, lat=None, lon=None):
    # Sends to topic 'alerts' — in frontend subscribe device to 'alerts' or to per-user topic
    body = message
    if lat and lon:
        body = f"{message} @ {lat:.3f},{lon:.3f}"
    msg = messaging.Message(
        notification=messaging.Notification(title="Streetly Alert", body=body),
        topic="alerts"
    )
    try:
        resp = messaging.send(msg)
        return {"ok": True, "resp": resp}
    except Exception as e:
        return {"ok": False, "error": str(e)}

