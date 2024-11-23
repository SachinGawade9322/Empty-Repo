# src/models/service.py

from utils.connection import get_db_connection  # Adjust this based on your project structure

class Service:
    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

    @staticmethod
    def create_service(title, description, price):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO services (title, description, price)
            VALUES (%s, %s, %s) RETURNING id
        """, (title, description, price))
        service_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return service_id

    @staticmethod
    def get_all_services():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM services")
        services = cur.fetchall()
        cur.close()
        conn.close()
        return services