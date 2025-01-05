import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview

# Doubly Linked List to manage orders
class DoublyLinkedList:
    class Node:
        def __init__(self, destination, activity, username, phone):
            self.destination = destination
            self.activity = activity
            self.username = username
            self.phone = phone
            self.next = None
            self.prev = None

    def __init__(self, max_size):
        self.head = None
        self.tail = None
        self.size = 0
        self.max_size = max_size

    def insert_order(self, destination, activity, username, phone):
        if self.size == self.max_size:
            print("Maximum order limit reached. Cannot add more orders.")
            return False  # No space for new orders

        new_node = self.Node(destination, activity, username, phone)

        if self.tail is None:  # Empty list
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1
        print(f"Order added: {destination} - {activity}")
        return True

    def remove_order(self, destination, activity):
        current = self.head
        while current:
            if current.destination == destination and current.activity == activity:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:  # Removing the head
                    self.head = current.next
                if current == self.tail:  # Removing the tail
                    self.tail = current.prev
                self.size -= 1
                print(f"Order removed: {destination} - {activity}")
                return True
            current = current.next

        print("Order not found.")
        return False

    def is_full(self):
        return self.size == self.max_size


# Travel itinerary app with fixed number of orders
class TravelItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Itinerary Planner")
        self.max_orders = 5  # Fixed number of orders
        self.order_list = DoublyLinkedList(self.max_orders)
        self.create_widgets()

        # Maximize the window without hiding buttons
        self.root.state("zoomed")

    def create_widgets(self):
        # Username and Phone Number Entry
        self.username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 18))
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        self.phone_label = tk.Label(self.root, text="Phone Number:", font=("Helvetica", 18))
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)

        self.phone_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.phone_entry.grid(row=1, column=1, pady=10, padx=10)

        # Labels and comboboxes for destination and activity
        self.destination_label = tk.Label(self.root, text="Destination:", font=("Helvetica", 18))
        self.destination_label.grid(row=2, column=0, padx=10, pady=10)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(self.root, textvariable=self.destination_var, state="readonly", 
                                                  font=("Helvetica", 16))
        self.destination_combobox['values'] = ("Select the Destination", "Volcanoes National Park", 
                                                "Nyungwe Forest National Park", "Lake Kivu", "Akagera National Park")
        self.destination_combobox.set("Select the Destination")
        self.destination_combobox.grid(row=2, column=1, pady=10, padx=10)

        self.activity_label = tk.Label(self.root, text="Activity:", font=("Helvetica", 18))
        self.activity_label.grid(row=3, column=0, padx=10, pady=10)

        self.activity_var = tk.StringVar()
        self.activity_combobox = ttk.Combobox(self.root, textvariable=self.activity_var, state="readonly", 
                                              font=("Helvetica", 16))
        self.activity_combobox['values'] = ("Select the Activity", "Leisure", "Hiking", "Swimming", 
                                            "Cultural Tour", "Wildlife Safari")
        self.activity_combobox.set("Select the Activity")
        self.activity_combobox.grid(row=3, column=1, pady=10, padx=10)

        # Buttons with custom background color
        self.add_button = tk.Button(self.root, text="Add Order", font=("Helvetica", 20), command=self.add_order, 
                                    bg="#4CAF50", fg="white")  # Green button with white text
        self.add_button.grid(row=4, column=0, pady=20, sticky="ew", padx=10)

        self.remove_button = tk.Button(self.root, text="Remove Order", font=("Helvetica", 20), command=self.remove_order, 
                                       bg="#F44336", fg="white")  # Red button with white text
        self.remove_button.grid(row=4, column=1, pady=20, sticky="ew", padx=10)

        self.display_button = tk.Button(self.root, text="Display Orders", font=("Helvetica", 20), command=self.display_orders, 
                                        bg="#2196F3", fg="white")  # Blue button with white text
        self.display_button.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew", padx=10)

        # Treeview for displaying the orders as a table
        self.itinerary_label = tk.Label(self.root, text="Itinerary (Orders):", font=("Helvetica", 18))
        self.itinerary_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.treeview = ttk.Treeview(self.root, columns=("Destination", "Activity", "Username", "Phone"), show="headings", height=5)
        self.treeview.heading("Destination", text="Destination")
        self.treeview.heading("Activity", text="Activity")
        self.treeview.heading("Username", text="Username")
        self.treeview.heading("Phone", text="Phone")
        self.treeview.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def add_order(self):
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        if self.order_list.is_full():
            messagebox.showerror("Error", "Cannot add more orders. Maximum limit reached.")
            return

        if destination == "Select the Destination" or activity == "Select the Activity":
            messagebox.showerror("Error", "Please select both a destination and an activity.")
            return

        if not username or not phone:
            messagebox.showerror("Error", "Please enter both username and phone number.")
            return

        success = self.order_list.insert_order(destination, activity, username, phone)
        if success:
            messagebox.showinfo("Success", f"Order added: {destination} - {activity}")
        self.display_orders()  # Update the displayed orders

    def remove_order(self):
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        if destination == "Select the Destination" or activity == "Select the Activity":
            messagebox.showerror("Error", "Please select both a destination and an activity.")
            return

        success = self.order_list.remove_order(destination, activity)
        if success:
            messagebox.showinfo("Success", f"Order removed: {destination} - {activity}")
        else:
            messagebox.showerror("Error", "Order not found.")
        self.display_orders()  # Update the displayed orders

    def display_orders(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        current = self.order_list.head
        if not current:
            self.treeview.insert("", "end", values=("No orders", "", "", ""))
            return

        while current:
            self.treeview.insert("", "end", values=(current.destination, current.activity, current.username, current.phone))
            current = current.next


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelItineraryApp(root)
    root.mainloop()
