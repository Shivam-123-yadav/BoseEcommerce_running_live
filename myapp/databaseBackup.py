import subprocess
import os
import zipfile
from datetime import datetime
import shutil
import schedule
import time

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BoseEcom',
        'USER': 'BoseEcom',
        'PASSWORD': 'K2!J?h5?E#@',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8', 
        },
    }
}

def backup_database():
    db_config = DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
    timestamp = datetime.now().strftime('%Y-%m-%d')
    destination_dir = f"databaseBackup/{timestamp}"
    os.makedirs(destination_dir, exist_ok=True)
    backup_file = os.path.join(destination_dir, f"{db_name}_backup_{timestamp}.sql")
    dump_command = [
        "mysqldump",
        f"--user={db_user}",
        f"--password={db_password}",
        f"--host={db_host}",
        f"--port={db_port}",
        "--default-character-set=utf8",
        db_name
    ]


    try:
        with open(backup_file, 'w') as output_file:
            subprocess.run(dump_command, stdout=output_file, check=True)
        print(f"Database backup successful! File saved to {backup_file}")

        zip_file = os.path.join(destination_dir, f"{db_name}_backup_{timestamp}.zip")
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            backup_zip.write(backup_file, os.path.basename(backup_file))
        print(f"Backup ZIP file created: {zip_file}")
        os.remove(backup_file)

    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

schedule.every().day.at("13:00").do(backup_database)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(20)

    # try:
    #     with open(backup_file, 'w') as output_file:
    #         subprocess.run(dump_command, stdout=output_file, check=True)
    #     print(f"Database backup successful! File saved to {backup_file}")

#         zip_file = os.path.join(destination_dir, f"{db_name}_backup_{timestamp}.zip")
#         with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
#             backup_zip.write(backup_file, os.path.basename(backup_file))
#         print(f"Backup ZIP file created: {zip_file}")
#         os.remove(backup_file)
#         destination_path = "/home/Bosecom/public_html/BoseEcommerce_running_live/media/databaseBackups"
#         os.makedirs(destination_path, exist_ok=True)
#         shutil.copytree(destination_dir, os.path.join(destination_path, timestamp))
#         print(f"Backup folder copied to {destination_path}")
#         shutil.rmtree(destination_dir)

#     except subprocess.CalledProcessError as e:
#         print(f"Error during backup: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")

# # schedule.every(1).minute.do(backup_database)
# schedule.every(10).seconds.do(backup_database)

# # Schedule the backup to run every Monday at 12:00 PM
# # schedule.every().monday.at("12:00").do(backup_database)

# # Schedule the backup to run daily at 12:00 PM
# # schedule.every().day.at("01:00").do(backup_database)


# if __name__ == "__main__":
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
