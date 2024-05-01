# Import necessary libraries
from tkinter import *
import sqlite3
from tkinter import messagebox

# Create the main window
root = Tk()
root.title("Ramos_LA3")
root.geometry("620x520")
root.config(background="#d1d1e9")

# Function to add a product
def add_product():
    # Create a new window for adding a product
    add_window = Toplevel(root)
    add_window.title("Add Product")

    # Labels and Entry widgets for name, price, and quantity
    Label(add_window, text="Name:", font=("Courier", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(add_window, text="Price:", font=("Courier", 10, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    price_entry = Entry(add_window)
    price_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(add_window, text="Quantity:", font=("Courier", 10, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    quantity_entry = Entry(add_window)
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    # Function to add product details to the database
    def add_product_to_database():
        name = name_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()

        try:
            price = int(price)
            quantity = int(quantity)

            # Connect to the database and insert product details
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("INSERT INTO products (Name, Price, Quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
            conn.close()

        except ValueError:
            # Show error message if price or quantity is not numeric
            messagebox.showerror("Error", "Price and Quantity must be numeric.")

    # Button to execute the add_product_to_database function
    Button(add_window, text="Done", command=add_product_to_database, font=("Courier", 10, "bold")).grid(row=3, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

# Function to view products
def view_products():
    try:
        # Connect to the database and fetch all products
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        # Clear the listbox and insert product details
        listbox.delete(0, END)
        for product in products:
            formatted_price = "₱{}".format(int(product[2]))
            product_details = " {} Product: {} ---------- Price: {} ---------- Quantity: {}".format(product[0],product[1], formatted_price, product[3])
            listbox.insert(END, product_details)
    except sqlite3.Error as e:
        print("Error fetching products:", e)

# Function to update a product
def update_product():
    # Create a new window for updating a product
    update_window = Toplevel(root)
    update_window.title("Update Product")

    # Labels and Entry widgets for product ID, new name, new price, and new quantity
    Label(update_window, text="Product ID:", font=("Courier", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    id_entry = Entry(update_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(update_window, text="New Name:", font=("Courier", 10, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    new_name_entry = Entry(update_window)
    new_name_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(update_window, text="New Price:", font=("Courier", 10, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    new_price_entry = Entry(update_window)
    new_price_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(update_window, text="New Quantity:", font=("Courier", 10, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    new_quantity_entry = Entry(update_window)
    new_quantity_entry.grid(row=3, column=1, padx=10, pady=5)

    # Function to update product details in the database
    def update_product_in_database():
        product_id = id_entry.get()
        new_name = new_name_entry.get()
        new_price = new_price_entry.get()
        new_quantity = new_quantity_entry.get()

        try:
            product_id = int(product_id)
            new_price = int(new_price)
            new_quantity = int(new_quantity)

            # Connect to the database and update product details
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("UPDATE products SET Name=?, Price=?, Quantity=? WHERE ID=?", (new_name, new_price, new_quantity, product_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product updated successfully.")
            update_window.destroy()
        except ValueError:
            # Show error message if product ID, price, or quantity is not numeric
            messagebox.showerror("Error", "Product ID, Price, and Quantity must be numeric.")

    # Button to execute the update_product_in_database function
    Button(update_window, text="Update", command=update_product_in_database, font=("Courier", 10, "bold")).grid(row=4, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

# Function to remove a product
def remove_product():
    # Create a new window for removing a product
    remove_window = Toplevel(root)
    remove_window.title("Remove Product")
    remove_window.geometry("300x100")

    # Label and Entry widget for product ID
    Label(remove_window, text="Product ID:", font=("Courier", 10, "bold")).grid(row=0, column=0, padx=10, pady=5,
                                                                                sticky="e")
    id_entry = Entry(remove_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Function to get product details and remove from database
    def get_product_details():
        product_id = id_entry.get()
        try:
            product_id = int(product_id)
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("SELECT * FROM products WHERE ID=?", (product_id,))
            product = c.fetchone()
            conn.close()

            if product:
                confirmation = messagebox.askyesno("Confirmation", f"Do you want to remove product {product[1]}?")
                if confirmation:
                    conn = sqlite3.connect("inventory.db")
                    c = conn.cursor()
                    c.execute("DELETE FROM products WHERE ID=?", (product_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Product removed successfully.")
                    remove_window.destroy()
                    view_products()
            else:
                messagebox.showerror("Error", "Product not found.")
        except ValueError:
            messagebox.showerror("Error", "Product ID must be numeric.")

    # Function to remove all products from the database
    def remove_all_products():
        confirmation = messagebox.askyesno("Confirmation", "Do you want to remove all products?")
        if confirmation:
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("DELETE FROM products")
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "All products removed successfully.")
            remove_window.destroy()
            view_products()

    # Button to execute the get_product_details function
    Button(remove_window, text="Search", command=get_product_details, font=("Courier", 10, "bold")).grid(row=1,
                                                                                                         column=0,
                                                                                                         pady=10)
    # Button to execute the remove_all_products function
    Button(remove_window, text="Remove All Products", command=remove_all_products, font=("Courier", 10, "bold")).grid(row=1,
                                                                                                                    column=1,
                                                                                                                    pady=10)

# Function to exit the application
def exit():
    root.destroy()

# Label for the title of the application
lbl_title = Label(root,text="Inventory",
    font=("Courier", 15, "bold", "italic"),
    fg="#2b2c34",
    relief=SUNKEN,
    bd=5,
    padx=10,
    pady=5)
lbl_title.pack()

# Frame to contain the listbox
frame_main = Frame(root, width=510, height=350)
frame_main.pack()
frame_main.pack_propagate(False)

# Listbox to display products
listbox = Listbox(frame_main, height=19, width=80)
listbox.pack(padx=10, pady=(10,0))

# Create a scrollbar
scrollbar = Scrollbar(frame_main, orient="vertical", command=listbox.yview)
scrollbar.pack(side=RIGHT, fill="y")

# Link scrollbar to listbox
listbox.config(yscrollcommand=scrollbar.set)

# Frame for buttons
frame_2 = Frame(root, width=510, height=60)
frame_2.pack(pady=20)
frame_2.pack_propagate(False)

# Buttons for adding, viewing, updating, and removing products, and for exiting the application
btn_add_product = Button(frame_2, text="Add Product", command=add_product, font=("Arial", 10, "bold"))
btn_add_product.pack(side=LEFT, padx=12, pady=0)

btn_view_product =  Button(frame_2, text="View Products", command=view_products, font=("Arial", 10, "bold"))
btn_view_product.pack(side=LEFT, padx=12, pady=0)

btn_update =  Button(frame_2, text="Update Product", command=update_product, font=("Arial", 10, "bold"))
btn_update.pack(side=LEFT, padx=12, pady=0)

btn_remove =  Button(frame_2, text="Remove Product", command=remove_product, font=("Arial", 10, "bold"))
btn_remove.pack(side=LEFT, padx=12, pady=0)

btn_exit = Button(root, text="EXIT", command=exit, font=("Courier", 10, "bold"), height=1, width=8)
btn_exit.pack(pady=(0,8))

# Run the application
root.mainloop()