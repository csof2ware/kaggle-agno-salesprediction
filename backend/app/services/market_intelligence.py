import requests

from app.services.ml_auth import MercadoLivreAuthService

BASE_URL = "https://api.mercadolibre.com"
auth_service = MercadoLivreAuthService()


def _auth_headers():
    token = auth_service.get_valid_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }


def get_trends():
    try:
        response = requests.get(
            f"{BASE_URL}/trends/MLB",
            headers=_auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        # garante lista
        if not isinstance(data, list):
            return {
                "error": "Resposta inesperada ao obter tendências",
                "raw_response": data,
            }

        return data

    except Exception as e:
        return {
            "error": "Falha ao obter tendências",
            "raw_response": str(e),
        }


def get_item_detail(item_id):
    response = requests.get(
        f"{BASE_URL}/items/{item_id}",
        headers=_auth_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def enrich(products):
    result = []

    for p in products:
        item_id = p.get("id")
        if not item_id:
            continue

        detail = get_item_detail(item_id)

        price = detail.get("price", 0) or 0
        sold = detail.get("sold_quantity", 0) or 0

        result.append({
            "title": detail.get("title", "Sem título"),
            "price": price,
            "sold": sold,
            "revenue_estimate": price * sold,
            "opportunity_score": 0,
        })

    return result


def score(products):
    if not products:
        return []

    avg_price = sum(p["price"] for p in products) / len(products) if products else 0

    for p in products:
        s = 0
        if p["sold"] > 100:
            s += 2
        if p["price"] < avg_price:
            s += 1
        if p["revenue_estimate"] > 10000:
            s += 2
        p["opportunity_score"] = s

    return sorted(products, key=lambda x: x["opportunity_score"], reverse=True)


def run_market_analysis():
    trends = get_trends()

    # 🔥 se vier erro, devolve erro estruturado e não quebra
    if isinstance(trends, dict) and trends.get("error"):
        return {
            "status": "error",
            "stage": "get_trends",
            "message": trends["error"],
            "details": trends.get("raw_response"),
            "results": [],
        }

    if not isinstance(trends, list):
        return {
            "status": "error",
            "stage": "get_trends",
            "message": "Formato inesperado de tendências",
            "details": trends,
            "results": [],
        }

    results = []

    for t in trends[:5]:
        if not isinstance(t, dict):
            continue

        keyword = t.get("keyword", "")
        if not keyword:
            continue

        response = requests.get(
            f"{BASE_URL}/sites/MLB/search",
            headers=_auth_headers(),
            params={"q": keyword},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        items = data.get("results", [])[:5]
        enriched = enrich(items)
        scored = score(enriched)

        results.append({
            "trend": keyword,
            "products": scored
        })

    return {
        "status": "success",
        "results": results
    }