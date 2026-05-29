const API_BASE = process.env.API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const CLIENT_API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function readJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed for ${path} (${response.status})`);
  }
  return (await response.json()) as T;
}

export type OverviewResponse = {
  summary: {
    net_worth: number;
    assets: number;
    liabilities: number;
    change_1d: number;
    change_30d: number;
  };
  account_groups: Array<{ group: string; total: number }>;
  spending: Array<{ category: string; amount: number }>;
  recent_transactions: Array<{
    id: string;
    date: string;
    merchant: string;
    category: string;
    amount: number;
  }>;
};

export type AccountsResponse = {
  accounts: Array<{
    id: string;
    institution: string;
    name: string;
    type: string;
    subtype: string;
    balance: number;
    status: "healthy" | "needs_reauth" | "broken";
  }>;
};

export type NetWorthResponse = {
  history: Array<{ date: string; value: number }>;
};

export type SpendingResponse = {
  categories: Array<{ category: string; amount: number }>;
};

export type RecentTransactionsResponse = {
  items: Array<{
    id: string;
    date: string;
    merchant: string;
    category: string;
    amount: number;
  }>;
};

export type SplitwiseBalancesResponse = {
  friends: Array<{ name: string; balance: number }>;
};

export type CryptoHoldingsResponse = {
  holdings: Array<{ symbol: string; quantity: number; value: number }>;
};

export const api = {
  overview: () => readJson<OverviewResponse>("/analytics/overview"),
  accounts: () => readJson<AccountsResponse>("/plaid/accounts"),
  netWorth: () => readJson<NetWorthResponse>("/analytics/net-worth"),
  spending: () => readJson<SpendingResponse>("/analytics/spending"),
  recentTransactions: () => readJson<RecentTransactionsResponse>("/analytics/transactions/recent"),
  splitwiseBalances: () => readJson<SplitwiseBalancesResponse>("/splitwise/balances"),
  cryptoHoldings: () => readJson<CryptoHoldingsResponse>("/crypto/holdings"),
};

async function readJsonClient<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${CLIENT_API_BASE}${path}`, {
    credentials: "include",
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  const json = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(json.detail ?? `API request failed for ${path} (${response.status})`);
  }
  return json as T;
}

export const clientApi = {
  accounts: () => readJsonClient<AccountsResponse>("/plaid/accounts"),
  splitwiseBalances: (sync = true) => readJsonClient<SplitwiseBalancesResponse>(`/splitwise/balances?sync=${sync}`),
  splitwiseConnect: (accessToken: string, tokenType: "bearer" | "api_key" = "bearer") =>
    readJsonClient<{ message: string }>("/splitwise/connect", {
      method: "POST",
      body: JSON.stringify({ access_token: accessToken, token_type: tokenType }),
    }),
  plaidCreateLinkToken: () => readJsonClient<{ link_token: string; expiration?: string }>("/plaid/link-token/create", { method: "POST" }),
  plaidExchangePublicToken: (publicToken: string) =>
    readJsonClient<{ message: string; item_id: number; institution_name: string; accounts_added: number }>(
      "/plaid/item/public_token/exchange",
      {
        method: "POST",
        body: JSON.stringify({ public_token: publicToken }),
      }
    ),
  plaidSyncTransactions: (itemId?: number) =>
    readJsonClient<{ message: string; new_transactions: number }>("/plaid/transactions/sync", {
      method: "POST",
      body: JSON.stringify({ item_id: itemId }),
    }),
};
