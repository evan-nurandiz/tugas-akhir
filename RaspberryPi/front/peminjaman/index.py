import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox as mb
# from RaspberryPi.BackEnd.attendace import getStudentData
import requests
import json
import asyncio


class PeminjamanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.headers = {'APP_KEY': 'B*Zeu>&HWg9`jx*j'}
        self.student_name = tk.StringVar()
        self.controller = controller
        self.barocode = tk.StringVar()
        self.book = []
        self.student = []
        self.book_id = []

        heading_label = tk.Label(self,
                                 text='Peminjaman Buku',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        # TOMBOL BUTTON
        button_frames = tk.Frame(self, bg='#3d3d5c')
        button_frames.pack(fill='both', pady=10)

        scan_rfid_button = tk.Button(button_frames,
                             command=self.getStudentInfo,
                             text='Scan Rfid',
                             relief='raised',
                             borderwidth=3,
                             width=10,
                             height=2).pack()

        lb = tk.Label(self, height=2, width=20, textvariable=self.student_name)
        lb.pack(padx=5, pady=10)

        # TOMBOL BUTTON
        button_frames2 = tk.Frame(self,bg='#3d3d5c')
        button_frames2.pack(fill='both', pady=10)

        scan_book_button = tk.Button(button_frames2,
                             command=self.GetBookBybarcode,
                             text='Scan Buku',
                             relief='raised',
                             borderwidth=3,
                             width=10,
                             height=2).pack()


        self.entryNum1 = tk.Entry(self, textvar=self.barocode)
        self.entryNum1.pack(expand=2, padx=20, pady=4)

        button_frames3 = tk.Frame(self, bg='#3d3d5c')
        button_frames3.pack(fill='both', pady=10)

        delete_button = tk.Button(button_frames3,
                             command=self.deleteRow,
                             text='hapus tabel',
                             relief='raised',
                             borderwidth=3,
                             width=10,
                             height=2).pack()

        frame = tk.Frame(self)
        frame.pack()



        self.tree = ttk.Treeview(frame, columns=(1, 2,3), height=5, show="headings")
        self.tree.pack(side='left')
        self.tree.heading(1, text="Penulis")
        self.tree.heading(2, text="Nama Buku")
        self.tree.heading(3, text="aksi")
        self.tree.column(1, width=300)
        self.tree.column(2, width=300)
        self.tree.column(3, width=100)

        # TOMBOL BUTTON
        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both')

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
                                command=self.CollectBorrow,
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

    def getStudentInfo(self):
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
            id = {'id': data['id']}
            verify = self.verifyLastBorrow(id)
            if(verify!=0):
                self.student_name.set(data['name'])
                self.student.append(data)
                print(data['name'])


    def GetBookBybarcode(self):
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
                self.tree.insert('', 'end', values=(book_info['writter'], book_info['title']))
                print(self.book)
            else:
                mb.showinfo('status', 'maksimal peminjaman 2 buku')
        self.barocode.set('')

    def CollectBorrow(self):
        if(len(self.student) and len(self.book) != 0):
            student_id = self.student[0]['id']
            self.book_id = []
            book = self.book
            for i in range(len(book)):
                data = (book[i]['id'])
                self.book_id.append(data)
            data = {
                'student_id': student_id,
                'type': 'borrow',
                'status': 'ongoing',
                'book_id': json.dumps(self.book_id),
            }
            response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow/store", data=data,
                                     headers=self.headers)
            if(response.text):
                mb.showinfo('status', 'peminjaman berhasil')
            else:
                mb.showinfo('status', 'peminjaman gagal')
        else:
            mb.showinfo('status', 'data belum lengkap')
        self.clearValue()

    def back(self):
        self.controller.show_frame('MenuPage')
        self.student_name.set('')

    def tick(self):
        current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
        self.time_label.config(text=current_time)
        self.time_label.after(200, self.tick)

    def clearValue(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.student_name.set('')
        self.book.clear()
        self.student.clear()
        self.book_id.clear()

    def verifyLastBorrow(self,id):
        response = requests.post("https://perpustakaan-elektro.my.id/api/RaspberryPi/borrow/history", data=id,
                                 headers=self.headers)
        if (response.status_code == 404):
            mb.showinfo('status', 'anda memiliki riwayat peminjaman yang belum selesai')
            return 0
        else:
            return 1

    def deleteRow(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.book.clear()

