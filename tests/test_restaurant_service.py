import os
import tempfile
import unittest

from restaurant_app.database import RestaurantDatabase
from restaurant_app.services import RestaurantService


class RestaurantServiceTest(unittest.TestCase):
    def setUp(self):
        fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.database = RestaurantDatabase(db_path=temp_path)
        self.service = RestaurantService(database=self.database)

    def test_create_customer(self):
        customer = self.service.create_customer("Andi", "08111111111", "andi@example.com")
        self.assertIsNotNone(customer["id"])
        self.assertEqual(customer["name"], "Andi")

    def test_create_table_and_reserve(self):
        self.service.create_table(5, 6)
        customer = self.service.create_customer("Budi", "08222222222", "budi@example.com")
        table = self.service.get_all_tables()[0]
        reservation = self.service.reserve_table(table["table_number"], customer["id"])
        self.assertEqual(reservation["status"], "reserved")

    def test_order_flow(self):
        customer = self.service.create_customer("Cici", "08333333333", "cici@example.com")
        self.service.create_table(10, 4)
        table = self.service.get_all_tables()[0]
        self.service.reserve_table(table["table_number"], customer["id"])

        order = self.service.create_order(customer["id"], table["id"])
        self.service.add_item_to_order(order["id"], "Ayam Bakar", 2, 35000)
        self.service.add_item_to_order(order["id"], "Es Jeruk", 2, 6000)

        completed = self.service.complete_order(order["id"])
        self.assertEqual(completed["status"], "completed")
        self.assertAlmostEqual(completed["total_amount"], 82000.0)

        history = self.service.get_customer_order_history(customer["id"])
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["status"], "completed")

    def test_daily_sales_report(self):
        customer = self.service.create_customer("Dina", "08444444444", "dina@example.com")
        self.service.create_table(7, 2)
        table = self.service.get_all_tables()[0]
        self.service.reserve_table(table["table_number"], customer["id"])

        order = self.service.create_order(customer["id"], table["id"])
        self.service.add_item_to_order(order["id"], "Sate", 3, 18000)
        self.service.complete_order(order["id"])

        report = self.service.get_daily_sales_report()
        self.assertEqual(report["order_count"], 1)
        self.assertAlmostEqual(report["total_sales"], 54000.0)


if __name__ == "__main__":
    unittest.main()
