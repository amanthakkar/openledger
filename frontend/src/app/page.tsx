import { BarList } from "@/components/BarList";
import { StatCard } from "@/components/StatCard";
import { TransactionsTable } from "@/components/TransactionsTable";
import { api } from "@/lib/api";

export default async function DashboardHome() {
  const data = await api.overview();

  return (
    <section>
      <div className="page-header">
        <h2>Dashboard Overview</h2>
        <p className="muted">Net worth, account mix, and recent activity</p>
      </div>

      <div className="grid-3">
        <StatCard label="Net Worth" value={data.summary.net_worth} change={data.summary.change_1d} />
        <StatCard label="Total Assets" value={data.summary.assets} />
        <StatCard label="Total Liabilities" value={data.summary.liabilities} />
      </div>

      <div className="grid-2" style={{ marginTop: "1rem" }}>
        <BarList title="Account Group Totals" items={data.account_groups.map((x) => ({ label: x.group, value: x.total }))} />
        <BarList title="Spending by Category (Month)" items={data.spending.map((x) => ({ label: x.category, value: x.amount }))} />
      </div>

      <div style={{ marginTop: "1rem" }}>
        <TransactionsTable title="Recent Transactions" rows={data.recent_transactions} />
      </div>
    </section>
  );
}
