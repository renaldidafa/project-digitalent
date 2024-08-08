import mysql.connector
from mysql.connector import Error

# Fungsi untuk membuat koneksi ke database
def create_connection():
    try:
        # Mengatur konfigurasi koneksi ke database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  
            database="stockops"
        )
        # Memeriksa apakah koneksi berhasil
        if connection.is_connected():
            return connection
    except Error as e:
        # Menampilkan pesan error jika terjadi kesalahan
        print(f"Error: {e}")
        return None

# Fungsi untuk menambahkan item ke dalam database
def add_item(item_id, name, description, stock, minimum_stock, price):
    try:
        # Membuat koneksi ke database
        connection = create_connection()
        if connection is None:
            return "Gagal terhubung ke database"
        
        # Membuat cursor untuk eksekusi query
        cursor = connection.cursor()
        # Query untuk menambahkan item
        query = "INSERT INTO items (id, name, description, stock, minimum_stock, price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (item_id, name, description, stock, minimum_stock, price)
        # Menjalankan query
        cursor.execute(query, values)
        # Menyimpan perubahan ke database
        connection.commit()
        return "Data barang berhasil ditambahkan"
    except Error as e:
        return f"Error: {e}"
    finally:
        # Menutup koneksi ke database
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fungsi untuk menghapus item dari database
def remove_item(item_id):
    try:
        # Membuat koneksi ke database
        connection = create_connection()
        if connection is None:
            return "Gagal terhubung ke database"
        
        # Membuat cursor untuk eksekusi query
        cursor = connection.cursor()
        # Query untuk menghapus item
        query = "DELETE FROM items WHERE id = %s"
        # Menjalankan query
        cursor.execute(query, (item_id,))
        # Menyimpan perubahan ke database
        connection.commit()
        # Memeriksa apakah ada baris yang terpengaruh oleh query
        if cursor.rowcount > 0:
            return "Data barang berhasil dihapus"
        else:
            return "Barang tidak ditemukan"
    except Error as e:
        return f"Error: {e}"
    finally:
        # Menutup koneksi ke database
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fungsi untuk memperbarui data item di database
def update_item(item_id, name=None, description=None, stock=None, minimum_stock=None, price=None):
    try:
        # Membuat koneksi ke database
        connection = create_connection()
        if connection is None:
            return "Gagal terhubung ke database"
        
        # Membuat cursor untuk eksekusi query
        cursor = connection.cursor()
        set_clause = []
        values = []

        # Menambahkan bagian yang perlu diperbarui ke dalam query
        if name:
            set_clause.append("name = %s")
            values.append(name)
        if description:
            set_clause.append("description = %s")
            values.append(description)
        if stock is not None:
            set_clause.append("stock = %s")
            values.append(stock)
        if minimum_stock is not None:
            set_clause.append("minimum_stock = %s")
            values.append(minimum_stock)
        if price is not None:
            set_clause.append("price = %s")
            values.append(price)

        # Jika tidak ada data yang diupdate
        if not set_clause:
            return "Tidak ada data yang diupdate"

        # Menggabungkan bagian-bagian query
        set_clause = ", ".join(set_clause)
        query = f"UPDATE items SET {set_clause} WHERE id = %s"
        values.append(item_id)
        # Menjalankan query
        cursor.execute(query, tuple(values))
        # Menyimpan perubahan ke database
        connection.commit()
        # Memeriksa apakah ada baris yang terpengaruh oleh query
        if cursor.rowcount > 0:
            return "Data barang berhasil diupdate"
        else:
            return "Barang tidak ditemukan"
    except Error as e:
        return f"Error: {e}"
    finally:
        # Menutup koneksi ke database
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fungsi untuk menampilkan semua item dari database
def show_items():
    try:
        # Membuat koneksi ke database
        connection = create_connection()
        if connection is None:
            return "Gagal terhubung ke database"
        
        # Membuat cursor untuk eksekusi query
        cursor = connection.cursor()
        # Query untuk mengambil semua data item
        query = "SELECT * FROM items"
        # Menjalankan query
        cursor.execute(query)
        # Mengambil semua hasil query
        results = cursor.fetchall()
        return results
    except Error as e:
        return f"Error: {e}"
    finally:
        # Menutup koneksi ke database
        if connection.is_connected():
            cursor.close()
            connection.close()
