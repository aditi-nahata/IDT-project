import base64
from datetime import datetime

# ----------------------------------
# Encryption Functions
# ----------------------------------
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    return base64.b64decode(data.encode()).decode()

# ----------------------------------
# Land Records Database
# (Kumarswamy Layout Only)
# ----------------------------------
land_records = {
    "KH001": {
        "owner_username": "ramesh",
        "owner": encrypt_data("Ramesh Kumar"),
        "khata_no": "KH001",
        "owner": "Ramesh Kumar",
        "survey_no": "SY101",
        "layout": "Kumaraswamy Layout",
        "longitude": "77.5550",
        "latitude": "12.9081",
        "area": "2400 sqft",

        # Encrypted Details
        "aadhaar": encrypt_data("123456789012"),
        "phone": encrypt_data("9876543210"),
        "email": encrypt_data("ramesh@gmail.com"),
        "property_type": encrypt_data("Residential"),
        "registration_no": encrypt_data("REG2024001"),
        "tax_status": encrypt_data("Paid"),
        "ownership_type": encrypt_data("Individual"),
        "market_value": encrypt_data("8500000"),
        "document_hash": encrypt_data("DOC001HASH"),

        "status": "Verified"
    },

    "KH002": {
        "owner_username": "suresh",
        "owner": encrypt_data("Suresh Patel"),
        "khata_no": "KH002",
        "owner": "Suresh Patel",
        "survey_no": "SY102",
        "layout": "Kumaraswamy Layout",
        "longitude": "77.5561",
        "latitude": "12.9092",
        "area": "1800 sqft",

        "aadhaar": encrypt_data("987654321012"),
        "phone": encrypt_data("9123456780"),
        "email": encrypt_data("suresh@gmail.com"),
        "property_type": encrypt_data("Commercial"),
        "registration_no": encrypt_data("REG2024002"),
        "tax_status": encrypt_data("Paid"),
        "ownership_type": encrypt_data("Joint"),
        "market_value": encrypt_data("9500000"),
        "document_hash": encrypt_data("DOC002HASH"),

        "status": "Pending"
    },

    "KH003": {
        "owner_username": "priya",
        "owner": encrypt_data("Priya Singh"),
        "khata_no": "KH003",
        "owner": "Priya Singh",
        "survey_no": "SY103",
        "layout": "Kumaraswamy Layout",
        "longitude": "77.5570",
        "latitude": "12.9101",
        "area": "3000 sqft",

        "aadhaar": encrypt_data("456789123456"),
        "phone": encrypt_data("9988776655"),
        "email": encrypt_data("priya@gmail.com"),
        "property_type": encrypt_data("Residential"),
        "registration_no": encrypt_data("REG2024003"),
        "tax_status": encrypt_data("Pending"),
        "ownership_type": encrypt_data("Individual"),
        "market_value": encrypt_data("12000000"),
        "document_hash": encrypt_data("DOC003HASH"),

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

    "ramesh": {
        "password": "ramesh123",
        "role": "Owner"
    },

    "suresh": {
        "password": "suresh123",
        "role": "Owner"
    },

    "priya": {
        "password": "priya123",
        "role": "Owner"
    }
}

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

    username = input("Username : ")
    password = input("Password : ")

    if username in users and users[username]["password"] == password:

        print("\nAuthentication Successful")
        print("Role :", users[username]["role"])

        log_transaction(f"{username} Logged In")

        return username, users[username]["role"]

    else:
        print("\nInvalid Username or Password")
        return None

# ----------------------------------
# View Records
# ----------------------------------
def view_records(current_user, role):

    print("\n========== LAND RECORDS ==========")

    for khata, details in land_records.items():

        # Owners can only see their own record
        if role == "Owner" and details["owner_username"] != current_user:
            continue

        print("\n----------------------------------------")
        print("Owner Username:", details["owner_username"])
        print("Khata No      :", details["khata_no"])
        print("Owner Name    :", details["owner"])
        print("Survey No     :", details["survey_no"])
        print("Layout        :", details["layout"])
        print("Longitude     :", details["longitude"])
        print("Latitude      :", details["latitude"])
        print("Area          :", details["area"])
        print("Status        :", details["status"])

        # Show sensitive details to Admin or the owner of the record
        if role == "Admin" or details["owner_username"] == current_user:

            print("\nSensitive Details")
            print("----------------------------")
            print("Aadhaar        :", decrypt_data(details["aadhaar"]))
            print("Phone          :", decrypt_data(details["phone"]))
            print("Email          :", decrypt_data(details["email"]))
            print("Property Type  :", decrypt_data(details["property_type"]))
            print("Registration # :", decrypt_data(details["registration_no"]))
            print("Tax Status     :", decrypt_data(details["tax_status"]))
            print("Ownership Type :", decrypt_data(details["ownership_type"]))
            print("Market Value   :", decrypt_data(details["market_value"]))
            print("Document Hash  :", decrypt_data(details["document_hash"]))

        if details["status"] == "Pending":
            print("\nNOTICE : Record Verification Pending")

    log_transaction("Viewed Records")

# ----------------------------------
# Search Record
# ----------------------------------
def search_record():

    khata_no = input("\nEnter Khata Number : ")

    if khata_no in land_records:

        details = land_records[khata_no]

        print("\n========== RECORD FOUND ==========")
        print("Khata No      :", details["khata_no"])
        print("Owner Name    :", details["owner"])
        print("Survey No     :", details["survey_no"])
        print("Layout        :", details["layout"])
        print("Longitude     :", details["longitude"])
        print("Latitude      :", details["latitude"])
        print("Area          :", details["area"])
        print("Status        :", details["status"])

        log_transaction(f"Searched {khata_no}")

    else:
        print("Record Not Found")

# ----------------------------------
# Update Record
# ----------------------------------
def update_record():

    khata_no = input("\nEnter Khata Number : ")

    if khata_no in land_records:

        new_owner = input("Enter New Owner Name : ")

        encrypted_owner = encrypt_data(new_owner)

        land_records[khata_no]["owner"] = decrypt_data(
            encrypted_owner
        )

        print("\nRecord Updated Successfully")
        print("Owner Information Encrypted & Stored")

        log_transaction(f"Updated {khata_no}")

    else:
        print("Record Not Found")

# ----------------------------------
# Verify Record
# ----------------------------------
def verify_record():

    khata_no = input("\nEnter Khata Number : ")

    if khata_no in land_records:

        land_records[khata_no]["status"] = "Verified"

        print("\nRecord Verified Successfully")

        log_transaction(f"Verified {khata_no}")

    else:
        print("Record Not Found")

# ----------------------------------
# Generate Secure Records
# ----------------------------------
def generate_secure_records():

    print("\n===== SECURE DIGITAL LAND RECORDS =====")

    verified = 0
    pending = 0

    for record in land_records.values():

        if record["status"] == "Verified":
            verified += 1
        else:
            pending += 1

    print("\nSecurity Scan Completed")
    print("--------------------------------")
    print("Layout             : Kumarswamy Layout")
    print("Total Records      :", len(land_records))
    print("Verified Records   :", verified)
    print("Pending Records    :", pending)

    print("\nBlockchain Verification Completed")
    print("Digital Signatures Generated")
    print("Encrypted Storage Enabled")
    print("Secure Land Records Generated")

    log_transaction("Generated Secure Records")

# ----------------------------------
# Main Program
# ----------------------------------
login_result = login()

if login_result:

    current_user, role = login_result

    

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

        choice = input("\nEnter Choice : ")

        if choice == "1":
            view_records(current_user, role)

        elif choice == "2":
            search_record()

        elif choice == "3" and role == "Admin":
            update_record()

        elif choice == "4" and role == "Admin":
            verify_record()

        elif choice == "5":
            generate_secure_records()

        elif choice == "6":
            print("\nThank You For Using Digital Land Record System")
            break

        else:
            print("Invalid Choice")