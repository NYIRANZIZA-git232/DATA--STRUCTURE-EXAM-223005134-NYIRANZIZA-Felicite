import tkinter as tk
from tkinter import ttk, messagebox

# TreeNode class to represent each node in the tree
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, node):
        if node in self.children:
            self.children.remove(node)

    def __str__(self):
        return self.name

# Travel itinerary app class with tree structure integration
class TravelItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Itinerary Planner")
        self.root.state("zoomed")  # Maximize the window at startup

        # Initialize the root of the tree (main destination)
        self.root_node = TreeNode("Travel Itinerary")

        # Predefined destinations
        self.volcanoes_node = TreeNode("Volcanoes National Park")
        self.nyungwe_node = TreeNode("Nyungwe Forest National Park")
        self.kivu_node = TreeNode("Lake Kivu")
        self.akagera_node = TreeNode("Akagera National Park")

        # Add predefined destinations to the root node
        self.root_node.add_child(self.volcanoes_node)
        self.root_node.add_child(self.nyungwe_node)
        self.root_node.add_child(self.kivu_node)
        self.root_node.add_child(self.akagera_node)

        # Set up the UI components
        self.create_widgets()

    def create_widgets(self):
        # Title label
        label = tk.Label(self.root, text="Personalized Travel Itinerary", font=("Helvetica", 24, 'bold'), bg="#f0f0f0")
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Destination selection
        self.destination_label = tk.Label(self.root, text="Destination:", font=("Helvetica", 18), bg="#f0f0f0")
        self.destination_label.grid(row=1, column=0, sticky="e", padx=10)

        self.destination_options = ["Volcanoes National Park", "Nyungwe Forest National Park", "Lake Kivu", "Akagera National Park"]
        self.destination_var = tk.StringVar()
        self.destination_var.set(self.destination_options[0])

        self.destination_combobox = ttk.Combobox(self.root, textvariable=self.destination_var, values=self.destination_options, font=("Helvetica", 18))
        self.destination_combobox.grid(row=1, column=1, pady=5, padx=10)

        # Activity selection
        self.activity_label = tk.Label(self.root, text="Activity:", font=("Helvetica", 18), bg="#f0f0f0")
        self.activity_label.grid(row=2, column=0, sticky="e", padx=10)

        self.activity_options = ["Leisuring", "Hiking", "Swimming", "Cultural Tour", "Wildlife Safari"]
        self.activity_var = tk.StringVar()
        self.activity_var.set(self.activity_options[0])

        self.activity_combobox = ttk.Combobox(self.root, textvariable=self.activity_var, values=self.activity_options, font=("Helvetica", 18))
        self.activity_combobox.grid(row=2, column=1, pady=5, padx=10)

        # Buttons for add and remove actions
        self.add_button = tk.Button(self.root, text="Add Activity", font=("Helvetica", 20), bg="#27ae60", fg="white", command=self.add_itinerary)
        self.add_button.grid(row=3, column=0, pady=20, sticky="ew", padx=10)

        self.remove_button = tk.Button(self.root, text="Remove Activity", font=("Helvetica", 20), bg="#e74c3c", fg="white", command=self.remove_itinerary)
        self.remove_button.grid(row=3, column=1, pady=20, sticky="ew", padx=10)

        # Itinerary listbox to display the tree structure
        self.itinerary_listbox = tk.Listbox(self.root, height=20, width=80, font=("Helvetica", 18))
        self.itinerary_listbox.grid(row=4, column=0, columnspan=2, pady=20)

        # Display tree button
        self.display_tree_button = tk.Button(self.root, text="Display Tree", font=("Helvetica", 20), bg="#3498db", fg="white", command=self.display_tree)
        self.display_tree_button.grid(row=5, column=0, columnspan=2, pady=20)

    def add_itinerary(self):
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        # Find the destination node in the tree
        destination_node = self.get_destination_node(destination)
        if not destination_node:
            messagebox.showerror("Error", "Destination not found.")
            return

        # Add the activity as a child of the destination node
        new_activity_node = TreeNode(activity)
        destination_node.add_child(new_activity_node)

        messagebox.showinfo("Success", f"Activity '{activity}' added to {destination}.")
        self.display_tree()

    def remove_itinerary(self):
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        # Find the destination node in the tree
        destination_node = self.get_destination_node(destination)
        if not destination_node:
            messagebox.showerror("Error", "Destination not found.")
            return

        # Find the activity node in the destination's children
        activity_node = self.get_activity_node(destination_node, activity)
        if not activity_node:
            messagebox.showerror("Error", "Activity not found.")
            return

        # Remove the activity node from the destination
        destination_node.remove_child(activity_node)

        messagebox.showinfo("Success", f"Activity '{activity}' removed from {destination}.")
        self.display_tree()

    def get_destination_node(self, name):
        for child in self.root_node.children:
            if child.name == name:
                return child
        return None

    def get_activity_node(self, destination_node, name):
        for child in destination_node.children:
            if child.name == name:
                return child
        return None

    def display_tree(self):
        self.itinerary_listbox.delete(0, tk.END)

        def traverse_tree(node, level=0):
            indentation = " " * (level * 4)
            self.itinerary_listbox.insert(tk.END, f"{indentation}{node.name}")
            for child in node.children:
                traverse_tree(child, level + 1)

        traverse_tree(self.root_node)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelItineraryApp(root)
    root.mainloop()
