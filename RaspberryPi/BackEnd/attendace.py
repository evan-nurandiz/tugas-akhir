import requests
import json
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522


headers = {'APP_KEY': 'B*Zeu>&HWg9`jx*j'}

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# def ReadRfid():
#     reader = SimpleMFRC522()
#     try:
#         id, text = reader.read()
#         print(id)
#         print(text)
#     finally:
#         GPIO.cleanup()
#         rfid = str(id)
#         return rfid



def attempt(rfid):
    response = requests.post("https://perpustakaan-elektro.my.id/api/raspberry/visitor", data=rfid, headers=headers)
    if (response.status_code == 404):
        return 0
    else:
        return 1


def getStudentData():
    student = []
    rfid = str(input("rfid: "))
    rfid = {'rfid': rfid}
    response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/find/student", data=rfid, headers=headers)
    data = json.loads(response.text)
    if(response.status_code == 404):
        print('mahasiswa tidak ditemukan')
        student = 0
        return  student
    else:
        data = data['data']
        student.append(data)
        return student







