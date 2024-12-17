import requests
from src.config.config import Config

def validate_email(email):
    # Assuming Truemail is hosted and accessible via an API endpoint
    url = f"http://your-truemail-instance/api/v1/validate?email={email}"
    headers = {
        'Authorization': f'Bearer {Config.TRUEMAIL_API_KEY}'  # Assuming API key is used for authentication
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    if data.get("result"):
        return {
            "email": email,
            "status": data["result"].get("status"),
            "score": data["result"].get("score", 0)
        }
    return {"email": email, "status":"unknown", "score":0} 