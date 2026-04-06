import ProductCard from "./ProductCard";

type Product = {
  title: string;
  price: number;
  sold: number;
  revenue_estimate: number;
  opportunity_score: number;
};

type Props = {
  trendItem: {
    trend: string;
    products: Product[];
  };
};

export default function TrendSection({ trendItem }: Props) {
  return (
    <section className="trend">
      <h2>🔥 {trendItem.trend}</h2>

      <div className="grid">
        {trendItem.products.map((p, i) => (
          <ProductCard key={i} product={p} />
        ))}
      </div>
    </section>
  );
}