import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and parse the .txt file
def parse_results(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Initialize lists to hold data
    process_types = []
    final_temps = []
    final_pressures = []
    work_done = []
    heat_transfer = []
    delta_internal_energy = []

    # Parse the file line by line
    process_data = {}
    for line in lines:
        line = line.strip()  # Remove leading/trailing spaces
        if line.startswith("RESULTS:"):
            # If a new result starts, save the old one if exists
            if process_data:
                process_types.append(process_data['type'])
                final_temps.append(process_data['final_temp'])
                final_pressures.append(process_data['final_pressure'])
                work_done.append(process_data['work_done'])
                heat_transfer.append(process_data['heat_transfer'])
                delta_internal_energy.append(process_data['delta_internal_energy'])
            
            # Initialize a new result
            process_data = {'type': line.replace('RESULTS: ', ''), 'final_temp': None, 'final_pressure': None, 'work_done': None, 'heat_transfer': None, 'delta_internal_energy': None}
        
        # Extract values from the lines
        elif line.startswith("Final Temperature:"):
            process_data['final_temp'] = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Final Pressure:"):
            process_data['final_pressure'] = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Work Done (W):"):
            process_data['work_done'] = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Heat Added (Q):"):
            process_data['heat_transfer'] = float(line.split(":")[1].strip().split()[0])
        elif line.startswith("Internal Energy Change (dU):"):
            process_data['delta_internal_energy'] = float(line.split(":")[1].strip().split()[0])

    # Append the last result after exiting the loop
    if process_data:
        process_types.append(process_data['type'])
        final_temps.append(process_data['final_temp'])
        final_pressures.append(process_data['final_pressure'])
        work_done.append(process_data['work_done'])
        heat_transfer.append(process_data['heat_transfer'])
        delta_internal_energy.append(process_data['delta_internal_energy'])

    return process_types, final_temps, final_pressures, work_done, heat_transfer, delta_internal_energy

# Function to generate visualizations
def generate_visualizations(process_types, final_temps, final_pressures, work_done, heat_transfer):
    # Visualization 1: Plot Work Done vs Heat Transfer
    plt.figure(figsize=(10, 6))
    plt.scatter(work_done, heat_transfer)
    plt.xlabel('Work Done (J)')
    plt.ylabel('Heat Transfer (J)')
    plt.title('Work Done vs Heat Transfer')
    plt.grid(True)
    plt.show()

    # Visualization 2: Plot Final Temperature vs Final Pressure
    plt.figure(figsize=(10, 6))
    plt.plot(final_temps, final_pressures, marker='o', linestyle='-', color='b')
    plt.xlabel('Final Temperature (K)')
    plt.ylabel('Final Pressure (Pa)')
    plt.title('Final Temperature vs Final Pressure')
    plt.grid(True)
    plt.show()

    # Visualization 3: Bar Plot for Process Type Frequency
    plt.figure(figsize=(10, 6))
    process_type_counts = {process: process_types.count(process) for process in set(process_types)}
    plt.bar(process_type_counts.keys(), process_type_counts.values())
    plt.xlabel('Process Type')
    plt.ylabel('Frequency')
    plt.title('Frequency of Each Process Type')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    # Visualization 4: Histogram of Work Done
    plt.figure(figsize=(10, 6))
    plt.hist(work_done, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Work Done (J)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Work Done')
    plt.grid(True)
    plt.show()

    # Visualization 5: Box Plot for Final Pressure
    plt.figure(figsize=(10, 6))
    sns.boxplot(final_pressures, color='lightcoral')
    plt.xlabel('Final Pressure (Pa)')
    plt.title('Box Plot of Final Pressure')
    plt.show()

# Function to handle the file selection and visualization
def on_file_select():
    # Open a file dialog to choose the results.txt file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Parse the file
        process_types, final_temps, final_pressures, work_done, heat_transfer, delta_internal_energy = parse_results(file_path)

        # Generate the visualizations
        generate_visualizations(process_types, final_temps, final_pressures, work_done, heat_transfer)

# Create the main window using Tkinter
window = tk.Tk()
window.title("Thermodynamic Data Visualizer")

# Add a label to give instructions to the user
label = tk.Label(window, text="Select the results.txt file to visualize thermodynamic data:")
label.pack(pady=10)

# Create a button to trigger the file selection and visualization
btn_generate = tk.Button(window, text="Generate Visualization", command=on_file_select)
btn_generate.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
