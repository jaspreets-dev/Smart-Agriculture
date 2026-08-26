import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
import mysql.connector

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Automatic Database and Table Setup
def initialize_database():
    # Connect without database first to create it if it doesn't exist
    temp_db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    temp_cursor = temp_db.cursor()
    temp_cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"
    )
    temp_cursor.close()
    temp_db.close()

    # Now connect to the smart_agri database and create the table
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            crop VARCHAR(50) NOT NULL,
            quantityKg INT NOT NULL,
            slotTime VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT 'Registered',
            paymentStatus VARCHAR(50) DEFAULT 'Pending'
        )
    """)
    cursor.close()
    db.close()


# Database connection helper for routes
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/")
def index():
    return render_template("index.html")


# API to get all farmers (Live Queue)
@app.route("/api/queue", methods=["GET"])
def get_queue():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM farmers")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"success": True, "queue": rows})


# API to register a farmer and book a slot
@app.route("/api/register", methods=["POST"])
def register_farmer():
    data = request.json
    name = data.get("name")
    crop = data.get("crop")
    quantity = data.get("quantityKg")
    slot = data.get("slotTime")

    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO farmers (name, crop, quantityKg, slotTime, status, paymentStatus) VALUES (%s, %s, %s, %s, 'Registered', 'Pending')"
    cursor.execute(query, (name, crop, quantity, slot))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True, "message": "Slot booked successfully!"})


if __name__ == "__main__":
    # Run setup before starting the web server
    initialize_database()
    print("Database and tables checked/created successfully!")
    app.run(debug=True, port=5000)