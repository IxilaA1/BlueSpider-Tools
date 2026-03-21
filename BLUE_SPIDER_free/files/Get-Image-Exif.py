# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import piexif
import exifread
import base64
import os
import tkinter
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from tkinter import filedialog
import time
import sys
import webbrowser

logo_ascii = """
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@00@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+00+--+%@#::#@%*--+00+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*0@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)



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

    def ConvertToDegrees(value):
        """
        Convert GPS coordinates from degrees/minutes/seconds format to decimal degrees.
        """
        try:
            # Handle different formats
            if isinstance(value, tuple) or isinstance(value, list):
                if len(value) >= 3:
                    # Format: (degrees, minutes, seconds)
                    degrees = float(value[0])
                    minutes = float(value[1])
                    seconds = float(value[2])
                    return degrees + (minutes / 60.0) + (seconds / 3600.0)
            elif isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                # Try to parse string format
                parts = value.replace('(', '').replace(')', '').split(',')
                if len(parts) >= 3:
                    degrees = float(parts[0].strip())
                    minutes = float(parts[1].strip())
                    seconds = float(parts[2].strip())
                    return degrees + (minutes / 60.0) + (seconds / 3600.0)
        except:
            pass
        return None

    def GetGPSFromExif(exif_data):
        """
        Extract GPS coordinates from EXIF data.
        """
        gps_latitude = None
        gps_longitude = None
        gps_latitude_ref = None
        gps_longitude_ref = None
        
        # Check if GPSInfo exists
        if 'GPSInfo' in exif_data:
            gps_info = exif_data['GPSInfo']
            
            # GPS tags mapping
            # 1: GPSLatitudeRef, 2: GPSLatitude, 3: GPSLongitudeRef, 4: GPSLongitude
            if isinstance(gps_info, dict):
                for tag_id, value in gps_info.items():
                    tag_name = GPSTAGS.get(tag_id, tag_id)
                    
                    if tag_name == 'GPSLatitudeRef':
                        if isinstance(value, bytes):
                            gps_latitude_ref = value.decode('utf-8')
                        else:
                            gps_latitude_ref = str(value)
                    elif tag_name == 'GPSLatitude':
                        gps_latitude = value
                    elif tag_name == 'GPSLongitudeRef':
                        if isinstance(value, bytes):
                            gps_longitude_ref = value.decode('utf-8')
                        else:
                            gps_longitude_ref = str(value)
                    elif tag_name == 'GPSLongitude':
                        gps_longitude = value
            elif isinstance(gps_info, (tuple, list)) and len(gps_info) >= 4:
                # Some formats store GPS data as a tuple/list
                gps_latitude_ref = gps_info[0] if len(gps_info) > 0 else None
                gps_latitude = gps_info[1] if len(gps_info) > 1 else None
                gps_longitude_ref = gps_info[2] if len(gps_info) > 2 else None
                gps_longitude = gps_info[3] if len(gps_info) > 3 else None
        
        # Convert to decimal if we have the data
        if gps_latitude and gps_longitude:
            lat = ConvertToDegrees(gps_latitude)
            lon = ConvertToDegrees(gps_longitude)
            
            if lat and lon:
                # Apply reference direction
                if gps_latitude_ref and gps_latitude_ref.upper() == 'S':
                    lat = -lat
                if gps_longitude_ref and gps_longitude_ref.upper() == 'W':
                    lon = -lon
                
                return lat, lon
        
        return None, None

    def FormatGPSLink(latitude, longitude):
        """
        Create Google Maps links from decimal coordinates.
        """
        if latitude is not None and longitude is not None:
            google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            openstreetmap_link = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"
            bing_maps_link = f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=15"
            
            return {
                'google': google_maps_link,
                'openstreetmap': openstreetmap_link,
                'bing': bing_maps_link
            }
        return None

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
            # For GPS coordinates, keep them as they are for processing
            if len(value) == 3 and all(isinstance(v, (int, float)) for v in value):
                return value
            return ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            return {k: CleanValue(v) for k, v in value.items()}
        else:
            return value
            
    def GetAllExif(image_path):
        """
        Extracts all available EXIF and file metadata.
        """
        exif_data = {}
        latitude = None
        longitude = None
        
        # Method 1: Use PIL to get EXIF data
        try:
            image = Image.open(image_path)
            exif_info = image._getexif()
            
            if exif_info:
                for tag_id, value in exif_info.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    exif_data[tag_name] = value
                
                # Extract GPS coordinates from PIL data
                if 'GPSInfo' in exif_data:
                    lat, lon = GetGPSFromExif(exif_data)
                    if lat and lon:
                        latitude = lat
                        longitude = lon
        except Exception as e:
            pass
        
        # Method 2: Use piexif for more detailed extraction
        try:
            exif_dict = piexif.load(image_path)
            
            # Process all IFD data
            for ifd in exif_dict:
                if isinstance(exif_dict[ifd], dict):
                    for tag in exif_dict[ifd]:
                        tag_name = piexif.TAGS.get(ifd, {}).get(tag, {"name": str(tag)})["name"]
                        raw_value = exif_dict[ifd][tag]
                        
                        if tag_name not in exif_data:
                            exif_data[tag_name] = CleanValue(raw_value)
                        
                        # Check for GPS data in GPS IFD
                        if ifd == 'GPS' and tag_name in ['GPSLatitude', 'GPSLongitude']:
                            if tag_name == 'GPSLatitude':
                                gps_lat_value = raw_value
                                gps_lat_ref = exif_dict['GPS'].get(1, 'N')
                                if isinstance(gps_lat_ref, bytes):
                                    gps_lat_ref = gps_lat_ref.decode('utf-8')
                                lat = ConvertToDegrees(gps_lat_value)
                                if lat:
                                    if gps_lat_ref and gps_lat_ref.upper() == 'S':
                                        lat = -lat
                                    latitude = lat
                            elif tag_name == 'GPSLongitude':
                                gps_lon_value = raw_value
                                gps_lon_ref = exif_dict['GPS'].get(3, 'E')
                                if isinstance(gps_lon_ref, bytes):
                                    gps_lon_ref = gps_lon_ref.decode('utf-8')
                                lon = ConvertToDegrees(gps_lon_value)
                                if lon:
                                    if gps_lon_ref and gps_lon_ref.upper() == 'W':
                                        lon = -lon
                                    longitude = lon
        except Exception as e:
            pass
        
        # Method 3: Use exifread as fallback
        if latitude is None or longitude is None:
            try:
                with open(image_path, 'rb') as f:
                    tags = exifread.process_file(f, details=True)
                    for tag in tags:
                        tag_name = tag.split()[-1] if ' ' in tag else tag
                        
                        # Look for GPS tags
                        if 'GPS' in tag:
                            if 'Latitude' in tag and 'Ref' not in tag:
                                lat_value = tags[tag]
                                lat_ref_tag = tag.replace('Latitude', 'LatitudeRef')
                                if lat_ref_tag in tags:
                                    lat_ref = str(tags[lat_ref_tag])
                                    lat = ConvertToDegrees(str(lat_value))
                                    if lat:
                                        if lat_ref and lat_ref.upper() == 'S':
                                            lat = -lat
                                        latitude = lat
                            elif 'Longitude' in tag and 'Ref' not in tag:
                                lon_value = tags[tag]
                                lon_ref_tag = tag.replace('Longitude', 'LongitudeRef')
                                if lon_ref_tag in tags:
                                    lon_ref = str(tags[lon_ref_tag])
                                    lon = ConvertToDegrees(str(lon_value))
                                    if lon:
                                        if lon_ref and lon_ref.upper() == 'W':
                                            lon = -lon
                                        longitude = lon
                        
                        # Add to exif_data if not already present
                        if tag_name not in exif_data:
                            exif_data[tag_name] = CleanValue(str(tags[tag]))
            except Exception as e:
                pass
        
        # Get image dimensions
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                depth = len(img.getbands())
                exif_data['Dimension'] = f"{width}x{height}"
                exif_data['Width'] = width
                exif_data['Height'] = height
                exif_data['Depth'] = depth
        except Exception as e:
            pass
        
        # Add file system information
        try:
            file_stats = os.stat(image_path)
            exif_data['File Name'] = os.path.basename(image_path)
            exif_data['File Type'] = os.path.splitext(image_path)[1]
            exif_data['File Size'] = f"{file_stats.st_size:,} bytes"
            exif_data['Creation Date'] = time.ctime(file_stats.st_ctime)
            exif_data['Date Modified'] = time.ctime(file_stats.st_mtime)
            exif_data['File Mode'] = oct(file_stats.st_mode)
            exif_data['Read Access'] = 'Yes' if os.access(image_path, os.R_OK) else 'No'
            exif_data['File Exists'] = 'Yes' if os.path.exists(image_path) else 'No'
        except Exception as e:
            pass
        
        # Add GPS coordinates and map links if found
        if latitude is not None and longitude is not None:
            exif_data['GPS Latitude'] = f"{latitude:.6f}°"
            exif_data['GPS Longitude'] = f"{longitude:.6f}°"
            exif_data['GPS Coordinates'] = f"{latitude:.6f}, {longitude:.6f}"
            
            # Generate map links
            map_links = FormatGPSLink(latitude, longitude)
            if map_links:
                exif_data['Google Maps Link'] = map_links['google']
                exif_data['OpenStreetMap Link'] = map_links['openstreetmap']
                exif_data['Bing Maps Link'] = map_links['bing']
        
        # Display all extracted information
        if exif_data:
            # Filter out technical tags that might not be needed
            display_data = {k: v for k, v in exif_data.items() if k not in ['ExifOffset', 'ExifTag', 'GPSTag', 'GPSInfo']}
            
            if display_data:
                max_key_length = max(len(k) for k in display_data.keys()) if display_data.keys() else 0
                
                print(f"\n{white}========================================================================================================================")
                print(f" {INFO_ADD} EXIF DATA EXTRACTED FROM: {os.path.basename(image_path)}")
                print(f"{white}========================================================================================================================\n")
                
                for key, value in sorted(display_data.items(), key=lambda x: x[0].lower()):
                    # Skip internal tags that we've already filtered
                    if key in ['ExifOffset', 'ExifTag', 'GPSTag', 'GPSInfo']:
                        continue
                    
                    # Format the value nicely
                    if isinstance(value, (tuple, list)) and len(value) == 3:
                        value_str = f"({value[0]}, {value[1]}, {value[2]})"
                    else:
                        value_str = str(value)
                    
                    print(f" {INFO_ADD} {key.ljust(max_key_length)} : {white + value_str}")
                    time.sleep(0.01)
                
                print(f"{white}========================================================================================================================\n")
                
                # Offer to open map links if GPS coordinates are found
                if latitude is not None and longitude is not None:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} GPS Coordinates Found!")
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Location: {latitude:.6f}, {longitude:.6f}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Would you like to open the location in Google Maps? (y/n): ", end="")
                    choice = input().strip().lower()
                    if choice == 'y':
                        webbrowser.open(map_links['google'])
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No readable EXIF information found.")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No EXIF information found in this image.")

    Slow(osint_banner)
    image_path = ChooseImageFile()
    
    if image_path:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching for EXIF information in the image...")
        GetAllExif(image_path)
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No image file selected or path provided. Exiting.")
        
    Continue()
    Reset()
    
except Exception as e:
    Error(e)