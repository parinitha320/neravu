import requests

API_URL = "http://127.0.0.1:8000"


def send_message(message, language):

    try:
        response = requests.post(
            f"{API_URL}/api/chat",
            json={
                "message": message,
                "language": language
            },
            timeout=10
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("ERROR:", e)
        raise