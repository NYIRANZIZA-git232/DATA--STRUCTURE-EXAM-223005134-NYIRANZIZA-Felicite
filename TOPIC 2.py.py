import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For using the Combobox
import re  # Regular expression module for phone validation
import heapq  # For implementing MinHeap functionality

# BinarySearchTree Class
class BinaryTreeNode:
    def __init__(self, key, destination, name, phone):
        self.left = None
        self.right = None
        self.key = key  # Rating or popularity (based on cost)
        self.destination = destination
        self.name = name
        self.phone = phone

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, destination, name, phone):
        if self.root is None:
            self.root = BinaryTreeNode(key, destination, name, phone)
        else:
            self._insert_recursive(self.root, key, destination, name, phone)

    def _insert_recursive(self, node, key, destination, name, phone):
        if key < node.key:
            if node.left is None:
                node.left = BinaryTreeNode(key, destination, name, phone)
            else:
                self._insert_recursive(node.left, key, destination, name, phone)
        else:
            if node.right is None:
                node.right = BinaryTreeNode(key, destination, name, phone)
            else:
                self._insert_recursive(node.right, key, destination, name, phone)

    def inorder(self):
        passengers = []
        self._inorder_recursive(self.root, passengers)
        return passengers

    def _inorder_recursive(self, node, passengers):
        if node:
            self._inorder_recursive(node.left, passengers)
            passengers.append((node.name, node.phone, node.destination, node.key))  # name, phone, destination, cost
            self._inorder_recursive(node.right, passengers)

# MinHeap Class
class MinHeap:
    def __init__(self):
        self.heap = []

    def add(self, cost, destination, name, phone):
        heapq.heappush(self.heap, (cost, destination, name, phone))

    def get_cheapest(self):
        if self.heap:
            return self.heap[0][2], self.heap[0][3], self.heap[0][1], self.heap[0][0]  # name, phone, destination, cost
        return None, None, None, None

    def show_all(self):
        return [f"{name} ({phone}) - {dest} - {cost} RWF" for cost, dest, name, phone in self.heap]

