import customtkinter as ctk
import database


# -------------------------------
# APPLICATION CONFIGURATION
# -------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "background": "#111318",
    "sidebar": "#181B22",
    "card": "#1C2029",
    "border": "#2B303B",
    "text": "#F1F3F8",
    "muted": "#9299A8",
    "blue": "#4B8BFF",
    "green": "#35C98A",
    "orange": "#F0A64B",
    "red": "#F06464"
}


# -------------------------------
# MAIN APPLICATION
# -------------------------------

class MiniStockApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("MiniStock | Inventory Manager")
        self.geometry("1150x750")
        self.minsize(950, 650)
        self.configure(fg_color=COLORS["background"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    # ---------------------------
    # SIDEBAR
    # ---------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=COLORS["sidebar"]
        )

        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Branding
        ctk.CTkLabel(
            self.sidebar,
            text="MiniStock",
            font=("Arial", 27, "bold"),
            text_color=COLORS["blue"]
        ).pack(pady=(35, 5), padx=25, anchor="w")

        ctk.CTkLabel(
            self.sidebar,
            text="INVENTORY MANAGEMENT",
            font=("Arial", 9, "bold"),
            text_color=COLORS["muted"]
        ).pack(padx=27, anchor="w", pady=(0, 35))

        # Navigation
        self.nav_buttons = {}

        navigation = [
            ("Dashboard", "dashboard"),
            ("Products", "products")
        ]

        for label, page in navigation:

            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=42,
                anchor="w",
                corner_radius=8,
                fg_color=COLORS["blue"] if page == "dashboard" else "transparent",
                hover_color="#303B50",
                text_color="white",
                font=("Arial", 14),
                command=lambda p=page: self.show_page(p)
            )

            button.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[page] = button

        # Bottom section
        ctk.CTkLabel(
            self.sidebar,
            text="MINISTOCK v1.0",
            font=("Arial", 10),
            text_color=COLORS["muted"]
        ).pack(side="bottom", pady=25)

    # ---------------------------
    # MAIN CONTENT AREA
    # ---------------------------

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=25
        )

        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        self.show_page("dashboard")

    # ---------------------------
    # PAGE NAVIGATION
    # ---------------------------

    def show_page(self, page):

        for widget in self.main_area.winfo_children():
            widget.destroy()

        for name, button in self.nav_buttons.items():

            button.configure(
                fg_color=COLORS["blue"] if name == page else "transparent"
            )

        if page == "dashboard":
            self.create_dashboard()

        elif page == "products":
            self.create_products_page()

    # ---------------------------
    # DASHBOARD
    # ---------------------------

    def create_dashboard(self):

        # Header
        header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 25))

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=("Arial", 29, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Overview of your store inventory",
            font=("Arial", 13),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(5, 0))

        # Scrollable dashboard content
        self.dashboard = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color="transparent"
        )

        self.dashboard.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.dashboard.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # Statistics
        stats = database.get_statistics()

        stat_cards = [
            (
                "Total Products",
                str(stats["total_products"]),
                "Registered products",
                COLORS["blue"]
            ),
            (
                "Stock Units",
                f"{stats['total_units']:,}",
                "Units available",
                COLORS["green"]
            ),
            (
                "Low Stock",
                str(stats["low_stock"]),
                "Need restocking",
                COLORS["orange"]
            ),
            (
                "Out of Stock",
                str(stats["out_of_stock"]),
                "Currently unavailable",
                COLORS["red"]
            )
        ]

        for index, (title, value, subtitle, color) in enumerate(stat_cards):
            row = index // 2
            column = index % 2

            self.create_stat_card(
                row, column, title, value, subtitle, color
            )

        # Product table heading
        ctk.CTkLabel(
            self.dashboard,
            text="Recent Inventory",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(35, 15)
        )

        self.create_product_table()

        # Low stock section
        ctk.CTkLabel(
            self.dashboard,
            text="Stock Alerts",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(30, 12)
        )

        self.create_stock_alert()

    # ---------------------------
    # STATISTICS CARDS
    # ---------------------------

    def create_stat_card(
        self, row, column, title, value, subtitle, color
    ):

        card = ctk.CTkFrame(
            self.dashboard,
            fg_color=COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )

        card.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=6,
            pady=6
        )

        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 13),
            text_color=COLORS["muted"]
        ).pack(anchor="w", padx=18, pady=(18, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 29, "bold"),
            text_color=color
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Arial", 11),
            text_color=COLORS["muted"]
        ).pack(anchor="w", padx=18, pady=(3, 18))

    # ---------------------------
    # PRODUCT TABLE
    # ---------------------------

    def create_product_table(self):

        table = ctk.CTkFrame(
            self.dashboard,
            fg_color=COLORS["card"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"]
        )

        table.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6
        )

        columns = ["ID", "Product", "Category", "Price", "Quantity", "Min stock"]

        for column, name in enumerate(columns):

            ctk.CTkLabel(
                table,
                text=name,
                font=("Arial", 12, "bold"),
                text_color=COLORS["muted"],
                anchor="w"
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=12,
                pady=14
            )

            table.grid_columnconfigure(column, weight=1)

        products = database.get_products()

        for row, product in enumerate(products, start=1):

            for column, value in enumerate(product):

                color = COLORS["text"]

                if column == 3 and value == "4":
                    color = COLORS["orange"]

                elif column == 3 and value == "0":
                    color = COLORS["red"]

                ctk.CTkLabel(
                    table,
                    text=value,
                    font=("Arial", 12),
                    text_color=color,
                    anchor="w"
                ).grid(
                    row=row,
                    column=column,
                    sticky="ew",
                    padx=12,
                    pady=12
                )

            ctk.CTkFrame(
                table,
                height=1,
                fg_color=COLORS["border"]
            ).grid(
                row=row + 1,
                column=0,
                columnspan=4,
                sticky="ew"
            )

    # ---------------------------
    # STOCK ALERTS
    # ---------------------------

    def create_stock_alert(self):
        alert = ctk.CTkFrame(
            self.dashboard,
            fg_color=COLORS["card"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"]
        )

        alert.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=6,
            pady=(0, 20)
        )

        low_stock_products = database.get_low_stock_products()

        if not low_stock_products:
            message = "All products are sufficiently stocked."
            color = COLORS["green"]
        else:
            message = None

        if message:
            ctk.CTkLabel(
                alert,
                text=message,
                font=("Arial", 13),
                text_color=color
            ).pack(anchor="w", padx=18, pady=16)

        else:
            for product in low_stock_products:
                if product["quantity"] == 0:
                    message = f"⚠  {product['name']} — Out of stock"
                    color = COLORS["red"]
                else:
                    message = (
                        f"⚠  {product['name']} — "
                        f"Only {product['quantity']} units remaining"
                    )
                    color = COLORS["orange"]

                ctk.CTkLabel(
                    alert,
                    text=message,
                    font=("Arial", 13),
                    text_color=color
                ).pack(anchor="w", padx=18, pady=8)

    # ---------------------------
    # TEMPORARY PRODUCTS PAGE
    # ---------------------------

    
    # ---------------------------
    # PRODUCTS PAGE
    # ---------------------------

    def create_products_page(self):

        header = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )
        header.pack(fill="x", pady=(10, 20))

        ctk.CTkLabel(
            header,
            text="Products",
            font=("Arial", 29, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Manage your store inventory",
            font=("Arial", 13),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(5, 0))

        # Search and add controls
        controls = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )
        controls.pack(fill="x", pady=(0, 18))

        self.search_entry = ctk.CTkEntry(
            controls,
            placeholder_text="Search products...",
            height=40,
            width=260
        )
        self.search_entry.pack(side="left")

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_products()
        )

        ctk.CTkButton(
            controls,
            text="+ Add Product",
            height=40,
            fg_color=COLORS["blue"],
            hover_color="#3475E0",
            command=lambda: self.open_product_dialog()
        ).pack(side="right")

        # Table container
        self.products_table = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color=COLORS["card"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.products_table.pack(fill="both", expand=True)

        self.refresh_products()

    # ---------------------------
    # REFRESH PRODUCT TABLE
    # ---------------------------

    def refresh_products(self):

        for widget in self.products_table.winfo_children():
            widget.destroy()

        # Table headings
        headers = [
            "ID", "Product", "Category",
            "Price", "Quantity", "Actions"
        ]

        for column, heading in enumerate(headers):

            self.products_table.grid_columnconfigure(
                column,
                weight=1 if column != 0 else 0
            )

            ctk.CTkLabel(
                self.products_table,
                text=heading,
                font=("Arial", 12, "bold"),
                text_color=COLORS["muted"]
            ).grid(
                row=0,
                column=column,
                padx=8,
                pady=15,
                sticky="w"
            )

        # Retrieve database records
        search = self.search_entry.get().strip()
        products = database.get_products(search)

        if not products:

            ctk.CTkLabel(
                self.products_table,
                text="No products found.",
                font=("Arial", 14),
                text_color=COLORS["muted"]
            ).grid(
                row=1,
                column=0,
                columnspan=6,
                pady=35
            )

            return

        # Display product rows
        for row, product in enumerate(products, start=1):

            values = [
                product["id"],
                product["name"],
                product["category"],
                f"₹{product['price']:,.2f}",
                product["quantity"]
            ]

            for column, value in enumerate(values):

                color = COLORS["text"]

                if column == 4:
                    if product["quantity"] == 0:
                        color = COLORS["red"]
                    elif product["quantity"] <= product["min_stock"]:
                        color = COLORS["orange"]

                ctk.CTkLabel(
                    self.products_table,
                    text=str(value),
                    font=("Arial", 12),
                    text_color=color
                ).grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=12,
                    sticky="w"
                )

            # Action buttons
            actions = ctk.CTkFrame(
                self.products_table,
                fg_color="transparent"
            )
            actions.grid(
                row=row,
                column=5,
                padx=5,
                pady=5
            )

            ctk.CTkButton(
                actions,
                text="Edit",
                width=55,
                height=28,
                fg_color="#354C70",
                hover_color="#45618A",
                command=lambda p=product: self.open_product_dialog(p)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions,
                text="Delete",
                width=60,
                height=28,
                fg_color="#743C42",
                hover_color="#9B414A",
                command=lambda pid=product["id"]: self.delete_product(pid)
            ).pack(side="left", padx=2)

    # ---------------------------
    # ADD / EDIT PRODUCT WINDOW
    # ---------------------------

    def open_product_dialog(self, product=None):

        import tkinter.messagebox as messagebox

        editing = product is not None

        dialog = ctk.CTkToplevel(self)

        dialog.title(
            "Edit Product" if editing else "Add Product"
        )
        dialog.geometry("420x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS["background"])
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Edit Product" if editing else "New Product",
            font=("Arial", 24, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=(25, 20))

        fields = {}

        field_data = [
            ("name", "Product Name"),
            ("category", "Category"),
            ("price", "Price (₹)"),
            ("quantity", "Quantity"),
            ("min_stock", "Minimum Stock")
        ]

        for key, label in field_data:

            ctk.CTkLabel(
                dialog,
                text=label,
                font=("Arial", 12),
                text_color=COLORS["muted"]
            ).pack(anchor="w", padx=40, pady=(8, 3))

            entry = ctk.CTkEntry(
                dialog,
                width=340,
                height=36,
                placeholder_text=label
            )
            entry.pack(padx=40)

            if editing:
                entry.insert(0, str(product[key]))

            elif key == "min_stock":
                entry.insert(0, "5")

            fields[key] = entry

        # Save operation
        def save_product():

            try:
                name = fields["name"].get()
                category = fields["category"].get()
                price = float(fields["price"].get())
                quantity = int(fields["quantity"].get())
                min_stock = int(fields["min_stock"].get())

                if not name.strip() or not category.strip():
                    raise ValueError("Name and category are required.")

                if not price >= 0 or quantity < 0 or min_stock < 0:
                    raise ValueError("Values cannot be negative.")

                if editing:

                    database.update_product(
                        product["id"],
                        name,
                        category,
                        price,
                        quantity,
                        min_stock
                    )

                else:

                    database.add_product(
                        name,
                        category,
                        price,
                        quantity,
                        min_stock
                    )

                dialog.destroy()
                self.refresh_products()

            except ValueError as error:

                messagebox.showerror(
                    "Invalid Input",
                    str(error),
                    parent=dialog
                )

            except Exception as error:

                messagebox.showerror(
                    "Database Error",
                    str(error),
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Save Product",
            width=340,
            height=42,
            fg_color=COLORS["blue"],
            hover_color="#3475E0",
            command=save_product
        ).pack(pady=25)

    # ---------------------------
    # DELETE PRODUCT
    # ---------------------------

    def delete_product(self, product_id):

        import tkinter.messagebox as messagebox

        confirm = messagebox.askyesno(
            "Delete Product",
            "Are you sure you want to delete this product?",
            parent=self
        )

        if confirm:

            database.delete_product(product_id)
            self.refresh_products()



# -------------------------------
# START APPLICATION
# -------------------------------

if __name__ == "__main__":

    app = MiniStockApp()
    app.mainloop()