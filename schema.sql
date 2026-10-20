CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    security_question TEXT,
    security_answer_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    company_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    buy_price REAL NOT NULL CHECK (buy_price > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    stock_symbol TEXT NOT NULL,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, stock_symbol),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    education TEXT,
    occupation TEXT,
    monthly_income REAL DEFAULT 0,
    monthly_savings REAL DEFAULT 0,
    monthly_expenses REAL DEFAULT 0,
    loans_emis REAL DEFAULT 0,
    financial_information TEXT,
    health_insurance TEXT,
    life_insurance TEXT,
    insurance_coverage REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    entry_type TEXT NOT NULL CHECK (entry_type IN ('income', 'expense')),
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    entry_date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    target_amount REAL NOT NULL CHECK (target_amount > 0),
    current_saved REAL DEFAULT 0,
    target_date TEXT NOT NULL,
    monthly_contribution REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    otp_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    used INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_settings (
    user_id INTEGER PRIMARY KEY,
    theme TEXT NOT NULL DEFAULT 'dark',
    compact_view INTEGER NOT NULL DEFAULT 0,
    animations_enabled INTEGER NOT NULL DEFAULT 1,
    goal_reminders INTEGER NOT NULL DEFAULT 1,
    portfolio_alerts INTEGER NOT NULL DEFAULT 1,
    savings_alerts INTEGER NOT NULL DEFAULT 1,
    expense_alerts INTEGER NOT NULL DEFAULT 1,
    risk_alerts INTEGER NOT NULL DEFAULT 1,
    ai_recommendations INTEGER NOT NULL DEFAULT 1,
    learning_reminders INTEGER NOT NULL DEFAULT 1,
    monthly_savings_target REAL NOT NULL DEFAULT 0,
    emergency_fund_months INTEGER NOT NULL DEFAULT 6,
    expected_return REAL NOT NULL DEFAULT 8,
    investment_horizon TEXT NOT NULL DEFAULT '3-7 years',
    ai_response_style TEXT NOT NULL DEFAULT 'Simple',
    learning_level TEXT NOT NULL DEFAULT 'Beginner',
    report_period TEXT NOT NULL DEFAULT 'Monthly',
    currency TEXT NOT NULL DEFAULT 'INR',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chatbot_messages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fitness_progress (
    user_id INTEGER PRIMARY KEY,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    active_challenge TEXT,
    challenge_progress REAL NOT NULL DEFAULT 0,
    completed_challenges INTEGER NOT NULL DEFAULT 0,
    badges_json TEXT NOT NULL DEFAULT '[]',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_accounts (
    user_id INTEGER PRIMARY KEY,
    virtual_balance REAL NOT NULL DEFAULT 1000000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_holdings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    avg_buy_price REAL NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, symbol),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_trade_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    trade_type TEXT NOT NULL CHECK (trade_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    total_amount REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS timed_trades (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    trade_type TEXT NOT NULL CHECK (trade_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    entry_price REAL NOT NULL,
    duration_minutes INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'closed', 'expired')),
    pnl REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
