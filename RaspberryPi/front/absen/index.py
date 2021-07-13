import tkinter as tk
import time
# from tkinter import messagebox as mb
# from helper.rfid import ReadRfid
# from BackEnd.attendace import attempt

class AbsenPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Absensi',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        scan_label = tk.Label(self,
                                       text='Scan Your KTM',
                                       font=('orbitron', 13),
                                       fg='white',
                                       bg='#3d3d5c')
        scan_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        # def absen():
        #     id = ReadRfid()
        #     rfid = {'rfid': id}
        #     status = attempt(rfid)
        #     if(status != 0):
        #         mb.showinfo('status', 'absen berhasil')
        #         controller.show_frame('MenuPage')
        #     else:
        #         mb.showinfo('status', 'absen gagal')
        #         controller.show_frame('MenuPage')
            

        back_button = tk.Button(button_frame,
                                text='Back',
                                relief='raised',
                                borderwidth=3,
                                width=10,
                                height=2)
        back_button.grid(row=0, column=0, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()