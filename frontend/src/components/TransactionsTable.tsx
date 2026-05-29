import { formatCurrency } from "@/lib/format";

type Transaction = {
  id: string;
  date: string;
  merchant: string;
  category: string;
  amount: number;
};

export function TransactionsTable({ title, rows }: { title: string; rows: Transaction[] }) {
  return (
    <section className="card">
      <h3>{title}</h3>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Merchant</th>
              <th>Category</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>{row.date}</td>
                <td>{row.merchant}</td>
                <td>{row.category}</td>
                <td className={row.amount >= 0 ? "positive" : "negative"}>{formatCurrency(row.amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
