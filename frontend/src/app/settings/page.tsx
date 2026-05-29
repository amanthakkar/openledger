"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { usePlaidLink } from "react-plaid-link";

import { clientApi, type AccountsResponse, type SplitwiseBalancesResponse } from "@/lib/api";
import { formatCurrency } from "@/lib/format";

export default function SettingsPage() {
  const [splitwiseToken, setSplitwiseToken] = useState("");
  const [splitwiseTokenType, setSplitwiseTokenType] = useState<"bearer" | "api_key">("bearer");
  const [status, setStatus] = useState("Use this page to connect Plaid and Splitwise.");
  const [linkToken, setLinkToken] = useState<string | null>(null);
  const [splitwise, setSplitwise] = useState<SplitwiseBalancesResponse>({ friends: [] });
  const [accounts, setAccounts] = useState<AccountsResponse>({ accounts: [] });
  const [activeAction, setActiveAction] = useState<string>("");

  const refreshData = useCallback(async () => {
    setActiveAction("refresh");
    try {
      const [balances, accountData] = await Promise.all([clientApi.splitwiseBalances(false), clientApi.accounts()]);
      setSplitwise(balances);
      setAccounts(accountData);
      setStatus("Refreshed provider data.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Could not refresh provider data.");
    } finally {
      setActiveAction("");
    }
  }, []);

  useEffect(() => {
    void refreshData();
  }, [refreshData]);

  const onSuccess = useCallback(
    async (publicToken: string) => {
      try {
        setActiveAction("plaid-connect");
        setStatus("Exchanging Plaid public token...");
        const result = await clientApi.plaidExchangePublicToken(publicToken);
        setStatus(`${result.institution_name} connected. ${result.accounts_added} accounts imported.`);
        await refreshData();
      } catch (error) {
        setStatus(error instanceof Error ? error.message : "Failed to exchange Plaid token");
      } finally {
        setActiveAction("");
      }
    },
    [refreshData]
  );

  const plaidConfig = useMemo(
    () => ({
      token: linkToken,
      onSuccess,
    }),
    [linkToken, onSuccess]
  );
  const { open, ready } = usePlaidLink(plaidConfig);

  async function createLinkToken() {
    try {
      setActiveAction("plaid-link-token");
      setStatus("Requesting Plaid link token...");
      const data = await clientApi.plaidCreateLinkToken();
      setLinkToken(data.link_token);
      setStatus("Link token ready. Click Connect with Plaid.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Could not create Plaid link token");
    } finally {
      setActiveAction("");
    }
  }

  async function syncPlaid() {
    try {
      setActiveAction("plaid-sync");
      setStatus("Running Plaid transaction sync...");
      const result = await clientApi.plaidSyncTransactions();
      setStatus(`Plaid sync complete. ${result.new_transactions} new transactions.`);
      await refreshData();
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Plaid sync failed");
    } finally {
      setActiveAction("");
    }
  }

  async function connectSplitwise() {
    try {
      setActiveAction("splitwise-sync");
      setStatus("Saving Splitwise token...");
      await clientApi.splitwiseConnect(splitwiseToken, splitwiseTokenType);
      const balances = await clientApi.splitwiseBalances(true);
      setSplitwise(balances);
      setStatus("Splitwise connected and balances synced.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Splitwise connection failed");
    } finally {
      setActiveAction("");
    }
  }

  const splitwiseNet = splitwise.friends.reduce((sum, row) => sum + row.balance, 0);

  return (
    <section>
      <div className="page-header">
        <h2>Settings & Connections</h2>
        <p className="muted">Connect providers, sync data, and verify account imports</p>
      </div>

      <p className="muted">{status}</p>
      <div className="card" style={{ marginBottom: "1rem" }}>
        <strong>Splitwise Net Balance: {formatCurrency(splitwiseNet)}</strong>
        <p className="muted" style={{ marginTop: "0.4rem" }}>
          Positive means others owe you. Negative means you owe others.
        </p>
      </div>

      <div className="grid-2">
        <div className="card">
          <h3>Plaid Connection</h3>
          <p className="muted">Generate a link token and connect an institution.</p>
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <button type="button" onClick={createLinkToken} disabled={Boolean(activeAction)}>
              {activeAction === "plaid-link-token" ? "Generating..." : "Generate Link Token"}
            </button>
            <button type="button" onClick={() => open()} disabled={!ready || !linkToken || Boolean(activeAction)}>
              {activeAction === "plaid-connect" ? "Connecting..." : "Connect with Plaid"}
            </button>
            <button type="button" onClick={syncPlaid} disabled={Boolean(activeAction)}>
              {activeAction === "plaid-sync" ? "Syncing..." : "Sync Transactions"}
            </button>
            <button type="button" onClick={refreshData} disabled={Boolean(activeAction)}>
              {activeAction === "refresh" ? "Refreshing..." : "Refresh Accounts"}
            </button>
          </div>
          <ul style={{ marginTop: "0.8rem" }}>
            {accounts.accounts.map((account) => (
              <li key={account.id}>
                {account.institution} - {account.name}: {formatCurrency(account.balance)}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h3>Splitwise Connection</h3>
          <p className="muted">Paste your Splitwise OAuth access token and sync balances.</p>
          <label htmlFor="splitwise-token-type">Token Type</label>
          <select
            id="splitwise-token-type"
            value={splitwiseTokenType}
            onChange={(event) => setSplitwiseTokenType(event.target.value as "bearer" | "api_key")}
            style={{ width: "100%", margin: "0.4rem 0 0.8rem" }}
          >
            <option value="bearer">OAuth Bearer Token</option>
            <option value="api_key">Splitwise API Key</option>
          </select>
          <input
            type="text"
            value={splitwiseToken}
            onChange={(event) => setSplitwiseToken(event.target.value)}
            placeholder="Splitwise access token"
            style={{ width: "100%", marginBottom: "0.75rem" }}
          />
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <button type="button" onClick={connectSplitwise} disabled={!splitwiseToken.trim() || Boolean(activeAction)}>
              {activeAction === "splitwise-sync" ? "Syncing..." : "Save Token & Sync"}
            </button>
            <button type="button" onClick={refreshData} disabled={Boolean(activeAction)}>
              {activeAction === "refresh" ? "Refreshing..." : "Refresh"}
            </button>
          </div>
          <ul style={{ marginTop: "0.8rem" }}>
            {splitwise.friends.map((friend, idx) => (
              <li key={`${friend.name}-${idx}`}>
                {friend.name}: {formatCurrency(friend.balance)}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
