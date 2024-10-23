import requests
import csv
import ftplib
import random
import os
from datetime import datetime
import schedule
import time

# Configuración
mockapi_url = 'https://67106bbda85f4164ef2dea12.mockapi.io/reclamos'
ftp_host = '172.31.54.23'
ftp_username = 'fabiliria'
ftp_password = '773H'
ftp_data = "reclamos"
ftp_directory_target = 'reclamos_validados'
backup_directory = 'respaldos_reclamos'

# Función para conectarse al FTP y descargar el archivo reclamos.csv
def download_reclamos_file():
    try:
        with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
            ftp.cwd(ftp_data)
            filename = 'reclamos.csv'
            local_file = open(filename, 'wb')
            ftp.retrbinary(f'RETR {filename}', local_file.write)
            local_file.close()
            print(f"{filename} descargado exitosamente.")
    except Exception as e:
        print(f"Error descargando el archivo: {e}")

# Función para subir un archivo al FTP
def upload_file_to_ftp(local_file, target_directory, target_filename):
    try:
        with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
            ftp.cwd(target_directory)
            with open(local_file, 'rb') as file:
                ftp.storbinary(f'STOR {target_filename}', file)
            print(f"Archivo {target_filename} subido exitosamente a {target_directory}.")
    except Exception as e:
        print(f"Error subiendo el archivo: {e}")

# Función para procesar el archivo reclamos.csv
def process_reclamos():
    input_file = 'reclamos.csv'
    output_file = 'reclamos_validados.csv'
    remaining_rows = []

    try:
        # Leer archivo CSV
        with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Leer los encabezados
            remaining_rows.append(headers)

            for row in reader:
                # Decidir aleatoriamente si mantenemos o eliminamos la fila
                if random.choice([True, False]):
                    remaining_rows.append(row)

        # Guardar las filas restantes en el nuevo archivo
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(remaining_rows)

        print(f"Archivo procesado y guardado como {output_file}.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")

# Función principal
def main():
    download_reclamos_file()
    process_reclamos()
    upload_file_to_ftp('reclamos_validados.csv', ftp_directory_target, 'reclamos_validados.csv')

# Programar la ejecución una vez al día a las 10:00 AM
schedule_time = "19:39"
schedule.every().day.at(schedule_time).do(main)

print(f"Script programado para ejecutarse todos los días a las {schedule_time}.")

# Bucle para mantener el script corriendo
while True:
    schedule.run_pending()
    time.sleep(1)
