import tkinter as tk
import time

from RaspberryPi.front.absen.index import AbsenPage
from RaspberryPi.front.peminjaman.index import PeminjamanPage
from RaspberryPi.front.pengembalian.index import PengembalianPage

columns = ('#1', '#2', '#3')

current_balance = 1000

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance': tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in ( MenuPage, AbsenPage, PeminjamanPage, PengembalianPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='Sistem Peminjaman Buku',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,
                                   text='Main Menu',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#3d3d5c')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text='Please make a selection',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#3d3d5c',
                                   anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def Absen():
            controller.show_frame('AbsenPage')

        absen_button = tk.Button(button_frame,
                                    text='Absen',
                                    command=Absen,
                                    borderwidth=3,
                                    width=50,
                                    height=5)
        absen_button.grid(row=0, column=0, pady=5)

        def peminjaman():
            controller.show_frame('PeminjamanPage')

        deposit_button = tk.Button(button_frame,
                                   text='Peminjaman',
                                   command=peminjaman,
                                   relief='raised',
                                   borderwidth=3,
                                   width=50,
                                   height=5)
        deposit_button.grid(row=1, column=0, pady=5)

        def pengembalian():
            controller.show_frame('PengembalianPage')

        balance_button = tk.Button(button_frame,
                                   text='Pengembalian',
                                   command=pengembalian,
                                   relief='raised',
                                   borderwidth=3,
                                   width=50,
                                   height=5)
        balance_button.grid(row=2, column=0, pady=5)


        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
