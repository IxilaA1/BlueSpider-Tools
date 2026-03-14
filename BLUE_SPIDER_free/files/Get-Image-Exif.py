import piexif
import exifread
import base64
import os
import tkinter
from PIL import Image
from tkinter import filedialog
import time
import sys




def ErrorModule(e):
    print(f"ERROR: Failed to import module: {e}")

def Title(title_text):
    print(f"\n--- {title_text} ---\n")

def current_time_hour():
    return time.strftime("%H:%M:%S")


BEFORE = "[LOG "
AFTER = "]"
INPUT = "[INPUT]"
INFO = "[INFO]"
WAIT = "[WAIT]"
ERROR = "[ERROR]"
INFO_ADD = "[DATA]"
reset = ""
white = ""
name_tool = "EXIF Extractor"
version_tool = "1.0"
osint_banner = "--- Image EXIF Analysis ---"

def Slow(text):
    print(text)

def Continue():
    input("\nPress Enter to continue...")

def Reset():
    pass

def Error(e):
    print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")


Title("Get Image Exif")

try:
    def ChooseImageFile():
        """
        Opens a file dialog for selecting an image file, or falls back to
        command-line input if the dialog fails.
        """
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")
            
            
            image_file_types = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"), ("All files", "*.*")]

            file = ""
            
            
            if sys.platform.startswith("win"):
                root = tkinter.Tk()

                root.withdraw()
                root.attributes('-topmost', True)
                file = filedialog.askopenfilename(parent=root, title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
                root.destroy()
            else:
                
                root = tkinter.Tk()
                root.withdraw()
                file = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
                root.destroy()
            
            
            if file:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File path: {white + file}")
                return file
            else:
                 
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File selection canceled. Falling back to manual input.")
                return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")

        except Exception as e:
            
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File dialog failed ({e}). Falling back to manual input.")
            return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")


    def CleanValue(value):
        """
        Cleans up raw EXIF values, decoding bytes to strings or formatting lists/tuples.
        """
        if isinstance(value, bytes):
            try:
                
                return value.decode('utf-8', errors='replace')
            except:
                
                return base64.b64encode(value).decode('utf-8')
        elif isinstance(value, (list, tuple)):
            
            return ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            
            return {k: CleanValue(v) for k, v in value.items()}
        else:
            
            return value
            
    def GetAllExif(image_path):
        """
        Extracts all available EXIF and file metadata using piexif, exifread, PIL, and os.
        """
        exif_data = {}

        
        try:
            exif_dict = piexif.load(image_path)
            for ifd in exif_dict:
                if isinstance(exif_dict[ifd], dict):
                    for tag in exif_dict[ifd]:
                        
                        tag_name = piexif.TAGS.get(ifd, {}).get(tag, {"name": tag})["name"]
                        raw_value = exif_dict[ifd][tag]
                        

                        if tag_name not in exif_data:
                            exif_data[f"{tag_name}"] = CleanValue(raw_value)
        except Exception as e:

            pass

        
        try:
            with open(image_path, 'rb') as f:
                
                tags = exifread.process_file(f, details=True)
                for tag in tags:
                    
                    label = tag.split()[-1]
                    
                    if label not in exif_data:
                        exif_data[label] = CleanValue(str(tags[tag]))
        except Exception as e:
            
            pass
            
        
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                depth = len(img.getbands())
                exif_data['Dimension'] = f"{width}x{height}"
                exif_data['Width'] = width
                exif_data['Height'] = height
                exif_data['Depth'] = depth
        except Exception as e:
            exif_data["Image Error"] = f"Could not open image file: {str(e)}"

        

        
        try:
            file_stats = os.stat(image_path)
            exif_data['Name'] = os.path.basename(image_path)
            exif_data['Type'] = os.path.splitext(image_path)[1]
            
            exif_data['Creation Date'] = time.ctime(file_stats.st_ctime)
            exif_data['Date Modified'] = time.ctime(file_stats.st_mtime)
            exif_data['Attributes (Mode)'] = oct(file_stats.st_mode)
            
            exif_data['Availability'] = 'Available (Read Access)' if os.access(image_path, os.R_OK) else 'Not available (No Read Access)'
            exif_data['Offline Status'] = 'Online (Exists)' if os.path.exists(image_path) else 'Offline (Does not Exist)'
        except Exception as e:
            exif_data["File Stats Error"] = str(e)
            
        
        if exif_data:
            
            max_key_length = max(len(k) for k in exif_data.keys()) if exif_data.keys() else 0

            print(f"\n{white}------------------------------------------------------------------------------------------------------------------------")
            
            for key, value in sorted(exif_data.items(), key=lambda x: x[0].lower()):
                
                print(f" {INFO_ADD} {key.ljust(max_key_length)} : {white + str(value)}")
                time.sleep(0.01)
            print(f"{white}------------------------------------------------------------------------------------------------------------------------\n")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No information found.")

    Slow(osint_banner)
    image_path = ChooseImageFile()
    
    
    if image_path:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching for information in the image roots...")
        GetAllExif(image_path)
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No image file selected or path provided. Exiting.")
        
    Continue()
    Reset()
    
except Exception as e:
    
    Error(e)