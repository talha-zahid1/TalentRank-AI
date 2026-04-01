from google import genai
from schemas.appschema import *
import json
setting = Settings()
client=genai.Client(api_key=setting.AI_API_KEY)


def get_skills(resume_text):
    try:
        prompt = f"""Extract all technical skills from the following resume text.Return the output strictly in JSON format:(no explanation, no extra text)
        {{
        "skills": []
        }}
        Resume :{resume_text}
        """
        response= client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
            )
        text=response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)
        
        # print(data.get("skills", []))
        return data.get("skills", [])
    except Exception as e:
        print("ERROR:", e)
        return []

