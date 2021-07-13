import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def ReadRfid():
        reader = SimpleMFRC522()

        try:
                id, text = reader.read()
                print(id)
                print(text)
        finally:
                GPIO.cleanup()
                rfid = str(id)
                return rfid