function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value || 0);
}

function getScoreLabel(score) {
  if (score >= 5) return "Alta oportunidade";
  if (score >= 3) return "Boa oportunidade";
  return "Baixa oportunidade";
}

export default function ProductCard({ product }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <h4 className="mb-3 text-base font-semibold text-slate-900">{product.title}</h4>

      <div className="grid gap-2 text-sm text-slate-700">
        <div><strong>Preço:</strong> {formatCurrency(product.price)}</div>
        <div><strong>Vendidos:</strong> {product.sold}</div>
        <div><strong>Faturamento estimado:</strong> {formatCurrency(product.revenue_estimate)}</div>
        <div><strong>Score:</strong> {product.opportunity_score}</div>
        <div><strong>Status:</strong> {getScoreLabel(product.opportunity_score)}</div>
      </div>
    </div>
  );
}