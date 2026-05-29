CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE plaid_items (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    institution_name VARCHAR(255) NOT NULL,
    institution_id VARCHAR(100) NOT NULL,
    access_token_encrypted TEXT NOT NULL,
    cursor VARCHAR(255),
    status VARCHAR(50) DEFAULT 'healthy' NOT NULL,
    last_synced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    plaid_item_id INT REFERENCES plaid_items(id) NOT NULL,
    plaid_account_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    official_name VARCHAR(255),
    type VARCHAR(50) NOT NULL,
    subtype VARCHAR(50),
    current_balance DECIMAL(12,2),
    available_balance DECIMAL(12,2),
    currency VARCHAR(3) DEFAULT 'USD' NOT NULL,
    is_hidden BOOLEAN DEFAULT FALSE NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    account_id INT REFERENCES accounts(id) NOT NULL,
    plaid_transaction_id VARCHAR(255) UNIQUE NOT NULL,
    date DATE NOT NULL,
    merchant_name VARCHAR(255),
    description VARCHAR(500),
    amount DECIMAL(12,2) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    is_recurring BOOLEAN DEFAULT FALSE NOT NULL,
    is_excluded BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE net_worth_snapshots (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    date DATE NOT NULL,
    total_assets DECIMAL(14,2) NOT NULL,
    total_liabilities DECIMAL(14,2) NOT NULL,
    net_worth DECIMAL(14,2) NOT NULL,
    breakdown JSONB NOT NULL,
    UNIQUE(user_id, date)
);

CREATE TABLE splitwise_balances (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    friend_name VARCHAR(255) NOT NULL,
    friend_id VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE holdings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,
    account_id INT REFERENCES accounts(id) NOT NULL,
    security_name VARCHAR(255) NOT NULL,
    ticker VARCHAR(20),
    quantity DECIMAL(14,6) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    value DECIMAL(14,2) NOT NULL,
    cost_basis DECIMAL(14,2),
    updated_at TIMESTAMP DEFAULT NOW()
);
