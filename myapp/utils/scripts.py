# import requests
# import pandas as pd
# import gspread
# from io import StringIO
# from oauth2client.service_account import ServiceAccountCredentials
# import time
# import hashlib
# import numpy as np


# SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# # SERVICE_ACCOUNT_FILE = r"/home/Bosecom/public_html/Credentials.json"
# SERVICE_ACCOUNT_FILE = r"/home/Bosecom/public_html/automation-scripts.json"

# def get_csv_hash(csv_content):
#     """Generate a hash for the CSV content to compare changes."""
#     return hashlib.md5(csv_content.encode('utf-8')).hexdigest()

# def update_google_sheet(spreadsheet_id, worksheet_name, urls, last_csv_hash):
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
#     gc = gspread.authorize(credentials)
#     sheet = gc.open_by_key(spreadsheet_id).worksheet(worksheet_name)
    
#     combined_df = pd.DataFrame()
#     new_hash = ""
    
#     for url in urls:
#         response = requests.get(url)
#         if response.status_code == 200:
#             csv_content = response.text
#             new_hash += get_csv_hash(csv_content)  # Append hash to track changes
            
#             try:
#                 df = pd.read_csv(StringIO(csv_content))
#                 combined_df = pd.concat([combined_df, df], ignore_index=True)
#             except Exception as e:
#                 print(f"Error reading CSV from {url}: {e}")
#         else:
#             print(f"Failed to fetch CSV from {url}. Status code: {response.status_code}")
    
#     if not combined_df.empty and new_hash != last_csv_hash:
#         try:
#             combined_df = combined_df.replace([np.nan, np.inf, -np.inf], "")
#             sheet.clear()
#             sheet.update([combined_df.columns.values.tolist()] + combined_df.values.tolist())
#             print(f"Data successfully updated in Google Sheets: {spreadsheet_id} - {worksheet_name}")
#             return new_hash
#         except Exception as e:
#             print(f"Error updating Google Sheet: {e}")
#     else:
#         print(f"No change in data, skipping update for {spreadsheet_id} - {worksheet_name}")
    
#     return last_csv_hash

# # Initialize last hashes
# last_hash_1 = ""
# last_hash_2 = ""
# last_hash_3 = ""
# last_hash_4 = ""
# last_hash_5 = ""
# last_hash_6 = ""
# last_hash_7 = ""
# last_hash_8 = ""

# while True:
# # ==========================================================================================    
#     # Update HP Offsite Reports
#     last_hash_1 = update_google_sheet(
#         "1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "hp", 
#         [
#             "https://hpservicecentre.co.in/export_offsite_reports.php",
#             "https://hpauthorisedservicecenter.co.in/export_offsite_reports.php"
#         ], 
#         last_hash_1
#     )

#     # # Update HP onsite Reports
#     last_hash_2= update_google_sheet(
#         "1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "hp", 
#         [
#             "https://hpservicecentre.co.in/export_customers.php",
#             "https://hpauthorisedservicecenter.co.in/export_customers.php"
#         ], 
#         last_hash_2
#     )
# # ============================================================================================


# # ==========================================================================================
#     # Update Lenovo Offsite Reports

#     last_hash_3 = update_google_sheet(
#         "1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "lenovo", 
#         [
#             "https://lenovoservicecentre.co.in/export_offsite_reports.php", 
#         ], 
#         last_hash_3
#     )



# # Update lenovo onsite Reports

#     last_hash_4 = update_google_sheet(
#         "1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "lenovo", 
#         [
#             "https://lenovoservicecentre.co.in/export_customers.php", 
#         ], 
#         last_hash_4
#     )
   
# # ============================================================================================


# # ==========================================================================================

# # Update dellspareindia Offsite Reports

#     last_hash_5 = update_google_sheet(
#         "1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "dell", 
#         [
#             "https://dellsparesindia.com/export_offsite_reports.php", 
#             "https://dellservicescentre.co.in/export_offsite_reports.php", 
#         ], 
#         last_hash_5
#     )


# # # Update dellspareindia onsite Reports

# #     # Update dellsparesindia onsite Reports
#     last_hash_6 = update_google_sheet(
#         "1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "dell", 
#         [
#             "http://dellsparesindia.com/export_customers.php",
#             "https://dellservicescentre.co.in/export_customers.php",
#         ], 
#         last_hash_6
#     )



# # ==========================================================================================


# # ==========================================================================================
# # Update acer Offsite Reports

#     last_hash_7 = update_google_sheet(
#         "1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "acer", 
#         [
#             "https://acerservicecentre.co.in/export_offsite_reports.php", 
#         ], 
#         last_hash_7
#     )



#     last_hash_8 = update_google_sheet(
#         "1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "acer", 
#         [
#             "http://acerservicecentre.co.in/export_customers.php", 
#         ], 
#         last_hash_8
#     )

# # ==========================================================================================

    
#     time.sleep(2)
import requests
import pandas as pd
import gspread
import time
import hashlib
import numpy as np
import logging
from io import StringIO
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "/home/Bosecom/public_html/automation-scripts.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
gc = gspread.authorize(credentials)
last_hashes = {}

