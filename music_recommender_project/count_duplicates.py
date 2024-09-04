from collections import Counter

# Function to count duplicate IDs in a text file
def count_duplicate_ids(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            ids = [line.split('id: ')[1].strip() for line in lines if line.startswith('id:')]
            id_count = Counter(ids)
            duplicates = {id_: count for id_, count in id_count.items() if count > 1}
            
            if duplicates:
                print(f"Found {len(duplicates)} duplicate IDs.")
                for id_, count in duplicates.items():
                    print(f"ID: {id_}, Count: {count}")
            else:
                print("No duplicate IDs found.")
                
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = 'urls.txt'
count_duplicate_ids(file_path)
