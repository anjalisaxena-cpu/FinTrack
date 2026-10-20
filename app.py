from pathlib import Path
import sqlite3

from flask import Flask, jsonify, redirect, render_template, session, url_for

from config import Config
from models.database import close_db, get_db
from market_data import get_all_stocks, get_market_overview, get_stock
from routes.auth import auth
from routes.chatbot import chatbot
from routes.expenses import expenses
from routes.goals import goals
from routes.learning import learning
from routes.notifications import notifications
from routes.portfolio import portfolio
from routes.profile import profile
from routes.reports import reports
from routes.risk import risk
from routes.trading import trading
from routes.upstox import upstox
from routes.watchlist import watchlist


app = Flask(__name__)
app.config.from_object(Config)


def create_database():
    database_path = Path(app.config["DATABASE"])
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    schema_path = Path(app.root_path) / "schema.sql"
    connection.executescript(schema_path.read_text(encoding="utf-8"))
    connection.commit()
    connection.close()


create_database()
app.teardown_appcontext(close_db)
app.register_blueprint(auth)
app.register_blueprint(portfolio)
app.register_blueprint(watchlist)
app.register_blueprint(profile)
app.register_blueprint(expenses)
app.register_blueprint(goals)
app.register_blueprint(risk)
app.register_blueprint(chatbot)
app.register_blueprint(learning)
app.register_blueprint(reports)
app.register_blueprint(notifications)
app.register_blueprint(trading)
app.register_blueprint(upstox)


@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    db = get_db()
    portfolio_rows = db.execute(
        "SELECT symbol, quantity, buy_price FROM portfolio WHERE user_id = ?",
        (session["user_id"],),
    ).fetchall()
    total_invested = sum(row["quantity"] * row["buy_price"] for row in portfolio_rows)
    total_current = sum(row["quantity"] * (get_stock(row["symbol"])["price"] if get_stock(row["symbol"]) else row["buy_price"]) for row in portfolio_rows)
    profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (session["user_id"],)).fetchone()
    entries = db.execute("SELECT entry_type, amount FROM expenses WHERE user_id = ?", (session["user_id"],)).fetchall()
    goals = db.execute("SELECT target_amount, current_saved FROM goals WHERE user_id = ?", (session["user_id"],)).fetchall()
    income = (profile["monthly_income"] if profile else 0) or sum(row["amount"] for row in entries if row["entry_type"] == "income")
    expenses = (profile["monthly_expenses"] if profile else 0) or sum(row["amount"] for row in entries if row["entry_type"] == "expense")
    savings = max(income - expenses, 0)
    savings_rate = (savings / income * 100) if income else 0
    holding_count = len({row["symbol"] for row in portfolio_rows})
    concentration = max((row["quantity"] * row["buy_price"] for row in portfolio_rows), default=0)
    concentration_rate = concentration / total_invested * 100 if total_invested else 0
    debt = (profile["loans_emis"] if profile else 0) or 0
    debt_ratio = debt / income * 100 if income else 0
    goal_progress = sum((row["current_saved"] / row["target_amount"] * 100) for row in goals if row["target_amount"]) / len(goals) if goals else 0
    emergency_months = savings / expenses if expenses else 0
    health_score = round(min(100, min(savings_rate, 30) + min(holding_count * 8, 20) + min(emergency_months * 5, 20) + max(15 - debt_ratio / 4, 0) + min(goal_progress / 5, 15)))
    health_level = "Strong" if health_score >= 75 else "Growing" if health_score >= 50 else "Needs attention"
    alerts = []
    if savings_rate < 20:
        alerts.append("Your savings rate is below 20% of income.")
    if concentration_rate > 60:
        alerts.append("Your portfolio is highly concentrated in one holding.")
    if goals and any(row["current_saved"] < row["target_amount"] * 0.25 for row in goals):
        alerts.append("One of your goals is still in its early progress stage.")
    if not alerts:
        alerts.append("No urgent alerts. Keep reviewing your plan each month.")
    return render_template("dashboard.html", total_invested=total_invested,
                           total_current=total_current, total_profit_loss=total_current - total_invested,
                           savings=savings, savings_rate=savings_rate, health_score=health_score,
                           health_level=health_level, alerts=alerts)


@app.route("/api/market")
def market_api():
    return jsonify(get_market_overview())


@app.route("/market")
def market():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    market_data = list(get_all_stocks().values())
    return render_template("market.html", market=market_data, market_overview=get_market_overview())


@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("settings.html")


@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("notifications.html")


if __name__ == "__main__":
    app.run(debug=True)
