import { TransactionsTable } from "@/components/TransactionsTable";
import { api } from "@/lib/api";

export default async function TransactionsPage() {
  const data = await api.recentTransactions();

  return (
    <section>
      <div className="page-header">
        <h2>Transactions</h2>
        <p className="muted">Search and filter wiring is next, recent feed is live</p>
      </div>
      <TransactionsTable title="Recent Transactions Feed" rows={data.items} />
    </section>
  );
}
