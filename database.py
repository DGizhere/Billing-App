import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",  # Replace with your MySQL password
            database="billing_app"
        )
        self.cursor = self.db.cursor()

    def insert_customer(self, name, phone, email, address):
        query = """
        INSERT INTO customers (name, phone, email, address)
        VALUES (%s, %s, %s, %s)
        """
        values = (name, phone, email, address)
        self.cursor.execute(query, values)
        self.db.commit()
        return self.cursor.lastrowid  # Return the last inserted customer ID

    def insert_bill(self, customer_id, item_name, quantity, price, total):
        query = """
        INSERT INTO bills (customer_id, item_name, quantity, price, total)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (customer_id, item_name, quantity, price, total)
        self.cursor.execute(query, values)
        self.db.commit()

    def retrieve_bills(self):
        query = """
        SELECT b.bill_id, c.name, b.item_name, b.quantity, b.total
        FROM bills b
        JOIN customers c ON b.customer_id = c.customer_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Return all bills with customer details

    def close_connection(self):
        self.cursor.close()
        self.db.close()