from task2 import HashTable

def menu():
    size = int(input('Enter the size of the hash table: '))
    key_field = input('Enter the name of the key field: ')
    fields = input('Enter the names of the other fields (comma-separated): ').split(',')
    hash_table = HashTable(size, key_field, fields)

    while True:
        print('\nHash Table Operations:')
        print('1. Add Record')
        print('2. Remove Record')
        print('3. Update Record')
        print('4. Search Record')
        print('5. Show Table')
        print('6. Exit')
        
        choice = int(input('Enter your choice: '))
        
        if choice == 1:
            values = input(f'Enter the values for {key_field} and {",".join(fields)}: ').split(',')
            hash_table.add_record(values)
        elif choice == 2:
            key_value = input(f'Enter the value of the {key_field} field to remove the record: ')
            hash_table.remove_record(key_value)
        elif choice == 3:
            key_value = input(f'Enter the value of the {key_field} field to update the record: ')
            new_values = input(f'Enter the new values for {key_field} and {",".join(fields)}: ').split(',')
            hash_table.update_record(key_value, new_values)
        elif choice == 4:
            key_value = input(f'Enter the value of the {key_field} field to search for the record: ')
            record = hash_table.search_record(key_value)
            if record is None:
                print('Record not found.')
            else:
                print(f'Record found: {record}')
        elif choice == 5:
            print([key_field, *fields])
            for record in hash_table.table:
                print(record) 
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == "__main__":
    menu()
