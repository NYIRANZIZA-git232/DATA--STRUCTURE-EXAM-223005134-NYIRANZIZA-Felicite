#include <iostream>     // For standard input and output
#include <cstring>      // For handling character arrays (like VIN, vehicleType)

using namespace std;    // To avoid prefixing standard functions with std::

/* Struct to store applicant's information */
struct Applicant {
    char vin[17];           // Vehicle Identification Number (max 16 characters + '\0')
    int age;                // Age of the applicant
    char vehicleType[10];   // Type of vehicle (e.g., "car", "truck")
};

/* Struct to store premium brackets based on age */
struct Bracket {
    float minAge, maxAge;   // Age range
    float premium;          // Premium amount for that age range
};

/* Abstract base class for quote engines */
class QuoteEngine {
protected:
    Bracket* brackets;      // Dynamic array to store brackets
    int bracketCount;       // Number of brackets

public:
    QuoteEngine() : brackets(nullptr), bracketCount(0) {}  // Constructor initializing members

    virtual ~QuoteEngine() {       // Virtual destructor to delete dynamic memory
        delete[] brackets;         // Free memory for brackets array
    }

    // Function to add a new age bracket
    void addBracket(const Bracket& b) {
        Bracket* newBrackets = new Bracket[bracketCount + 1];  // Create larger array
        for (int i = 0; i < bracketCount; ++i)                 // Copy existing brackets
            newBrackets[i] = brackets[i];
        newBrackets[bracketCount] = b;                         // Add new bracket
        delete[] brackets;                                     // Delete old array
        brackets = newBrackets;                                // Point to new array
        bracketCount++;                                        // Increase count
    }

    // Function to remove a bracket at a specific index
    void removeBracket(int index) {
        if (index < 0 || index >= bracketCount) {              // Check valid index
            cout << "Invalid bracket index!" << endl;
            return;
        }
        Bracket* newBrackets = new Bracket[bracketCount - 1];  // Create smaller array
        for (int i = 0, j = 0; i < bracketCount; ++i) {
            if (i != index) {                                  // Skip the index to remove
                newBrackets[j++] = brackets[i];                // Copy remaining brackets
            }
        }
        delete[] brackets;                                     // Delete old array
        brackets = newBrackets;                                // Update pointer
        bracketCount--;                                        // Decrease count
    }

    // Function to list all brackets
    void listBrackets() const {
        if (bracketCount == 0) {                               // If no brackets exist
            cout << "No brackets defined.\n";
            return;
        }
        for (int i = 0; i < bracketCount; ++i) {               // Loop through brackets
            cout << i << ". Age Range: [" << brackets[i].minAge << "-" << brackets[i].maxAge
                 << "], Premium: frw" << brackets[i].premium << endl;
        }
    }

    // Pure virtual function to calculate premium (to be implemented in derived classes)
    virtual float calculate(const Applicant* applicant) = 0;
};

/* Basic quote engine - returns the normal premium */
class BasicQuoteEngine : public QuoteEngine {
public:
    float calculate(const Applicant* applicant) override {     // Override the virtual method
        Bracket* ptr = brackets;                               // Pointer to brackets array
        for (int i = 0; i < bracketCount; ++i, ++ptr) {        // Loop through brackets
            if (applicant->age >= ptr->minAge && applicant->age <= ptr->maxAge) {
                return ptr->premium;                           // Return matched premium
            }
        }
        return -1.0f;                                           // No matching bracket
    }
};

/* Premium quote engine - returns 1.5x of the normal premium */
class PremiumQuoteEngine : public QuoteEngine {
public:
    float calculate(const Applicant* applicant) override {     // Override the virtual method
        Bracket* ptr = brackets;                               // Pointer to brackets array
        for (int i = 0; i < bracketCount; ++i, ++ptr) {        // Loop through brackets
            if (applicant->age >= ptr->minAge && applicant->age <= ptr->maxAge) {
                return ptr->premium * 1.5f;                     // Return 1.5x of premium
            }
        }
        return -1.0f;                                           // No matching bracket
    }
};

// Display menu options
void showMenu() {
    cout << "\n=== Insurance Quote Engine Menu ===\n";
    cout << "1. Add Bracket\n";
    cout << "2. Remove Bracket\n";
    cout << "3. List Brackets\n";
    cout << "4. Input Applicant and Calculate Premium\n";
    cout << "5. Exit\n";
    cout << "Choose an option: ";
}

/* Main function - program entry point */
int main() {
    QuoteEngine** engines = new QuoteEngine*[2];     // Create array of 2 QuoteEngine pointers
    engines[0] = new BasicQuoteEngine();             // First is BasicQuoteEngine
    engines[1] = new PremiumQuoteEngine();           // Second is PremiumQuoteEngine

    int choice;                                      // User menu choice
    do {
        showMenu();                                  // Show menu
        cin >> choice;                               // Read user input
        cin.ignore();                                // Clear newline from buffer

        switch (choice) {
            case 1: {                                // Add bracket
                Bracket b;
                cout << "Enter Min Age: ";
                cin >> b.minAge;
                cout << "Enter Max Age: ";
                cin >> b.maxAge;
                cout << "Enter Premium: ";
                cin >> b.premium;
                engines[0]->addBracket(b);           // Add to Basic Engine
                engines[1]->addBracket(b);           // Add to Premium Engine
                cout << "Bracket added to both engines.\n";
                break;
            }
            case 2: {                                // Remove bracket
                int index;
                cout << "Enter index to remove: ";
                cin >> index;
                engines[0]->removeBracket(index);    // Remove from both engines
                engines[1]->removeBracket(index);
                cout << "Bracket removed from both engines.\n";
                break;
            }
            case 3: {                                // List brackets
                cout << "--- Brackets in Basic Engine ---\n";
                engines[0]->listBrackets();
                cout << "--- Brackets in Premium Engine ---\n";
                engines[1]->listBrackets();
                break;
            }
            case 4: {                                // Enter applicant and calculate premium
                Applicant applicant;
                cout << "Enter VIN (16 chars max): ";
                cin.ignore();                        // Clear leftover newline
                cin.getline(applicant.vin, 17);      // Read VIN
                cout << "Enter Age: ";
                cin >> applicant.age;                // Read age
                cout << "Enter Vehicle Type: ";
                cin.ignore();                        // Clear newline
                cin.getline(applicant.vehicleType, 10); // Read vehicle type

                for (int i = 0; i < 2; ++i) {         // Loop through both engines
                    float premium = engines[i]->calculate(&applicant);
                    if (premium == -1.0f)
                        cout << "Engine " << i << ": No matching bracket for age.\n";
                    else
                        cout << "Engine " << i << " Premium: frw" << premium << endl;
                }
                break;
            }
            case 5:
                cout << "Exiting...\n";              // Exit message
                break;
            default:
                cout << "Invalid choice.\n";         // Handle invalid input
        }

    } while (choice != 5);                           // Continue until user exits

    // Clean up dynamically allocated memory
    for (int i = 0; i < 2; ++i)
        delete engines[i];
    delete[] engines;

    return 0;                                        // End of program
}
