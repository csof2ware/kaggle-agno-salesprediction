import { useEffect, useState } from "react";
import { getMarketAnalysis, type MarketResponse } from "./services/api";
import TrendSection from "./components/TrendSection";
import "./App.css";

export default function App() {
  const [data, setData] = useState<MarketResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const result = await getMarketAnalysis();
        setData(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <div className="container">
      <h1>AGNO Market Intelligence</h1>

      {loading && <p>Carregando...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data?.status === "error" && (
        <div style={{ color: "orange" }}>
          <p>⚠️ Backend retornou erro</p>
          <p>{data.message}</p>
        </div>
      )}

      {data?.status === "success" &&
        data.results.map((trend, index) => (
          <TrendSection key={index} trendItem={trend} />
        ))}
    </div>
  );
}