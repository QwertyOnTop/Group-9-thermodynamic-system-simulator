import tkinter as tk
from tkinter import messagebox

def save_input():
    try:
        # Open the file in write mode
        with open("input_values.txt", "w") as f:
            # Write the input values to the file
            f.write(f"n={n_entry.get()}\n")
            f.write(f"T={T_entry.get()}\n")
            f.write(f"V1={V1_entry.get()}\n")
            f.write(f"V2={V2_entry.get()}\n")
            f.write(f"P={P_entry.get()}\n")
            f.write(f"gamma={gamma_entry.get()}\n")
        
        messagebox.showinfo("Success", "Values saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI window
root = tk.Tk()
root.title("Thermodynamic Simulator Inputs")

# Create labels and entry widgets for user input
tk.Label(root, text="Number of moles (n):").grid(row=0, column=0)
n_entry = tk.Entry(root)
n_entry.grid(row=0, column=1)

tk.Label(root, text="Temperature (T) in K:").grid(row=1, column=0)
T_entry = tk.Entry(root)
T_entry.grid(row=1, column=1)

tk.Label(root, text="Initial Volume (V1) in m^3:").grid(row=2, column=0)
V1_entry = tk.Entry(root)
V1_entry.grid(row=2, column=1)

tk.Label(root, text="Final Volume (V2) in m^3:").grid(row=3, column=0)
V2_entry = tk.Entry(root)
V2_entry.grid(row=3, column=1)

tk.Label(root, text="Pressure (P) in Pa:").grid(row=4, column=0)
P_entry = tk.Entry(root)
P_entry.grid(row=4, column=1)

tk.Label(root, text="Gamma (γ) for Adiabatic Process:").grid(row=5, column=0)
gamma_entry = tk.Entry(root)
gamma_entry.grid(row=5, column=1)

# Add a Save button
save_button = tk.Button(root, text="Save Values", command=save_input)
save_button.grid(row=6, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
