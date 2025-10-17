import sqlite3
import csv

def create_database():
    """Create the database and table if they don't exist"""
    conn = sqlite3.connect('placenta_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS placenta_study (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geo_accession TEXT,
            title TEXT,
            organism TEXT,
            data_type TEXT,
            extracted_molecule TEXT,
            superseries TEXT,
            summary TEXT,
            publication_date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

def load_csv_to_database(csv_file):
    """Load data from CSV file into the database"""
    conn = sqlite3.connect('placenta_database.db')
    cursor = conn.cursor()
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO placenta_study (
                    geo_accession, title, organism, data_type, 
                    extracted_molecule, superseries, summary, publication_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('geo_accession', ''),
                row.get('title', ''),
                row.get('organism', ''),
                row.get('data_type', ''),
                row.get('extracted_molecule', ''),
                row.get('superseries', ''),
                row.get('summary', ''),
                row.get('publication_date', '')
            ))
    
    conn.commit()
    conn.close()
    print(f"Data from {csv_file} loaded successfully!")

def view_all_data():
    """View all data in the database"""
    conn = sqlite3.connect('placenta_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM placenta_study')
    rows = cursor.fetchall()
    
    print(f"\nTotal records: {len(rows)}\n")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Accession: {row[1]}")
        print(f"Title: {row[2]}")
        print(f"Organism: {row[3]}")
        print(f"Data Type: {row[4]}")
        print("-" * 50)
    
    conn.close()

if __name__ == "__main__":
    print("Placenta Database CSV Loader")
    print("=" * 50)
    
    # Step 1: Create database
    create_database()
    
    # Step 2: Load CSV (update 'your_data.csv' to your actual CSV filename)
    csv_filename = input("\nEnter CSV filename (or press Enter to skip): ").strip()
    
    if csv_filename:
        try:
            load_csv_to_database(csv_filename)
            view_all_data()
        except FileNotFoundError:
            print(f"Error: File '{csv_filename}' not found!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Skipping CSV load. Database is ready for data.")
