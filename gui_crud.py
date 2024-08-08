import tkinter as tk
from tkinter import messagebox, ttk
import crud_operations as crud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Kelas untuk aplikasi manajemen inventaris
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Ops (Aplikasi Manajemen Inventaris)")
        self.root.geometry("1000x600")
        self.root.configure(bg='#f0f0f0')

        self.create_widgets()

    # Fungsi untuk membuat widget di dalam aplikasi
    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="Selamat Datang di StockOps!", font=("Helvetica", 18, "bold"), bg='#f0f0f0')
        header.pack(pady=10)

        # Frame untuk form input
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(pady=10)

        # Labels dan Entry Widgets
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        tk.Label(frame, text="Kode Barang:", font=label_font, bg='#f0f0f0').grid(row=0, column=0, sticky=tk.W, pady=2)
        self.id_entry = tk.Entry(frame, font=entry_font)
        self.id_entry.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="Nama:", font=label_font, bg='#f0f0f0').grid(row=1, column=0, sticky=tk.W, pady=2)
        self.name_entry = tk.Entry(frame, font=entry_font)
        self.name_entry.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Deskripsi:", font=label_font, bg='#f0f0f0').grid(row=2, column=0, sticky=tk.W, pady=2)
        self.description_entry = tk.Entry(frame, font=entry_font)
        self.description_entry.grid(row=2, column=1, pady=2)

        tk.Label(frame, text="Stok:", font=label_font, bg='#f0f0f0').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.stock_entry = tk.Entry(frame, font=entry_font)
        self.stock_entry.grid(row=3, column=1, pady=2)

        tk.Label(frame, text="Stok Minimum:", font=label_font, bg='#f0f0f0').grid(row=4, column=0, sticky=tk.W, pady=2)
        self.minimum_stock_entry = tk.Entry(frame, font=entry_font)
        self.minimum_stock_entry.grid(row=4, column=1, pady=2)

        tk.Label(frame, text="Harga:", font=label_font, bg='#f0f0f0').grid(row=5, column=0, sticky=tk.W, pady=2)
        self.price_entry = tk.Entry(frame, font=entry_font)
        self.price_entry.grid(row=5, column=1, pady=2)

        # Frame untuk tombol
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)

        button_font = ("Helvetica", 12)
        tk.Button(button_frame, text="Save", font=button_font, command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update", font=button_font, command=self.update_item).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear", font=button_font, command=self.clear_entries).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Delete", font=button_font, command=self.remove_item).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Analisis", font=button_font, command=self.show_analysis_menu).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Exit", font=button_font, command=self.root.quit).grid(row=0, column=5, padx=5)

        # Tabel untuk menampilkan data barang
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Stock", "Minimum Stock", "Price"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Nama Barang")
        self.tree.heading("Description", text="Deskripsi")
        self.tree.heading("Stock", text="Stok")
        self.tree.heading("Minimum Stock", text="Minimum Stok")
        self.tree.heading("Price", text="Harga")

        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center", stretch=tk.NO)

        self.tree.column("Description", width=250)

        self.tree.pack(pady=20, fill="x", expand=True)
        self.show_items()

        # Gaya untuk tabel
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#f0f0f0")
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})]) # Menghilangkan border

    # Fungsi untuk menambahkan item ke database
    def add_item(self):
        try:
            item_id = int(self.id_entry.get())
            name = self.name_entry.get()
            description = self.description_entry.get()
            stock = int(self.stock_entry.get())
            minimum_stock = int(self.minimum_stock_entry.get())
            price = float(self.price_entry.get())

            if not name or not description:
                raise ValueError("Semua kolom harus diisi")

            result = crud.add_item(item_id, name, description, stock, minimum_stock, price)
            messagebox.showinfo("Info", result)
            self.show_items()
        except ValueError as ve:
            messagebox.showerror("Error", f"Input tidak valid: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # Fungsi untuk menghapus item dari database
    def remove_item(self):
        try:
            if not self.tree.selection():
                messagebox.showwarning("Warning", "Pilih item yang ingin dihapus")
                return
            selected_item = self.tree.selection()[0]
            item_id = self.tree.item(selected_item)['values'][0]
            result = crud.remove_item(item_id)
            messagebox.showinfo("Info", result)
            self.show_items()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # Fungsi untuk memperbarui item di database
    def update_item(self):
        try:
            item_id = self.id_entry.get()
            if not item_id:
                messagebox.showwarning("Warning", "Masukkan Kode Barang yang ingin diupdate")
                return

            name = self.name_entry.get() or None
            description = self.description_entry.get() or None
            stock = self.stock_entry.get()
            stock = int(stock) if stock else None
            minimum_stock = self.minimum_stock_entry.get()
            minimum_stock = int(minimum_stock) if minimum_stock else None
            price = self.price_entry.get()
            price = float(price) if price else None

            result = crud.update_item(item_id, name, description, stock, minimum_stock, price)
            messagebox.showinfo("Info", result)
            self.show_items()
        except ValueError as ve:
            messagebox.showerror("Error", f"Input tidak valid: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # Fungsi untuk menampilkan semua item dari database
    def show_items(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            items = crud.show_items()
            if isinstance(items, str):
                messagebox.showerror("Error", items)
            else:
                for item in items:
                    self.tree.insert("", "end", values=item)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    # Fungsi untuk menghapus data dari form input
    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.minimum_stock_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    # Fungsi untuk menampilkan menu analisis
    def show_analysis_menu(self):
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Menu Analisis")
        analysis_window.geometry("400x200")
        
        tk.Button(analysis_window, text="Stok Terbanyak", font=("Helvetica", 12), command=self.analyze_stock).pack(pady=10)
        tk.Button(analysis_window, text="Harga Tertinggi", font=("Helvetica", 12), command=self.analyze_price).pack(pady=10)
        tk.Button(analysis_window, text="Stok Di Bawah Minimum", font=("Helvetica", 12), command=self.analyze_below_minimum).pack(pady=10)
        tk.Button(analysis_window, text="Kembali", font=("Helvetica", 12), command=analysis_window.destroy).pack(pady=10)

    # Fungsi untuk analisis stok terbanyak
    def analyze_stock(self):
        items = crud.show_items()
        if isinstance(items, str):
            messagebox.showerror("Error", items)
        else:
            items_sorted = sorted(items, key=lambda x: x[3], reverse=True)  # Mengurutkan berdasarkan stok
            item_names = [item[1] for item in items_sorted]
            item_stocks = [item[3] for item in items_sorted]

            fig, ax = plt.subplots()
            ax.barh(item_names, item_stocks, color='skyblue')
            ax.set_xlabel('Stok')
            ax.set_title('Stok Barang')
            ax.invert_yaxis()  # Untuk menampilkan yang terbanyak di atas

            for i in ax.patches:
                ax.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()), fontsize=10, color='dimgrey')

            plt.tight_layout()
            
            top = tk.Toplevel(self.root)
            top.title("Analisis Stok Barang")
            canvas = FigureCanvasTkAgg(fig, master=top)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            tk.Button(top, text="Kembali", font=("Helvetica", 12), command=top.destroy).pack(pady=10)
            canvas.draw()

    # Fungsi untuk analisis harga tertinggi
    def analyze_price(self):
        items = crud.show_items()
        if isinstance(items, str):
            messagebox.showerror("Error", items)
        else:
            items_sorted = sorted(items, key=lambda x: x[5], reverse=True)  # Mengurutkan berdasarkan harga
            item_names = [item[1] for item in items_sorted]
            item_prices = [item[5] for item in items_sorted]

            fig, ax = plt.subplots()
            ax.barh(item_names, item_prices, color='lightgreen')
            ax.set_xlabel('Harga')
            ax.set_title('Harga Barang')
            ax.invert_yaxis()  # Untuk menampilkan yang tertinggi di atas

            for i in ax.patches:
                ax.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()), fontsize=10, color='dimgrey')

            plt.tight_layout()
            
            top = tk.Toplevel(self.root)
            top.title("Analisis Harga Barang")
            canvas = FigureCanvasTkAgg(fig, master=top)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            tk.Button(top, text="Kembali", font=("Helvetica", 12), command=top.destroy).pack(pady=10)
            canvas.draw()

    # Fungsi untuk analisis stok di bawah minimum
    def analyze_below_minimum(self):
        items = crud.show_items()
        if isinstance(items, str):
            messagebox.showerror("Error", items)
        else:
            below_minimum = [item for item in items if item[3] < item[4]]  # Barang di bawah stok minimum
            item_names = [item[1] for item in below_minimum]
            item_stocks = [item[3] for item in below_minimum]

            fig, ax = plt.subplots()
            ax.barh(item_names, item_stocks, color='salmon')
            ax.set_xlabel('Stok')
            ax.set_title('Barang di Bawah Stok Minimum')
            ax.invert_yaxis()  # Untuk menampilkan yang terbanyak di atas

            for i in ax.patches:
                ax.text(i.get_width() + 0.2, i.get_y() + 0.5, str(i.get_width()), fontsize=10, color='dimgrey')

            plt.tight_layout()
            
            top = tk.Toplevel(self.root)
            top.title("Analisis Barang di Bawah Stok Minimum")
            canvas = FigureCanvasTkAgg(fig, master=top)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            tk.Button(top, text="Kembali", font=("Helvetica", 12), command=top.destroy).pack(pady=10)
            canvas.draw()

# Fungsi utama untuk menjalankan GUI
def main_gui():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

# Mengeksekusi aplikasi jika file ini dijalankan
if __name__ == "__main__":
    main_gui()
