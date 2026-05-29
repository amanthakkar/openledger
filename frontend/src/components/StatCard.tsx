import { formatCurrency, signedCurrency } from "@/lib/format";

type StatCardProps = {
  label: string;
  value: number;
  change?: number;
};

export function StatCard({ label, value, change }: StatCardProps) {
  return (
    <article className="card stat-card">
      <p className="muted">{label}</p>
      <h3>{formatCurrency(value)}</h3>
      {typeof change === "number" ? (
        <p className={change >= 0 ? "positive" : "negative"}>{signedCurrency(change)} today</p>
      ) : null}
    </article>
  );
}
