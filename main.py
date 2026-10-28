import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB = "mobil_shop.db"

# ================= DATABASE =================
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # Aksessuarlar / telefonlar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        condition TEXT
    )
    """)
    # Mijozlar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT
    )
    """)
    # Sotib olish jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        client_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)
    # Foydalanuvchilar jadvali (login)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    # Admin qo‘shish
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users(username,password) VALUES(?,?)", ("admin","1234"))
    con.commit()
    con.close()

def get_connection():
    return sqlite3.connect(DB)

# ================= LOGIN WINDOW =================
def login_window():
    login_win = tk.Tk()
    login_win.title("Mobil Sawda - Login")
    login_win.geometry("450x350")
    login_win.configure(bg="#1abc9c")  # zamonaviy turquoise fon

    tk.Label(login_win, text="📱 Mobil Sawda Platformasi", font=("Arial", 18, "bold"), bg="#1abc9c", fg="white").pack(pady=25)
    tk.Label(login_win, text="Paydalaniwshi ati", bg="#1abc9c", fg="white", font=("Arial",12)).pack()
    e_user = tk.Entry(login_win, font=("Arial",12))
    e_user.pack(pady=8)

    tk.Label(login_win, text="Parol", bg="#1abc9c", fg="white", font=("Arial",12)).pack()
    e_pass = tk.Entry(login_win, show="*", font=("Arial",12))
    e_pass.pack(pady=8)

    def login():
        username = e_user.get()
        password = e_pass.get()
        with get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
            if cur.fetchone():
                login_win.destroy()
                main_window()
            else:
                messagebox.showerror("Xato", "Login yaki parol qate!")

    tk.Button(login_win, text="Kiriw", width=18, bg="#16a085", fg="white", font=("Arial", 12, "bold"), command=login).pack(pady=20)

    login_win.mainloop()

