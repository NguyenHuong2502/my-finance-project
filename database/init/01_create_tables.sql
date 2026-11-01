-- ==========================================
-- 1. USERS
-- ==========================================

CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 2. WALLETS
-- ==========================================

CREATE TABLE wallets (
    wallet_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    wallet_name VARCHAR(100) NOT NULL,
    initial_balance NUMERIC(15,2) NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_wallets_users
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT chk_wallets_balance
        CHECK (initial_balance >= 0),

    CONSTRAINT uq_wallets_user_name
        UNIQUE (user_id, wallet_name)
);


-- ==========================================
-- 3. CATEGORIES
-- ==========================================

CREATE TABLE categories (
    category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT,
    category_name VARCHAR(100) NOT NULL,
    category_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_categories_users
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT chk_categories_type
        CHECK (category_type IN ('INCOME', 'EXPENSE')),

    CONSTRAINT uq_categories_user_name_type
        UNIQUE (user_id, category_name, category_type)
);


-- ==========================================
-- 4. TRANSACTIONS
-- ==========================================

CREATE TABLE transactions (
    transaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wallet_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    amount NUMERIC(15,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_wallets
        FOREIGN KEY (wallet_id)
        REFERENCES wallets(wallet_id),

    CONSTRAINT fk_transactions_categories
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),

    CONSTRAINT chk_transactions_amount
        CHECK (amount > 0),

    CONSTRAINT chk_transactions_type
        CHECK (transaction_type IN ('INCOME', 'EXPENSE'))
);


-- ==========================================
-- 5. BUDGETS
-- ==========================================

CREATE TABLE budgets (
    budget_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    budget_name VARCHAR(100) NOT NULL,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_budgets_users
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT chk_budgets_month
        CHECK (month BETWEEN 1 AND 12),

    CONSTRAINT chk_budgets_year
        CHECK (year BETWEEN 2000 AND 9999),

    CONSTRAINT uq_budgets_user_month_year
        UNIQUE (user_id, month, year)
);


-- ==========================================
-- 6. BUDGET CATEGORIES
-- ==========================================

CREATE TABLE budget_categories (
    budget_category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    budget_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    limit_amount NUMERIC(15,2) NOT NULL,

    CONSTRAINT fk_budget_categories_budgets
        FOREIGN KEY (budget_id)
        REFERENCES budgets(budget_id),

    CONSTRAINT fk_budget_categories_categories
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),

    CONSTRAINT chk_budget_categories_limit
        CHECK (limit_amount >= 0),

    CONSTRAINT uq_budget_categories
        UNIQUE (budget_id, category_id)
);