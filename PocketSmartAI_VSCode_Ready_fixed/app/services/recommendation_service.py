from app.services.fallback import home_fallback, jewelry_fallback, party_fallback
from app.services.gemini_service import generate_recommendations


FALLBACKS = {
    "home": home_fallback,
    "party": party_fallback,
    "jewelry": jewelry_fallback,
}


def _number(value) -> float:
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0


def normalize_result(planner: str, data: dict, result: dict) -> dict:
    budget = float(data["budget"])

    allocation_raw = result.get("allocation") or {}
    allocation = {
        str(key): round(_number(value), 2)
        for key, value in allocation_raw.items()
    }

    total = sum(allocation.values())
    if total > budget and total > 0:
        factor = budget / total
        allocation = {
            key: round(value * factor, 2)
            for key, value in allocation.items()
        }

    recommendations = []
    for raw in result.get("recommendations") or []:
        if not isinstance(raw, dict):
            continue

        recommendations.append(
            {
                "category": str(raw.get("category", "General")),
                "name": str(raw.get("name", "Suggested option")),
                "estimated_price": _number(raw.get("estimated_price", 0)),
                "platform": str(raw.get("platform", "Google")),
                "reason": str(raw.get("reason", "Practical option.")),
                "search_url": str(raw.get("search_url", "https://www.google.com")),
            }
        )

    if not recommendations:
        raise ValueError("Gemini returned no usable recommendations.")

    tips = [str(tip) for tip in (result.get("tips") or [])][:10]
    if not tips:
        tips = ["Verify current pricing and availability before purchase."]

    return {
        "planner": planner,
        "title": str(result.get("title", f"{planner.title()} Budget Plan")),
        "budget": budget,
        "allocation": allocation,
        "summary": str(result.get("summary", "AI-generated budget recommendation.")),
        "recommendations": recommendations,
        "tips": tips,
        "disclaimer": str(
            result.get(
                "disclaimer",
                "Verify current prices and availability before purchasing.",
            )
        ),
        "ai_generated": bool(result.get("ai_generated", True)),
    }


def get_recommendations(
    planner: str,
    data: dict,
    image_path: str | None = None,
) -> dict:
    if planner not in FALLBACKS:
        raise ValueError(f"Unsupported planner: {planner}")

    try:
        ai_result = generate_recommendations(
            planner=planner,
            data=data,
            image_path=image_path,
        )
        if ai_result:
            return normalize_result(planner, data, ai_result)
    except Exception as exc:
        print(f"[PocketSmart AI] Gemini unavailable; using fallback: {exc}")

    return FALLBACKS[planner](data)
