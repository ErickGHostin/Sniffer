import DefSniffer
from Tkinter import *
from functools import partial

global cap, footlabelY
cap = []
footlabelY = 100

def Executar():
    global input, foot, janela
    janela = CriarJanela()
    input = CriarInput(janela)
    CriarLabel(janela)
    CriarBotao(janela)
    janela.mainloop()

def Capturar():
    global input, foot, cap
    interface = input.get()
    for x in range(1,2):
        print(x)
        result = DefSniffer.Captura(interface)
        foot = CriarFoot(janela, result)
        cap.append(result)
    for pkt in cap:
        for i in pkt:
            print(i)


def CriarJanela():
    aba = Tk()
    aba.title("Sniffer")
    aba.configure(background='white')
    abaX = 800
    abaY = 800
    aba.geometry("%sx%s" %(abaX, abaY))
    return aba

def CriarLabel(aba):
    headlabel = Label(aba, text='Digite a interface: ')
    headlabel.configure(background='white')
    headlabelX = 10
    headlabelY = 10
    headlabel.place(x=headlabelX,y=headlabelY)

def CriarInput(aba):
    headinput = Entry(aba)
    headinputX = 150
    headinputY = 10
    headinput.place(x=headinputX,y=headinputY)
    return headinput

def CriarBotao(aba):
    midbuttonX = 10
    midbuttonY = 50
    midbuttonW = 31
    midbutton = Button(aba, width=midbuttonW, text='Capturar!', command=Capturar)
    midbutton.place(x=midbuttonX, y=midbuttonY)

def CriarFoot(aba,result):
    global footlabelY
    for x in result:
        footlabel = Label(aba, text='')
        footlabel.configure(background='white')
        footlabelX = 150
        footlabel.place(x=footlabelX, y=footlabelY)
        source, destination, protocol = Ler(x)
        footlabel["text"] += "Source: %s | Destination: %s | Protocol: %s" % (source, destination, protocol)
        footbtnX = 10
        CriarBotaoP(aba, x, footbtnX, footlabelY)
        footlabelY += 25
    return footlabel

def Ler(x):
    x = str(x)
    # print("-------aki--")
    # print(x.find("Layer IP:"))
    # print("-------aki--")
    texto = x[x.find("Layer IP:"):x.find("Destination GeoIP:")]
    # sourcei = texto.find("	Source: ")
    # sourcef = texto.find("	Header checksum status:")
    # destinationi = texto.find("Destination:")
    # destinationf = texto.find("0000 00..:")
    # protocoli = texto.find("Protocol: ")
    # Protocolf = texto.find("Destination GeoIP:")
    destination = texto[texto.find("Destination:") + 12:texto.find("	Destination GeoIP Country:")]
    texto = texto[texto.find("	Destination GeoIP Country:"):]
    source = texto[texto.find("	Source: ")+9:texto.find("	Header checksum status:")]
    texto = texto[texto.find("	Header checksum status:"):]
    protocol = texto[texto.find("Protocol: ")+10:texto.find("	Destination GeoIP:")]
    source = Limpar(source,[' ','\n'])
    destination = Limpar(destination,[' ','\n'])
    protocol = Limpar(protocol,[' ','\n'])
    if len(destination) >= 15:
        destination = destination[:destination.find("0000")]
    if len(source) >= 15:
        source = source[:15]
    # if len(protocol) >= 8:
        # protocol = protocol[:8]
    return source, destination, protocol

def CriarBotaoP(aba, PKT, X,Y):
    AbrirPKT = partial(Abrir, PKT)
    button = Button(aba, width=10, text='Abrir', command=AbrirPKT)
    button.place(x=X, y=Y)
    return button

def CriarJanelaTexto():
    aba = Tk()
    aba.title("Pacote")
    abaX = 800
    abaY = 400
    aba.geometry("%sx%s" %(abaX, abaY))
    return aba

def Abrir(PKT):
    janelan = CriarJanelaTexto()
    CriarTexto(janelan,PKT)
    return true

def CriarTexto(aba,PKT):
    text = Text(aba, width=800, height=400, bg="white")
    text.insert(INSERT, PKT)
    text.pack()
    # headlabel = Label(aba, text=PKT)
    # headlabelX = 10
    # headlabelY = 10
    # headlabel.place(x=headlabelX,y=headlabelY)

def Limpar(texto,list):
    ntexto = ''
    for c in texto:
        if c not in list:
            ntexto += c
    return ntexto

if __name__ == '__main__':
    Executar()