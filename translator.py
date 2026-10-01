import requests


LANGUAGE_CODES = {
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Marathi": "mr"
}


SCRIPT_RANGES = {
    "Kannada": (0x0C80, 0x0CFF),
    "Hindi": (0x0900, 0x097F),
    "Telugu": (0x0C00, 0x0C7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Marathi": (0x0900, 0x097F)
}


def has_wrong_script(text, language):

    if language not in SCRIPT_RANGES:
        return False

    start, end = SCRIPT_RANGES[language]

    for char in text:

        if not char.isalpha():
            continue

        code = ord(char)

        if not (start <= code <= end):
            return True

    return False


def looks_like_prompt(text):

    bad_patterns = [
        "1.",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
        "7.",
        "8.",
        "9.",
        "10.",
        "IMPORTANT",
        "IMPORTANT:",
        "ಪ್ರಮುಖ:",
        "महत्वाचे:",
        "முக்கிய:",
        "ముఖ్యమైనది:"
    ]

    return any(pattern in text for pattern in bad_patterns)


def translate_to_language(text, language):

    if language == "English":
        return text

    if language not in LANGUAGE_CODES:
        return text

    code = LANGUAGE_CODES[language]

    prompt = f"""Translate the English text below into {language}.

Return ONLY the translated text.
Do not repeat the instructions.
Do not add explanations.
Do not add numbered lists.

English text:
<<<
{text}
>>>

{language} translation:"""

    for attempt in range(2):

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
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 100
                }
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()["message"]["content"].strip()

        if not has_wrong_script(result, language) and not looks_like_prompt(result):
            return result

        prompt = f"""Translate ONLY this sentence into {language}.
Output only the translation.

{text}"""

    return result