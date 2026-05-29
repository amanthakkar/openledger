import { formatCurrency } from "@/lib/format";

type Point = {
  date: string;
  value: number;
};

export function LineTrend({ title, points }: { title: string; points: Point[] }) {
  if (points.length === 0) {
    return null;
  }

  const min = Math.min(...points.map((p) => p.value));
  const max = Math.max(...points.map((p) => p.value));
  const span = Math.max(max - min, 1);

  const polyline = points
    .map((point, index) => {
      const x = (index / Math.max(points.length - 1, 1)) * 100;
      const y = 100 - ((point.value - min) / span) * 100;
      return `${x},${y}`;
    })
    .join(" ");

  const latest = points[points.length - 1];

  return (
    <section className="card">
      <div className="line-header">
        <h3>{title}</h3>
        <strong>{formatCurrency(latest.value)}</strong>
      </div>
      <svg className="line-chart" viewBox="0 0 100 100" preserveAspectRatio="none" role="img" aria-label={title}>
        <polyline fill="none" stroke="currentColor" strokeWidth="2.5" points={polyline} />
      </svg>
      <p className="muted">Last {points.length} points</p>
    </section>
  );
}
