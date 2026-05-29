import { BarList } from "@/components/BarList";
import { api } from "@/lib/api";

export default async function BudgetsPage() {
  const data = await api.spending();

  return (
    <section>
      <div className="page-header">
        <h2>Budgets & Goals</h2>
        <p className="muted">Budget engine is pending; current spend categories are loaded</p>
      </div>
      <BarList
        title="Current Month Spend by Category"
        items={data.categories.map((item) => ({ label: item.category, value: item.amount }))}
      />
    </section>
  );
}
