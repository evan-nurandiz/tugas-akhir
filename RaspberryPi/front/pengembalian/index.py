import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox as mb
import requests
import json
from RaspberryPi.BackEnd.ReturnBook.returnBook import getDataFromApi
import numpy as np


class PengembalianPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.headers = {'APP_KEY': 'B*Zeu>&HWg9`jx*j'}
        self.student_name = tk.StringVar()
        self.controller = controller
        self.borrow_book_barcode = []
        self.return_book_barcode = []
        self.barocode = tk.StringVar()
        self.book = []
        self.student = []

        heading_label = tk.Label(self,
                                 text='Pengembalian Buku',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        # TOMBOL BUTTON
        button_frames = tk.Frame(self, bg='#33334d')
        button_frames.pack(fill='both', expand=True)

        get_data = tk.Button(button_frames,
                                command=self.getStudentInfo,
                                text='Scan Rfid',
                                relief='raised',
                                borderwidth=3,
                                width=10,
                                height=2).pack()

        lb = tk.Label(self, height=1, width=20, textvariable=self.student_name)
        lb.pack(padx=5, pady=10)

        book_borrow = tk.Label(self, text='Buku yang dipinjam')
        book_borrow.pack()
        self.lb_borrow = tk.Listbox(self,  width=20, height=4)
        self.lb_borrow.pack(padx=1, pady=5)

        self.entryNum1 = tk.Entry(self, textvar=self.barocode)
        self.entryNum1.pack(expand=2, padx=20, pady=4)

        button_frames2 = tk.Frame(self, bg='#33334d')
        button_frames2.pack(fill='both', expand=True,)

        get_data = tk.Button(button_frames2,
                             command=self.GetBookBybarcode,
                             text='Scan Buku',
                             relief='raised',
                             borderwidth=3,
                             width=10,
                             height=2).pack()

        book_scan = tk.Label(self, text='Buku yang discan')
        book_scan.pack()

        self.lb2 = tk.Listbox(self, width=20, height=4)
        self.lb2.pack(padx=5, pady=10)

        # TOMBOL BUTTON
        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)


        back_button = tk.Button(button_frame,
                                command=self.back,
                                text='Back',
                                relief='raised',
                                borderwidth=3,
                                width=10,
                                height=2)
        back_button.grid(row=0, column=0)

        send_frame = tk.Frame(self, bg='#33334d')
        send_frame.pack(fill='both', expand=True)

        send_button = tk.Button(send_frame,
                                command=self.compare,
                                text='Confirm',
                                relief='raised',
                                borderwidth=3,
                                width=10,
                                height=2)
        send_button.grid(row=0, column=1)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')


        self.time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        self.time_label.pack(side='right')

        self.tick()

    def back(self):
        self.lb_borrow.delete(0,tk.END)
        self.student_name.set('')
        self.controller.show_frame('MenuPage')
        self.borrow_book_barcode.clear()


    def GetBookBybarcode(self):
        if(len(self.student) == 0 and self.student_name):
            mb.showinfo('status', 'anda belum memindai RFID')
            self.barocode.set('')
        else:
            i = 0
            barcode_id = self.entryNum1.get()
            barcode = {'barcode': barcode_id}
            response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/find/book", data=barcode,
                                     headers=self.headers)
            data = json.loads(response.text)
            if (response.status_code == 404):
                mb.showinfo('status', 'Buku tidak ada')
            else:
                if(len(self.book) <= 2):
                    self.book.append(data['data'])
                    book_info = data['data']
                    self.lb2.insert(i,book_info['title'])
                    self.return_book_barcode.append(book_info['barcode'])
                    ++i
                    print(self.return_book_barcode)
                else:
                    mb.showinfo('status', 'maksimal peminjaman 2 buku')
            self.barocode.set('')

    def getStudentInfo(self, send_frame=None):

        rfid = str('1A2B3B')
        rfid = {'rfid': rfid}
        response = requests.post('https://perpustakaan-elektro.my.id/api/RaspberryPi/find/student', data=rfid,
                                 headers=self.headers)
        data = json.loads(response.text)
        if response.status_code == 404:
            print('mahasiswa tidak ditemukan')
            student = 0
            return student
        else:
            data = data['data']
            print(data['name'])
            id = {'id': data['id']}
            response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow-data", data=id,
                                     headers=self.headers)
            if (response.status_code == 404):
                print('anda tidak memiliki riwayat peminjaman')
                mb.showinfo('status', 'anda belum tidak memiliki riwayat perminjaman')
                return 0
            else:
                self.student_name.set(data['name'])
                self.student.append(data)
                data = json.loads(response.text)
                book = data['data']
                for i in range(len(book)):
                    self.borrow_book_barcode.append(book[i]['barcode'])
                    self.lb_borrow.insert([i],book[i]['title'])
                    print(book[i])
                print(self.borrow_book_barcode)

    def compare(self):
        if (len(self.student) == 0 and self.student_name and
                len(self.borrow_book_barcode and self.return_book_barcode) ==0):
            mb.showinfo('status', 'data belum lengkap')
        else:
            id = {'id': self.student[0]['id']}
            return_book = self.return_book_barcode
            borrow_book = self.borrow_book_barcode
            a = np.array_equal(return_book, borrow_book)
            print(a)
            if a is True:
                response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/return", data=id,
                                         headers=self.headers)
                data = json.loads(response.text)
                if data:
                    mb.showinfo('status', 'pengembalian berhasil')
                else:
                    mb.showinfo('status', 'pengembalian gagal')
            else:
                mb.showinfo('status', 'buku tidak sama')




    def tick(self):
        current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
        self.time_label.config(text=current_time)
        self.time_label.after(200,self.tick)





