import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry  # Import the DateEntry widget from tkcalendar

# Circular Queue class to manage itinerary orders
class CircularQueue:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.queue = [None] * max_size
        self.front = -1
        self.rear = -1

    def enqueue(self, username, phone, destination, activity, date):
        if (self.rear + 1) % self.max_size == self.front:
            return False  # Queue is full

        if self.front == -1:  # If the queue is empty
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.max_size

        self.queue[self.rear] = (username, phone, destination, activity, date)
        return True

    def dequeue(self):
        if self.front == -1:
            return None  # Queue is empty

        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.max_size

        return item

    def display(self):
        if self.front == -1:
            return []

        items = []
        i = self.front
        while i != self.rear:
            items.append(self.queue[i])
            i = (i + 1) % self.max_size
        items.append(self.queue[self.rear])
        return items


# Main Travel Itinerary App
class TravelItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Itinerary Planner")
        self.root.state("zoomed")  # Make the window maximized

        self.itinerary_manager = CircularQueue(max_size=5)  # Fixed size of 5 orders

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Travel Itinerary Planner", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        # Frame for Input Fields
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Username Entry
        tk.Label(input_frame, text="Username:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(input_frame, font=("Helvetica", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Phone Number Entry
        tk.Label(input_frame, text="Phone Number:", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = tk.Entry(input_frame, font=("Helvetica", 14))
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        # Destination Selection
        tk.Label(input_frame, text="Destination:", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.destination_var = tk.StringVar(value="Select Destination")
        self.destination_combobox = ttk.Combobox(
            input_frame, textvariable=self.destination_var, font=("Helvetica", 14), state="readonly"
        )
        self.destination_combobox["values"] = [
            "Volcanoes National Park",
            "Nyungwe Forest National Park",
            "Lake Kivu",
            "Akagera National Park",
            "Kigali City Tour",
        ]
        self.destination_combobox.grid(row=2, column=1, padx=10, pady=5)

        # Activity Selection
        tk.Label(input_frame, text="Activity:", font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.activity_var = tk.StringVar(value="Select Activity")
        self.activity_combobox = ttk.Combobox(
            input_frame, textvariable=self.activity_var, font=("Helvetica", 14), state="readonly"
        )
        self.activity_combobox["values"] = [
            "Leisuring",
            "Hiking",
            "Swimming",
            "Cultural Tour",
            "Wildlife Safari",
        ]
        self.activity_combobox.grid(row=3, column=1, padx=10, pady=5)

        # Date Selection with Date Picker
        tk.Label(input_frame, text="Date:", font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.date_picker = DateEntry(
            input_frame,
            font=("Helvetica", 14),
            date_pattern="yyyy-mm-dd"  # Ensures the date is formatted as YYYY-MM-DD
        )
        self.date_picker.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Add Itinerary Button
        add_button = tk.Button(
            button_frame,
            text="Add Itinerary",
            font=("Helvetica", 14),
            bg="lightgreen",
            fg="black",
            command=self.add_itinerary
        )
        add_button.grid(row=0, column=0, padx=10)

        # Remove Activity Button
        remove_button = tk.Button(
            button_frame,
            text="Remove Activity",
            font=("Helvetica", 14),
            bg="lightcoral",
            fg="black",
            command=self.remove_itinerary
        )
        remove_button.grid(row=0, column=1, padx=10)

        # Clear Fields Button
        clear_button = tk.Button(
            button_frame,
            text="Clear Fields",
            font=("Helvetica", 14),
            bg="lightblue",
            fg="black",
            command=self.clear_fields
        )
        clear_button.grid(row=0, column=2, padx=10)

        # Table to Display Itinerary
        self.tree = ttk.Treeview(
            self.root, columns=("Username", "Phone", "Destination", "Activity", "Date"), show="headings", height=10
        )
        self.tree.heading("Username", text="Username")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Activity", text="Activity")
        self.tree.heading("Date", text="Date")
        self.tree.column("Username", width=150, anchor="center")
        self.tree.column("Phone", width=150, anchor="center")
        self.tree.column("Destination", width=200, anchor="center")
        self.tree.column("Activity", width=200, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.pack(pady=20)

    def add_itinerary(self):
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        destination = self.destination_var.get()
        activity = self.activity_var.get()
        date = self.date_picker.get()

        if not username or not phone or destination == "Select Destination" or activity == "Select Activity":
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return

        if not self.itinerary_manager.enqueue(username, phone, destination, activity, date):
            response = messagebox.askyesno("Queue Full", "The itinerary is full. Remove the oldest entry?")
            if response:
                self.itinerary_manager.dequeue()
                self.itinerary_manager.enqueue(username, phone, destination, activity, date)
            else:
                return

        self.update_table()
        self.clear_fields()
        messagebox.showinfo("Itinerary Added", "Your itinerary has been added.")

    def remove_itinerary(self):
        if self.itinerary_manager.dequeue():
            self.update_table()
            messagebox.showinfo("Itinerary Removed", "The oldest itinerary has been removed.")
        else:
            messagebox.showerror("Remove Error", "No itineraries to remove!")

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for entry in self.itinerary_manager.display():
            self.tree.insert("", "end", values=entry)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.destination_var.set("Select Destination")
        self.activity_var.set("Select Activity")


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelItineraryApp(root)
    root.mainloop()
