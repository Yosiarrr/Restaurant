# Sistem Pemesanan Restoran

Aplikasi pemesanan restoran berbasis Python dengan pendekatan pemrograman terstruktur dan berorientasi objek. Aplikasi ini mendukung:

- manajemen pelanggan
- manajemen meja dan status reservasi
- pembuatan pesanan dan item pesanan
- laporan penjualan harian dan ringkasan meja
- dukungan database SQLite untuk pengujian lokal dan opsi konfigurasi MySQL/MariaDB

## Struktur Proyek

- `main.py` : entry point aplikasi CLI
- `restaurant_app/` : paket aplikasi
  - `config.py` : konfigurasi database dan environment
  - `database.py` : koneksi dan skema database
  - `models.py` : model data berbasis class
  - `services.py` : logika bisnis restoran
  - `app.py` : antarmuka CLI
- `tests/` : unit test
- `database_schema.sql` : skema SQL database

## Persyaratan

- Python 3.10+
- MySQL/MariaDB (opsional untuk production)
- package `mysql-connector-python` (opsional, akan diinstall dari `requirements.txt`)

## Menjalankan Aplikasi

1. Buat lingkungan virtual (opsional):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Menjalankan Unit Test

```bash
python -m unittest discover -s tests -v
```

## Konfigurasi MySQL

Atur variabel environment berikut sebelum menjalankan aplikasi:

```bash
set DB_TYPE=mysql
set DB_HOST=localhost
set DB_PORT=3306
set DB_NAME=restaurant_db
set DB_USER=root
set DB_PASSWORD=secret
```

Jika `DB_TYPE` tidak diatur atau tidak tersedia, aplikasi otomatis menggunakan database SQLite yang akan dibuat di `restaurant.db`.

## Fitur Utama

- `create_customer()`
- `create_table()`
- `reserve_table()`
- `create_order()`
- `add_item_to_order()`
- `complete_order()`
- `get_customer_order_history()`
- `get_daily_sales_report()`
- `get_table_status_summary()`

## Catatan Arsitektur

Aplikasi ini menggabungkan prinsip pemrograman terstruktur dan berbasis objek dengan memisahkan:

- model data di `models.py`
- akses data di `database.py`
- logika bisnis di `services.py`
- interaksi pengguna di `app.py`

Hal ini memudahkan maintenance, testing, dan pengembangan lebih lanjut.
