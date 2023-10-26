import os
import zipfile
import shutil
import tarfile

directory = r"C:\Users\Ccrrq\Downloads\submissions" # Set your directory to process here
keyword = 'hw3' # Set your keyword here
# The script will find those upload files without putting them in folder (eg. name-date-hw3) as required
class DirectoryProcessor:
    def __init__(self, directory, keyword):
        self.directory = directory
        self.extracted_dir = os.path.join(directory, 'extracted')
        self.keyword = keyword

    def extract_tar_files(self):
        bad_upload_dir = os.path.join(self.directory, 'BadUpload')
        os.makedirs(bad_upload_dir, exist_ok=True)
        for filename in os.listdir(self.directory):
            if filename.endswith(('.tar', '.tar.gz')):
                tar_path = os.path.join(self.directory, filename)
                # Removing file extension to get folder name
                folder_name = filename
                for ext in ['.tar', '.tar.gz']:
                    folder_name = folder_name.replace(ext, '')
                # Adding 'NotZip-' prefix to the folder name
                folder_name = 'NotZip-' + folder_name
                extract_to_dir = os.path.join(bad_upload_dir, folder_name)
                os.makedirs(extract_to_dir, exist_ok=True)
                with tarfile.open(tar_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to_dir)
                    print(f'Extracted {filename} to {extract_to_dir}')


    def extract_zip_files(self):
        self.extract_tar_files()
        os.makedirs(self.extracted_dir, exist_ok=True)
        for filename in os.listdir(self.directory):
            if filename.endswith('.zip'):
                zip_path = os.path.join(self.directory, filename)
                extract_to_dir = os.path.join(self.extracted_dir, filename[:-4])
                os.makedirs(extract_to_dir, exist_ok=True)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to_dir)
                    print(f'Extracted {filename} to {extract_to_dir}')

    def check_subdirectories(self):
        good_upload_dir = os.path.join(self.directory, 'GoodUpload')
        os.makedirs(good_upload_dir, exist_ok=True)

        bad_upload_dir = os.path.join(self.directory, 'BadUpload')
        os.makedirs(bad_upload_dir, exist_ok=True)

        for subdir in os.listdir(self.extracted_dir):
            subdir_path = os.path.join(self.extracted_dir, subdir)
            if os.path.isdir(subdir_path) and subdir not in ['GoodUpload', 'BadUpload']:
                print_subdir = True
                for item in os.listdir(subdir_path):
                    item_path = os.path.join(subdir_path, item)
                    if os.path.isdir(item_path) and self.keyword in item:
                        print_subdir = False
                        dest_path = os.path.join(good_upload_dir, item)
                        shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
                        break
                if print_subdir:
                    dest_path = os.path.join(bad_upload_dir, subdir)
                    shutil.copytree(subdir_path, dest_path, dirs_exist_ok=True)
                    print(f'Directory without "-hw3" in the name: {subdir}')

processor = DirectoryProcessor(directory, keyword)
processor.extract_zip_files()
processor.check_subdirectories()
