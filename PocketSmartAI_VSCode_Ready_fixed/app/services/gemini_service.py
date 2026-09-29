import json
from pathlib import Path

from google import genai
from google.genai import types

from app.config import settings


SYSTEM_INSTRUCTION = """
You are PocketSmart AI, a budget-aware recommendation assistant.

Supported planners:
1. Home interior planning
2. Party planning
3. Jewelry planning

Return ONLY valid JSON.

Required top-level fields:
- planner
- title
- budget
- allocation
- summary
- recommendations
- tips
- disclaimer
- ai_generated

Each recommendation must contain:
- category
- name
- estimated_price
- platform
- reason
- search_url

Rules:
- Currency is Indian Rupees.
- Keep the total allocated budget within the supplied budget.
- Estimated prices are not live quotes.
- Never claim inventory or availability is guaranteed.
- Do not invent product IDs or exact marketplace product URLs.
- Use Google search URLs focused on the requested marketplace.
- Keep recommendations practical and concise.
- For outfit images, use only visible clothing color/style information.
- Do not identify people or infer sensitive personal information.
"""


def _get_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _extract_json(text: str) -> dict:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in Gemini response.")

    return json.loads(cleaned[start:end + 1])


def generate_recommendations(
    planner: str,
    data: dict,
    image_path: str | None = None,
) -> dict | None:
    client = _get_client()

    if client is None:
        return None

    prompt = (
        SYSTEM_INSTRUCTION
        + "\n\nPlanner:\n"
        + planner
        + "\n\nUser input:\n"
        + json.dumps(data, ensure_ascii=False, indent=2)
    )

    contents: list = [prompt]

    if image_path:
        path = Path(image_path)
        image_bytes = path.read_bytes()
        mime_type = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }[path.suffix.lower()]

        contents.insert(
            0,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),
        )
        contents.append(
            "Use the uploaded outfit only as visual context for style and color coordination."
        )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.30,
            max_output_tokens=5000,
            response_mime_type="application/json",
        ),
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = _extract_json(response.text)
    result["planner"] = planner
    result["budget"] = float(data["budget"])
    result["ai_generated"] = True
    return result
