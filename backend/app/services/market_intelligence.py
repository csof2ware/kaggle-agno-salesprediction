import requests

from app.services.ml_auth import MercadoLivreAuthService

BASE_URL = "https://api.mercadolibre.com"
auth_service = MercadoLivreAuthService()

# fallback estratégico para manter o MVP funcional
FALLBACK_KEYWORDS = [
    "ferramentas",
    "eletronicos",
    "utensilios domesticos",
    "roupas",
    "calcados",
]


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


def get_products_by_keyword(keyword: str):
    response = requests.get(
        f"{BASE_URL}/sites/MLB/search",
        headers=_auth_headers(),
        params={"q": keyword},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


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

        try:
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
        except Exception:
            continue

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
        if p["revenue_estimate"] > 10000:
            s += 2

        p["opportunity_score"] = s

    return sorted(products, key=lambda x: x["opportunity_score"], reverse=True)


def run_market_analysis():
    trends = get_trends()

    keywords = []

    # tenta usar tendências reais
    if isinstance(trends, list):
        for t in trends[:5]:
            if isinstance(t, dict) and t.get("keyword"):
                keywords.append(t["keyword"])

    # fallback se trends falhar
    if not keywords:
        keywords = FALLBACK_KEYWORDS

    results = []

    for keyword in keywords:
        try:
            items = get_products_by_keyword(keyword)[:5]
            enriched = enrich(items)
            scored = score(enriched)

            results.append({
                "trend": keyword,
                "products": scored
            })
        except Exception:
            results.append({
                "trend": keyword,
                "products": []
            })

    return {
        "status": "success",
        "message": "Análise gerada com tendências reais ou fallback por categorias estratégicas",
        "results": results
    }