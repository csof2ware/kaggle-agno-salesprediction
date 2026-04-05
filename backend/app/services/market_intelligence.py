import requests
import os

TOKEN = os.getenv("ML_ACCESS_TOKEN")
BASE_URL = "https://api.mercadolibre.com"


def get_trends():
    return requests.get(f"{BASE_URL}/trends/MLB").json()


def get_item_detail(item_id):
    return requests.get(f"{BASE_URL}/items/{item_id}").json()


def enrich(products):
    result = []

    for p in products:
        detail = get_item_detail(p["id"])

        price = detail.get("price", 0)
        sold = detail.get("sold_quantity", 0)

        result.append({
            "id": p["id"],
            "title": detail.get("title"),
            "price": price,
            "sold": sold,
            "revenue": price * sold
        })

    return result


def score(products):
    if not products:
        return []

    avg_price = sum(p["price"] for p in products) / len(products)

    for p in products:
        s = 0

        if p["sold"] > 100:
            s += 2
        if p["price"] < avg_price:
            s += 1
        if p["revenue"] > 10000:
            s += 2

        p["score"] = s

    return sorted(products, key=lambda x: x["score"], reverse=True)


def run_market_analysis():
    trends = get_trends()

    if not isinstance(trends, list):
        return {
            "error": "Falha ao obter tendências",
            "raw_response": trends
        }

    enriched = enrich(trends[:10])
    ranked = score(enriched)

    return {
        "total_products": len(ranked),
        "products": ranked
    }