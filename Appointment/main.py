import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json
import os
from idcard import generate_id_card


# --- Appointment Class ---
class Appointment:
    def __init__(self, name, date_time, reason):
        self.name = name
        self.date_time = date_time
        self.reason = reason

    def to_dict(self):
        return {
            "name": self.name,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M"),
            "reason": self.reason
        }

    @staticmethod
    def from_dict(data):
        return Appointment(
            data["name"],
            datetime.datetime.strptime(data["date_time"], "%Y-%m-%d %H:%M"),
            data["reason"]
        )

# --- Scheduler App ---
class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Scheduler")
        self.appointments = []
        self.load_appointments()

        # --- Input Form ---
        self.name_var = tk.StringVar()
        self.reason_var = tk.StringVar()
        self.datetime_var = tk.StringVar()

        tk.Label(root, text="Name").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Date & Time (YYYY-MM-DD HH:MM)").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable=self.datetime_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Reason").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.reason_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(root, text="Add Appointment", command=self.add_appointment).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Treeview to Display Appointments ---
        self.tree = ttk.Treeview(root, columns=("Name", "DateTime", "Reason"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("DateTime", text="Date & Time")
        self.tree.heading("Reason", text="Reason")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10)

        tk.Button(root, text="Delete Selected", command=self.delete_appointment).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Create ID Card", command=self.create_id_card).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.refresh_tree()

    # --- Add Appointment ---
    def add_appointment(self):
        name = self.name_var.get().strip()
        reason = self.reason_var.get().strip()
        date_str = self.datetime_var.get().strip()

        if not name or not reason or not date_str:
            messagebox.showwarning("Missing Fields", "All fields are required.")
            return

        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date Format", "Please use YYYY-MM-DD HH:MM")
            return

        # --- Check for Duplicates ---
        if any(a.name == name and a.date_time == dt for a in self.appointments):
            messagebox.showwarning("Duplicate Entry", "This appointment already exists.")
            return

        new_appt = Appointment(name, dt, reason)
        self.appointments.append(new_appt)
        self.save_appointments()
        self.refresh_tree()

        # Clear form
        self.name_var.set("")
        self.datetime_var.set("")
        self.reason_var.set("")

    # --- Delete Selected Appointment ---
    def delete_appointment(self):
        selected_item = self.tree.selection()
        if selected_item:
            idx = self.tree.index(selected_item)
            del self.appointments[idx]
            self.save_appointments()
            self.refresh_tree()

    # --- Refresh Tree View ---
    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for appt in sorted(self.appointments, key=lambda x: x.date_time):
            self.tree.insert("", "end", values=(appt.name, appt.date_time.strftime("%Y-%m-%d %H:%M"), appt.reason))

    # --- Save Appointments to JSON ---
    def save_appointments(self):
        with open("appointments.json", "w") as f:
            json.dump([a.to_dict() for a in self.appointments], f, indent=4)

    # --- Load Appointments from JSON ---
    def load_appointments(self):
        if os.path.exists("appointments.json"):
            with open("appointments.json", "r") as f:
                try:
                    data = json.load(f)
                    self.appointments = [Appointment.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load appointments file. File may be corrupted.")
                    self.appointments = []
    # --- Create ID Card for Selected ---
    def create_id_card(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an appointment to generate ID card.")
            return

        idx = self.tree.index(selected_item)
        appt = self.appointments[idx]
        appt_data = appt.to_dict()

        # Save with a custom name like "id_card_<name>.png"
        filename = f"id_card_{appt.name.replace(' ', '_')}.png"
        generate_id_card(appt_data, filename)

        messagebox.showinfo("ID Card Created", f"ID card saved as {filename}")

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
