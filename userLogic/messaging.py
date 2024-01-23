import eel

eel.init('gui')  # Folder containing your HTML, CSS, and JavaScript files

@eel.expose
def send_message(message):
    # This function receives the message from the Python side
    # Add your logic to handle the message
    print(f"Received message: {message}")
    eel.showmsg(message)

# Start the Eel application
try:
    eel.start('index.html', size=(700, 500), mode='chrome', port=0)
except (SystemExit, MemoryError, KeyboardInterrupt):
    # Handle exceptions when the Eel application is closed
    pass
except Exception as e:
    # Print other exceptions for troubleshooting
    print(f"Error: {e}")

