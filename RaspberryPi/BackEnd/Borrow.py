import requests
import json

headers = {'APP_KEY': 'B*Zeu>&HWg9`jx*j'}

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=3)
    print(text)

def getStudentData():
    id = str(input("rfid: "))
    rfid = {'rfid': id}
    response = requests.post("http://127.0.0.1:8000/api/RaspberryPi/find/student", data=rfid, headers=headers)
    data = jprint(response.json()['data'])
    return data


def getBookById(barcodeid):
    response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/find/book", data=barcodeid, headers=headers)
    data = json.loads(response.text)
    if (response.status_code == 404):
        return 0
    else:
        return data


def borrow(student):
    id = {'id': student[0]['id']}
    verify = verifyLastBorrow(id)
    if(verify != 0):
        bookId = []
        books = []
        barcode = ''
        while len(bookId) != 2:
            barcode = str(input("barcode: "))
            barcodeid = {'barcode': barcode}
            if barcode != 'send':
                data = getBookById(barcodeid)
                if(data == 0):
                    print('buku tidak ada')
                else:
                    data = data['data']
                    books.append(data)
                    bookId.append(data['id'])
        CollectData(student, books)


def CollectData(student, books):
    student_id = student[0]['id']
    book_id = []
    book = books
    for i in range(len(book)):
        data = (book[i]['id'])
        book_id.append(data)
    data = {
        'student_id': student_id,
        'type': 'borrow',
        'status': 'ongoing',
        'book_id': json.dumps(book_id),
    }
    # data = json.dumps(data)
    # print(data)
    sendData(data)


def sendData(data):
    response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow/store", data=data, headers=headers)
    print(response.text)

def verifyLastBorrow(id):
    response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow/history",data=id, headers=headers)
    data = json.loads(response.text)
    if (response.status_code == 404):
        print('riwayat peminjaman belum selesai')
        return 0
    else:
        return 1












