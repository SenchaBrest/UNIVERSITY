from task1 import Table

def menu():
    key_field = input('Enter the name of the key field: ')
    fields = input('Enter the names of the other fields (comma-separated): ').split(',')
    table = Table(key_field, fields)
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Add Record")
        print("2. Remove Record")
        print("3. Update Record")
        print("4. Search Record")
        print("5. Show Table")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            values = []
            values.append(input(f"Enter value for {key_field}: "))
            for field in fields:
                values.append(input(f"Enter value for {field}: "))
            table.add_record(values)  
        elif choice == "2":
            key_value = input(f"Enter {key_field} of record to remove: ")
            table.remove_record(key_value)           
        elif choice == "3":
            key_value = input(f"Enter {key_field} of record to update: ")
            record = table.search_record(key_value)
            if record:
                print(f"Current values for record {key_value}:")
                print(f"{key_field}: {record[0]}")
                for i, field in enumerate(fields):
                    print(f"{field}: {record[i+1]}")
                new_values = []
                new_values.append(key_value)
                for field in fields:
                    new_values.append(input(f"Enter new value for {field}: "))
                table.update_record(key_value, new_values)
        elif choice == "4":
            key_value = input(f"Enter {key_field} of record to search: ")
            record = table.search_record(key_value)
            if record:
                print(f"Record found:")
                print(f"{key_field}: {record[0]}")
                for i, field in enumerate(fields):
                    print(f"{field}: {record[i+1]}")
            else:
                print("Record not found.")   
        elif choice == "5":
            print([key_field, *fields])
            for record in table.table:
                print(record)       
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()