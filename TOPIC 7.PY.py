import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# TreeNode class to represent each node in the tree
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []  # Activities under this destination

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, node):
        if node in self.children:
            self.children.remove(node)

    def __str__(self):
        return self.name

# Activity class to represent an activity with a priority
class Activity:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __str__(self):
        return f"{self.name} (Priority: {self.priority})"

# Travel itinerary app class with tree structure integration
class TravelItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Itinerary Planner")
        self.root.state("zoomed")  # Make the window maximized

        # Initialize the root of the tree (main destination)
        self.root_node = TreeNode("Travel Itinerary")

        # Predefined destinations with activities and priorities
        self.volcanoes_node = TreeNode("Volcanoes National Park")
        self.volcanoes_node.add_child(Activity("Leisuring", 1))
        self.volcanoes_node.add_child(Activity("Hiking", 2))
        self.volcanoes_node.add_child(Activity("Swimming", 3))

        self.nyungwe_node = TreeNode("Nyungwe Forest National Park")
        self.nyungwe_node.add_child(Activity("Leisuring", 2))
        self.nyungwe_node.add_child(Activity("Hiking", 1))

        self.kivu_node = TreeNode("Lake Kivu")
        self.kivu_node.add_child(Activity("Leisuring", 3))
        self.kivu_node.add_child(Activity("Swimming", 1))

        self.akagera_node = TreeNode("Akagera National Park")
        self.akagera_node.add_child(Activity("Wildlife Safari", 1))
        self.akagera_node.add_child(Activity("Cultural Tour", 2))

        # Add predefined destinations to the root node
        self.root_node.add_child(self.volcanoes_node)
        self.root_node.add_child(self.nyungwe_node)
        self.root_node.add_child(self.kivu_node)
        self.root_node.add_child(self.akagera_node)

        # Set up the UI components
        self.create_widgets()

    def create_widgets(self):
        # Title label
        label = tk.Label(self.root, text="Personalized Travel Itinerary", font=("Helvetica", 24, 'bold'))
        label.grid(row=0, column=0, columnspan=3, pady=20)

        # Destination Dropdown (Combobox)
        self.destination_label = tk.Label(self.root, text="Destination:", font=("Helvetica", 18))
        self.destination_label.grid(row=1, column=0, sticky="e", padx=10)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(self.root, textvariable=self.destination_var,
                                                  values=["Select the Destination", 
                                                          "Volcanoes National Park", 
                                                          "Nyungwe Forest National Park", 
                                                          "Lake Kivu", 
                                                          "Akagera National Park"], 
                                                  state="readonly")
        self.destination_combobox.set("Select the Destination")  # Default value
        self.destination_combobox.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        self.destination_combobox.bind("<<ComboboxSelected>>", self.update_activity_menu)

        # Activity Dropdown (Combobox)
        self.activity_label = tk.Label(self.root, text="Activity:", font=("Helvetica", 18))
        self.activity_label.grid(row=2, column=0, sticky="e", padx=10)

        self.activity_var = tk.StringVar()
        self.activity_combobox = ttk.Combobox(self.root, textvariable=self.activity_var,
                                               values=["Select the Activity"], 
                                               state="readonly")
        self.activity_combobox.set("Select the Activity")  # Default value
        self.activity_combobox.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        # Add Activity Button with background color change
        self.add_button = tk.Button(self.root, text="Add Activity", font=("Helvetica", 20), 
                                    command=self.add_itinerary, bg="#4CAF50", fg="white")
        self.add_button.grid(row=3, column=0, pady=20, sticky="ew", padx=10)

        # Remove Activity Button with background color change
        self.remove_button = tk.Button(self.root, text="Remove Activity", font=("Helvetica", 20), 
                                       command=self.remove_itinerary, bg="#f44336", fg="white")
        self.remove_button.grid(row=3, column=1, pady=20, sticky="ew", padx=10)

        # Treeview for displaying the itinerary like a table
        self.tree = ttk.Treeview(self.root, columns=("Destination", "Activity"), show="headings", height=15)
        self.tree.grid(row=4, column=0, columnspan=3, pady=20, padx=10, sticky="nsew")

        # Add scrollbar to the Treeview
        self.tree_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=4, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # Define columns and headings
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Activity", text="Activity")
        self.tree.column("Destination", width=300)
        self.tree.column("Activity", width=300)

        # Display Tree Button with background color change
        self.display_tree_button = tk.Button(self.root, text="Display Selected Tree", font=("Helvetica", 20), 
                                             command=self.display_tree, bg="#2196F3", fg="white")
        self.display_tree_button.grid(row=5, column=0, columnspan=3, pady=20, sticky="ew")

        # Sort by Priority Button with background color change
        self.sort_button = tk.Button(self.root, text="Sort by Priority", font=("Helvetica", 20), 
                                     command=self.sort_by_priority, bg="#FFC107", fg="white")
        self.sort_button.grid(row=6, column=0, columnspan=3, pady=20, sticky="ew")

        # Configure grid to expand
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=0)

    def update_activity_menu(self, event):
        # Clear the current activity options
        self.activity_var.set("Select the Activity")
        
        # Get the destination node
        selected_destination = self.destination_var.get()
        destination_node = self.get_destination_node(selected_destination)
        if destination_node:
            activities = [activity.name for activity in destination_node.children]
            self.activity_combobox["values"] = activities
            self.activity_combobox.set("Select the Activity")  # Reset the activity combobox to default
        else:
            messagebox.showerror("Error", "Selected destination does not exist.")

    def add_itinerary(self):
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        if destination == "Select the Destination" or activity == "Select the Activity":
            messagebox.showerror("Error", "Please select both a destination and an activity.")
            return

        # Find the destination node in the tree
        destination_node = self.get_destination_node(destination)
        if not destination_node:
            messagebox.showerror("Error", "Destination not found.")
            return

        # Add the activity as a child of the destination node
        new_activity_node = Activity(activity, 1)  # Priority can be added dynamically if needed
        destination_node.add_child(new_activity_node)

        messagebox.showinfo("Success", f"Activity '{activity}' added to {destination}.")
        self.display_tree()  # Update the tree display

    def remove_itinerary(self):
        destination = self.destination_var.get()
        activity = self.activity_var.get()

        if destination == "Select the Destination" or activity == "Select the Activity":
            messagebox.showerror("Error", "Please select both a destination and an activity.")
            return

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
        self.display_tree()  # Update the tree display

    def get_destination_node(self, name):
        # Traverse the root node's children to find the matching destination node
        for child in self.root_node.children:
            if child.name == name:
                return child
        return None

    def get_activity_node(self, destination_node, name):
        # Traverse the destination node's children to find the matching activity node
        for child in destination_node.children:
            if child.name == name:
                return child
        return None

    def display_tree(self):
        # Show the current hierarchy in the tree structure
        self.tree.delete(*self.tree.get_children())

        # Get the selected destination
        selected_destination = self.destination_var.get()
        if selected_destination == "Select the Destination":
            messagebox.showerror("Error", "Please select a destination first.")
            return

        # Find the destination node
        destination_node = self.get_destination_node(selected_destination)
        if destination_node:
            for activity in destination_node.children:
                self.tree.insert("", "end", values=(destination_node.name, activity.name))
        else:
            messagebox.showerror("Error", "Destination not found.")

    def sort_by_priority(self):
        # Sort the activities under each destination by their priority using Counting Sort
        for destination_node in self.root_node.children:
            destination_node.children = self.counting_sort_activities(destination_node.children)
        
        self.display_tree()  # Update the tree display after sorting

    def counting_sort_activities(self, activities):
        # Find the maximum priority value to set the range of counts
        max_priority = max(activity.priority for activity in activities)
        count = [0] * (max_priority + 1)  # Counting array for priorities
        output = [None] * len(activities)

        # Count the occurrences of each priority
        for activity in activities:
            count[activity.priority] += 1

        # Modify the count array to store the actual position of the activity in output array
        for i in range(1, len(count)):
            count[i] += count[i - 1]

        # Place the activities in the correct position in the output array
        for activity in reversed(activities):
            output[count[activity.priority] - 1] = activity
            count[activity.priority] -= 1

        return output

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelItineraryApp(root)
    root.mainloop()