# GUI with Tkinter
class TravelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personalized Travel Itinerary App")
        
        # Set fullscreen but keep window controls visible
        self.root.attributes('-fullscreen', True)  # Make window fullscreen
        self.root.bind("<F11>", self.toggle_fullscreen)  # Toggle fullscreen mode on F11 press
        self.root.bind("<Escape>", self.end_fullscreen)  # Exit fullscreen on Escape

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_width = int(self.screen_width * 0.5)  # 50% of screen width
        self.window_height = int(self.screen_height * 0.75)  # Adjust the height to keep elements visible
        self.root.geometry(f"{self.window_width}x{self.window_height}")  # Set window size to 50% width
        self.root.configure(bg='#dfe6e9')  # Background color

        # Initialize BinarySearchTree and MinHeap
        self.bst = BinarySearchTree()
        self.min_heap = MinHeap()

        # Predefined destinations and their base costs
        self.destinations = {
            "Volcanoes National Park": 400000,
            "Akagera National Park": 250000,
            "Nyungwe Forest National Park": 120000,
            "Lake Kivu": 50000,
            "Kigali Genocide Memorial": None,  # No predefined cost, can be entered
            "Butare (Museum)": 150000,
        }

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg='#dfe6e9')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame for Input Section (Left side)
        self.input_frame = tk.Frame(self.main_frame, bg='#dfe6e9')
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Frame for Output Section (Right side)
        self.output_frame = tk.Frame(self.main_frame, bg='#dfe6e9')
        self.output_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nw", rowspan=5)

        # Close Button
        self.close_button = tk.Button(self.root, text="Close", font=("Arial", 14), command=self.close_app, bg="red", fg="white", bd=0, padx=10, pady=5)
        self.close_button.place(x=self.window_width - 80, y=10)  # Position it at the top-right corner

        # Heading Label
        self.title_label = tk.Label(self.input_frame, text="Welcome to Your Travel App", font=("Helvetica", 20, 'bold'), bg='#dfe6e9')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n", padx=10)

        # Passenger Name Entry
        self.name_label = tk.Label(self.input_frame, text="Passenger Name:", font=("Arial", 16), bg='#dfe6e9')
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.name_entry = tk.Entry(self.input_frame, font=("Arial", 16), width=25, bd=2, relief="solid")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Phone Number Entry
        self.phone_label = tk.Label(self.input_frame, text="Phone Number:", font=("Arial", 16), bg='#dfe6e9')
        self.phone_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.phone_entry = tk.Entry(self.input_frame, font=("Arial", 16), width=25, bd=2, relief="solid")
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10)

        # Destination Combobox
        self.dest_label = tk.Label(self.input_frame, text="Destination Name:", font=("Arial", 16), bg='#dfe6e9')
        self.dest_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.dest_var = tk.StringVar()
        self.dest_var.set(list(self.destinations.keys())[0])  # Default to first destination
        self.dest_combobox = ttk.Combobox(self.input_frame, textvariable=self.dest_var, values=list(self.destinations.keys()), state="readonly", width=22, font=("Arial", 16))
        self.dest_combobox.grid(row=3, column=1, padx=10, pady=10)
        self.dest_combobox.bind("<<ComboboxSelected>>", self.update_cost)

        # Cost Entry Field
        self.cost_label = tk.Label(self.input_frame, text="Cost (RWF):", font=("Arial", 16), bg='#dfe6e9')
        self.cost_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.cost_entry = tk.Entry(self.input_frame, font=("Arial", 16), width=25, bd=2, relief="solid")
        self.cost_entry.grid(row=4, column=1, padx=10, pady=10)

        # Buttons Frame
        self.button_frame = tk.Frame(self.input_frame, bg='#dfe6e9')
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Add to BST
        self.add_bst_button = tk.Button(self.button_frame, text="Add to BST (Sorted by Rating)", font=("Arial", 16), command=self.add_to_bst, width=30, bg="#FF9800", fg="white", bd=0, padx=10, pady=10)
        self.add_bst_button.grid(row=0, column=0, padx=10, pady=10)

        # Add to MinHeap
        self.add_heap_button = tk.Button(self.button_frame, text="Add to MinHeap (Optional)", font=("Arial", 16), command=self.add_to_min_heap, width=30, bg="#4CAF50", fg="white", bd=0, padx=10, pady=10)
        self.add_heap_button.grid(row=1, column=0, padx=10, pady=10)

        # Show Sorted Destinations
        self.show_sorted_button = tk.Button(self.button_frame, text="Show Sorted Destinations", font=("Arial", 16), command=self.show_sorted, width=30, bg="#9C27B0", fg="white", bd=0, padx=10, pady=10)
        self.show_sorted_button.grid(row=2, column=0, padx=10, pady=10)

        # Show Cheapest Destinations
        self.show_cheapest_button = tk.Button(self.button_frame, text="Show Cheapest Destination (MinHeap)", font=("Arial", 16), command=self.show_cheapest, width=30, bg="#3F51B5", fg="white", bd=0, padx=10, pady=10)
        self.show_cheapest_button.grid(row=3, column=0, padx=10, pady=10)

        # Output Label for Sorted Destinations
        self.output_label = tk.Label(self.output_frame, text="Sorted Destinations:", font=("Arial", 16, "bold"), bg='#dfe6e9')
        self.output_label.grid(row=0, column=0, pady=10, sticky="w")

        # Output Subtitle for Cheapest Destinations
        self.output_subtitle = tk.Label(self.output_frame, text="Cheapest Destination (MinHeap):", font=("Arial", 16, "bold"), bg='#dfe6e9')
        self.output_subtitle.grid(row=1, column=0, pady=10, sticky="w")

        # Output Display Area for Sorted Destinations
        self.output_listbox = tk.Listbox(self.output_frame, width=50, height=10, font=("Arial", 14), bd=2, relief="solid")
        self.output_listbox.grid(row=2, column=0, padx=10, pady=10)

        # Output Display Area for Cheapest Destinations
        self.cheapest_listbox = tk.Listbox(self.output_frame, width=50, height=5, font=("Arial", 14), bd=2, relief="solid")
        self.cheapest_listbox.grid(row=3, column=0, padx=10, pady=10)

    def close_app(self):
        """ Close the application """
        self.root.quit()

    def toggle_fullscreen(self, event=None):
        """ Toggle fullscreen mode on F11 press """
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def end_fullscreen(self, event=None):
        """ Exit fullscreen on Escape key press """
        self.root.attributes('-fullscreen', False)
        self.root.geometry(f"{self.window_width}x{self.window_height}")  # Return to normal size

    def update_cost(self, *args):
        # Update the cost entry field when a destination is selected
        dest = self.dest_var.get()
        if self.destinations[dest] is None:
            self.cost_entry.delete(0, tk.END)  # Clear the field for custom cost input
            self.cost_entry.config(state="normal")  # Enable the cost entry field for custom input
        else:
            self.cost_entry.delete(0, tk.END)  # Clear the field
            self.cost_entry.insert(0, str(self.destinations[dest]))  # Insert the predefined cost
            self.cost_entry.config(state="normal")  # Allow editing

    def validate_phone_number(self, phone_number):
        # Check if phone number is exactly 10 digits and starts with 078, 079, 072, or 073
        phone_pattern = r"^(078|079|072|073)\d{7}$"
        return bool(re.match(phone_pattern, phone_number)) and len(phone_number) == 10

    def add_to_bst(self):
        # Function to add a destination to BST (sorted by rating)
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        destination = self.dest_var.get()
        cost = self.cost_entry.get()

        if not name or not phone or not destination:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not self.validate_phone_number(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        try:
            cost = float(cost)
        except ValueError:
            messagebox.showerror("Error", "Invalid cost value.")
            return

        self.bst.insert(cost, destination, name, phone)
        messagebox.showinfo("Success", f"{destination} added to BST.")

    def add_to_min_heap(self):
        # Function to add a destination to MinHeap
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        destination = self.dest_var.get()
        cost = self.cost_entry.get()

        if not name or not phone or not destination:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not self.validate_phone_number(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        try:
            cost = float(cost)
        except ValueError:
            messagebox.showerror("Error", "Invalid cost value.")
            return

        self.min_heap.add(cost, destination, name, phone)
        messagebox.showinfo("Success", f"{destination} added to MinHeap.")

    def show_sorted(self):
        # Show sorted destinations from BST in the listbox
        sorted_destinations = self.bst.inorder()
        self.output_listbox.delete(0, tk.END)
        for name, phone, dest, cost in sorted_destinations:
            self.output_listbox.insert(tk.END, f"{name} ({phone}) - {dest} - {cost} RWF")

    def show_cheapest(self):
        # Show the cheapest destination from MinHeap in the listbox
        name, phone, dest, cost = self.min_heap.get_cheapest()
        self.cheapest_listbox.delete(0, tk.END)
        if name:
            self.cheapest_listbox.insert(tk.END, f"{name} ({phone}) - {dest} - {cost} RWF")
        else:
            self.cheapest_listbox.insert(tk.END, "No destinations in MinHeap.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()
