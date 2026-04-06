const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function normalizeProduct(product = {}) {
  return {
    title: product.title ?? "Sem título",
    price: Number(product.price ?? 0),
    sold: Number(product.sold ?? product.sold_quantity ?? 0),
    revenue_estimate: Number(product.revenue_estimate ?? product.revenue ?? 0),
    opportunity_score: Number(product.opportunity_score ?? product.score ?? 0),
  };
}

function normalizeTrendItem(item = {}) {
  return {
    trend: item.trend ?? item.keyword ?? "Sem tendência",
    products: Array.isArray(item.products)
      ? item.products.map(normalizeProduct)
      : [],
  };
}

export async function getMarketAnalysis() {
  const response = await fetch(${API_BASE_URL}/market-analysis);

  if (!response.ok) {
    throw new Error(Erro ao buscar análise: ${response.status});
  }

  const data = await response.json();

  if (!Array.isArray(data)) {
    return [];
  }

  return data.map(normalizeTrendItem);
}