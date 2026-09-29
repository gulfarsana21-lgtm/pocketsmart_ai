from urllib.parse import quote_plus


PLATFORM_DOMAINS = {
    "Amazon": "amazon.in",
    "Flipkart": "flipkart.com",
    "IKEA": "ikea.com",
    "Swiggy": "swiggy.com",
    "Zomato": "zomato.com",
    "OYO": "oyorooms.com",
}


def build_search_url(platform: str, query: str) -> str:
    domain = PLATFORM_DOMAINS.get(platform, "google.com")
    encoded_query = quote_plus(query.strip())

    return (
        "https://www.google.com/search?q="
        f"site%3A{quote_plus(domain)}+{encoded_query}"
    )
