import { LineTrend } from "@/components/LineTrend";
import { api } from "@/lib/api";

export default async function NetWorthPage() {
  const data = await api.netWorth();

  return (
    <section>
      <div className="page-header">
        <h2>Net Worth</h2>
        <p className="muted">30-point trend from MVP analytics endpoint</p>
      </div>
      <LineTrend title="Net Worth Trend" points={data.history} />
    </section>
  );
}
