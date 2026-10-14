import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from restaurant_app.services import RestaurantService


class RestaurantDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restoran")
        self.root.geometry("1360x760")
        self.root.minsize(1180, 680)
        self.root.configure(bg="#f5efe8")

        self.service = RestaurantService()
        self.selected_customer_id = None
        self.selected_table_id = None
        self.selected_menu_id = None
        self.selected_reservation_id = None
        self.customer_id_map = {}
        self.table_id_map = {}
        self.menu_id_map = {}

        self.pages = {}
        self.nav_buttons = {}

        self.build_shell()
        self.build_dashboard_page()
        self.build_customers_page()
        self.build_tables_page()
        self.build_menu_page()
        self.build_reservations_page()
        self.build_orders_page()
        self.build_reports_page()

        self.show_page("dashboard")
        self.refresh_all_data()

    def build_shell(self):
        sidebar = tk.Frame(self.root, bg="#1f2937", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Restoran",
            bg="#1f2937",
            fg="#ffffff",
            font=("Segoe UI", 28, "bold"),
        ).place(x=28, y=28)

        tk.Label(
            sidebar,
            text="Management System",
            bg="#1f2937",
            fg="#cbd5e1",
            font=("Segoe UI", 10),
        ).place(x=30, y=72)

        nav_container = tk.Frame(sidebar, bg="#1f2937")
        nav_container.place(x=18, y=120, width=185)

        nav_items = [
            ("Dashboard", "dashboard"),
            ("Pelanggan", "customers"),
            ("Meja", "tables"),
            ("Menu", "menu"),
            ("Reservasi", "reservations"),
            ("Pesanan", "orders"),
            ("Laporan", "reports"),
        ]

        for idx, (text, key) in enumerate(nav_items):
            btn = tk.Button(
                nav_container,
                text=text,
                bg="#1f2937",
                fg="#f8fafc",
                font=("Segoe UI", 11, "bold"),
                bd=0,
                cursor="hand2",
                padx=12,
                pady=12,
                width=16,
                anchor="w",
                command=lambda k=key: self.show_page(k),
            )
            btn.grid(row=idx, column=0, sticky="ew", pady=4)
            self.nav_buttons[key] = btn

        self.main = tk.Frame(self.root, bg="#f5efe8")
        self.main.pack(side="left", fill="both", expand=True)

    def show_page(self, key):
        for page_key, page in self.pages.items():
            if page_key == key:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()

        for nav_key, button in self.nav_buttons.items():
            if nav_key == key:
                button.configure(bg="#d97706", fg="#ffffff")
            else:
                button.configure(bg="#1f2937", fg="#f8fafc")

    def build_dashboard_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["dashboard"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 20))

        tk.Label(
            header,
            text="Dashboard",
            bg="#f5efe8",
            fg="#111827",
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Ringkasan operasional restoran",
            bg="#f5efe8",
            fg="#6b7280",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        cards = tk.Frame(frame, bg="#f5efe8")
        cards.pack(fill="x", padx=28)

        self.dashboard_cards = {}
        cards_data = [
            ("Pesanan Hari Ini", "0", "#dbeafe", "#2563eb"),
            ("Meja Tersedia", "0", "#dcfce7", "#16a34a"),
            ("Reservasi Aktif", "0", "#fef3c7", "#d97706"),
            ("Pendapatan", "Rp 0", "#f3e8ff", "#7c3aed"),
        ]

        for index, (title, value, bg, fg) in enumerate(cards_data):
            card = tk.Frame(cards, bg=bg, padx=20, pady=20)
            card.pack(side="left", fill="y", expand=True, padx=(0, 16))
            tk.Label(card, text=title, bg=bg, fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            label = tk.Label(card, text=value, bg=bg, fg="#111827", font=("Segoe UI", 26, "bold"))
            label.pack(anchor="w", pady=(8, 0))
            tk.Label(card, text="Update terbaru", bg=bg, fg=fg, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            self.dashboard_cards[index] = label

        content = tk.Frame(frame, bg="#f5efe8")
        content.pack(fill="both", expand=True, padx=28, pady=26)

        left = tk.Frame(content, bg="#ffffff", padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True, padx=(0, 16))

        tk.Label(left, text="Reservasi Terbaru", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w")

        cols = ("Pelanggan", "Meja", "Tanggal", "Waktu", "Status")
        self.dashboard_reservations_tree = ttk.Treeview(left, columns=cols, show="headings", height=12)
        for col in cols:
            self.dashboard_reservations_tree.heading(col, text=col)
            self.dashboard_reservations_tree.column(col, anchor="center", width=130)
        self.dashboard_reservations_tree.pack(fill="both", expand=True, pady=(14, 0))

        right = tk.Frame(content, bg="#ffffff", padx=20, pady=20)
        right.pack(side="right", fill="y")

        tk.Label(right, text="Status Kitchen", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w")

        self.kitchen_status_labels = []
        statuses = [
            ("Sedang Disiapkan", "0", "#fbbf24"),
            ("Siap Diantar", "0", "#16a34a"),
            ("Butuh Review", "0", "#ef4444"),
        ]
        for label_text, value, color in statuses:
            row = tk.Frame(right, bg="#ffffff")
            row.pack(fill="x", pady=12)
            tk.Label(row, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", side="left")
            value_label = tk.Label(row, text=value, bg="#ffffff", fg=color, font=("Segoe UI", 11, "bold"))
            value_label.pack(anchor="e", side="right")
            self.kitchen_status_labels.append(value_label)

    def build_customers_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["customers"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 20))

        tk.Label(header, text="Pelanggan", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        form_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        form_container.pack(side="left", fill="y", padx=28)

        tk.Label(form_container, text="Data Pelanggan", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        self.customer_entries = {}
        for label_text, key in [("Nama", "name"), ("Telepon", "phone"), ("Email", "email")]:
            tk.Label(form_container, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
            entry = tk.Entry(form_container, width=32, font=("Segoe UI", 10), bg="#f9fafb")
            entry.pack(fill="x", pady=(0, 8))
            self.customer_entries[key] = entry

        button_row = tk.Frame(form_container, bg="#ffffff")
        button_row.pack(fill="x", pady=(12, 0))

        tk.Button(button_row, text="Tambah Pelanggan", bg="#16a34a", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.add_customer).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Edit", bg="#f59e0b", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.edit_customer_selected).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Hapus", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.delete_customer_selected).pack(side="left")

        table_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 28))

        tk.Label(table_container, text="Daftar Pelanggan", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        columns = ("id", "No", "Nama", "Telepon", "Email")
        self.customer_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=16)
        self.customer_tree.heading("id", text="ID")
        self.customer_tree.column("id", width=0, stretch=False)
        for col in ("No", "Nama", "Telepon", "Email"):
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, anchor="center")
        self.customer_tree.column("No", width=60)
        self.customer_tree.column("Nama", width=180)
        self.customer_tree.column("Telepon", width=140)
        self.customer_tree.column("Email", width=210)
        self.customer_tree.pack(fill="both", expand=True)

        self.customer_tree.bind("<<TreeviewSelect>>", self.customer_selected)

    def build_tables_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["tables"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 18))
        tk.Label(header, text="Meja", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        form_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        form_container.pack(side="left", fill="y", padx=28)

        tk.Label(form_container, text="Data Meja", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        self.table_entries = {}
        for key, label_text in [("table_number", "Nomor Meja"), ("capacity", "Kapasitas"), ("status", "Status")]:
            tk.Label(form_container, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
            entry = tk.Entry(form_container, width=32, font=("Segoe UI", 10), bg="#f9fafb")
            entry.pack(fill="x", pady=(0, 8))
            self.table_entries[key] = entry

        button_row = tk.Frame(form_container, bg="#ffffff")
        button_row.pack(fill="x", pady=(12, 0))
        tk.Button(button_row, text="Tambah Meja", bg="#2563eb", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.add_table).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Edit", bg="#f59e0b", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.edit_table_selected).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Hapus", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.delete_table_selected).pack(side="left")

        table_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 28))

        tk.Label(table_container, text="Daftar Meja", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        columns = ("id", "No", "Nomor Meja", "Kapasitas", "Status")
        self.table_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        self.table_tree.heading("id", text="ID")
        self.table_tree.column("id", width=0, stretch=False)
        for col in ("No", "Nomor Meja", "Kapasitas", "Status"):
            self.table_tree.heading(col, text=col)
            self.table_tree.column(col, anchor="center")
        self.table_tree.column("No", width=60)
        self.table_tree.column("Nomor Meja", width=170)
        self.table_tree.column("Kapasitas", width=120)
        self.table_tree.column("Status", width=150)
        self.table_tree.pack(fill="both", expand=True)

        self.table_tree.bind("<<TreeviewSelect>>", self.table_selected)

    def build_menu_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["menu"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 18))
        tk.Label(header, text="Menu", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        form_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        form_container.pack(side="left", fill="y", padx=28)

        tk.Label(form_container, text="Data Menu", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        self.menu_entries = {}
        for key, label_text in [("name", "Nama Menu"), ("category", "Kategori"), ("price", "Harga"), ("status", "Status")]:
            tk.Label(form_container, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
            entry = tk.Entry(form_container, width=32, font=("Segoe UI", 10), bg="#f9fafb")
            entry.pack(fill="x", pady=(0, 8))
            self.menu_entries[key] = entry

        button_row = tk.Frame(form_container, bg="#ffffff")
        button_row.pack(fill="x", pady=(12, 0))
        tk.Button(button_row, text="Tambah Menu", bg="#d97706", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.add_menu).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Edit", bg="#f59e0b", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.edit_menu_selected).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Hapus", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.delete_menu_selected).pack(side="left")

        table_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 28))

        tk.Label(table_container, text="Daftar Menu", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        columns = ("id", "No", "Nama Menu", "Harga", "Status")
        self.menu_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        self.menu_tree.heading("id", text="ID")
        self.menu_tree.column("id", width=0, stretch=False)
        for col in ("No", "Nama Menu", "Harga", "Status"):
            self.menu_tree.heading(col, text=col)
            self.menu_tree.column(col, anchor="center")
        self.menu_tree.column("No", width=60)
        self.menu_tree.column("Nama Menu", width=220)
        self.menu_tree.column("Harga", width=140)
        self.menu_tree.column("Status", width=130)
        self.menu_tree.pack(fill="both", expand=True)

        self.menu_tree.bind("<<TreeviewSelect>>", self.menu_selected)

    def build_reservations_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["reservations"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 18))
        tk.Label(header, text="Reservasi", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        form_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        form_container.pack(side="left", fill="y", padx=28)

        tk.Label(form_container, text="Reservasi Meja", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        self.reservation_entries = {}
        self.customer_combo = ttk.Combobox(form_container, state="readonly", width=30, font=("Segoe UI", 10))
        self.customer_combo.pack(fill="x", pady=(0, 8))
        tk.Label(form_container, text="Pelanggan", bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        self.customer_combo.pack(fill="x")

        self.table_combo = ttk.Combobox(form_container, state="readonly", width=30, font=("Segoe UI", 10))
        self.table_combo.pack(fill="x", pady=(0, 8))
        tk.Label(form_container, text="Meja", bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        self.table_combo.pack(fill="x")

        for key, label_text in [("reservation_date", "Tanggal"), ("reservation_time", "Waktu"), ("guest_count", "Tamu"), ("status", "Status")]:
            tk.Label(form_container, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
            entry = tk.Entry(form_container, width=32, font=("Segoe UI", 10), bg="#f9fafb")
            entry.pack(fill="x", pady=(0, 8))
            self.reservation_entries[key] = entry

        button_row = tk.Frame(form_container, bg="#ffffff")
        button_row.pack(fill="x", pady=(12, 0))
        tk.Button(button_row, text="Buat Reservasi", bg="#7c3aed", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.add_reservation).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Edit", bg="#f59e0b", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.edit_reservation_selected).pack(side="left", padx=(0, 8))
        tk.Button(button_row, text="Hapus", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.delete_reservation_selected).pack(side="left")

        table_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 28))

        tk.Label(table_container, text="Daftar Reservasi", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        columns = ("id", "No", "Pelanggan", "Meja", "Tanggal", "Waktu", "Tamu", "Status")
        self.reservation_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        self.reservation_tree.heading("id", text="ID")
        self.reservation_tree.column("id", width=0, stretch=False)
        for col in ("No", "Pelanggan", "Meja", "Tanggal", "Waktu", "Tamu", "Status"):
            self.reservation_tree.heading(col, text=col)
            self.reservation_tree.column(col, anchor="center")
        self.reservation_tree.column("No", width=60)
        self.reservation_tree.column("Pelanggan", width=160)
        self.reservation_tree.column("Meja", width=100)
        self.reservation_tree.column("Tanggal", width=120)
        self.reservation_tree.column("Waktu", width=120)
        self.reservation_tree.column("Tamu", width=100)
        self.reservation_tree.column("Status", width=120)
        self.reservation_tree.pack(fill="both", expand=True)

        self.reservation_tree.bind("<<TreeviewSelect>>", self.reservation_selected)

    def build_orders_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["orders"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 18))
        tk.Label(header, text="Pesanan", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        form_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        form_container.pack(side="left", fill="y", padx=28)

        tk.Label(form_container, text="Buat Pesanan", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        self.order_entries = {}
        self.order_customer_combo = ttk.Combobox(form_container, state="readonly", width=30, font=("Segoe UI", 10))
        self.order_customer_combo.pack(fill="x", pady=(0, 8))
        tk.Label(form_container, text="Pelanggan", bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        self.order_customer_combo.pack(fill="x")

        self.order_table_combo = ttk.Combobox(form_container, state="readonly", width=30, font=("Segoe UI", 10))
        self.order_table_combo.pack(fill="x", pady=(0, 8))
        tk.Label(form_container, text="Meja", bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        self.order_table_combo.pack(fill="x")

        for key, label_text in [("menu_name", "Nama Menu"), ("quantity", "Jumlah"), ("unit_price", "Harga Satuan")]:
            tk.Label(form_container, text=label_text, bg="#ffffff", fg="#374151", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
            entry = tk.Entry(form_container, width=32, font=("Segoe UI", 10), bg="#f9fafb")
            entry.pack(fill="x", pady=(0, 8))
            self.order_entries[key] = entry

        button_row = tk.Frame(form_container, bg="#ffffff")
        button_row.pack(fill="x", pady=(12, 0))
        tk.Button(button_row, text="Buat Pesanan", bg="#16a34a", fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=18, pady=10, command=self.add_order).pack(side="left")

        table_container = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 28))

        tk.Label(table_container, text="Data Pesanan", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 14))

        columns = ("id", "No", "Pelanggan", "Tanggal", "Total", "Status")
        self.order_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        self.order_tree.heading("id", text="ID")
        self.order_tree.column("id", width=0, stretch=False)
        for col in ("No", "Pelanggan", "Tanggal", "Total", "Status"):
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, anchor="center")
        self.order_tree.column("No", width=60)
        self.order_tree.column("Pelanggan", width=180)
        self.order_tree.column("Tanggal", width=140)
        self.order_tree.column("Total", width=140)
        self.order_tree.column("Status", width=120)
        self.order_tree.pack(fill="both", expand=True)

    def build_reports_page(self):
        frame = tk.Frame(self.main, bg="#f5efe8")
        self.pages["reports"] = frame

        header = tk.Frame(frame, bg="#f5efe8")
        header.pack(fill="x", padx=28, pady=(26, 18))

        tk.Label(header, text="Laporan", bg="#f5efe8", fg="#111827", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        action = tk.Frame(frame, bg="#f5efe8")
        action.pack(fill="x", padx=28, pady=(0, 16))
        tk.Button(
            action,
            text="Tampilkan",
            bg="#1f6feb",
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=18,
            pady=10,
            command=self.show_report,
        ).pack(anchor="w")

        report_box = tk.Frame(frame, bg="#ffffff", padx=18, pady=18)
        report_box.pack(fill="both", expand=True, padx=28)

        tk.Label(report_box, text="Laporan Reservasi", bg="#ffffff", fg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 16))

        columns = ("id", "No", "Pelanggan", "Meja", "Tanggal", "Status")
        self.report_tree = ttk.Treeview(report_box, columns=columns, show="headings", height=14)
        self.report_tree.heading("id", text="ID")
        self.report_tree.column("id", width=0, stretch=False)
        for col in ("No", "Pelanggan", "Meja", "Tanggal", "Status"):
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, anchor="center")
        self.report_tree.column("No", width=70)
        self.report_tree.column("Pelanggan", width=190)
        self.report_tree.column("Meja", width=100)
        self.report_tree.column("Tanggal", width=140)
        self.report_tree.column("Status", width=150)
        self.report_tree.pack(fill="both", expand=True)

    def refresh_all_data(self):
        self.load_customers()
        self.load_tables()
        self.load_menu_items()
        self.load_reservations()
        self.load_orders()
        self.load_reports()
        self.load_dashboard_summary()
        self.refresh_dropdowns()

    def refresh_dropdowns(self):
        customers = self.service.get_all_customers()
        self.customer_id_map = {c["name"]: c["id"] for c in customers}
        self.customer_combo["values"] = [c["name"] for c in customers]
        self.order_customer_combo["values"] = [c["name"] for c in customers]

        tables = self.service.get_all_tables()
        self.table_id_map = {f"Meja {t['table_number']}": t["id"] for t in tables}
        self.table_combo["values"] = [f"Meja {t['table_number']} ({t['status']})" for t in tables]
        self.order_table_combo["values"] = [f"Meja {t['table_number']} ({t['status']})" for t in tables]

        menu_items = self.service.get_all_menu_items()
        self.menu_id_map = {m["name"]: m["id"] for m in menu_items}

    def load_customers(self):
        for row in self.customer_tree.get_children():
            self.customer_tree.delete(row)

        customers = self.service.get_all_customers()
        for index, customer in enumerate(customers, start=1):
            self.customer_tree.insert(
                "",
                "end",
                values=(customer["id"], index, customer["name"], customer["phone"], customer["email"]),
            )

    def customer_selected(self, event):
        selected = self.customer_tree.selection()
        if not selected:
            self.selected_customer_id = None
            return
        item = self.customer_tree.item(selected[0], "values")
        self.selected_customer_id = item[0]
        self.customer_entries["name"].delete(0, tk.END)
        self.customer_entries["name"].insert(0, item[2])
        self.customer_entries["phone"].delete(0, tk.END)
        self.customer_entries["phone"].insert(0, item[3])
        self.customer_entries["email"].delete(0, tk.END)
        self.customer_entries["email"].insert(0, item[4])

    def add_customer(self):
        name = self.customer_entries["name"].get().strip()
        phone = self.customer_entries["phone"].get().strip()
        email = self.customer_entries["email"].get().strip()
        if not name or not email:
            messagebox.showwarning("Peringatan", "Nama dan email pelanggan harus diisi.")
            return
        try:
            self.service.create_customer(name, phone, email)
            messagebox.showinfo("Berhasil", "Pelanggan berhasil ditambahkan.")
            self.clear_customer_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def edit_customer_selected(self):
        if not self.selected_customer_id:
            messagebox.showwarning("Peringatan", "Pilih pelanggan terlebih dahulu.")
            return
        name = self.customer_entries["name"].get().strip()
        phone = self.customer_entries["phone"].get().strip()
        email = self.customer_entries["email"].get().strip()
        try:
            self.service.update_customer(self.selected_customer_id, name, phone, email)
            messagebox.showinfo("Berhasil", "Pelanggan berhasil diubah.")
            self.clear_customer_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_customer_selected(self):
        if not self.selected_customer_id:
            messagebox.showwarning("Peringatan", "Pilih pelanggan terlebih dahulu.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus pelanggan ini?"):
            try:
                self.service.delete_customer(self.selected_customer_id)
                messagebox.showinfo("Berhasil", "Pelanggan berhasil dihapus.")
                self.clear_customer_form()
                self.refresh_all_data()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def clear_customer_form(self):
        for entry in self.customer_entries.values():
            entry.delete(0, tk.END)
        self.selected_customer_id = None

    def load_tables(self):
        for row in self.table_tree.get_children():
            self.table_tree.delete(row)

        tables = self.service.get_all_tables()
        for index, table in enumerate(tables, start=1):
            self.table_tree.insert(
                "",
                "end",
                values=(table["id"], index, table["table_number"], table["capacity"], table["status"]),
            )

    def table_selected(self, event):
        selected = self.table_tree.selection()
        if not selected:
            self.selected_table_id = None
            return
        item = self.table_tree.item(selected[0], "values")
        self.selected_table_id = item[0]
        self.table_entries["table_number"].delete(0, tk.END)
        self.table_entries["table_number"].insert(0, item[2])
        self.table_entries["capacity"].delete(0, tk.END)
        self.table_entries["capacity"].insert(0, item[3])
        self.table_entries["status"].delete(0, tk.END)
        self.table_entries["status"].insert(0, item[4])

    def reservation_selected(self, event):
        selected = self.reservation_tree.selection()
        if not selected:
            self.selected_reservation_id = None
            return
        item = self.reservation_tree.item(selected[0], "values")
        # columns: (id, No, Pelanggan, Meja, Tanggal, Waktu, Tamu, Status)
        self.selected_reservation_id = item[0]
        customer_name = item[2]
        table_number = item[3]
        reservation_date = item[4]
        reservation_time = item[5]
        guest_count = item[6]
        status = item[7]

        # set combos and form fields
        try:
            self.customer_combo.set(customer_name)
        except Exception:
            pass

        # find and set matching table combo entry
        for val in self.table_combo["values"]:
            if str(val).startswith(f"Meja {table_number}"):
                try:
                    self.table_combo.set(val)
                except Exception:
                    pass
                break

        self.reservation_entries["reservation_date"].delete(0, tk.END)
        self.reservation_entries["reservation_date"].insert(0, reservation_date)
        self.reservation_entries["reservation_time"].delete(0, tk.END)
        self.reservation_entries["reservation_time"].insert(0, reservation_time)
        self.reservation_entries["guest_count"].delete(0, tk.END)
        self.reservation_entries["guest_count"].insert(0, guest_count)
        self.reservation_entries["status"].delete(0, tk.END)
        self.reservation_entries["status"].insert(0, status)

    def add_table(self):
        table_number = self.table_entries["table_number"].get().strip()
        capacity = self.table_entries["capacity"].get().strip()
        status = self.table_entries["status"].get().strip() or "available"
        if not table_number or not capacity:
            messagebox.showwarning("Peringatan", "Nomor meja dan kapasitas harus diisi.")
            return
        try:
            self.service.create_table(int(table_number), int(capacity), status)
            messagebox.showinfo("Berhasil", "Meja berhasil ditambahkan.")
            self.clear_table_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def edit_table_selected(self):
        if not self.selected_table_id:
            messagebox.showwarning("Peringatan", "Pilih meja terlebih dahulu.")
            return
        table_number = self.table_entries["table_number"].get().strip()
        capacity = self.table_entries["capacity"].get().strip()
        status = self.table_entries["status"].get().strip() or "available"
        try:
            self.service.update_table(self.selected_table_id, int(table_number), int(capacity), status)
            messagebox.showinfo("Berhasil", "Meja berhasil diubah.")
            self.clear_table_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_table_selected(self):
        if not self.selected_table_id:
            messagebox.showwarning("Peringatan", "Pilih meja terlebih dahulu.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus meja ini?"):
            try:
                self.service.delete_table(self.selected_table_id)
                messagebox.showinfo("Berhasil", "Meja berhasil dihapus.")
                self.clear_table_form()
                self.refresh_all_data()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def clear_table_form(self):
        for entry in self.table_entries.values():
            entry.delete(0, tk.END)
        self.selected_table_id = None

    def load_menu_items(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)

        menu_items = self.service.get_all_menu_items()
        for index, item in enumerate(menu_items, start=1):
            self.menu_tree.insert(
                "",
                "end",
                values=(item["id"], index, item["name"], self.format_rupiah(item["price"]), item["status"]),
            )

    def load_reservations(self):
        for row in self.reservation_tree.get_children():
            self.reservation_tree.delete(row)

        reservations = self.service.get_all_reservations()
        for index, item in enumerate(reservations, start=1):
            self.reservation_tree.insert(
                "",
                "end",
                values=(
                    item["id"],
                    index,
                    item["customer_name"],
                    item["table_number"],
                    item["reservation_date"],
                    item["reservation_time"],
                    item["guest_count"],
                    item["status"],
                ),
            )

    @staticmethod
    def parse_rupiah(value):
        if value is None:
            return 0.0
        text = str(value).strip()
        if not text:
            return 0.0
        text = text.replace("Rp", "").replace("rp", "")
        text = text.replace(" ", "")

        if "," in text and "." in text:
            if text.rfind(",") > text.rfind("."):
                text = text.replace(".", "").replace(",", ".")
            else:
                text = text.replace(",", "")
        elif "," in text:
            if text.count(",") == 1:
                text = text.replace(",", ".")
            else:
                text = text.replace(",", "")

        text = text.replace(".", "")
        try:
            return float(text)
        except ValueError:
            return 0.0

    @staticmethod
    def format_rupiah(value):
        try:
            amount = float(value)
        except (TypeError, ValueError):
            return ""
        integer_part = int(amount)
        if integer_part <= 0:
            return ""
        formatted = f"{integer_part:,.0f}".replace(",", ".")
        return f"Rp {formatted}"

    def clear_menu_form(self):
        for entry in self.menu_entries.values():
            entry.delete(0, tk.END)
        self.selected_menu_id = None

    def menu_selected(self, event):
        selected = self.menu_tree.selection()
        if not selected:
            self.selected_menu_id = None
            return

        item = self.menu_tree.item(selected[0], "values")
        self.selected_menu_id = item[0]
        menu_item = next((entry for entry in self.service.get_all_menu_items() if entry["id"] == self.selected_menu_id), None)

        if menu_item is None:
            return

        self.menu_entries["name"].delete(0, tk.END)
        self.menu_entries["name"].insert(0, menu_item["name"])
        self.menu_entries["category"].delete(0, tk.END)
        self.menu_entries["category"].insert(0, menu_item.get("category", ""))
        self.menu_entries["price"].delete(0, tk.END)
        self.menu_entries["price"].insert(0, self.format_rupiah(menu_item["price"]))
        self.menu_entries["status"].delete(0, tk.END)
        self.menu_entries["status"].insert(0, menu_item.get("status", "available"))

    def add_menu(self):
        name = self.menu_entries["name"].get().strip()
        category = self.menu_entries["category"].get().strip() or "umum"
        price_raw = self.menu_entries["price"].get().strip()
        status = self.menu_entries["status"].get().strip() or "available"
        if not name or not price_raw:
            messagebox.showwarning("Peringatan", "Nama menu dan harga harus diisi.")
            return
        price_value = self.parse_rupiah(price_raw)
        if price_value <= 0:
            messagebox.showwarning("Peringatan", "Harga menu harus lebih besar dari 0.")
            return
        try:
            self.service.create_menu_item(name, category, price_value, status)
            messagebox.showinfo("Berhasil", "Menu berhasil ditambahkan.")
            self.clear_menu_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def edit_menu_selected(self):
        if not self.selected_menu_id:
            messagebox.showwarning("Peringatan", "Pilih menu terlebih dahulu.")
            return
        name = self.menu_entries["name"].get().strip()
        category = self.menu_entries["category"].get().strip() or "umum"
        price_raw = self.menu_entries["price"].get().strip()
        status = self.menu_entries["status"].get().strip() or "available"
        price_value = self.parse_rupiah(price_raw)
        if not name or price_value <= 0:
            messagebox.showwarning("Peringatan", "Nama menu dan harga harus valid.")
            return
        try:
            self.service.update_menu_item(self.selected_menu_id, name, category, price_value, status)
            messagebox.showinfo("Berhasil", "Menu berhasil diubah.")
            self.clear_menu_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_menu_selected(self):
        if not self.selected_menu_id:
            messagebox.showwarning("Peringatan", "Pilih menu terlebih dahulu.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus menu ini?"):
            try:
                self.service.delete_menu_item(self.selected_menu_id)
                messagebox.showinfo("Berhasil", "Menu berhasil dihapus.")
                self.clear_menu_form()
                self.refresh_all_data()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def add_reservation(self):
        customer_name = self.customer_combo.get().strip()
        table_value = self.table_combo.get().strip()
        reservation_date = self.reservation_entries["reservation_date"].get().strip()
        reservation_time = self.reservation_entries["reservation_time"].get().strip()
        guest_count = self.reservation_entries["guest_count"].get().strip()
        status = self.reservation_entries["status"].get().strip() or "pending"
        if not customer_name or not table_value or not reservation_date or not reservation_time or not guest_count:
            messagebox.showwarning("Peringatan", "Semua field reservasi harus diisi.")
            return

        customer_id = self.customer_id_map.get(customer_name)
        table_id = self.table_id_map.get(table_value.split(" (")[0])
        if customer_id is None or table_id is None:
            messagebox.showerror("Error", "Pelanggan atau meja tidak valid.")
            return
        try:
            self.service.create_reservation(customer_id, table_id, reservation_date, reservation_time, int(guest_count), status)
            self.service.reserve_table(int(table_value.split(" ")[1].split("(")[0]), customer_id)
            messagebox.showinfo("Berhasil", "Reservasi berhasil dibuat.")
            self.clear_reservation_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def edit_reservation_selected(self):
        if not self.selected_reservation_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi terlebih dahulu.")
            return
        customer_name = self.customer_combo.get().strip()
        table_value = self.table_combo.get().strip()
        reservation_date = self.reservation_entries["reservation_date"].get().strip()
        reservation_time = self.reservation_entries["reservation_time"].get().strip()
        guest_count = self.reservation_entries["guest_count"].get().strip()
        status = self.reservation_entries["status"].get().strip() or "pending"
        try:
            customer_id = self.customer_id_map.get(customer_name)
            table_id = self.table_id_map.get(table_value.split(" (")[0])
            self.service.update_reservation(self.selected_reservation_id, customer_id, table_id, reservation_date, reservation_time, int(guest_count), status)
            messagebox.showinfo("Berhasil", "Reservasi berhasil diubah.")
            self.clear_reservation_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_reservation_selected(self):
        if not self.selected_reservation_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi terlebih dahulu.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus reservasi ini?"):
            try:
                self.service.delete_reservation(self.selected_reservation_id)
                messagebox.showinfo("Berhasil", "Reservasi berhasil dihapus.")
                self.clear_reservation_form()
                self.refresh_all_data()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def clear_reservation_form(self):
        self.customer_combo.set("")
        self.table_combo.set("")
        for entry in self.reservation_entries.values():
            entry.delete(0, tk.END)
        self.selected_reservation_id = None

    def add_order(self):
        customer_name = self.order_customer_combo.get().strip()
        table_value = self.order_table_combo.get().strip()
        menu_name = self.order_entries["menu_name"].get().strip()
        quantity = self.order_entries["quantity"].get().strip()
        unit_price_raw = self.order_entries["unit_price"].get().strip()
        if not customer_name or not table_value or not menu_name or not quantity or not unit_price_raw:
            messagebox.showwarning("Peringatan", "Semua field pesanan harus diisi.")
            return
        customer_id = self.customer_id_map.get(customer_name)
        table_id = self.table_id_map.get(table_value.split(" (")[0])
        if customer_id is None or table_id is None:
            messagebox.showerror("Error", "Pelanggan atau meja tidak valid.")
            return
        try:
            unit_price = self.parse_rupiah(unit_price_raw)
            if unit_price <= 0:
                raise ValueError("Harga satuan harus lebih dari 0.")
            order = self.service.create_order(customer_id, table_id)
            self.service.add_item_to_order(order["id"], menu_name, int(quantity), unit_price)
            messagebox.showinfo("Berhasil", "Pesanan berhasil dibuat.")
            self.clear_order_form()
            self.refresh_all_data()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def clear_order_form(self):
        self.order_customer_combo.set("")
        self.order_table_combo.set("")
        for entry in self.order_entries.values():
            entry.delete(0, tk.END)

    def load_orders(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        orders = self.service.get_all_orders()
        for index, item in enumerate(orders, start=1):
            self.order_tree.insert(
                "",
                "end",
                values=(item["id"], index, item["customer_name"], item["created_at"], f"Rp {float(item['total_amount']):,.0f}", item["status"]),
            )

    def load_reports(self):
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)

        reservations = self.service.get_all_reservations()
        for index, item in enumerate(reservations, start=1):
            self.report_tree.insert(
                "",
                "end",
                values=(item["id"], index, item["customer_name"], item["table_number"], item["reservation_date"], item["status"]),
            )

    def load_dashboard_summary(self):
        customers = self.service.get_all_customers()
        tables = self.service.get_all_tables()
        reservations = self.service.get_all_reservations()
        orders = self.service.get_all_orders()

        available_tables = sum(1 for t in tables if t["status"] == "available")
        self.dashboard_cards[0].configure(text=str(len(orders)))
        self.dashboard_cards[1].configure(text=str(available_tables))
        self.dashboard_cards[2].configure(text=str(len(reservations)))

        total_sales = sum(float(o["total_amount"]) for o in orders)
        self.dashboard_cards[3].configure(text=f"Rp {total_sales:,.0f}")

        for label in self.kitchen_status_labels:
            label.configure(text="0")

        for row in self.dashboard_reservations_tree.get_children():
            self.dashboard_reservations_tree.delete(row)
        for item in reservations[:5]:
            self.dashboard_reservations_tree.insert(
                "",
                "end",
                values=(item["customer_name"], item["table_number"], item["reservation_date"], item["reservation_time"], item["status"]),
            )

    def show_report(self):
        self.load_reports()
        messagebox.showinfo("Laporan", "Laporan reservasi berhasil ditampilkan.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantDashboardApp(root)
    root.mainloop()