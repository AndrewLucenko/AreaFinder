import google.genai as genai

client = genai.Client(api_key="AIzaSyA7DRc4Sw862eKfv1k25VzXBxNOLjCKirU")

def get_place_description(name: str, score: float) -> str:
    prompt = f"""
    Write a short and vivid 2–3 sentence description of a place.
    Name: {name}
    Score: {score}

    The description must be:
    - concise (max 35 words)
    - friendly and tourist-oriented
    - do NOT mention the score
    - describe atmosphere, vibe, who would like this place
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )

    return response.text.strip()