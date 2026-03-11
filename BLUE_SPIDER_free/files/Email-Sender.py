import smtplib
import os
import time
from email.mime.text import MIMEText
from pwinput import pwinput 
MAX_MESSAGES = 10000 


VERT = "\033[32m"
RESET = "\033[0m"


original_print = print


def print(*args, **kwargs):
    original_print(VERT, end="")
    original_print(*args, **kwargs)
    original_print(RESET, end="\n")

    
logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@            

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)


RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    print("===  Email SPAMER Sender ===\n")

    sender = input("Enter YOUR email address: ")
    password = input("Enter your email APP PASSWORD: ")
    recipient = input("Enter the CLIENT email address: ")

    try:
        count = int(input(f"How many emails do you want to send ? (1 to {MAX_MESSAGES}): "))
    except ValueError:
        print("Invalid number.")
        return

    if count < 1 or count > MAX_MESSAGES:
        print(f"Error: You must choose between 1 and {MAX_MESSAGES} emails.")
        return

    subject = input("Email subject: ")
    body = input("Email message: ")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            print("\nConnecting to the email server...")
            server.login(sender, password)
            print("Connected successfully!\n")

            for i in range(count):
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = recipient

                
                print(f"{RED}Sending email {i+1}/{count}...{RESET}")

                server.send_message(msg)

                
                print(f"{GREEN}Email {i+1}/{count} sent successfully!{RESET}")

    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")


if __name__ == "__main__":
    main()
