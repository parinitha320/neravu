from fastapi import FastAPI
from pydantic import BaseModel
import requests
from safety import check_safety
from translator import translate_to_language
from alerts import send_child_alert


app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    language: str = "English"
    child_email: str = "demo@example.com"


@app.get("/")
def home():
    return {"message": "Neravu backend is working!"}


def ask_qwen(message):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:7b",
            "messages": [
                {
                    "role": "system",
                    "content": (
                         "You are Neravu, an AI companion for elderly users. "
                         "Give short, simple, practical answers. "
                         "Use simple English because your answer will be translated "
                         "into an Indian language. "
                         "Keep normal answers to 2 or 3 short sentences. "
                         "Do not use emojis, slang, complicated words, or long lists. "
                         "Do not give a medical diagnosis. "
                         "For serious health situations, advise contacting a family member, "
                         "caregiver, or healthcare professional."
)
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False,
            "options": {
                 "temperature": 0.1,
                 "num_predict": 120
}
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def translate_text(text, language):
    language_prompts = {
        "Kannada": "Translate this into Kannada. Use natural Kannada script.",
        "Telugu": "Translate this into Telugu. Use natural Telugu script.",
        "Tamil": "Translate this into Tamil. Use natural Tamil script.",
        "Hindi": "Translate this into Hindi. Use natural Hindi script.",
        "Marathi": "Translate this into Marathi. Use natural Marathi script."
    }

    prompt = (
    f"{language_prompts[language]}\n\n"
    "IMPORTANT: Output ONLY the requested language. "
    "Do not mix English, Hindi, Telugu, Tamil, Marathi, "
    "or any other language into the translation. "
    "Keep the meaning simple and natural for an elderly user.\n\n"
    f"Text to translate:\n{text}"
 )

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "translategemma:4b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


@app.post("/chat")
def chat(request: ChatRequest):

    urgent_messages = {
        "English": (
            "This may be an urgent situation. "
            "Please contact a family member, caregiver, "
            "or local emergency medical service immediately."
        ),

        "Kannada": (
            "ಇದು ತುರ್ತು ಪರಿಸ್ಥಿತಿಯಾಗಿರಬಹುದು. "
            "ದಯವಿಟ್ಟು ತಕ್ಷಣ ಕುಟುಂಬದ ಸದಸ್ಯರನ್ನು, ಆರೈಕೆದಾರರನ್ನು "
            "ಅಥವಾ ಸ್ಥಳೀಯ ತುರ್ತು ವೈದ್ಯಕೀಯ ಸೇವೆಯನ್ನು ಸಂಪರ್ಕಿಸಿ."
        ),

        "Telugu": (
            "ఇది అత్యవసర పరిస్థితి కావచ్చు. "
            "దయచేసి వెంటనే కుటుంబ సభ్యుడిని, సంరక్షకుడిని "
            "లేదా స్థానిక అత్యవసర వైద్య సేవలను సంప్రదించండి."
        ),

        "Hindi": (
            "यह एक आपातकालीन स्थिति हो सकती है। "
            "कृपया तुरंत परिवार के किसी सदस्य, देखभाल करने वाले व्यक्ति "
            "या स्थानीय आपातकालीन चिकित्सा सेवा से संपर्क करें।"
        ),

        "Tamil": (
            "இது அவசர நிலையாக இருக்கலாம். "
            "தயவுசெய்து உடனடியாக குடும்ப உறுப்பினர், பராமரிப்பாளர் "
            "அல்லது உள்ளூர் அவசர மருத்துவ சேவையைத் தொடர்பு கொள்ளுங்கள்."
        ),

        "Marathi": (
            "ही एक आपत्कालीन परिस्थिती असू शकते. "
            "कृपया त्वरित कुटुंबातील सदस्य, काळजीवाहक "
            "किंवा स्थानिक आपत्कालीन वैद्यकीय सेवेशी संपर्क साधा."
        )
    }

    if check_safety(request.message):
        alert = send_child_alert(
            request.message,
            request.child_email
        )
        return {
            "reply": urgent_messages.get(
                request.language,
                urgent_messages["English"]
            ),
            "language": request.language,
            "urgent": True,
            "child_alert_sent": alert["sent"],
            "child_email": alert["recipient"]

        }

    answer = ask_qwen(request.message)
    final_answer = translate_to_language(answer, request.language)

    

    return {
        "reply": final_answer,
        "language": request.language,
        "urgent": False
    }