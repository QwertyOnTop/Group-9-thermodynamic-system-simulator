#include <iostream>
#include <iomanip>
#include <cmath>
#include <string>
#include <vector>
#include <limits>
#include <fstream> // Include fstream for file handling

using namespace std;

// Constants
const double R = 8.314; // Ideal Gas Constant J/(mol*K)

// Structure to store process results
struct ProcessResult {
    string type;
    double workDone;
    double heatTransfer;
    double deltaInternalEnergy;
    double finalTemp;
    double finalPressure;
    double finalVolume;
};

// Function Prototypes
void displayHeader();
void displayMenu();
double getValidatedInput(string prompt, double min = 0.000001);
void processIsothermal(double n, double T, double V1, double V2);
void processIsobaric(double n, double P, double V1, double V2, double molarHeatCapacityV);
void processIsochoric(double n, double V, double T1, double T2, double molarHeatCapacityV);
void processAdiabatic(double n, double T1, double V1, double V2, double gamma);
void printResults(const ProcessResult& res);  // Declare the function to write results to CSV
void clearScreen();

// Main Function
int main() {
    int choice;
    bool running = true;

    while (running) {
        displayHeader();
        displayMenu();
        
        cout << "\nSelect a process (1-5): ";
        while (!(cin >> choice) || choice < 1 || choice > 5) {
            cout << "Invalid selection. Please enter 1-5: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }

        if (choice == 5) {
            running = false;
            cout << "Exiting Simulator. Thank you!" << endl;
            break;
        }

        // Common inputs for most processes
        double n = getValidatedInput("Enter number of moles (mol): ");
        double molarHeatCapacityV = 1.5 * R; // Default for Monatomic Ideal Gas (3/2 R)

        switch (choice) {
            case 1: { // Isothermal
                double T = getValidatedInput("Enter constant temperature (K): ");
                double V1 = getValidatedInput("Enter initial volume (m^3): ");
                double V2 = getValidatedInput("Enter final volume (m^3): ");
                processIsothermal(n, T, V1, V2);
                break;
            }
            case 2: { // Isobaric
                double P = getValidatedInput("Enter constant pressure (Pa): ");
                double V1 = getValidatedInput("Enter initial volume (m^3): ");
                double V2 = getValidatedInput("Enter final volume (m^3): ");
                processIsobaric(n, P, V1, V2, molarHeatCapacityV);
                break;
            }
            case 3: { // Isochoric
                double V = getValidatedInput("Enter constant volume (m^3): ");
                double T1 = getValidatedInput("Enter initial temperature (K): ");
                double T2 = getValidatedInput("Enter final temperature (K): ");
                processIsochoric(n, V, T1, T2, molarHeatCapacityV);
                break;
            }
            case 4: { // Adiabatic
                double T1 = getValidatedInput("Enter initial temperature (K): ");
                double V1 = getValidatedInput("Enter initial volume (m^3): ");
                double V2 = getValidatedInput("Enter final volume (m^3): ");
                double gamma = 1.67; // Default for monatomic gas
                processAdiabatic(n, T1, V1, V2, gamma);
                break;
            }
        }

        cout << "\nPress Enter to return to menu...";
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cin.get();
    
    }

    return 0;
}

// Implementation of calculation functions

void processIsothermal(double n, double T, double V1, double V2) {
    ProcessResult res;
    res.type = "Isothermal (Constant Temperature)";
    // Formula: W = nRT * ln(V2/V1)
    res.workDone = n * R * T * log(V2 / V1);
    res.deltaInternalEnergy = 0; // Delta U = 0 for isothermal ideal gas
    res.heatTransfer = res.workDone; 
    res.finalTemp = T;
    res.finalVolume = V2;
    res.finalPressure = (n * R * T) / V2;
    printResults(res); // Call printResults to write the data to CSV
}

void processIsobaric(double n, double P, double V1, double V2, double mcv) {
    ProcessResult res;
    res.type = "Isobaric (Constant Pressure)";
    double T1 = (P * V1) / (n * R);
    double T2 = (P * V2) / (n * R);
    double mcp = mcv + R; // Cp = Cv + R

    res.workDone = P * (V2 - V1);
    res.deltaInternalEnergy = n * mcv * (T2 - T1);
    res.heatTransfer = n * mcp * (T2 - T1);
    res.finalTemp = T2;
    res.finalPressure = P;
    res.finalVolume = V2;
    printResults(res); // Call printResults to write the data to CSV
}

void processIsochoric(double n, double V, double T1, double T2, double mcv) {
    ProcessResult res;
    res.type = "Isochoric (Constant Volume)";
    res.workDone = 0; // No volume change
    res.deltaInternalEnergy = n * mcv * (T2 - T1);
    res.heatTransfer = res.deltaInternalEnergy;
    res.finalTemp = T2;
    res.finalVolume = V;
    res.finalPressure = (n * R * T2) / V;
    printResults(res); // Call printResults to write the data to CSV
}

void processAdiabatic(double n, double T1, double V1, double V2, double gamma) {
    ProcessResult res;
    res.type = "Adiabatic (No Heat Exchange)";
    // T1*V1^(gamma-1) = T2*V2^(gamma-1)
    res.finalTemp = T1 * pow((V1 / V2), (gamma - 1));
    res.heatTransfer = 0;
    
    double mcv = R / (gamma - 1);
    res.deltaInternalEnergy = n * mcv * (res.finalTemp - T1);
    res.workDone = -res.deltaInternalEnergy;
    res.finalVolume = V2;
    res.finalPressure = (n * R * res.finalTemp) / V2;
    printResults(res); // Call printResults to write the data to CSV
}

// Utility Functions
double getValidatedInput(string prompt, double min) {
    double value;
    while (true) {
        cout << prompt;
        if (cin >> value && value >= min) {
            return value;
        } else {
            cout << "Invalid input. Please enter a positive value." << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }
}

// Function to print results to a .txt file and CSV file
void printResults(const ProcessResult& res) {
    // Open the text file in append mode
    ofstream file("results.txt", ios::app);
    
    // Check if file exists and is empty to determine if we need to write headers
    ifstream checkFile("results.csv");
    bool fileEmpty = !checkFile.good() || checkFile.peek() == EOF;
    checkFile.close();
    
    ofstream csvFile("results.csv", ios::app);

    // Check if the files are open successfully
    if (!file) {
        cout << "Error opening text file!" << endl;
        return;
    }
    if (!csvFile) {
        cout << "Error opening CSV file!" << endl;
        return;
    }

    // Write header to CSV if file is empty (only on first write)
    if (fileEmpty) {
        csvFile << "Process Type,Final Temperature,Final Pressure,Final Volume,Work Done (W),Heat Added (Q),Internal Energy Change (dU)" << endl;
    }

    // Write the results in CSV format
    csvFile << fixed << setprecision(2);
    csvFile << res.type << "," << res.finalTemp << "," << res.finalPressure << "," 
            << res.finalVolume << "," << res.workDone << "," << res.heatTransfer << "," 
            << res.deltaInternalEnergy << endl;
    csvFile.close();

    // Write the results in a human-readable format to the text file
    file << "----------------------------------------" << endl;
    file << "RESULTS: " << res.type << endl;
    file << "----------------------------------------" << endl;
    file << fixed << setprecision(2);
    file << "Final Temperature: " << res.finalTemp << " K" << endl;
    file << "Final Pressure:    " << res.finalPressure << " Pa" << endl;
    file << "Final Volume:      " << res.finalVolume << " m^3" << endl;
    file << "Work Done (W):     " << res.workDone << " J" << endl;
    file << "Heat Added (Q):    " << res.heatTransfer << " J" << endl;
    file << "Internal Energy Change (dU): " << res.deltaInternalEnergy << " J" << endl;
    file << "----------------------------------------" << endl;
    file << endl; // Add an empty line between results
    file.close();

    // Also print to console
    cout << "\n----------------------------------------" << endl;
    cout << " RESULTS: " << res.type << endl;
    cout << "----------------------------------------" << endl;
    cout << fixed << setprecision(2);
    cout << "Final Temperature: " << res.finalTemp << " K" << endl;
    cout << "Final Pressure:    " << res.finalPressure << " Pa" << endl;
    cout << "Final Volume:      " << res.finalVolume << " m^3" << endl;
    cout << "Work Done (W):     " << res.workDone << " J" << endl;
    cout << "Heat Added (Q):    " << res.heatTransfer << " J" << endl;
    cout << "Internal Energy Change (dU): " << res.deltaInternalEnergy << " J" << endl;
    cout << "----------------------------------------" << endl;
}

void displayHeader() {
    cout << "========================================" << endl;
    cout << "     THERMODYNAMIC SYSTEM SIMULATOR     " << endl;
    cout << "========================================" << endl;
}

void displayMenu() {
    cout << "1. Isothermal Process" << endl;
    cout << "2. Isobaric Process" << endl;
    cout << "3. Isochoric Process" << endl;
    cout << "4. Adiabatic Process" << endl;
    cout << "5. Exit Program" << endl;
}

void clearScreen() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}
