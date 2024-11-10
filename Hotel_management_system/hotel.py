import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk

# Define the Hotel Management System class
class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x600")  # Increased height for better visibility
        
        # Room data (room number, guest name, check-in status, and price)
        self.rooms = {
            101: {"guest_name": "", "status": "Available", "price": 100},
            102: {"guest_name": "", "status": "Available", "price": 150},
            103: {"guest_name": "", "status": "Available", "price": 120},
            104: {"guest_name": "", "status": "Available", "price": 200},
            105: {"guest_name": "", "status": "Available", "price": 180}
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Hotel Management System", font=("Helvetica", 18))
        title_label.pack(pady=20)
        
        # Room display
        self.room_status_label = tk.Label(self.root, text="Room Status", font=("Helvetica", 14))
        self.room_status_label.pack(pady=10)
        
        # Frame for room status display
        self.room_frame = tk.Frame(self.root)
        self.room_frame.pack(pady=10)
        
        # Create labels for each room status
        self.room_labels = {}
        for room_num, room_info in self.rooms.items():
            room_label = tk.Label(self.room_frame, text=f"Room {room_num}: {room_info['status']}", font=("Helvetica", 12))
            room_label.grid(row=room_num-101, column=0, padx=10, pady=5)
            self.room_labels[room_num] = room_label
        
        # Buttons
        check_in_button = tk.Button(self.root, text="Check-in Guest", font=("Helvetica", 12), command=self.check_in)
        check_in_button.pack(pady=10)
        
        check_out_button = tk.Button(self.root, text="Check-out Guest", font=("Helvetica", 12), command=self.check_out)
        check_out_button.pack(pady=10)
    
    def check_in(self):
        # Get room number and guest name from user
        room_num = simpledialog.askinteger("Check-in", "Enter Room Number (101-105):")
        if room_num not in self.rooms:
            messagebox.showerror("Error", "Invalid room number!")
            return
        if self.rooms[room_num]["status"] == "Occupied":
            messagebox.showerror("Error", "Room already occupied!")
            return
        
        guest_name = simpledialog.askstring("Check-in", "Enter Guest Name:", parent=self.root)
        if guest_name:
            # Show room price
            room_price = self.rooms[room_num]["price"]
            
            # Create new window for food service and price display
            check_in_window = tk.Toplevel(self.root)
            check_in_window.title(f"Check-in - Room {room_num}")
            check_in_window.geometry("400x300")  # Larger window for better input display
            
            # Room price label
            price_label = tk.Label(check_in_window, text=f"Room Price: ${room_price}", font=("Helvetica", 14))
            price_label.pack(pady=20)
            
            # Food service checkbox
            food_service_var = tk.IntVar()
            food_service_checkbox = tk.Checkbutton(check_in_window, text="Include Food Service ($30)", variable=food_service_var, font=("Helvetica", 12))
            food_service_checkbox.pack(pady=10)
            
            # Confirm button
            def confirm_check_in():
                food_service = 30 if food_service_var.get() else 0
                total_bill = room_price + food_service
                self.rooms[room_num]["guest_name"] = guest_name
                self.rooms[room_num]["status"] = "Occupied"
                self.update_room_status()
                messagebox.showinfo("Success", f"Guest {guest_name} checked-in to Room {room_num}. Total Bill: ${total_bill}")
                check_in_window.destroy()
            
            confirm_button = tk.Button(check_in_window, text="Confirm Check-in", font=("Helvetica", 12), command=confirm_check_in)
            confirm_button.pack(pady=20)
    
    def check_out(self):
        # Get room number from user
        room_num = simpledialog.askinteger("Check-out", "Enter Room Number (101-105):")
        if room_num not in self.rooms:
            messagebox.showerror("Error", "Invalid room number!")
            return
        if self.rooms[room_num]["status"] == "Available":
            messagebox.showerror("Error", "Room is already vacant!")
            return
        # Confirm checkout
        guest_name = self.rooms[room_num]["guest_name"]
        bill = self.calculate_bill(room_num)
        confirm = messagebox.askyesno("Confirm Check-out", f"Guest {guest_name} will be checked out. Bill: ${bill}\nDo you want to proceed?")
        if confirm:
            self.rooms[room_num]["guest_name"] = ""
            self.rooms[room_num]["status"] = "Available"
            self.update_room_status()
            messagebox.showinfo("Success", f"Guest {guest_name} checked-out from Room {room_num}")
    
    def calculate_bill(self, room_num):
        # Basic calculation based on room number
        if room_num == 101:
            return 100
        elif room_num == 102:
            return 150
        elif room_num == 103:
            return 120
        elif room_num == 104:
            return 200
        elif room_num == 105:
            return 180
        return 0
    
    def update_room_status(self):
        # Update room status display
        for room_num, room_info in self.rooms.items():
            status = room_info["status"]
            self.room_labels[room_num].config(text=f"Room {room_num}: {status}")

# Create the main window and pass it to the HotelManagementSystem class
root = tk.Tk()
hotel_system = HotelManagementSystem(root)
root.mainloop()