def get_csv_hash(csv_content):
    """Generate a hash for the CSV content to compare changes."""
    return hashlib.md5(csv_content.encode('utf-8')).hexdigest()

def update_google_sheet(spreadsheet_id, worksheet_name, urls, last_csv_hash, max_retries=6):
    """
    Fetch CSV data from URLs, update Google Sheets if data has changed.
    Returns the new hash of the updated data.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            sheet = gc.open_by_key(spreadsheet_id).worksheet(worksheet_name)
            break 
        except gspread.exceptions.APIError as e:
            attempt += 1
            logging.warning(f"Attempt {attempt}: Google Sheets API error: {e}")
            time.sleep(2 ** attempt)  
    else:
        logging.error(f"Failed to fetch Google Sheet {spreadsheet_id} - {worksheet_name} after {max_retries} retries")
        return last_csv_hash

    combined_df = pd.DataFrame()
    new_hash = ""

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error if status code is not 200

            csv_content = response.text
            new_hash += get_csv_hash(csv_content)

            df = pd.read_csv(StringIO(csv_content))
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        except requests.RequestException as e:
            logging.error(f"Failed to fetch CSV from {url}: {e}")
        except pd.errors.EmptyDataError:
            logging.warning(f"CSV from {url} is empty.")
        except Exception as e:
            logging.error(f"Error processing CSV from {url}: {e}")

    if not combined_df.empty and new_hash != last_csv_hash:
        try:
            combined_df = combined_df.replace([np.nan, np.inf, -np.inf], "")
            sheet.clear()
            sheet.update([combined_df.columns.values.tolist()] + combined_df.values.tolist())
            logging.info(f"Data updated in Google Sheets: {spreadsheet_id} - {worksheet_name}")
            return new_hash
        except Exception as e:
            logging.error(f"Error updating Google Sheet: {e}")
    else:
        logging.info(f"No data change, skipping update for {spreadsheet_id} - {worksheet_name}")

    return last_csv_hash

def main():
    sheet_mapping = {
        "hp_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "hp", [
            "https://hpservicecentre.co.in/export_offsite_reports.php",
            "https://hpauthorisedservicecenter.co.in/export_offsite_reports.php",
            "https://hpsparesindia.com/export_offsite_reports.php",
            "https://hpservicecenter.tech/export_offsite_reports.php"
        ]),
        "hp_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "hp", [
            "https://hpservicecentre.co.in/export_customers.php",
            "https://hpauthorisedservicecenter.co.in/export_customers.php",
            "https://hpsparesindia.com/export_customers.php",
            "https://hpservicecenter.tech/export_customers.php"
        ]),
        "lenovo_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "lenovo", [
            "https://lenovoservicecentre.co.in/export_offsite_reports.php"
        ]),
        "lenovo_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "lenovo", [
            "https://lenovoservicecentre.co.in/export_customers.php"
        ]),
        "dell_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "dell", [
            "https://mydellrepairs.in/export_offsite_reports.php",
            "https://dellsparesindia.com/export_offsite_reports.php",
            "https://dellservicecentre.com/export_offsite_reports.php",
            "https://dellservicecenter.info/export_offsite_reports.php",
            "https://dellservicescentre.co.in/export_offsite_reports.php"
        ]),
        "dell_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "dell", [
            # "https://mydellrepairs.in/export_customers.php",
            # "http://dellsparesindia.com/export_customers.php",
            # "https://dellservicescentre.co.in/export_customers.php"
            "https://mydellrepairs.in/export_customers.php",
            "https://dellsparesindia.com/export_customers.php",
            "https://dellservicecentre.com/export_customers.php",
            "https://dellservicecenter.info/export_customers.php",
            "https://dellservicescentre.co.in/export_customers.php"
        ]),
        "acer_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "acer", [
            # "https://acerservicecentre.co.in/export_offsite_reports.php"
            "https://laptopservicencenter.in/export_offsite_reports.php"
        ]),
        "acer_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "acer", [
            # "http://acerservicecentre.co.in/export_customers.php"
            "https://laptopservicencenter.in/export_customers.php"
        ]),

        "asus_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "asus", [
            "https://asusservicecentre.in/export_offsite_reports.php"
        ]),
        "asus_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "asus", [
            "https://asusservicecentre.in/export_customers.php"
        ]),
        
         "apple_offsite": ("1ltBqCMvf_oS-_nAi9_8ivnZj1SPyJ3ATQ8kvopivIfg", "apple", [
            "https://appleservicescentre.co.in/export_offsite_reports.php"
        ]),
        "apple_onsite": ("1qspsZh3m3PQtKVWgTFW4LGyOpXb_PCG4OXwSfn6L6dc", "apple", [
            "https://appleservicescentre.co.in/export_customers.php"
        ]),
    }

    # Initialize last hashes if not set
    for key in sheet_mapping.keys():
        last_hashes.setdefault(key, "")

    while True:
        for key, (spreadsheet_id, worksheet_name, urls) in sheet_mapping.items():
            last_hashes[key] = update_google_sheet(spreadsheet_id, worksheet_name, urls, last_hashes[key])

        logging.info("Waiting for the next update cycle...\n")
        time.sleep(600)  # Run every 10 minutes

if __name__ == "__main__":
    main()


