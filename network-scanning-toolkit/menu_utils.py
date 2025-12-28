"""
Author: Patrick Godinez
File Name: menu_utils.py
Assignment 2

    Description:
        This class contains several functions for displaying menu options, accepting user input
        and validating choices.
"""

from datetime import datetime, timezone

def get_menu_choice(menu_items):
    """
    Displays a numbered menu, checks and accepts users input, and returns the user selection
    """
    menu_title = "CyberSecurity Toolkit"
    print(f"\n{menu_title}\n" + "-" * len(menu_title))

    #display menu options with numbered labels
    counter = 1
    for item in menu_items:
        print(str(counter) + ". " + item)
        counter += 1
    
    #input loop until correct choice is made may rework later
    while True:
        choice = input("Enter the number of your selection: ")

        #here we check to make sure input is a valid digit and within the range of choices
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(menu_items):
                return menu_items[choice - 1]
        #print the error message and try again 
        print("Invalid choice, please try again.")

def make_record(host, port, proto, state, name="N/A", reason="N/A", product="N/A", version="N/A", cpe="N/A"):
    now = datetime.now(timezone.utc)
    #creates a record dictionary with UTC timestamp
    return {
        "UTC Date": now.strftime("%Y-%m-%d"),
        "UTC Time": now.strftime("%H:%M:%S"),
        "host": host,
        "protocol": proto,
        "port": port,
        "name": name,
        "reason": reason,
        "product": product,
        "version": version,
        "cpe": cpe,
        "state": state
    }   

def print_table(records):
    """
    Prints the scan results
    """

    if not records:
        print("\nNothing to display.\n")
        return

    print("\nScan results:")
    print("------------------------------------")

    for r in records:
        print(f"Host: {r['host']}, Port: {r['port']}, Protocol: {r['protocol']}, State: {r['state']}")

    print("------------------------------------")

def save_csv(records, filename="scan_results.csv"):
    """
    Saves a list of scan result dictionaries to a CSV file
    returns an error if occurs
    """
    import csv
    if not records:
        print("No data has been saved")
        return False
    
    columns = ["UTC Date", "UTC Time", "host", "protocol", "port", "name", "reason", "product", "version", "cpe", "state"]
    
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for r in records:
                writer.writerow({c: r.get(c, "") for c in columns})
        print(f"Results saved successfully to {filename}")
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return False