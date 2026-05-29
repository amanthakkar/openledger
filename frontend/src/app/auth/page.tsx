 "use client";

import { FormEvent, useMemo, useState } from "react";

type SessionUser = {
  id: number;
  email: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("Not authenticated");
  const [session, setSession] = useState<SessionUser | null>(null);

  const canSubmit = useMemo(() => email.length > 3 && password.length >= 8, [email, password]);

  async function postAuth(path: "/auth/signup" | "/auth/login", event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("Submitting...");
    try {
      const response = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail ?? "Auth request failed");
      }
      setSession(data);
      setStatus(path === "/auth/signup" ? "Account created and logged in" : "Logged in");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function loadSession() {
    setStatus("Checking session...");
    try {
      const response = await fetch(`${API_BASE}/auth/session`, {
        credentials: "include",
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail ?? "Not authenticated");
      }
      setSession(data);
      setStatus("Session active");
    } catch (error) {
      setSession(null);
      setStatus(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function logout() {
    await fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
    setSession(null);
    setStatus("Logged out");
  }

  return (
    <section>
      <div className="page-header">
        <h2>Authentication</h2>
        <p className="muted">Optional in local mode. The app auto-selects your local profile if you skip login.</p>
      </div>

      <div className="grid-2">
        <form className="card" onSubmit={(event) => postAuth("/auth/signup", event)}>
          <h3>Create Account</h3>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            style={{ width: "100%", margin: "0.4rem 0 0.8rem" }}
          />
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="At least 8 characters"
            style={{ width: "100%", margin: "0.4rem 0 1rem" }}
          />
          <button type="submit" disabled={!canSubmit}>
            Sign up
          </button>
        </form>

        <form className="card" onSubmit={(event) => postAuth("/auth/login", event)}>
          <h3>Login</h3>
          <p className="muted">Use existing account credentials</p>
          <button type="submit" disabled={!canSubmit}>
            Login
          </button>
          <div style={{ marginTop: "0.8rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <button type="button" onClick={loadSession}>
              Check Session
            </button>
            <button type="button" onClick={logout}>
              Logout
            </button>
          </div>
          <p className="muted" style={{ marginTop: "0.8rem" }}>
            {status}
          </p>
          {session ? (
            <p>
              Signed in as <strong>{session.email}</strong> (user #{session.id})
            </p>
          ) : null}
        </form>
      </div>
    </section>
  );
}
