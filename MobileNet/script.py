import os
import pandas as pd

def extract_total_cycles(file_path):
    """
    Extract 'Total Cycles' value from the COMPUTE_REPORT.csv file.
    Assumes the first column is names and the second column contains values.
    """
    # Read the CSV and assume the relevant row contains 'Total Cycles'
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure column names are stripped of leading/trailing spaces
    df.columns = df.columns.str.strip()
    
    # Sum values in the 'Total Cycles' column
    print(df.columns)
    if 'Overall Util %' in df.columns:
        total_cycles_sum = df['Overall Util %'].astype(float).sum()
        print(f"Sum of Total Cycles: {int(total_cycles_sum)}")
        return int(total_cycles_sum)
    else:
        print("Column 'Total Cycles' not found in the CSV file.")
        return 0
def process_folders(base_dir):
    """
    Process folders, compute values, and print the results in the required format.
    """
    results = []

    # Iterate through folders in the base directory
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        
        # Ensure it's a valid folder and extract the number (e.g., cnn12is -> 12)
        if os.path.isdir(folder_path) and folder[3:5].isdigit():
            matrix_size = int(folder[3:len(folder)-2])  # Extract size (12, 16, etc.)
            compute_file = os.path.join(folder_path, "COMPUTE_REPORT.csv")
            
            # Check if COMPUTE_REPORT.csv exists
            if os.path.exists(compute_file):
                scaled_value = extract_total_cycles(compute_file)/28
                # scaled_value = total_cycles * (matrix_size ** 2)
                
                # Determine dataflow type (IS, OS, WS) from folder name
                dataflow = "IS" if "is" in folder else "OS" if "os" in folder else "WS"
                
                # Append to results
                results.append((matrix_size, scaled_value, dataflow))
                print(f"{matrix_size}, {scaled_value}, {dataflow}")
            else:
                print(f"COMPUTE_REPORT.csv not found in {folder}")

    # Sort results by matrix size for clarity
    results.sort()
    print("\nFinal Results:")
    for res in results:
        print(f"{res[0]}, {res[1]}, {res[2]}")

if __name__ == "__main__":
    base_directory = "."  # Replace with the path to your folders

    process_folders(base_directory)
