import requests
import csv
import ftplib
from datetime import datetime
import schedule
import time

# Replace with your MockAPI endpoint
mockapi_url = 'https://67106bbda85f4164ef2dea12.mockapi.io/reclamos'  # Example endpoint

# FTP server details
ftp_host = '172.31.54.23'
ftp_username = 'fabiliria'
ftp_password = '773H'
ftp_directory = 'reclamos'  # Directory for the main file
backup_directory = 'respaldos_reclamos'  # Directory for the backups

def fetch_and_upload_data():
    # Make a request to the API
    response = requests.get(mockapi_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Get the JSON data

        # Get the keys from the first item to use as headers for the CSV
        headers = data[0].keys() if data else []

        # Create the CSV file locally
        local_file = 'reclamos.csv'
        with open(local_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write the headers
            writer.writeheader()

            # Write each row of data
            for row in data:
                writer.writerow(row)

        print(f"Data successfully written to '{local_file}'")

        # Upload the CSV file to the FTP server
        try:
            with ftplib.FTP(ftp_host) as ftp:
                ftp.login(user=ftp_username, passwd=ftp_password)

                # -------- Upload to reclamos directory --------
                ftp.cwd(ftp_directory)

                # Try to delete the existing reclamos.csv if it exists
                try:
                    ftp.delete(local_file)
                    print(f"Existing file '{local_file}' deleted.")
                except ftplib.error_perm as e:
                    if "550" in str(e):
                        print(f"No existing file named '{local_file}' to delete.")
                    else:
                        raise

                # Open the file in binary mode to upload
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {local_file}', file)
                print(f"File '{local_file}' successfully uploaded to FTP server in reclamos directory")

                # -------- Upload to respaldos_reclamos directory with date --------
                # Change to the backup directory
                ftp.cwd(f"/{backup_directory}")

                # Generate a filename with the current date
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"reclamos_{current_date}.csv"

                # Upload the file to the backup directory with the date in the name
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {backup_file}', file)

                print(f"File '{backup_file}' successfully uploaded to FTP server in respaldos_reclamos directory")

        except ftplib.all_errors as e:
            print(f"FTP error: {e}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Programar la ejecución una vez al día a las 10:00 AM
schedule_time = "19:38"
schedule.every().day.at(schedule_time).do(fetch_and_upload_data)

print(f"Script programado para ejecutarse todos los días a las {schedule_time}.")

# Bucle para mantener el script corriendo
while True:
    schedule.run_pending()
    time.sleep(1)
