const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export type Product = {
  title: string;
  price: number;
  sold: number;
  revenue_estimate: number;
  opportunity_score: number;
};

export type TrendItem = {
  trend: string;
  products: Product[];
};

export type MarketResponse = {
  status: "success" | "error";
  message?: string;
  results: TrendItem[];
};

function normalizeProduct(product: any): Product {
  return {
    title: product?.title ?? "Sem título",
    price: Number(product?.price ?? 0),
    sold: Number(product?.sold ?? product?.sold_quantity ?? 0),
    revenue_estimate: Number(product?.revenue_estimate ?? 0),
    opportunity_score: Number(product?.opportunity_score ?? 0),
  };
}

function normalizeTrend(item: any): TrendItem {
  return {
    trend: item?.trend ?? "Sem tendência",
    products: Array.isArray(item?.products)
      ? item.products.map(normalizeProduct)
      : [],
  };
}

export async function getMarketAnalysis(): Promise<MarketResponse> {
  const response = await fetch(`${API_BASE_URL}/market-analysis`);

  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }

  const data = await response.json();

  return {
    status: data?.status ?? "error",
    message: data?.message,
    results: Array.isArray(data?.results)
      ? data.results.map(normalizeTrend)
      : [],
  };
}