# ================= MAIN WINDOW =================
def main_window():
    root = tk.Tk()
    root.title("Mobil Sawda Platformasi")
    root.geometry("1000x600")
    root.configure(bg="#ecf0f1")

    # ===== HEADER =====
    header = tk.Frame(root, bg="#34495e", height=60)
    header.pack(fill="x")
    tk.Label(header, text="📱 MOBIL TELEFONLAR HAM AKSESSUARLAR", font=("Arial", 20, "bold"), fg="white", bg="#34495e").pack(pady=10)

    main = tk.Frame(root, bg="#ecf0f1")
    main.pack(fill="both", expand=True)

    # ===== MENU =====
    menu = tk.Frame(main, width=220, bg="#2c3e50")
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    # ===== CONTENT =====
    content = tk.Frame(main, bg="#ecf0f1")
    content.pack(side="right", fill="both", expand=True)

    def clear():
        for w in content.winfo_children():
            w.destroy()

    # ================= DASHBOARD =================
    def dashboard_page():
        clear()
        tk.Label(content, text="📊 Dashboard", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)
        with get_connection() as con:
            p = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]
            c = con.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
            s = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]

        stats = tk.Frame(content, bg="#ecf0f1")
        stats.pack(pady=20)
        tk.Label(stats, text=f"Aksessuarlar sani: {p}", font=("Arial", 14), bg="#ecf0f1", fg="#2c3e50").pack(pady=5)
        tk.Label(stats, text=f"Klientler sani: {c}", font=("Arial", 14), bg="#ecf0f1", fg="#2c3e50").pack(pady=5)
        tk.Label(stats, text=f"Satilgan aksesuarlar sani: {s}", font=("Arial", 14), bg="#ecf0f1", fg="#2c3e50").pack(pady=5)

    # ================= PRODUCTS =================
    def products_page():
        clear()
        tk.Label(content, text="📦 Aksessuarlar ham Telefonlar", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=10)

        form = tk.Frame(content, bg="#ecf0f1")
        form.pack(pady=10)
        tk.Label(form, text="Ati", bg="#ecf0f1", font=("Arial",12)).grid(row=0, column=0, padx=5, pady=5)
        e_name = tk.Entry(form, font=("Arial",12))
        e_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Bahasi", bg="#ecf0f1", font=("Arial",12)).grid(row=1, column=0, padx=5, pady=5)
        e_price = tk.Entry(form, font=("Arial",12))
        e_price.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Jagdayi", bg="#ecf0f1", font=("Arial",12)).grid(row=2, column=0, padx=5, pady=5)
        e_condition = ttk.Combobox(form, values=["Jaqsi","Ortasha","Jaman"], state="readonly", font=("Arial",12))
        e_condition.grid(row=2, column=1, padx=5, pady=5)
        e_condition.set("Jaqsi")

        table_frame = tk.Frame(content)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        table = ttk.Treeview(table_frame, columns=("id","n","p","c"), show="headings", height=10)
        table.pack(side="left", fill="both", expand=True)
        for col, txt in zip(("id","n","p","c"), ("ID","Nomi","Narxi","Holati")):
            table.heading(col, text=txt)
        table.tag_configure('oddrow', background="#dff9fb")
        table.tag_configure('evenrow', background="#f1f2f6")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def load():
            table.delete(*table.get_children())
            with get_connection() as con:
                rows = con.execute("SELECT * FROM products").fetchall()
                for i, r in enumerate(rows):
                    tag = 'evenrow' if i %2==0 else 'oddrow'
                    table.insert("", "end", values=r, tags=(tag,))

        def add():
            if not e_name.get() or not e_price.get() or not e_condition.get():
                messagebox.showwarning("Xato","Hamme maydanlardi toldirin!")
                return
            with get_connection() as con:
                con.execute("INSERT INTO products(name,price,condition) VALUES(?,?,?)",
                            (e_name.get(), e_price.get(), e_condition.get()))
            e_name.delete(0, tk.END)
            e_price.delete(0, tk.END)
            e_condition.set("Yaxshi")
            load()

        def delete():
            sel = table.selection()
            if not sel: return
            if messagebox.askyesno("Ogohlantirish","Oshiresiz be?"):
                pid = table.item(sel[0])["values"][0]
                with get_connection() as con:
                    con.execute("DELETE FROM products WHERE id=?", (pid,))
                load()

        btn = tk.Frame(content, bg="#ecf0f1")
        btn.pack(pady=5)
        tk.Button(btn, text="➕ Qosiw", command=add, bg="#27ae60", fg="white", width=14, font=("Arial",12,"bold")).pack(side="left", padx=5)
        tk.Button(btn, text="🗑️ Oshiriw", command=delete, bg="#c0392b", fg="white", width=14, font=("Arial",12,"bold")).pack(side="left", padx=5)

        load()

    # ================= CLIENTS =================
    def clients_page():
        clear()
        tk.Label(content, text="👥 Klientler", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=10)

        form = tk.Frame(content, bg="#ecf0f1")
        form.pack(pady=10)
        tk.Label(form, text="FIO", bg="#ecf0f1", font=("Arial",12)).grid(row=0, column=0, padx=5, pady=5)
        e_name = tk.Entry(form, font=("Arial",12))
        e_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Email", bg="#ecf0f1", font=("Arial",12)).grid(row=1, column=0, padx=5, pady=5)
        e_email = tk.Entry(form, font=("Arial",12))
        e_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Telefon", bg="#ecf0f1", font=("Arial",12)).grid(row=2, column=0, padx=5, pady=5)
        e_phone = tk.Entry(form, font=("Arial",12))
        e_phone.grid(row=2, column=1, padx=5, pady=5)

        table_frame = tk.Frame(content)
        table_frame.pack(fill="both", expand=True, pady=10)

        table = ttk.Treeview(table_frame, columns=("i","n","e","p"), show="headings", height=10)
        table.pack(side="left", fill="both", expand=True)
        for c, txt in zip(("i","n","e","p"), ("ID","Ism","Email","Telefon")):
            table.heading(c, text=txt)
        table.tag_configure('oddrow', background="#dff9fb")
        table.tag_configure('evenrow', background="#f1f2f6")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def load():
            table.delete(*table.get_children())
            with get_connection() as con:
                rows = con.execute("SELECT * FROM clients").fetchall()
                for i,r in enumerate(rows):
                    tag = 'evenrow' if i%2==0 else 'oddrow'
                    table.insert("", "end", values=r, tags=(tag,))

        def add():
            if not e_name.get() or not e_email.get() or not e_phone.get():
                messagebox.showwarning("Xato","Hamme maydanlardi toldirin!")
                return
            with get_connection() as con:
                con.execute("INSERT INTO clients(name,email,phone) VALUES(?,?,?)",
                            (e_name.get(), e_email.get(), e_phone.get()))
            e_name.delete(0, tk.END)
            e_email.delete(0, tk.END)
            e_phone.delete(0, tk.END)
            load()

        def delete():
            sel = table.selection()
            if not sel: return
            if messagebox.askyesno("Ogohlantirish","Oshiresiz be?"):
                cid = table.item(sel[0])["values"][0]
                with get_connection() as con:
                    con.execute("DELETE FROM clients WHERE id=?", (cid,))
                load()

        btn = tk.Frame(content, bg="#ecf0f1")
        btn.pack(pady=5)
        tk.Button(btn, text="➕ Qosiw", command=add, bg="#27ae60", fg="white", width=14, font=("Arial",12,"bold")).pack(side="left", padx=5)
        tk.Button(btn, text="🗑️ Oshiriw", command=delete, bg="#c0392b", fg="white", width=14, font=("Arial",12,"bold")).pack(side="left", padx=5)

        load()

    # ================= SALES =================
    def sales_page():
        clear()
        tk.Label(content, text="💰 Satip aliw", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=10)

        tk.Label(content, text="Aksessuar ID", bg="#ecf0f1", font=("Arial",12)).pack()
        e_prod = tk.Entry(content, font=("Arial",12))
        e_prod.pack(pady=5)

        tk.Label(content, text="Klient ID", bg="#ecf0f1", font=("Arial",12)).pack()
        e_client = tk.Entry(content, font=("Arial",12))
        e_client.pack(pady=5)

        def add():
            if not e_prod.get() or not e_client.get():
                messagebox.showwarning("Xato","Hamme maydanlardi toldirin!")
                return
            with get_connection() as con:
                con.execute("INSERT INTO sales(product_id,client_id) VALUES(?,?)",
                            (e_prod.get(), e_client.get()))
            e_prod.delete(0, tk.END)
            e_client.delete(0, tk.END)
            messagebox.showinfo("OK","Sawda qosildi")

        tk.Button(content, text="💾 Qosiw", command=add, bg="#2980b9", fg="white", width=15, font=("Arial",12,"bold")).pack(pady=10)

    # ===== MENU BUTTONS =====
    btn_params = {"width":20, "font":("Arial",12,"bold"), "bg":"#34495e", "fg":"white"}
    tk.Button(menu, text="📊 Dashboard", command=dashboard_page, **btn_params).pack(pady=5)
    tk.Button(menu, text="📦 Aksessuarlar", command=products_page, **btn_params).pack(pady=5)
    tk.Button(menu, text="👥 Klientler", command=clients_page, **btn_params).pack(pady=5)
    tk.Button(menu, text="💰 Satip aliw", command=sales_page, **btn_params).pack(pady=5)

    dashboard_page()
    root.mainloop()

# ================= RUN =================
if __name__ == "__main__":
    init_db()
    login_window()
