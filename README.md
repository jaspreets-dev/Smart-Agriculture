# Smart Agriculture

A lightweight Flask and MySQL web application for managing farmer registrations and live queues.

## 🚀 Quick Setup Guide

1. **Clone the repo** & open your terminal inside the project folder.
2. **Make sure MySQL Server is running** on your computer.
3. **Install dependencies:**
   ```bash
   pip install Flask mysql-connector-python python-dotenv
4. **Create a `.env` file** in the root folder and add your local MySQL credentials:
   ```env
   DB_HOST=127.0.0.1
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=smart_agri
5. **The run the app using `python app.py`**