import serial
import time

# --- CONFIGURATION ---
SERIAL_PORT = 'COM4'
BAUD_RATE = 115200
OUTPUT_FILENAME = 'DTS_Timecode_ROM_v1.46.bin'
READ_CHUNK_SIZE = 512
TIMEOUT_SECONDS = 1        # Prevents blocking indefinitely if data stops arriving

def read_serial_to_binary():
    print(f"Opening {SERIAL_PORT} at {BAUD_RATE} baud...")
    
    try:
        # Initialize the serial port connection
        ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT_SECONDS)
        
        # Flush the hardware buffers to start fresh
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Open file
        with open(OUTPUT_FILENAME, 'wb') as bin_file:
            print(f"Successfully connected. Saving incoming binary data to '{OUTPUT_FILENAME}'...")
            
            while True:
                # Check how many bytes are waiting in the queue
                bytes_waiting = ser.inWaiting()
                
                if bytes_waiting > 0:
                    # Read the incoming data (returns raw bytes)
                    # We read either the waiting size or our predefined chunk size
                    raw_data = ser.read(min(bytes_waiting, READ_CHUNK_SIZE))
                    
                    # Write directly to the binary file without any string conversions
                    bin_file.write(raw_data)
                    bin_file.flush() 
                    
                else:
                    # Small sleep to prevent high CPU utilization when idling
                    time.sleep(0.01)
                    
    except serial.SerialException as e:
        print(f"\nSerial Error: {e}. Please check your port and connections.")
    except KeyboardInterrupt:
        print("\nRecording stopped by user. File saved successfully.")
    finally:
        # Ensure the serial port is closed upon exit
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port connection closed.")

if __name__ == '__main__':
    read_serial_to_binary()
