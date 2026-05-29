 "use client";

import { useEffect, useState } from "react";

import { clientApi, type AccountsResponse } from "@/lib/api";
import { formatCurrency } from "@/lib/format";

export default function AccountsPage() {
  const [data, setData] = useState<AccountsResponse>({ accounts: [] });
  const [error, setError] = useState("");

  useEffect(() => {
    clientApi
      .accounts()
      .then((next) => setData(next))
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section>
      <div className="page-header">
        <h2>Accounts</h2>
        <p className="muted">Institution connections and balances</p>
      </div>
      {error ? <p className="negative">Could not load accounts: {error}</p> : null}

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Institution</th>
                <th>Account</th>
                <th>Type</th>
                <th>Balance</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.accounts.map((account) => (
                <tr key={account.id}>
                  <td>{account.institution}</td>
                  <td>{account.name}</td>
                  <td>
                    {account.type} / {account.subtype}
                  </td>
                  <td>{formatCurrency(account.balance)}</td>
                  <td>
                    <span className="status-pill">{account.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
