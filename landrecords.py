import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ==========================================
# 1. DATABASE SETUP & INITIALIZATION
# ==========================================
def format_inr(amount):
    try:
        amount = float(amount)
    except:
        return "₹0"

    amount = round(amount)

    s = str(int(amount))

    if len(s) <= 3:
        return f"₹{s}"

    last_three = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return f"₹{','.join(parts)},{last_three}"
def init_db():
    conn = sqlite3.connect("land_registry.db")
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )""")
    
    # Create Land Records Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS land_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        khata_no TEXT NOT NULL,
        bhoomi_no TEXT NOT NULL,
        owner_name TEXT,
        survey_no TEXT,
        latitude TEXT,
        longitude TEXT,
        area_sft REAL,
        sale_value REAL,
        status TEXT DEFAULT 'Pending'
    )""")
    
    # Populate System User Matrix
    system_users = [
        ('admin1', 'admin123', 'Admin'),
        ('admin2', 'secure789', 'Admin'),
        ('Aarav Mehta', 'aarav123', 'Owner'),
        ('Diya Patel', 'diya456', 'Owner')
    ]
    
    for username, password, role in system_users:
        try:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
        except sqlite3.IntegrityError:
            pass 
        
    # Seed 12 Baseline Land Records (Updated with Aarav Mehta and Diya Patel)
    cursor.execute("SELECT COUNT(*) FROM land_records")
    if cursor.fetchone()[0] == 0:
        sample_lands = [
            ('K-101', 'B-501', 'Aarav Mehta', 'S-99', '12.97', '77.59', 1200, 0, 'Verified'),
            ('K-102', 'B-502', 'None (Govt Property)', 'S-100', '13.01', '77.62', 2400, 7104750, 'Pending'),
            ('K-103', 'B-503', 'None (Govt Property)', 'S-101', '12.85', '77.40', 1800, 4925960, 'Verified'),
            ('K-104', 'B-504', 'Diya Patel', 'S-102', '12.92', '77.51', 1500, 0, 'Pending'),
            ('K-105', 'B-505', 'None (Govt Property)', 'S-103', '13.10', '77.70', 3000, 10420300, 'Verified'),
            ('K-106', 'B-506', 'None (Govt Property)', 'S-104', '12.95', '77.53', 1100, 4262850, 'Verified'),
            ('K-107', 'B-507', 'None (Govt Property)', 'S-105', '13.05', '77.66', 2200, 8430970, 'Pending'),
            ('K-108', 'B-508', 'Aarav Mehta', 'S-106', '12.88', '77.45', 1350, 0, 'Verified'),
            ('K-109', 'B-509', 'None (Govt Property)', 'S-107', '12.99', '77.58', 4000, 20000500, 'Verified'),
            ('K-110', 'B-510', 'None (Govt Property)', 'S-108', '13.02', '77.61', 950, 3599740, 'Pending'),
            ('K-111', 'B-511', 'None (Govt Property)', 'S-109', '12.81', '77.38', 2100, 6820560, 'Pending'),
            ('K-112', 'B-512', 'Diya Patel', 'S-110', '13.15', '77.75', 3500, 0, 'Verified')
        ]
        cursor.executemany("""
            INSERT INTO land_records (khata_no, bhoomi_no, owner_name, survey_no, latitude, longitude, area_sft, sale_value, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_lands)

    conn.commit()
    conn.close()

# ==========================================
# 2. MAIN APPLICATION GUI CLASS
# ==========================================
class LandRegistryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Digital Land Registry System")
        self.root.geometry("1100x650")
        
        self.current_user = None
        self.current_role = None
        
        self.show_login_screen()

    def show_register_screen(self):
        reg = tk.Toplevel(self.root)
        reg.title("Owner Registration")
        reg.geometry("350x220")

        ttk.Label(reg, text="Create Owner Account", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(reg, text="Username / Full Name").pack()
        username_entry = ttk.Entry(reg, width=25)
        username_entry.pack(pady=3)

        ttk.Label(reg, text="Password").pack()
        password_entry = ttk.Entry(reg, show="*", width=25)
        password_entry.pack(pady=3)

        ttk.Label(reg, text="Confirm Password").pack()
        confirm_entry = ttk.Entry(reg, show="*", width=25)
        confirm_entry.pack(pady=3)

        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Username and password are required.")
                return

            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            try:
                conn = sqlite3.connect("land_registry.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, "Owner")
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Owner account created successfully.")
                reg.destroy()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

        ttk.Button(reg, text="Register", command=register).pack(pady=15)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN INTERFACE ---
    def show_login_screen(self):
        self.clear_screen()
        
        frame = ttk.Frame(self.root, padding="30")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="Secure Land Registry Login", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=25)
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Secure Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Register New Owner", command=self.show_register_screen).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Display Available System Accounts Info Box
        info_frame = ttk.LabelFrame(frame, text=" Seeded Test Accounts ")
        info_frame.grid(row=5, column=0, columnspan=2, pady=5, sticky="we")

        seed_info = "Admin: admin1 / admin123\nOwner 1: Aarav Mehta / aarav123\nOwner 2: Diya Patel / diya456"
        ttk.Label(info_frame, text=seed_info, justify="left", font=("Courier", 9)).pack(padx=5, pady=5)
        
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = sqlite3.connect("land_registry.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.current_user = username
            self.current_role = result[0]
            messagebox.showinfo("Success", f"Logged in successfully as {self.current_role}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid secure credentials.")

    # --- DASHBOARD LAYOUT ---
    def show_dashboard(self):
        self.clear_screen()
        
        # Navigation Bar
        nav_frame = ttk.Frame(self.root, relief="raised", padding="10")
        nav_frame.pack(fill="x", side="top")
        
        ttk.Label(nav_frame, text=f"Active Session: {self.current_user} ({self.current_role})", font=("Arial", 11, "bold")).pack(side="left")
        ttk.Button(nav_frame, text="Logout", command=self.show_login_screen).pack(side="right")
        
        if self.current_role == "Admin":
            ttk.Button(nav_frame, text="View Price Graph", command=self.show_chart_window).pack(side="right", padx=10)
        
        # Content Layout Split
        self.main_content = ttk.Frame(self.root, padding="10")
        self.main_content.pack(fill="both", expand=True)
        
        # LEFT: Data Grid Treeview
        left_frame = ttk.Frame(self.main_content)
        left_frame.pack(fill="both", expand=True, side="left", padx=5)
        
        # Title depending on role
        panel_title = " My Owned Land Asset Records " if self.current_role == "Owner" else " Master Registry Database Records "
        table_frame = ttk.LabelFrame(left_frame, text=panel_title)
        table_frame.pack(fill="both", expand=True, side="top", pady=5)
        
        columns = ("id", "khata", "bhoomi", "owner", "survey", "lat", "long", "area", "price", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("khata", text="Khata No")
        self.tree.heading("bhoomi", text="Bhoomi No")
        self.tree.heading("owner", text="Owner Name")
        self.tree.heading("survey", text="Survey No")
        self.tree.heading("lat", text="Lat")
        self.tree.heading("long", text="Long")
        self.tree.heading("area", text="Area")
        self.tree.heading("price", text="Price")
        self.tree.heading("status", text="Status")
        
        for col in columns:
            self.tree.column(col, width=80, anchor="center")
        self.tree.column("owner", width=120)
        
        self.tree.pack(fill="both", expand=True, side="left")
        self.tree.bind("<<TreeviewSelect>>", self.handle_row_selection)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")
        
        # RIGHT: Dynamic Operational Actions & Inputs Management Bar
        self.right_frame = ttk.LabelFrame(self.main_content, text=" Control Actions Panel ", padding="10")
        self.right_frame.pack(fill="y", side="right", padx=5)
        
        self.setup_control_panel()
        self.load_table_data()

    # --- DYNAMIC ACTION MANAGEMENT FORMS ---
    def setup_control_panel(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        if self.current_role == "Admin":
            # Admin Management Panel Form
            ttk.Label(self.right_frame, text="Land Entry Form Editor", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
            
            ttk.Label(self.right_frame, text="Khata No:").grid(row=1, column=0, sticky="w", pady=2)
            self.ent_khata = ttk.Entry(self.right_frame, width=18)
            self.ent_khata.grid(row=1, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Bhoomi No:").grid(row=2, column=0, sticky="w", pady=2)
            self.ent_bhoomi = ttk.Entry(self.right_frame, width=18)
            self.ent_bhoomi.grid(row=2, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Owner Name:").grid(row=3, column=0, sticky="w", pady=2)
            self.ent_owner = ttk.Entry(self.right_frame, width=18)
            self.ent_owner.grid(row=3, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Survey No:").grid(row=4, column=0, sticky="w", pady=2)
            self.ent_survey = ttk.Entry(self.right_frame, width=18)
            self.ent_survey.grid(row=4, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Latitude:").grid(row=5, column=0, sticky="w", pady=2)
            self.ent_lat = ttk.Entry(self.right_frame, width=18)
            self.ent_lat.grid(row=5, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Longitude:").grid(row=6, column=0, sticky="w", pady=2)
            self.ent_long = ttk.Entry(self.right_frame, width=18)
            self.ent_long.grid(row=6, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Area (Sft):").grid(row=7, column=0, sticky="w", pady=2)
            self.ent_area = ttk.Entry(self.right_frame, width=18)
            self.ent_area.grid(row=7, column=1, pady=2)
            
            ttk.Label(self.right_frame, text="Sale Value:").grid(row=8, column=0, sticky="w", pady=2)
            self.ent_price = ttk.Entry(self.right_frame, width=18)
            self.ent_price.grid(row=8, column=1, pady=2)
            
            # Form Actions Row Buttons
            btn_frame1 = ttk.Frame(self.right_frame)
            btn_frame1.grid(row=9, column=0, columnspan=2, pady=10)
            ttk.Button(btn_frame1, text="Add New", command=self.admin_add_record).pack(side="left", padx=2)
            ttk.Button(btn_frame1, text="Save Edit", command=self.admin_edit_record).pack(side="left", padx=2)
            
            sep = ttk.Separator(self.right_frame, orient="horizontal")
            sep.grid(row=10, column=0, columnspan=2, sticky="ew", pady=5)
            
            # SystemAuditing/Audit Deletion
            ttk.Button(self.right_frame, text="Verify (Approve) Record", command=self.admin_verify_record).grid(row=11, column=0, columnspan=2, pady=4, sticky="ew")
            ttk.Button(self.right_frame, text="Delete Entry", command=self.admin_delete_record).grid(row=12, column=0, columnspan=2, pady=4, sticky="ew")
            
        else:
            # Owner Operations Display Only Frame 
            ttk.Label(self.right_frame, text="Owner Information Desk", font=("Arial", 11, "bold")).pack(pady=5)
            
            info_text = f"Welcome, {self.current_user}.\n\nYour dashboard automatically identifies and isolates your assets securely.\n\nThe records shown to the left are exclusively verified or pending properties matching your credentials."
            ttk.Label(self.right_frame, text=info_text, wraplength=160, justify="left", foreground="dimgray").pack(pady=10)

    # --- AUTOMATED DATA SYNC LOAD (Isolated for Owner Logging In) ---
    def load_table_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect("land_registry.db")
        cursor = conn.cursor()
        
        # Strict dynamic filtering based on user credentials
        if self.current_role == "Owner":
            cursor.execute("SELECT * FROM land_records WHERE owner_name = ?", (self.current_user,))
        else:
            cursor.execute("SELECT * FROM land_records")
            
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
         row = list(row)
 
         row[8] = format_inr(row[8])   # already stored in INR

         self.tree.insert("", "end", values=row)
        
        

    def handle_row_selection(self, event):
        if self.current_role != "Admin":
            return
        selected = self.tree.selection()
        if not selected:
            return
            
        values = self.tree.item(selected[0])['values']
        
        # Clear fields and load selected database values into text entries
        self.ent_khata.delete(0, tk.END); self.ent_khata.insert(0, values[1])
        self.ent_bhoomi.delete(0, tk.END); self.ent_bhoomi.insert(0, values[2])
        self.ent_owner.delete(0, tk.END); self.ent_owner.insert(0, values[3])
        self.ent_survey.delete(0, tk.END); self.ent_survey.insert(0, values[4])
        self.ent_lat.delete(0, tk.END); self.ent_lat.insert(0, values[5])
        self.ent_long.delete(0, tk.END); self.ent_long.insert(0, values[6])
        self.ent_area.delete(0, tk.END); self.ent_area.insert(0, values[7])
        self.ent_price.delete(0, tk.END)

        price = str(values[8]).replace("₹", "").replace(",", "")

        self.ent_price.insert(0, price)

    # ==========================================
    # 3. BACKEND PROCESSING BUSINESS LOGIC
    # ==========================================
    
    # --- ADMIN: ADD ASSET ---
    def admin_add_record(self):
        try:
            conn = sqlite3.connect("land_registry.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO land_records (khata_no, bhoomi_no, owner_name, survey_no, latitude, longitude, area_sft, sale_value, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
            """, (self.ent_khata.get(), self.ent_bhoomi.get(), self.ent_owner.get(), self.ent_survey.get(),
                  self.ent_lat.get(), self.ent_long.get(), float(self.ent_area.get()), float(self.ent_price.get())))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "New registry data block added successfully with 'Pending' audit status!")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Validation Error", f"Failed to save record. Ensure numerical inputs are correct.\nError: {e}")

    # --- ADMIN: EDIT ASSET ---
    def admin_edit_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Missing", "Pick a record row from the grid list first to save edits.")
            return
        record_id = self.tree.item(selected[0])['values'][0]
        
        try:
            conn = sqlite3.connect("land_registry.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE land_records 
                SET khata_no=?, bhoomi_no=?, owner_name=?, survey_no=?, latitude=?, longitude=?, area_sft=?, sale_value=?
                WHERE id=?
            """, (self.ent_khata.get(), self.ent_bhoomi.get(), self.ent_owner.get(), self.ent_survey.get(),
                  self.ent_lat.get(), self.ent_long.get(), float(self.ent_area.get()), float(
                                                                                             self.ent_price.get()
                                                                                             .replace("₹", "")
                                                                                             .replace(",", "")
                                                                                            ), record_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Record registry block #{record_id} successfully updated.")
            self.load_table_data()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    # --- ADMIN: AUDIT VERIFY ---
    def admin_verify_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record row to approve.")
            return
        values = self.tree.item(selected[0])['values']
        
        if values[9] == "Verified":
            messagebox.showinfo("Information", "This asset block is already cleared and verified.")
            return
            
        conn = sqlite3.connect("land_registry.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE land_records SET status='Verified' WHERE id=?", (values[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo("Asset Verified", f"Audit complete. Entry ID #{values[0]} is now 'Verified'.")
        self.load_table_data()

    # --- ADMIN: DELETE ASSET ---
    def admin_delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry row to wipe from the database ledger.")
            return
        record_id = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you absolutely sure you want to delete entry #{record_id}?"):
            conn = sqlite3.connect("land_registry.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM land_records WHERE id=?", (record_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Record removed from registry successfully.")
            self.load_table_data()

    # --- PRICE ANALYTICS CHART CANVAS ---
    def show_chart_window(self):
        graph_win = tk.Toplevel(self.root)
        graph_win.title("Marketplace Pricing Analytics Engine")
        graph_win.geometry("900x500")
        
        ttk.Label(graph_win, text="Market Prices of Available Lands", font=("Arial", 12, "bold")).pack(pady=10)
        
        conn = sqlite3.connect("land_registry.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bhoomi_no, sale_value FROM land_records WHERE owner_name LIKE '%None%'")
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            ttk.Label(graph_win, text="No properties are currently available on the open market.").pack(pady=50)
            return
            
        canvas = tk.Canvas(graph_win, width=800, height=350, bg="white")
        canvas.pack(pady=10)
        
        canvas.create_line(50, 210, 550, 210, width=2)
        canvas.create_line(50, 30, 50, 210, width=2)

        max_val = max([x[1] for x in data]) if data else 100000
        bar_width = 35
        spacing = 20
        start_x = 65
        
        for i, (bhoomi, val) in enumerate(data):
            
            inr_val = val
            height = int((inr_val / max_val) * 155) if max_val > 0 else 0
            x0 = start_x + (i * (bar_width + spacing))
            y0 = 210 - height
            x1 = x0 + bar_width
            y1 = 210
            
            canvas.create_rectangle(x0, y0, x1, y1, fill="#2ecc71", outline="#27ae60")
            canvas.create_text(
             (x0 + x1)/2,
             y0 - 10,
             text=format_inr(inr_val),
              font=("Arial", 8, "bold")
            )
            canvas.create_text((x0 + x1)/2, 225, text=bhoomi, font=("Arial", 7), angle=15)

# ==========================================
# 4. RUNTIME SYSTEM EXECUTION 
# ==========================================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LandRegistryApp(root)
    root.mainloop()