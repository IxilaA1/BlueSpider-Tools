# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import time
import sys
import os

    
logo_ascii = """
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@             

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)


def send_webhook_message_sequentially(webhook_url, data, current_send, total_sends, webhook_index, num_webhooks):
    """
    Attempts to send a message and handles rate limiting (429) errors.
    """
    attempt = 0
    max_attempts = 5
    
    while attempt < max_attempts:
        attempt += 1
        try:
            sys.stdout.write(f"Sending {current_send}/{total_sends} [Webhook {webhook_index}/{num_webhooks}] (Attempt {attempt})... \r")
            sys.stdout.flush()

            response = requests.post(webhook_url, json=data)
            
            
            if response.status_code == 204:
                print(f"SUCCESS: Send {current_send}/{total_sends} via Webhook {webhook_index} completed.                              ")
                return True
            
            
            elif response.status_code == 429:
                try:
                    error_data = response.json()
                    wait_time = error_data.get("retry_after", 1.0) 
                    
                    print(f"RATE LIMITED: Send {current_send}/{total_sends}. Waiting {wait_time:.3f}s (Attempt {attempt}/{max_attempts})...")
                    time.sleep(wait_time)
                
                except Exception:
                    print(f"RATE LIMITED: Send {current_send}/{total_sends}, JSON error. Waiting 1s (Attempt {attempt}/{max_attempts})...")
                    time.sleep(1)
            
            
            else:
                print(f"FAILURE: Send {current_send}/{total_sends} on Webhook {webhook_index}. Error {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"CONNECTION ERROR: Send {current_send}/{total_sends}. Exception occurred: {e}")
            return False
            
    print(f"FINAL FAILURE: Send {current_send}/{total_sends} on Webhook {webhook_index} failed after {max_attempts} attempts.")
    return False




bot_name = input("Bot Name: ")
message = input("Message to send: ")


avatar_url = input("Bot Avatar URL (optional, leave blank to use default): ") 


webhook_input = input("Discord Webhook URL(s) (separate by commas or spaces): ")

webhook_urls = [url.strip() for url in webhook_input.replace(',', ' ').split() if url.strip()]

if not webhook_urls:
    print("No webhook URL provided. Exiting script.")
    sys.exit(1)

num_webhooks = len(webhook_urls)
print(f"SUCCESS: {num_webhooks} Webhook(s) detected for sending.")


try:
    num_sends = int(input("Total number of messages to send: "))
    if num_sends <= 0:
        print("The number of sends must be greater than zero.")
        sys.exit(1)
except ValueError:
    print("Invalid input. The number of sends must be an integer.")
    sys.exit(1)


data = {
    "username": bot_name,
    "content": message
}


if avatar_url:
    data["avatar_url"] = avatar_url
    print(f"INFO: Using custom avatar URL: {avatar_url}")
else:
    print("INFO: Using webhook's default avatar.")


print(f"\nStarting sequential send of {num_sends} messages, distributed over {num_webhooks} webhook(s).")

for i in range(num_sends):
    webhook_index_to_use = i % num_webhooks
    current_webhook_url = webhook_urls[webhook_index_to_use]
    
    send_webhook_message_sequentially(
        current_webhook_url, 
        data, 
        i + 1, 
        num_sends, 
        webhook_index_to_use + 1,
        num_webhooks
    )

print("\nSequential multi-webhook operation completed.")