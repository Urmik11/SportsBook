# 🏆 SportsBook: Full-Stack Django Cricket Betting Portal

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-brightgreen)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

**SportsBook** is a **full-featured online cricket betting platform** built with **Django**, allowing users to **place bets**, **manage deposits and withdrawals**, and **track live match scores**. The project includes **secure authentication**, **admin controls**, and **automatic bet settlement**.

## 📌 Features:

- **User Management:**
  - **Secure register/login/logout.**
  - **Session-based authentication.**

- **Account & Wallet:**
  - **Balance management.**
  - **Deposit & withdrawal requests** with **admin approval.**
  - **Real-time balance updates** after bets.

- **Betting System:**
  - **Place bets on live matches.**
  - **Track active and settled bets.**
  - **Automatic payout** after match completion.

- **Match Management:**
  - **Admin manages matches** (upcoming, active, completed).
  - **Live score updates** via **web scraping.**
  - **Team-wise betting statistics.**

- **Admin Panel:**
  - **Approve/reject deposits and withdrawals.**
  - **Settle matches and distribute winnings.**
  - **Complete oversight** of users, accounts, and bets.

- **Security:**
  - **Password hashing** and **custom authentication.**
  - **Middleware** to prevent caching sensitive pages.
  - **Validations** for deposits, withdrawals, and bets.

## 🛠️ Technologies Used:

- **Backend & Frontend:** Django 5.2
- **Database:** SQLite
- **Web Scraping:** BeautifulSoup4
- **Styling:** Bootstrap 5
- **Authentication:** Django sessions with custom user model
- **API:** Django REST Framework (JWT)

