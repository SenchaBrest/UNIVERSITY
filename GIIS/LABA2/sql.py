import sqlite3
import csv


class AddressBookDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def create_table(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                                name TEXT PRIMARY KEY,
                                address TEXT
                            )''')
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def add_contact(self, name, address):
        try:
            self.cursor.execute("INSERT INTO contacts (name, address) VALUES (?, ?)", (name, address))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def edit_contact(self, old_name, new_name, new_address):
        try:
            self.cursor.execute("UPDATE contacts SET name=?, address=? WHERE name=?", (new_name, new_address, old_name))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def delete_contact(self, name):
        try:
            self.cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def get_all_contacts(self, sort_by_name=False, sort_order='asc'):
        try:
            order_clause = f"ORDER BY name {sort_order.upper()}" if sort_by_name else ""
            query = f"SELECT * FROM contacts {order_clause}"
            self.cursor.execute(query)
            all_contacts = self.cursor.fetchall()
            return all_contacts
        except sqlite3.Error:
            return None

    def get_contact_by_index(self, index, sort):
        if sort is not None:
            all_contacts = self.get_all_contacts(sort_by_name=True, sort_order=sort)
        else:
            all_contacts = self.get_all_contacts(sort_by_name=False)
        if all_contacts is not None and 0 <= index < len(all_contacts):
            return all_contacts[index]
        return None

    def get_index_by_name(self, contact_name, sort):
        if sort is not None:
            all_contacts = self.get_all_contacts(sort_by_name=True, sort_order=sort)
        else:
            all_contacts = self.get_all_contacts(sort_by_name=False)
        if all_contacts is not None:
            for index, contact in enumerate(all_contacts):
                if contact[0] == contact_name:
                    return index
        return None

    def get_table_size(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM contacts")
            size = self.cursor.fetchone()[0]
            return size
        except sqlite3.Error:
            return None

    def export_to_vcf(self, filename):
        try:
            with open(filename, 'w', newline='') as vcf_file:
                vcf_writer = csv.writer(vcf_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                all_contacts = self.get_all_contacts()
                for contact in all_contacts:
                    vcf_writer.writerow(['BEGIN:VCARD'])
                    vcf_writer.writerow(['VERSION:3.0'])
                    vcf_writer.writerow(['FN:' + contact[0]])
                    vcf_writer.writerow(['ADR;TYPE=HOME:' + contact[1]])
                    vcf_writer.writerow(['END:VCARD'])
            return True
        except IOError:
            return False

    def import_from_vcf(self, filename):
        try:
            with open(filename, 'r', newline='') as vcf_file:
                vcf_reader = csv.reader(vcf_file, delimiter='\t')
                for row in vcf_reader:
                    if row[0] == 'BEGIN:VCARD':
                        name = None
                        address = None
                        while True:
                            row = next(vcf_reader)
                            if row[0] == 'END:VCARD':
                                break
                            elif row[0].startswith('FN'):
                                name = row[0].split(':')[1]
                            elif row[0].startswith('ADR;TYPE=HOME'):
                                address = row[0].split(':')[1]
                        if name and address:
                            self.add_contact(name, address)
            return True
        except (IOError, StopIteration):
            return False

    def close(self):
        self.connection.close()
