#restaurant management system
import tkinter as tk 
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class order_management:
    def __init__(self,root):
        self.root = root
        self.root.title("restaurant management app")
        self.root.geometry("800x600")

        self.menu_items = {
            "french fries":2,
            "burger":5,
            "chicken nuggets":4,
            "apple pie":1,
            "pizza":8,
            "sprite":2,
        }
        self.exchange_rate = 82
        self.setup_background()
        frame = ttk.Frame(self.root,padding=20)
        frame.place(relx=0.5,rely=0.5,anchor="center")
        ttk.Label(frame,text="restaurant order management",font=("Arial",20,"bold")).grid(row=0,columnspan=3,pady=10)
        self.menu_labels = {}
        self.menu_quantities = {}
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):

            label = ttk.Label(
            frame,
            text=f"{item} (${price})",
            font=("Arial", 12)
            )
        label.grid(row=i,column = 0,padx=10,pady=5,sticky="w")
        self.menu_labels[item] = label
        entry = ttk.Entry(frame, width=5)
        entry.grid(row=i, column=1, padx=10, pady=5)
        self.menu_quantities[item] = entry
        ttk.Label(
        frame,
        text="Currency:",
        font=("Arial", 12)
        ).grid(row=len(self.menu_items)+1, column=0, pady=10)
        self.currency_var = tk.StringVar(value="USD")

        currency_dropdown = ttk.Combobox(
        frame,
        textvariable=self.currency_var,
        values=("USD", "INR"),
        state="readonly",
        width=10
        )
        currency_dropdown.grid(
        row=len(self.menu_items)+1,
        column=1,
        pady=10
        )

        self.currency_var.trace_add("write", self.update_menu_prices)

        # Order button
        ttk.Button(
        frame,
        text="Place Order",
        command=self.place_order
        ).grid(
        row=len(self.menu_items)+2,
        columnspan=3,
        pady=15
        )


    def setup_background(self):
        self.canvas = tk.Canvas(self.root,width = 800,height = 600)
        self.canvas.pack(fill="both",expand=True)
        bg_image = Image.open("food.jpg")
        self.background_image = ImageTk.PhotoImage(bg_image)

        self.canvas.create_image(0,0,anchor = tk.NW,image = self.background_image)
    def update_menu_prices(self,*args):
        currency = self.currency_var.get()
        if currency == "INR":
            symbol = "₹"
            rate = self.exchange_rate
        else:
            symbol = "$"
            rate = 1 
        for item,label in self.menu_labels.items():
            price = self.menu_items[item]*rate
            label.config(
            text=f"{item} ({symbol}{price:.2f})"
            )
    def place_order(self):
        total_cost = 0
        currency = self.currency_var.get()
        if currency == "INR":
            symbol = "₹"
            rate = self.exchange_rate
        else:
            symbol = "$"
            rate = 1 
        order_summary = "order summary\n"
        for item, entry in self.menu_quantities.items():
            try:
                quantity = int(entry.get())
            except ValueError:
                quantity = 0
            if quantity>0:
                price = self.menu_items[item]*rate
                cost = quantity*price
                total_cost+=cost
                order_summary += (
                f"{item}: {quantity} x "
                f"{symbol}{price:.2f} = "
                f"{symbol}{cost:.2f}\n"
                )
        if total_cost>0:
            order_summary += (
            f"\nTotal Cost: "
            f"{symbol}{total_cost:.2f}"
            )
            messagebox.showinfo("order placed",order_summary)
            for entry in self.menu_quantities.values():
                entry.delete(0,tk.END)
        else:
            messagebox.showerror("error","please order at least one item")
if __name__ == "__main__":
    root = tk.Tk()
    app = order_management(root)
    root.mainloop()