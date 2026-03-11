import requests
import time
import json
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


def spam_webhook(webhook_url, message_content, count, delay=0.5):
    """
    Sends a message repeatedly to a Discord Webhook.

    :param webhook_url: The full Discord Webhook URL.
    :param message_content: The content of the message to send.
    :param count: The number of times to send the message.
    :param delay: Delay in seconds between each message to respect rate limits.
    """
    if not all([webhook_url, message_content, count]):
        print("Error: All parameters (URL, content, count) must be provided.")
        return

    
    payload = {
        "content": message_content
        
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    print(f"\n--- Starting Spamming ({count} times) ---")
    
    sent_count = 0
    
    for i in range(count):
        try:
            
            response = requests.post(webhook_url, headers=headers, json=payload)
            
           
            if response.status_code == 204:
                sent_count += 1
                print(f"[{i + 1}/{count}] Message sent successfully.")
            
            
            elif response.status_code == 429:
                data = response.json()
                retry_after = data.get('retry_after', 1) / 1000.0  
                print(f"RATE LIMITED! Waiting for {retry_after:.2f} seconds before retrying...")
                time.sleep(retry_after)
               
                continue 
            
            
            else:
                print(f"[{i + 1}/{count}] ERROR: Failed to send message (Status: {response.status_code}).")
                print("Response content:", response.text)
                
                break

        except requests.exceptions.RequestException as e:
            print(f"[{i + 1}/{count}] Connection Error: {e}")
            break
        
        
        time.sleep(delay)

    print(f"\n--- Spamming Finished ---")
    print(f"Total successful messages sent: {sent_count}")
    print(f"Total attempts: {count}")
    



print("--- DISCORD WEBHOOK SPAMMER TOOL ---")


WEBHOOK_LINK = input("Enter the full Discord Webhook URL: ")
MESSAGE_CONTENT = input("Enter the message content to send: ")

while True:
    try:
       
        MESSAGE_COUNT = int(input("Enter the number of times to send the message: "))
        if MESSAGE_COUNT <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


spam_webhook(WEBHOOK_LINK, MESSAGE_CONTENT, MESSAGE_COUNT)