#Hi, I'm Aimorn. I'm Diving into Python to streamline research and empower scientists, often writing scripts to tackle daily challenges and sharing them for broader use.

#The temperature log file from the MiSeq contains extensive data, as it records information from the day the instrument was installed.When FAS, FSE, or customers need to verify whether the temperature of the flow cell or chiller is within the proper range, it can be time-consuming to wait for and load the data from the .csv file. 

#I’ve written a Python script to assist those struggling with this process. You only add input prompts for the start and end dates.It filters out only the dates you specify, and you can easily tweak the date format in the script. 

#Hopefully, this will help you breeze through the data, so you can spend less time waiting and more time enjoying your coffee break and free time!



import pandas as pd
import os
import glob

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define file patterns for Excel and CSV files
file_patterns = [os.path.join(current_directory, '*.xlsx'), os.path.join(current_directory, '*.csv')]

# Get list of all Excel and CSV files in the directory
excel_files = []
for pattern in file_patterns:
    excel_files.extend(glob.glob(pattern))

# Prompt user for the date range to filter by (m/d/yyyy format)
start_date_str = input("Enter the start date (m/d/yyyy): ")
end_date_str = input("Enter the end date (m/d/yyyy): ")

# Convert input dates to datetime
start_date = pd.to_datetime(start_date_str, format='%m/%d/%Y', errors='coerce')
end_date = pd.to_datetime(end_date_str, format='%m/%d/%Y', errors='coerce')

if pd.isna(start_date) or pd.isna(end_date):
    print("Invalid date format. Please use m/d/yyyy.")
else:
    # Ensure end_date is greater than start_date
    if start_date > end_date:
        print("Start date must be before or equal to end date.")
    else:
        # Columns to extract
        columns_to_extract = ['Date', 'Time', 'Ambient Temperature C', 'Temperature C', 'SetPoint C']

        # Process each file
        for input_file_path in excel_files:
            # Construct output file path
            base_name = os.path.basename(input_file_path)
            output_file_name = f"filtered_{base_name}"
            output_file_path = os.path.join(current_directory, output_file_name)

            # Load the file based on extension
            if input_file_path.endswith('.xlsx'):
                df = pd.read_excel(input_file_path)
            elif input_file_path.endswith('.csv'):
                # Read CSV file with low_memory=False to handle mixed types
                df = pd.read_csv(input_file_path, low_memory=False)

            # Strip leading and trailing spaces from column names
            df.columns = df.columns.str.strip()

            # Print columns to check if 'Date' exists and to handle naming issues
            print(f"Columns in {input_file_path}: {df.columns.tolist()}")

            # Adjust column name if necessary
            date_column = 'Date' if 'Date' in df.columns else 'date'

            # Ensure the date column is in datetime format if it exists
            if date_column in df.columns:
                df[date_column] = pd.to_datetime(df[date_column], format='%m/%d/%Y', errors='coerce')

                # Filter the DataFrame by the date range
                filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

                # Check if there are any rows after filtering
                if not filtered_df.empty:
                    # Extract specific columns, checking if they exist
                    existing_columns = [col for col in columns_to_extract if col in df.columns]
                    filtered_df = filtered_df[existing_columns]

                    # Save the filtered data to a new file
                    if input_file_path.endswith('.xlsx'):
                        filtered_df.to_excel(output_file_path, index=False)
                    elif input_file_path.endswith('.csv'):
                        filtered_df.to_csv(output_file_path, index=False)

                    print(f"Filtered data saved to {output_file_path}")
                else:
                    print(f"No data found for the date range {start_date_str} to {end_date_str} in file {input_file_path}")
            else:
                print(f"'{date_column}' column not found in file {input_file_path}")
