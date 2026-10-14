from .services import RestaurantService


class RestaurantApp:
    """CLI sederhana untuk mengakses layanan restoran."""

    def __init__(self, service: RestaurantService | None = None):
        self.service = service or RestaurantService()

    def run_demo(self):
        customer = self.service.create_customer("Rina", "08123456789", "rina@example.com")
        self.service.create_table(1, 4)
        self.service.create_table(2, 2)

        table = self.service.get_all_tables()[0]
        self.service.reserve_table(table["table_number"], customer["id"])
        order = self.service.create_order(customer["id"], table["id"])
        self.service.add_item_to_order(order["id"], "Nasi Goreng", 2, 25000)
        self.service.add_item_to_order(order["id"], "Es Teh", 2, 5000)
        self.service.complete_order(order["id"])

        return {
            "customer": customer,
            "table": table,
            "order": order,
            "daily_report": self.service.get_daily_sales_report(),
            "customer_history": self.service.get_customer_order_history(customer["id"]),
        }
