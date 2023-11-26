
class HardwareInterface:
    def __init__(self):
        # Set up serial connection
        # Obtain status from arduino
        # Set the locked attribute accordingly
        self.locked = False

    def lock(self):
        # Send lock command to arduino, wait for confirmation, then set locked attribute
        self.locked = True
        # Return True if successful, False otherwise
        return True

    def unlock(self):
        # Send unlock command to arduino, wait for confirmation, then set locked attribute
        self.locked = False

        # Return True if successful, False otherwise
        return True

    def is_locked(self):
        return self.locked
    
# Mimicking singleton pattern through exporting a single instance:
hw = HardwareInterface()

