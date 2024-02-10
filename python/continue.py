import sys

def press_any_key_to_continue_or_exit():
    """Prompt the user to press any key to continue or exit."""
    print("Press any key to continue or 'q' to exit.")
    key_pressed = input()

    if key_pressed.lower() == 'q':
        print("Exiting...")
        sys.exit()
    else:
        print("Continuing...")

# Example usage:
press_any_key_to_continue_or_exit()
