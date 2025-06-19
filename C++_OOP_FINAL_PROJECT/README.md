INSURANCE QUOTE ENGINE SYSTEM
-----------------------------

The purpose of this project is to design a dynamic insurance quote engine system that calculates insurance premiums based on an applicant's age. Using C++ object-oriented programming, the system introduces structs to store applicant and age-based bracket information. An abstract class QuoteEngine provides a common interface for calculating premiums, with two derived classes (BasicQuoteEngine and PremiumQuoteEngine) implementing specific pricing strategies. The project demonstrates key concepts such as inheritance, polymorphism, and dynamic memory management. Users can interact with the system via a menu to add, remove, or list age brackets and compute premiums. Pointer arithmetic is used to efficiently search for matching age ranges. The result is a flexible and modular system that mimics real-world insurance logic. It serves as a practical application of advanced C++ principles in solving real business problems

ASSIGNED TASK
-------------
For this project, I was assigned to create a C++ program that calculates insurance premiums based on a person's age and vehicle information. I started by defining two structures: one called Applicant to store details like VIN, age, and vehicle type, and another called Bracket to hold the premium rates based on age ranges. I used dynamic memory to manage the brackets. Then, I created an abstract class called QuoteEngine with a virtual calculate() function. From that, I made two classes: BasicQuoteEngine for normal premiums and PremiumQuoteEngine for 1.5× premiums. This helped me apply inheritance and polymorphism. I also used pointer arithmetic to scan through the bracket array efficiently. Finally, I added menu options so the user can add, remove, or list brackets and calculate premiums easily.

HOW IT WAS WORKED
------------------
To complete this project, I started by creating two structures: one for the applicant's details and another for storing premium brackets based on age. I then built an abstract base class called QuoteEngine to serve as the main interface for calculating premiums. Inside this class, I included functions to add, remove, and list premium brackets dynamically using memory allocation. After that, I created two derived classes: BasicQuoteEngine, which returns the normal premium, and PremiumQuoteEngine, which multiplies the premium by 1.5. Both classes override the calculate() function, demonstrating the use of inheritance and polymorphism. I used pointer arithmetic to loop through the bracket array for efficient matching based on age. Finally, I implemented a menu system so the user can interact with the program by adding or removing brackets and calculating premiums for any applicant entered. The program was tested and successfully gave correct outputs based on user inputs.

IMPLEMENTED CODE
----------------
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

    return 0;                                     // end of program
}
