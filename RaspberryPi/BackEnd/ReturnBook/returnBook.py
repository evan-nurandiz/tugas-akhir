import requests
import json

headers = {'APP_KEY': 'B*Zeu>&HWg9`jx*j'}

def getDataFromApi(id):
    response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow-data", data=id, headers=headers)
    if (response.status_code == 404):
        print('anda tidak memiliki riwayat peminjaman')
        return 0
    else:
        data = json.loads(response.text)
        return data


def getBorrowData(student):
    student_id = student[0]['id']
    id = {'id' : student_id}
    data = getDataFromApi(id)
    if(data != 0):
        borrow_books = data['data']
        books = data['data']
        for i in range(len(books)):
            books[i]['status'] = 'false'
            print(borrow_books[i])
        returnStatus = 0
        while returnStatus == 0:
            entry = str(input("barcode: "))
            for key in books:
                if key['status'] == 'false':
                    if entry == key['barcode']:
                        key['status'] = 'true'
                        print(key)
                elif key['status'] == 'true':
                    returnStatus = 1
        updateBorrowData(id)
        print('buku berhasil dikembalikan')


def updateBorrowData(id):
    response = requests.post("http://127.0.0.1:8000/api/RaspberryPi/return", data=id, headers=headers)
    data = json.loads(response.text)
    return data



