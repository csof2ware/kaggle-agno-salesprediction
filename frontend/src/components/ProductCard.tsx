type Props = {
  product: {
    title: string;
    price: number;
    sold: number;
    revenue_estimate: number;
    opportunity_score: number;
  };
};

function formatCurrency(value: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

export default function ProductCard({ product }: Props) {
  return (
    <div className="card">
      <h4>{product.title}</h4>

      <p>💰 {formatCurrency(product.price)}</p>
      <p>📦 Vendidos: {product.sold}</p>
      <p>📊 Receita: {formatCurrency(product.revenue_estimate)}</p>
      <p>⭐ Score: {product.opportunity_score}</p>
    </div>
  );
}