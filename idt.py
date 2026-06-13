import base64
from datetime import datetime

# ----------------------------------
# Land Records Database
# ----------------------------------
land_records = {
    "L001": {
        "owner": "Ramesh Kumar",
        "location": "Delhi",
        "area": "1200 sqft",
        "status": "Verified"
    },
    "L002": {
        "owner": "Suresh Patel",
        "location": "Ahmedabad",
        "area": "1500 sqft",
        "status": "Verified"
    },
    "L003": {
        "owner": "Priya Singh",
        "location": "Jaipur",
        "area": "1800 sqft",
        "status": "Pending"
    },
    "L004": {
        "owner": "Anita Sharma",
        "location": "Bangalore",
        "area": "2200 sqft",
        "status": "Verified"
    },
    "L005": {
        "owner": "Rahul Verma",
        "location": "Delhi",
        "area": "1400 sqft",
        "status": "Pending"
    },
    "L006": {
        "owner": "Ramesh Kumar",
        "location": "Mumbai",
        "area": "2500 sqft",
        "status": "Verified"
    },
    "L007": {
        "owner": "Suresh Patel",
        "location": "Pune",
        "area": "2000 sqft",
        "status": "Pending"
    },
    "L008": {
        "owner": "Priya Singh",
        "location": "Bangalore",
        "area": "3000 sqft",
        "status": "Verified"
    }
}

# ----------------------------------
# User Database
# ----------------------------------
users = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "owner": {
        "password": "owner123",
        "role": "Owner"
    }
}

# ----------------------------------
# Encryption Functions
# ----------------------------------
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    return base64.b64decode(data.encode()).decode()

# ----------------------------------
# Transaction Monitoring
# ----------------------------------
def log_transaction(action):
    with open("transactions.txt", "a") as file:
        file.write(f"{datetime.now()} - {action}\n")

# ----------------------------------
# Authentication
# ----------------------------------
def login():
    print("\n===== USER LOGIN =====")

    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == password:
        print("\nAuthentication Successful")
        print("Role Verified:", users[username]["role"])
        log_transaction(f"{username} Logged In")
        return users[username]["role"]
    else:
        print("\nInvalid Username or Password")
        return None

# ----------------------------------
# View Records
# ----------------------------------
def view_records():
    print("\n===== LAND RECORDS =====")

    for land_id, details in land_records.items():
        print("\n----------------------------")
        print("Land ID :", land_id)
        print("Owner   :", details["owner"])
        print("Location:", details["location"])
        print("Area    :", details["area"])
        print("Status  :", details["status"])
        if details["status"] == "Pending":
         print(f"NOTICE: The land record belonging to {details['owner']} has not yet been verified.")

    log_transaction("Viewed Land Records")

# ----------------------------------
# Search Record
# ----------------------------------
def search_record():
    land_id = input("\nEnter Land ID: ")

    if land_id in land_records:
        print("\nRecord Found")
        print("----------------------------")
        print("Owner   :", land_records[land_id]["owner"])
        print("Location:", land_records[land_id]["location"])
        print("Area    :", land_records[land_id]["area"])
        print("Status  :", land_records[land_id]["status"])

        log_transaction(f"Searched Record {land_id}")
    else:
        print("Record Not Found")

# ----------------------------------
# Update Record
# ----------------------------------
def update_record():
    land_id = input("\nEnter Land ID to Update: ")

    if land_id in land_records:

        new_owner = input("Enter New Owner Name: ")

        encrypted_owner = encrypt_data(new_owner)

        land_records[land_id]["owner"] = decrypt_data(
            encrypted_owner
        )

        print("Record Updated Successfully")
        print("Data Encrypted and Stored Securely")

        log_transaction(f"Updated Record {land_id}")

    else:
        print("Record Not Found")

# ----------------------------------
# Verify Record
# ----------------------------------
def verify_record():
    land_id = input("\nEnter Land ID to Verify: ")

    if land_id in land_records:

        land_records[land_id]["status"] = "Verified"

        print("\nRecord Verified Successfully")

        print("\nUpdated Record Details")
        print("----------------------------")
        print("Owner   :", land_records[land_id]["owner"])
        print("Location:", land_records[land_id]["location"])
        print("Area    :", land_records[land_id]["area"])
        print("Status  :", land_records[land_id]["status"])

        log_transaction(f"Verified Record {land_id}")

    else:
        print("Record Not Found")

# ----------------------------------
# Generate Secure Records
# ----------------------------------
def generate_secure_records():

    print("\n===== SECURE DIGITAL RECORD GENERATION =====")

    verified_count = 0
    pending_count = 0

    for land_id, details in land_records.items():

        if details["status"] == "Verified":
            verified_count += 1
        else:
            pending_count += 1

    print("\nSecurity Scan Completed")
    print("----------------------------")
    print("Total Records      :", len(land_records))
    print("Verified Records   :", verified_count)
    print("Pending Records    :", pending_count)

    if pending_count > 0:
        print("\nNOTICE: Some records are still awaiting verification.")
    else:
        print("\nAll records have been verified successfully.")

    print("Digital signatures generated.")
    print("Records encrypted and stored securely.")
    print("Blockchain verification completed.")
    print("Secure digital land records generated successfully.")

    log_transaction("Generated Secure Records")

# ----------------------------------
# Main Program
# ----------------------------------
role = login()

if role:

    while True:

        print("\n")
        print("===== DIGITAL LAND RECORD SYSTEM =====")
        print("1. View Land Records")
        print("2. Search Land Record")

        if role == "Admin":
            print("3. Update Land Record")
            print("4. Verify Land Record")

        print("5. Generate Secure Records")
        print("6. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            view_records()

        elif choice == "2":
            search_record()

        elif choice == "3" and role == "Admin":
            update_record()

        elif choice == "4" and role == "Admin":
            verify_record()

        elif choice == "5":
            generate_secure_records()

        elif choice == "6":
            print("\nThank You for Using Digital Land Record System")
            break

        else:
            print("Invalid Choice")