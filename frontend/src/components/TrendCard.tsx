import ProductCard from "./ProductCard";

export default function TrendCard({ trendItem }) {
  return (
    <section className="mb-8 rounded-3xl border border-slate-200 bg-slate-50 p-6">
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-slate-900">🔥 Tendência: {trendItem.trend}</h2>
        <p className="mt-2 text-slate-600">
          Produtos relacionados à tendência extraída da API do Mercado Livre.
        </p>
      </div>

      {trendItem.products.length === 0 ? (
        <div className="rounded-xl bg-white p-4 text-slate-500">
          Nenhum produto encontrado para esta tendência.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {trendItem.products.map((product, index) => (
            <ProductCard key={${trendItem.trend}-${index}} product={product} />
          ))}
        </div>
      )}
    </section>
  );
}