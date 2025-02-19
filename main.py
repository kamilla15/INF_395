import sqlite3

def init_db():
    conn = sqlite3.connect("lost_and_found.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        location TEXT NOT NULL,
                        date_found TEXT NOT NULL,
                        claimed TEXT DEFAULT 'No'
                    )''')
    conn.commit()
    conn.close()

def report_item():
    name = input("Enter item name: ")
    category = input("Enter category: ")
    location = input("Enter location found: ")
    date_found = input("Enter date found (YYYY-MM-DD): ")
    
    conn = sqlite3.connect("lost_and_found.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, category, location, date_found) VALUES (?, ?, ?, ?)", 
                   (name, category, location, date_found))
    conn.commit()
    conn.close()
    print("Item reported successfully!")

def search_item():
    keyword = input("Enter item name, category, or location: ")
    conn = sqlite3.connect("lost_and_found.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ? OR location LIKE ?", 
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print("\nFound Items:")
        for item in results:
            print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Location: {item[3]}, Date Found: {item[4]}, Claimed: {item[5]}")
    else:
        print("No items found.")

def view_unclaimed():
    conn = sqlite3.connect("lost_and_found.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE claimed = 'No'")
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print("\nUnclaimed Items:")
        for item in results:
            print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Location: {item[3]}, Date Found: {item[4]}")
    else:
        print("No unclaimed items.")

def claim_item():
    item_id = input("Enter item ID to claim: ")
    conn = sqlite3.connect("lost_and_found.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET claimed = 'Yes' WHERE id = ? AND claimed = 'No'", (item_id,))
    if cursor.rowcount:
        print("Item claimed successfully!")
    else:
        print("Invalid ID or item already claimed.")
    conn.commit()
    conn.close()


def main():
    init_db()
    while True:
        print("\nLost & Found System")
        print("1. Report a Found Item")
        print("2. Search for a Lost Item")
        print("3. View All Unclaimed Items")
        print("4. Claim an Item")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            report_item()
        elif choice == "2":
            search_item()
        elif choice == "3":
            view_unclaimed()
        elif choice == "4":
            claim_item()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
