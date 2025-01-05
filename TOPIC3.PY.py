import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Define the Itinerary Item class
class ItineraryItem:
    def __init__(self, destination, activity, date):
        self.destination = destination
        self.activity = activity
        self.date = date

    def __str__(self):
        return f"{self.activity} in {self.destination} on {self.date}"

# Define the Travel Itinerary class to manage the list
class TravelItinerary:
    def __init__(self):
        self.itinerary = []  # List to hold itinerary items

    def add_itinerary_item(self, item):
        self.itinerary.append(item)

    def remove_itinerary_item(self, activity):
        self.itinerary = [item for item in self.itinerary if item.activity != activity]

    def get_itinerary_items(self):
        return [str(item) for item in self.itinerary]

# Create the main app class with tkinter UI
class TravelItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Itinerary Planner")
        self.root.state("zoomed")  # Maximize the window at startup
        self.itinerary_manager = TravelItinerary()
        
        # Set up the UI components
        self.create_widgets()

    def create_widgets(self):
        # Labels
        label = tk.Label(self.root, text="Personalized Travel Itinerary", font=("Helvetica", 24, 'bold'), bg="#f0f0f0")
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Fixed Destinations (ComboBox)
        self.destination_label = tk.Label(self.root, text="Destination:", font=("Helvetica", 18), bg="#f0f0f0")
        self.destination_label.grid(row=1, column=0, sticky="e", padx=10)

        self.destination_options = ["Select the Destination", "Volcanoes National Park", "Nyungwe Forest National Park", "Lake Kivu", "Akagera National Park"]
        self.destination_var = tk.StringVar()
        self.destination_var.set(self.destination_options[0])  # Default value is "Select the Destination"

        self.destination_combobox = ttk.Combobox(self.root, textvariable=self.destination_var, values=self.destination_options, font=("Helvetica", 18))
        self.destination_combobox.grid(row=1, column=1, pady=5, padx=10)

        # Fixed Activities (ComboBox) with "Leisuring" as default
        self.activity_label = tk.Label(self.root, text="Activity:", font=("Helvetica", 18), bg="#f0f0f0")
        self.activity_label.grid(row=2, column=0, sticky="e", padx=10)

        self.activity_options = ["Select the Activity", "Leisuring", "Hiking", "Swimming", "Cultural Tour", "Wildlife Safari", "Other"]
        self.activity_var = tk.StringVar()
        self.activity_var.set(self.activity_options[0])  # Default value is "Select the Activity"

        self.activity_combobox = ttk.Combobox(self.root, textvariable=self.activity_var, values=self.activity_options, font=("Helvetica", 18))
        self.activity_combobox.grid(row=2, column=1, pady=5, padx=10)

        # Entry for custom activity if "Other" is selected
        self.custom_activity_label = tk.Label(self.root, text="Custom Activity:", font=("Helvetica", 18), bg="#f0f0f0")
        self.custom_activity_label.grid(row=3, column=0, sticky="e", padx=10)
        self.custom_activity_entry = tk.Entry(self.root, font=("Helvetica", 18))
        self.custom_activity_entry.grid(row=3, column=1, pady=5, padx=10)

        # Date Row (with dropdown for predefined dates)
        self.date_label = tk.Label(self.root, text="Date:", font=("Helvetica", 18), bg="#f0f0f0")
        self.date_label.grid(row=4, column=0, sticky="e", padx=10)

        self.date_options = ["Select the Date", "2025-01-10", "2025-01-11", "2025-01-12", "2025-01-13", "Custom"]
        self.date_var = tk.StringVar()
        self.date_var.set(self.date_options[0])  # Default value is "Select the Date"

        self.date_combobox = ttk.Combobox(self.root, textvariable=self.date_var, values=self.date_options, font=("Helvetica", 18))
        self.date_combobox.grid(row=4, column=1, pady=5, padx=10)

        # Entry for custom date if "Custom" is selected
        self.custom_date_label = tk.Label(self.root, text="Custom Date (YYYY-MM-DD):", font=("Helvetica", 18), bg="#f0f0f0")
        self.custom_date_label.grid(row=5, column=0, sticky="e", padx=10)
        self.custom_date_entry = tk.Entry(self.root, font=("Helvetica", 18))
        self.custom_date_entry.grid(row=5, column=1, pady=5, padx=10)

        # Buttons for Add Itinerary, View Itinerary, and Remove Activity (on the same line)
        self.add_button = tk.Button(self.root, text="Add Itinerary", font=("Helvetica", 20), bg="#27ae60", fg="white", command=self.add_itinerary)
        self.view_button = tk.Button(self.root, text="View Itinerary", font=("Helvetica", 20), bg="#3498db", fg="white", command=self.view_itinerary)
        self.remove_button = tk.Button(self.root, text="Remove Activity", font=("Helvetica", 20), bg="#e74c3c", fg="white", command=self.remove_itinerary)

        # Place the buttons in the same row, each taking 1/3 of the space
        self.add_button.grid(row=6, column=0, pady=20, sticky="ew", padx=10)
        self.view_button.grid(row=6, column=1, pady=20, sticky="ew", padx=10)
        self.remove_button.grid(row=6, column=2, pady=20, sticky="ew", padx=10)

        # Itinerary Listbox to display added itinerary items
        self.itinerary_listbox = tk.Listbox(self.root, height=10, width=80, font=("Helvetica", 18), selectmode=tk.SINGLE)
        self.itinerary_listbox.grid(row=7, column=0, columnspan=3, pady=20)

        # Update the visibility of the custom date entry based on the selected date
        self.date_var.trace("w", self.update_custom_date_visibility)

    def update_custom_date_visibility(self, *args):
        selected_date = self.date_var.get()
        if selected_date == "Custom":
            self.custom_date_label.grid(row=5, column=0, sticky="e", padx=10)
            self.custom_date_entry.grid(row=5, column=1, pady=5, padx=10)
        else:
            self.custom_date_label.grid_forget()
            self.custom_date_entry.grid_forget()

    def add_itinerary(self):
        # Get input data
        destination = self.destination_var.get()  # Get selected destination
        activity = self.activity_var.get()  # Get selected activity
        if activity == "Other":
            activity = self.custom_activity_entry.get()  # Use custom activity if selected
        date = self.date_var.get()  # Get selected date
        if date == "Custom":
            date = self.custom_date_entry.get()  # Use custom date if selected

        # Create itinerary item and add to the manager
        new_item = ItineraryItem(destination, activity, date)
        self.itinerary_manager.add_itinerary_item(new_item)

        # Clear the entries
        self.activity_var.set(self.activity_options[0])  # Reset to "Select the Activity"
        self.date_var.set(self.date_options[0])  # Reset to "Select the Date"
        self.custom_activity_entry.delete(0, tk.END)
        self.custom_date_entry.delete(0, tk.END)

        messagebox.showinfo("Itinerary Added", "Your itinerary item has been added successfully!")

    def view_itinerary(self):
        # Clear the listbox and show updated itinerary items
        self.itinerary_listbox.delete(0, tk.END)
        for item in self.itinerary_manager.get_itinerary_items():
            self.itinerary_listbox.insert(tk.END, item)

    def remove_itinerary(self):
        selected_item_index = self.itinerary_listbox.curselection()
        if selected_item_index:
            selected_item_text = self.itinerary_listbox.get(selected_item_index)
            # Extract activity name from the selected item string
            activity_name = selected_item_text.split(" in ")[0]  # Get the activity name part

            # Remove the item from the itinerary manager
            self.itinerary_manager.remove_itinerary_item(activity_name)

            # Refresh the listbox
            self.view_itinerary()
            messagebox.showinfo("Itinerary Removed", f"The activity '{activity_name}' has been removed.")
        else:
            messagebox.showwarning("No Selection", "Please select an activity to remove.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelItineraryApp(root)
    root.mainloop()
