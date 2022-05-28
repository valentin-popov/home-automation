import serial
from tkinter import *
import speech_recognition as sr

isOn = False  # variabila booleana care descrie starea releului
alarmaOn = False
# A SE COMENTA URMATOAREA LINIE PENTRU A PUTEA VEDEA INTERFATA FARA CONEXIUNE LA PLACA
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1, writeTimeout=1)


def toggleRelay():
    global isOn
    if isOn:  # daca este aprins inainte de apasare
        toggle1.config(image=off)  # butonul ia imaginea cu off la apasare
        isOn = False
        arduino.write(b'0')

    else:
        toggle1.config(image=on)
        isOn = True
        arduino.write(b'1')


def alarma():
    global alarmaOn
    if alarmaOn:  # daca este pornita
        toggle2.config(image=off)  # butonul ia imaginea cu off
        alarmaOn = False
        arduino.write(b'3')

    else:
        toggle2.config(image=on)
        alarmaOn = True
        arduino.write(b'2')


def citesteTemperatura():
    string = arduino.readline().decode('utf-8')
    string = string.replace("\r\n", "")
    string = string.split(',')
    print(string)
    textbox1.delete(1.0, END)
    textbox2.delete(1.0, END)
    textbox1.insert(END, string[0] + "°C")
    textbox2.insert(END, string[1] + "%")


def comenziVocale():
    global isOn
    global alarmaOn
    sprec = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = sprec.listen(source)
    print(sprec.recognize_google(audio, language='ro-RO'))
    if sprec.recognize_google(audio, language='ro-RO') == "aprinde" and not isOn:
        toggleRelay()
        isOn = True

    if sprec.recognize_google(audio, language='ro-RO') == "stinge" and isOn:
        toggleRelay()
        isOn = False

    if sprec.recognize_google(audio, language='ro-RO') == "pornește alarma" and not alarmaOn:
        alarma()
        alarmaOn = True

    if sprec.recognize_google(audio, language='ro-RO') == "oprește alarma" and alarmaOn:
        alarma()
        alarmaOn = False


window = Tk()  # face o fereastra goala
window.title("Home Automation")
window.geometry('650x500')
window.resizable(False, False)

# imaginile pentru starile butonului
on = PhotoImage(file="butonon.png")
off = PhotoImage(file="butonoff.png")
microphone = PhotoImage(file="microphone.png")

label1 = Label(window, text='Home Automation', font=("Arial", 28), fg="#0b7907")
label1.place(x=325, y=80, anchor="center")

label2 = Label(window, text='Lumina', font=("Serif", 12))
label2.place(x=150, y=170, anchor='center')

toggle1 = Button(window, image=off, command=toggleRelay, relief=FLAT)
toggle1.place(x=150, y=200, anchor="center")

label3 = Label(window, text='Alarma', font=("Serif", 12))
label3.place(x=150, y=250, anchor='center')

toggle2 = Button(window, image=off, command=alarma, relief=FLAT)
toggle2.place(x=150, y=280, anchor="center")

label4 = Label(window, text='Temperatura', font=("Serif", 12))
label4.place(x=462, y=172, anchor='center')

textbox1 = Text(window, width=20, height=1)
textbox1.place(x=380, y=190)

label5 = Label(window, text='Umiditate', font=("Serif", 12))
label5.place(x=462, y=232, anchor='center')

textbox2 = Text(window, width=20, height=1)
textbox2.place(x=380, y=250)

butonTemperatura = Button(window, text='Citeste date', command=citesteTemperatura, height=2, width=17)
butonTemperatura.place(x=380, y=300)

butonVoce = Button(window, image=microphone, command=comenziVocale, relief=FLAT)
butonVoce.place(x=150, y=350, anchor="center")
window.mainloop()

