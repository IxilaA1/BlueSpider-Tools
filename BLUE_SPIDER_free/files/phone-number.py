import phonenumbers
from phonenumbers import geocoder, carrier, timezone



def Title(title_text):
    print(f"--- {title_text} ---")


def current_time_hour():
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")

BEFORE = "["
AFTER = "]"
INPUT_PROMPT = "INPUT"
WAIT_MESSAGE = "WAIT"
INFO_MESSAGE = "INFO"
ERROR_MESSAGE = "ERROR"
RESET_COLOR = "\033[0m"
WAIT_COLOR = "\033[33m"
INFO_COLOR = "\033[36m"
ERROR_COLOR = "\033[31m"
WHITE_COLOR = "\033[97m"
RED_COLOR = "\033[31m"

def Slow(text):
    print(text)

def Continue():
    input("\nPress Enter to continue...")

def Reset():
    pass

Title("Phone Number Lookup")

try:
    
    phone_number = input(f"\n{BEFORE}{current_time_hour()}{AFTER} {INPUT_PROMPT} Phone Number -> {RESET_COLOR}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT_COLOR}{WAIT_MESSAGE}{RESET_COLOR} Information Retrieval...{RESET_COLOR}")
    
    try:
        
        parsed_number = phonenumbers.parse(phone_number, None)
        
        if phonenumbers.is_valid_number(parsed_number):
            status = "Valid"
        else:
            status = "Invalid"


        if phone_number.startswith("+"):
            
            country_code = "+" + str(parsed_number.country_code)
        else:
            country_code = "None (No + prefix)"
            
        
        try: operator = carrier.name_for_number(parsed_number, "en")
        except: operator = "None"
        
        
        try: 
            if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE:
                type_number = "Mobile"
            elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.FIXED_LINE:
                type_number = "Fixed Line"
            else:
                type_number = str(phonenumbers.number_type(parsed_number)).split('.')[-1]
        except: type_number = "None"

        try: 
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = ", ".join(timezones) if timezones else "None"
        except: timezone_info = "None"
            
        try: country = phonenumbers.region_code_for_number(parsed_number)
        except: country = "None"
            
        
        try: region = geocoder.description_for_number(parsed_number, "en")
        except: region = "None"
            
        try: formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except: formatted_number = "None"
            
        
        INFO_ADD = INFO_COLOR + "ⓘ" + RESET_COLOR
        
        Slow(f"""
{WHITE_COLOR}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Phone              : {WHITE_COLOR}{phone_number}{RED_COLOR}
 {INFO_ADD} Formatted          : {WHITE_COLOR}{formatted_number}{RED_COLOR}
 {INFO_ADD} Status             : {WHITE_COLOR}{status}{RED_COLOR}
 {INFO_ADD} Country Code (E.164): {WHITE_COLOR}{country_code}{RED_COLOR}
 {INFO_ADD} Country (Region)   : {WHITE_COLOR}{country}{RED_COLOR}
 {INFO_ADD} Region/Location    : {WHITE_COLOR}{region}{RED_COLOR}
 {INFO_ADD} Timezone(s)        : {WHITE_COLOR}{timezone_info}{RED_COLOR}
 {INFO_ADD} Operator/Carrier   : {WHITE_COLOR}{operator}{RED_COLOR}
 {INFO_ADD} Number Type        : {WHITE_COLOR}{type_number}{RED_COLOR}
{WHITE_COLOR}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")
        Continue()
        Reset()
    except Exception:
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO_COLOR}{INFO_MESSAGE}{RESET_COLOR} Invalid Format or Number Cannot Be Parsed!")
        Continue()
        Reset()
except Exception as e:
    print(f"{ERROR_COLOR}{ERROR_MESSAGE}: {e}{RESET_COLOR}")