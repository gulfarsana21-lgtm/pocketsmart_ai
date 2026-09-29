from app.services.marketplaces import build_search_url


def home_fallback(data: dict) -> dict:
    budget = float(data["budget"])

    allocation = {
        "Furniture": round(budget * 0.45, 2),
        "Lighting": round(budget * 0.18, 2),
        "Decor": round(budget * 0.20, 2),
        "Storage": round(
            budget - budget * 0.45 - budget * 0.18 - budget * 0.20,
            2,
        ),
    }

    return {
        "planner": "home",
        "title": "Home Interior Budget Plan",
        "budget": budget,
        "allocation": allocation,
        "summary": (
            f"Starter plan for {', '.join(data['rooms'])} "
            f"with a {data['style']} preference."
        ),
        "recommendations": [
            {
                "category": "Furniture",
                "name": "Compact sofa or seating set",
                "estimated_price": round(
                    allocation["Furniture"] * 0.60, 2
                ),
                "platform": "Amazon",
                "reason": (
                    f"Suitable as a starting point for a "
                    f"{data['style']} interior."
                ),
                "search_url": build_search_url(
                    "Amazon", "compact sofa seating"
                ),
            },
            {
                "category": "Lighting",
                "name": "LED ceiling and ambient lights",
                "estimated_price": round(
                    allocation["Lighting"] * 0.65, 2
                ),
                "platform": "IKEA",
                "reason": "Adds practical and layered lighting.",
                "search_url": build_search_url(
                    "IKEA", "LED ceiling ambient lights"
                ),
            },
            {
                "category": "Decor",
                "name": "Wall art and accent decor",
                "estimated_price": round(
                    allocation["Decor"] * 0.55, 2
                ),
                "platform": "Amazon",
                "reason": "Adds personality without consuming the whole budget.",
                "search_url": build_search_url(
                    "Amazon", "wall art accent decor"
                ),
            },
            {
                "category": "Storage",
                "name": "Organizer or cabinet solution",
                "estimated_price": round(
                    allocation["Storage"] * 0.70, 2
                ),
                "platform": "IKEA",
                "reason": "Helps keep rooms organized.",
                "search_url": build_search_url(
                    "IKEA", "storage organizer cabinet"
                ),
            },
        ],
        "tips": [
            "Measure spaces before ordering furniture.",
            "Compare seller ratings and return policies.",
            "Keep a small reserve for delivery and unexpected costs.",
            "Buy essential furniture first, then add decor.",
        ],
        "disclaimer": (
            "Fallback recommendations use estimates and search links. "
            "Verify current price and availability before buying."
        ),
        "ai_generated": False,
    }


def party_fallback(data: dict) -> dict:
    budget = float(data["budget"])

    allocation = {
        "Food": round(budget * 0.50, 2),
        "Venue": round(budget * 0.20, 2),
        "Decoration": round(budget * 0.18, 2),
        "Entertainment": round(
            budget - budget * 0.50 - budget * 0.20 - budget * 0.18,
            2,
        ),
    }

    return {
        "planner": "party",
        "title": "Party Budget Plan",
        "budget": budget,
        "allocation": allocation,
        "summary": (
            f"{data['event_type']} plan for {data['guests']} "
            f"guests in {data['city']}."
        ),
        "recommendations": [
            {
                "category": "Food",
                "name": f"Food/catering plan for {data['guests']} guests",
                "estimated_price": allocation["Food"],
                "platform": "Zomato",
                "reason": "Reserve a major portion of the event budget for food and compare menus.",
                "search_url": build_search_url(
                    "Zomato", f"party catering {data['city']}"
                ),
            },
            {
                "category": "Venue",
                "name": "Budget-friendly event venue search",
                "estimated_price": allocation["Venue"],
                "platform": "OYO",
                "reason": "Compare venue or accommodation-style event options where applicable.",
                "search_url": build_search_url(
                    "OYO", f"{data['city']} event venue"
                ),
            },
            {
                "category": "Decoration",
                "name": "Theme decoration package",
                "estimated_price": allocation["Decoration"],
                "platform": "Amazon",
                "reason": "A coordinated theme can be created with reusable decoration items.",
                "search_url": build_search_url(
                    "Amazon", f"{data['event_type']} decoration"
                ),
            },
            {
                "category": "Entertainment",
                "name": "Speaker and simple activity setup",
                "estimated_price": allocation["Entertainment"],
                "platform": "Amazon",
                "reason": "Provides a simple entertainment component without overspending.",
                "search_url": build_search_url(
                    "Amazon", "party speaker games"
                ),
            },
        ],
        "tips": [
            "Confirm per-person food pricing.",
            "Check what the venue includes in its quoted price.",
            "Reserve money for last-minute expenses.",
            "Confirm venue capacity and timing before booking.",
        ],
        "disclaimer": (
            "Vendor prices, availability and service quality must be verified directly."
        ),
        "ai_generated": False,
    }


def jewelry_fallback(data: dict) -> dict:
    budget = float(data["budget"])

    allocation = {
        "Main Jewelry": round(budget * 0.60, 2),
        "Earrings": round(budget * 0.22, 2),
        "Accessories": round(
            budget - budget * 0.60 - budget * 0.22,
            2,
        ),
    }

    return {
        "planner": "jewelry",
        "title": "Jewelry Budget Plan",
        "budget": budget,
        "allocation": allocation,
        "summary": (
            f"{data['style']} jewelry ideas for a "
            f"{data['occasion']} occasion."
        ),
        "recommendations": [
            {
                "category": "Main Jewelry",
                "name": f"{data['style']} necklace or pendant",
                "estimated_price": allocation["Main Jewelry"],
                "platform": "Amazon",
                "reason": (
                    f"Suggested for a {data['occasion']} occasion "
                    f"with a {data['style']} preference."
                ),
                "search_url": build_search_url(
                    "Amazon", f"{data['style']} necklace pendant"
                ),
            },
            {
                "category": "Earrings",
                "name": "Matching earrings",
                "estimated_price": allocation["Earrings"],
                "platform": "Flipkart",
                "reason": "Choose a pair that complements the main jewelry piece.",
                "search_url": build_search_url(
                    "Flipkart", "matching earrings jewelry"
                ),
            },
            {
                "category": "Accessories",
                "name": "Bracelet or bangle",
                "estimated_price": allocation["Accessories"],
                "platform": "Amazon",
                "reason": "Adds a coordinated finishing touch.",
                "search_url": build_search_url(
                    "Amazon", "bracelet bangle"
                ),
            },
        ],
        "tips": [
            "Match metal tone with the outfit and occasion.",
            "Consider the outfit neckline before choosing a necklace.",
            "Check dimensions, material and return policy.",
            "Keep shipping and extra charges inside the final budget.",
        ],
        "disclaimer": (
            "Image-based matching is advisory. Verify color, material, dimensions and current price."
        ),
        "ai_generated": False,
    }
