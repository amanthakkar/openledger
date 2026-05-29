import { formatCurrency } from "@/lib/format";

type BarItem = {
  label: string;
  value: number;
};

type BarListProps = {
  title: string;
  items: BarItem[];
};

export function BarList({ title, items }: BarListProps) {
  const max = Math.max(...items.map((item) => Math.abs(item.value)), 1);

  return (
    <section className="card">
      <h3>{title}</h3>
      <div className="bar-list">
        {items.map((item) => (
          <div key={item.label} className="bar-row">
            <div className="bar-row-label">
              <span>{item.label}</span>
              <span>{formatCurrency(item.value)}</span>
            </div>
            <div className="bar-track">
              <div className="bar-fill" style={{ width: `${(Math.abs(item.value) / max) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
