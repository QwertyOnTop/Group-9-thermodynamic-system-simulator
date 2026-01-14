import matplotlib.pyplot as plt
import seaborn as sns

# Lists to hold the extracted data
process_types = []
work_done = []
heat_transfer = []
delta_internal_energy = []
final_temp = []
final_pressure = []
final_volume = []

# Read the text file and extract data
with open('results.txt', 'r') as file:
    lines = file.readlines()

    # Loop through the lines and extract relevant datapython
    for line in lines:
        # Check if the line contains data about a process type
        if "RESULTS:" in line:
            # Extract process type (e.g., Isothermal)
            process_type = line.split(":")[1].strip()
            process_types.append(process_type)
        elif "Final Temperature" in line:
            # Extract Final Temperature
            temp = float(line.split(":")[1].strip().replace("K", ""))
            final_temp.append(temp)
        elif "Final Pressure" in line:
            # Extract Final Pressure
            pressure = float(line.split(":")[1].strip().replace("Pa", ""))
            final_pressure.append(pressure)
        elif "Final Volume" in line:
            # Extract Final Volume
            volume = float(line.split(":")[1].strip().replace("m^3", ""))
            final_volume.append(volume)
        elif "Work Done" in line:
            # Extract Work Done
            work = float(line.split(":")[1].strip().replace("J", ""))
            work_done.append(work)
        elif "Heat Added" in line:
            # Extract Heat Added (Heat Transfer)
            heat = float(line.split(":")[1].strip().replace("J", ""))
            heat_transfer.append(heat)
        elif "Internal Energy Change" in line:
            # Extract Internal Energy Change
            delta = float(line.split(":")[1].strip().replace("J", ""))
            delta_internal_energy.append(delta)

# Convert extracted data to lists (they should have the same length)
print("Process Types: ", process_types)
print("Work Done: ", work_done)
print("Heat Transfer: ", heat_transfer)
print("Delta Internal Energy: ", delta_internal_energy)
print("Final Temperature: ", final_temp)
print("Final Pressure: ", final_pressure)
print("Final Volume: ", final_volume)

# Visualization Example 1: Scatter Plot of Work Done vs Heat Transfer
plt.figure(figsize=(10, 6))
plt.scatter(work_done, heat_transfer, c='blue', marker='o')
plt.xlabel('Work Done (J)')
plt.ylabel('Heat Transfer (J)')
plt.title('Work Done vs Heat Transfer')
plt.grid(True)
plt.show()

# Visualization Example 2: Line Plot for Final Temperature vs Final Pressure
plt.figure(figsize=(10, 6))
plt.plot(final_temp, final_pressure, marker='o', linestyle='-', color='b')
plt.xlabel('Final Temperature (K)')
plt.ylabel('Final Pressure (Pa)')
plt.title('Final Temperature vs Final Pressure')
plt.grid(True)
plt.show()

# Visualization Example 3: Bar Plot of Frequency of Process Types
plt.figure(figsize=(10, 6))
process_counts = {process: process_types.count(process) for process in set(process_types)}
plt.bar(process_counts.keys(), process_counts.values(), color='lightcoral')
plt.xlabel('Process Type')
plt.ylabel('Count')
plt.title('Frequency of Each Process Type')
plt.xticks(rotation=45, ha='right')
plt.show()

# Visualization Example 4: Histogram of Work Done
plt.figure(figsize=(10, 6))
plt.hist(work_done, bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Work Done (J)')
plt.ylabel('Frequency')
plt.title('Histogram of Work Done')
plt.grid(True)
plt.show()

# Visualization Example 5: Heatmap of Final Temperature vs Final Pressure
plt.figure(figsize=(10, 6))
plt.hexbin(final_temp, final_pressure, gridsize=30, cmap='YlGnBu')
plt.colorbar(label='Counts in bin')
plt.xlabel('Final Temperature (K)')
plt.ylabel('Final Pressure (Pa)')
plt.title('Heatmap of Final Temperature vs Final Pressure')
plt.show()