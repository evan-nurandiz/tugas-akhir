from tkinter import *
import tkinter
import requests
import json

def getDataFromApi(id):
    response = requests.post("http://127.0.0.1:8000/api/RaspberryPi/borrow-data", data=id)
    data = json.loads(response.text)
    return data

top1 = Tk()
lb = Listbox(top1)
cars = ["Ford", "Volvo", "BMW"]
id = {'id' : '2'}
book = getDataFromApi(id)
data = book['data']
print(book)
for x in range(len(data)):
    print(data[x])
    lb.insert(1, data[x]['title'])
lb.pack()
top1.mainloop()