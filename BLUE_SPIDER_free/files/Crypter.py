import hashlib
import os

def process_file():
    """Handles the user input and the file encryption/decryption process."""

    
    print("--- File Processor ---")
    while True:
        mode = input("Select operation (E for Encrypt, D for Decrypt): ").upper()
        if mode in ('E', 'D'):
            break
        print("Invalid selection. Please enter 'E' or 'D'.")

    operation = "Encryption" if mode == 'E' else "Decryption"
    print(f"\nSelected operation: **{operation}**")
    print("----------------------")



    input_path = input("Enter the exact path of the file to process (e.g., C:\\Users\\...\\file.txt): ")
    
    
    output_name = input("Enter the desired name for the output file: ")
    
    
    key = input("Enter the secret key: ")
    

    keys = hashlib.sha256(key.encode('utf-8')).digest()
    
    
    try:
        
        input_directory = os.path.dirname(input_path)
        if not input_directory:
             
             input_directory = os.getcwd() 

        
        output_path = os.path.join(input_directory, output_name)

    except Exception as e:
        print(f"\n Error resolving file paths: {e}")
        return

    
    print(f"\nProcessing file: {input_path}")
    print(f"Saving output to: {output_path}")

    try:
        
        with open(input_path, 'rb') as f_input:
           
            with open(output_path, 'wb') as f_output:
                i = 0  
                
                
                while True:
                    
                    read_byte = f_input.read(1)
                    
                    
                    if not read_byte:
                        break
                    
                    
                    c = ord(read_byte)
                    
                    
                    j = i % len(keys)
                    
                    
                    
                    b = bytes([c ^ keys[j]])
                    
                    
                    f_output.write(b)
                    
                    
                    i = i + 1
            
        print(f"\n Operation {operation} completed successfully!")
        print(f"The file '{output_name}' has been created in the directory: {input_directory}")

    except FileNotFoundError:
        print(f"\n Error: The input file was not found at the specified location: {input_path}")
    except Exception as e:
        print(f"\n An unexpected error occurred during file processing: {e}")


if __name__ == "__main__":
    process_file()