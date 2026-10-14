from datetime import datetime

from .database import RestaurantDatabase


class RestaurantService:
    """Mengelola logika bisnis restoran dengan pendekatan OOP dan terstruktur."""

    def __init__(self, database: RestaurantDatabase | None = None):
        self.database = database or RestaurantDatabase()
        self.database.initialize()

    def create_customer(self, name: str, phone: str, email: str):
        if not name or not email:
            raise ValueError("Nama dan email pelanggan harus diisi.")

        query = "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)"
        customer_id = self.database.execute_query(query, (name, phone, email))
        return {"id": customer_id, "name": name, "phone": phone, "email": email}

    def update_customer(self, customer_id: int, name: str, phone: str, email: str):
        if not name or not email:
            raise ValueError("Nama dan email pelanggan harus diisi.")
        query = "UPDATE customers SET name = ?, phone = ?, email = ? WHERE id = ?"
        self.database.execute_query(query, (name, phone, email, customer_id))
        return {"id": customer_id, "name": name, "phone": phone, "email": email}

    def delete_customer(self, customer_id: int):
        self.database.execute_query("DELETE FROM customers WHERE id = ?", (customer_id,))

    def get_customer_by_email(self, email: str):
        row = self.database.fetch_one(
            "SELECT * FROM customers WHERE email = ?",
            (email,),
        )
        if row is None:
            return None
        return dict(row)

    def create_table(self, table_number: int, capacity: int, status: str = "available"):
        if capacity <= 0:
            raise ValueError("Kapasitas meja harus lebih dari 0.")

        query = "INSERT INTO tables (table_number, capacity, status) VALUES (?, ?, ?)"
        table_id = self.database.execute_query(query, (table_number, capacity, status))
        return {"id": table_id, "table_number": table_number, "capacity": capacity, "status": status}

    def update_table(self, table_id: int, table_number: int, capacity: int, status: str):
        if capacity <= 0:
            raise ValueError("Kapasitas meja harus lebih dari 0.")
        self.database.execute_query(
            "UPDATE tables SET table_number = ?, capacity = ?, status = ? WHERE id = ?",
            (table_number, capacity, status, table_id),
        )
        return {"id": table_id, "table_number": table_number, "capacity": capacity, "status": status}

    def delete_table(self, table_id: int):
        self.database.execute_query("DELETE FROM tables WHERE id = ?", (table_id,))

    def create_menu_item(self, name: str, category: str, price: float, status: str = "available"):
        if not name:
            raise ValueError("Nama menu harus diisi.")
        query = "INSERT INTO menu_items (name, category, price, status) VALUES (?, ?, ?, ?)"
        item_id = self.database.execute_query(query, (name, category, price, status))
        return {"id": item_id, "name": name, "category": category, "price": float(price), "status": status}

    def update_menu_item(self, item_id: int, name: str, category: str, price: float, status: str):
        if not name:
            raise ValueError("Nama menu harus diisi.")
        self.database.execute_query(
            "UPDATE menu_items SET name = ?, category = ?, price = ?, status = ? WHERE id = ?",
            (name, category, price, status, item_id),
        )
        return {"id": item_id, "name": name, "category": category, "price": float(price), "status": status}

    def delete_menu_item(self, item_id: int):
        self.database.execute_query("DELETE FROM menu_items WHERE id = ?", (item_id,))

    def reserve_table(self, table_number: int, customer_id: int):
        table = self.database.fetch_one(
            "SELECT * FROM tables WHERE table_number = ?",
            (table_number,),
        )
        if table is None:
            raise ValueError("Meja tidak ditemukan.")
        if table["status"] != "available":
            raise ValueError("Meja tersebut sudah tidak tersedia.")

        self.database.execute_query(
            "UPDATE tables SET status = 'reserved' WHERE id = ?",
            (table["id"],),
        )
        return {"table_id": table["id"], "customer_id": customer_id, "status": "reserved"}

    def create_reservation(self, customer_id: int, table_id: int, reservation_date: str, reservation_time: str, guest_count: int, status: str = "pending"):
        if guest_count <= 0:
            raise ValueError("Jumlah tamu harus lebih dari 0.")
        query = "INSERT INTO reservations (customer_id, table_id, reservation_date, reservation_time, guest_count, status) VALUES (?, ?, ?, ?, ?, ?)"
        reservation_id = self.database.execute_query(query, (customer_id, table_id, reservation_date, reservation_time, guest_count, status))
        return {"id": reservation_id, "customer_id": customer_id, "table_id": table_id, "reservation_date": reservation_date, "reservation_time": reservation_time, "guest_count": guest_count, "status": status}

    def update_reservation(self, reservation_id: int, customer_id: int, table_id: int, reservation_date: str, reservation_time: str, guest_count: int, status: str):
        if guest_count <= 0:
            raise ValueError("Jumlah tamu harus lebih dari 0.")
        self.database.execute_query(
            "UPDATE reservations SET customer_id = ?, table_id = ?, reservation_date = ?, reservation_time = ?, guest_count = ?, status = ? WHERE id = ?",
            (customer_id, table_id, reservation_date, reservation_time, guest_count, status, reservation_id),
        )
        return {"id": reservation_id, "customer_id": customer_id, "table_id": table_id, "reservation_date": reservation_date, "reservation_time": reservation_time, "guest_count": guest_count, "status": status}

    def delete_reservation(self, reservation_id: int):
        self.database.execute_query("DELETE FROM reservations WHERE id = ?", (reservation_id,))

    def create_order(self, customer_id: int, table_id: int):
        customer = self.database.fetch_one("SELECT * FROM customers WHERE id = ?", (customer_id,))
        table = self.database.fetch_one("SELECT * FROM tables WHERE id = ?", (table_id,))

        if customer is None:
            raise ValueError("Pelanggan tidak ditemukan.")
        if table is None:
            raise ValueError("Meja tidak ditemukan.")

        order_id = self.database.execute_query(
            "INSERT INTO orders (customer_id, table_id, total_amount, status) VALUES (?, ?, 0, 'open')",
            (customer_id, table_id),
        )
        return {"id": order_id, "customer_id": customer_id, "table_id": table_id, "status": "open", "total_amount": 0.0}

    def add_item_to_order(self, order_id: int, menu_name: str, quantity: int, unit_price: float):
        if quantity <= 0:
            raise ValueError("Jumlah item harus lebih dari 0.")

        self.database.execute_query(
            "INSERT INTO order_items (order_id, menu_name, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (order_id, menu_name, quantity, unit_price),
        )

        items = self.database.fetch_all("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        total = sum(item["quantity"] * float(item["unit_price"]) for item in items)
        self.database.execute_query(
            "UPDATE orders SET total_amount = ? WHERE id = ?",
            (total, order_id),
        )
        return {"order_id": order_id, "menu_name": menu_name, "quantity": quantity, "unit_price": unit_price, "total_amount": total}

    def complete_order(self, order_id: int):
        order = self.database.fetch_one("SELECT * FROM orders WHERE id = ?", (order_id,))
        if order is None:
            raise ValueError("Pesanan tidak ditemukan.")

        self.database.execute_query(
            "UPDATE orders SET status = 'completed' WHERE id = ?",
            (order_id,),
        )
        self.database.execute_query(
            "UPDATE tables SET status = 'available' WHERE id = ?",
            (order["table_id"],),
        )
        return {"id": order_id, "status": "completed", "total_amount": float(order["total_amount"])}

    def get_customer_order_history(self, customer_id: int):
        orders = self.database.fetch_all(
            "SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC",
            (customer_id,),
        )
        result = []
        for order in orders:
            items = self.database.fetch_all(
                "SELECT * FROM order_items WHERE order_id = ?",
                (order["id"],),
            )
            result.append({
                "id": order["id"],
                "table_id": order["table_id"],
                "created_at": order["created_at"],
                "total_amount": float(order["total_amount"]),
                "status": order["status"],
                "items": [dict(item) for item in items],
            })
        return result

    def get_daily_sales_report(self, day: str | None = None):
        if day is None:
            day = datetime.now().strftime("%Y-%m-%d")

        # Use localtime conversion because SQLite CURRENT_TIMESTAMP may be stored in UTC.
        rows = self.database.fetch_all(
            "SELECT * FROM orders WHERE date(created_at, 'localtime') = ? AND status = 'completed'",
            (day,),
        )
        total_sales = sum(float(row["total_amount"]) for row in rows)
        return {
            "date": day,
            "total_sales": total_sales,
            "order_count": len(rows),
            "orders": [dict(row) for row in rows],
        }

    def get_table_status_summary(self):
        rows = self.database.fetch_all(
            "SELECT table_number, capacity, status FROM tables ORDER BY table_number"
        )
        return [dict(row) for row in rows]

    def get_all_customers(self):
        rows = self.database.fetch_all("SELECT * FROM customers ORDER BY id")
        return [dict(row) for row in rows]

    def get_all_tables(self):
        rows = self.database.fetch_all("SELECT * FROM tables ORDER BY table_number")
        return [dict(row) for row in rows]

    def get_all_menu_items(self):
        rows = self.database.fetch_all("SELECT * FROM menu_items ORDER BY id")
        return [dict(row) for row in rows]

    def get_all_reservations(self):
        query = """
            SELECT r.id, c.name AS customer_name, t.table_number, r.reservation_date, r.reservation_time,
                   r.guest_count, r.status
            FROM reservations r
            JOIN customers c ON c.id = r.customer_id
            JOIN tables t ON t.id = r.table_id
            ORDER BY r.id
        """
        rows = self.database.fetch_all(query)
        return [dict(row) for row in rows]

    def get_all_orders(self):
        query = """
            SELECT o.id, c.name AS customer_name, o.created_at AS created_at, o.total_amount, o.status, t.table_number
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            JOIN tables t ON t.id = o.table_id
            ORDER BY o.id
        """
        rows = self.database.fetch_all(query)
        return [dict(row) for row in rows]
