import tkinter.font as tkFont
from tkinter import filedialog
import threading
from ViewDialog import *

from tkinter import *
import os.path
from tkinter import ttk
from CustomText import *
from TextLineNumbers import *
from Acionamento import *
from LeitorComando import *
from Arquivos import*

os.system('xset r off')

terminou = False

def _on_change(event):
    linenumbers.redraw(0)
    programa.tag_delete("erro")
    return

root = Tk()
root.title('Fresa CNC')
root.geometry("600x600+10+10")
root.option_add("Font", "consolas 20")

LeftFrame = Frame(root, padx = 10, pady = 10) 
RightFrame = Frame(root, padx = 10, pady = 10)
LeftFrame.grid(column=0, row=0, sticky=(N,W,E,S))
RightFrame.grid(column=1, row=0, sticky=(N,W,E,S))

programaMsg = StringVar()
programaMsg.set("Programa - %s" % ("sem nome"))

Label(LeftFrame, textvariable = programaMsg).pack()

programa = CustomText(LeftFrame)
programa.bind("<<Change>>", _on_change)
programa.bind("<Configure>", _on_change)
vscroll = Scrollbar(LeftFrame, orient=VERTICAL, command=programa.yview)
programa['yscroll'] = vscroll.set
vscroll.pack(side="right", fill="y")

linenumbers = TextLineNumbers(LeftFrame, width=50)
linenumbers.attach(programa)
linenumbers.pack(side="left", fill="y")

programa.pack(side="left", fill="both", expand=True)

Label(RightFrame, text = 'Configurações').pack()

Label(RightFrame, text = 'Tempo Pulso(us)', pady = 5).pack()
velText = Entry(RightFrame)
velText.insert(END, 100)
velText.pack()

Label(RightFrame, text = 'Multiplicador passos X', pady = 5).pack()
passoXText = Entry(RightFrame)
passoXText.insert(END, 1)
passoXText.pack()

Label(RightFrame, text = 'Multiplicador passos Y', pady = 5).pack()
passoYText = Entry(RightFrame)
passoYText.insert(END, 1)
passoYText.pack()

Label(RightFrame, text = 'Multiplicador passos Z', pady = 5).pack()
passoZText = Entry(RightFrame)
passoZText.insert(END, 1)
passoZText.pack()

erroMsg = StringVar()
somaMsg = StringVar()
somaMsg.set("Somas\nX:0\nY:0\nZ:0\n\nX:0\nY:0\nZ:0")

def Soma(event):
    comandos = programa.get("1.0",END).split('\n')

    somas = [0,0,0]

    for i in range(0, len(comandos)):        
        try:        
            comando = comandos[i]                

            if not (comando[0] in ['+', '-']):
                continue

            if str.upper(comando) == '+RELE':
                continue

            if str.upper(comando) == '-RELE':
                continue               

            if len(comando) != 12:
                continue
            
            somas[0] += int(comando[0:4])
            somas[1] += int(comando[4:8])
            somas[2] += int(comando[8:12])

        except:
            pass

    mx = int(passoXText.get())
    my = int(passoYText.get())
    mz = int(passoZText.get())

    somaMsg.set("Somas\nX:%d\nY:%d\nZ:%d\n\nX:%d\nY:%d\nZ:%d" % 
        (somas[0], somas[1],somas[2], somas[0]*mx, somas[1]*my,somas[2]*mz))

labelErro = Label(RightFrame, textvariable = erroMsg, pady = 20, fg='red').pack()
labelSoma = Label(RightFrame, textvariable = somaMsg, fg='black')
labelSoma.bind("<Button-1>", Soma)
labelSoma.pack()

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

acionamento = Acionamento()

andandoLinha = 0

def Salvar():

    f = filedialog.asksaveasfile(initialdir = "/home/pi/ARQUIVOS CNC", filetypes=[("Fresa files", ".frs")], defaultextension=".frs")   

    if f is None:
        return

    textToSave = velText.get() + ';'
    textToSave += passoXText.get() + ';'
    textToSave += passoYText.get() + ';'
    textToSave += passoZText.get() + '\n'

    textToSave += str(programa.get("1.0", END))
    f.write(textToSave)
    f.close() 

    programaMsg.set("Programa - %s" % (f.name.split('/')[-1]))

def SetaTexto(e, text):
    e.delete(0, END)
    e.insert(0, text)
    return

def Abrir():

    f = filedialog.askopenfile(initialdir = "/home/pi/ARQUIVOS CNC", filetypes=[("Fresa files", ".frs")])
    if f == None:
        return
    
    arquivo = Arquivos().Le(f)
    if arquivo == None:
        return

    parametros = arquivo[0].split(';')

    programaMsg.set("Programa - %s" % (f.name.split('/')[-1]))

    global andandoLinha
    global terminou

    terminou = False
    andandoLinha = 0

    #parametros
    SetaTexto(velText, parametros[0])
    SetaTexto(passoXText, parametros[1])
    SetaTexto(passoYText, parametros[2])
    SetaTexto(passoZText, parametros[3])

    acionamento.AcumPassos = [0,0,0]

    #programa
    conteudo = ""
    for i in range(1,len(arquivo)):
        conteudo += arquivo[i] + '\n'

    programa.delete("1.0", END)
    programa.insert("1.0", conteudo)

def Parar():
    if acionamento.Acionado:
        return
    acionamento.Acionado = True
    acionamento.Retorna(velText.get(), passoXText.get(), passoYText.get(), passoZText.get())    
    acionamento.Acionado = False

    global terminou
    global andandoLinha
    andandoLinha = 0
    terminou = False

def Pausar():
    if not acionamento.Acionado:
        return
    acionamento.Acionado = False    

def Aciona():

    if acionamento.Acionado:
        return

    global andandoLinha
    global terminou

    linhas = programa.get("1.0",END).split('\n')
    acionamento.Acionado = True    

    erroMsg.set('')

    noGosub = None
    procuraFinalGosub = False
    i = andandoLinha
    while i < len(linhas):
        try:        

            if not acionamento.Acionado:
                break

            linha = linhas[i]

            if not (linha[0] in ['+', '-']):
                raise

            cmd = LeitorComando().Le(i, linha, linhas)
            if cmd == None:
                i+=1
                continue

            if cmd[0] == cRELE_ON:
                acionamento.AcionaRele(1)
                i+=1
                continue

            if cmd[0] == cRELE_OFF:
                acionamento.AcionaRele(0)
                i+=1
                continue

            if procuraFinalGosub and cmd[0] == cFIM:
                i = noGosub
                noGosub = None
                procuraFinalGosub = False
                continue

            if cmd[0] == cGOSUB:
                noGosub = i + 1
                i = cmd[1]
                procuraFinalGosub = True
                continue

            programa.tag_delete("linha")
            programa.tag_add("linha", str(i + 1) + ".0",  str(i + 1) + ".end")
            programa.tag_config("linha", background="yellow", foreground="black")

            programa.see(str(i + 1) + ".0")
            
            if cmd[0] == cCOORDS:            
                x = cmd[1][0]
                y = cmd[1][1]
                z = cmd[1][2]                
                acionamento.Anda(x, y, z, velText.get(), passoXText.get(), passoYText.get(), passoZText.get())
                andandoLinha = i + 1
                
            i += 1
            
        except: 
            i += 1           
            if not acionamento.Acionado: 
                erroMsg.set(str("Erro na linha %d" % (i+1)) )                
                programa.tag_delete("erro")
                programa.tag_add("erro", str(i + 1) + ".0",  str(i + 1) + ".end")
                programa.tag_config("erro", background="red", foreground="white")
                return
            pass

    _on_change(None)    
    if acionamento.Acionado:
        andandoLinha = 0    
        programa.tag_delete("linha")
        terminou = True

    acionamento.Acionado = False    

def KeyUp(event):
    if event.keysym in ['F5','F6','F7','F8','F9','F10']:
        acionamento.AcionadoManual = False

def KeyDown(event):    
    if not (event.keysym in ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12']): 
        return

    global terminou        
    
    if event.keysym == 'F1' :

        if terminou:
            return

        if not acionamento.Acionado:
            thread = threading.Thread(target = Aciona)    
            thread.daemon = True 
            thread.start()
        else:
            Pausar()

    if event.keysym == 'F2':
        Parar()

    if event.keysym == 'F3':
        Salvar()

    if event.keysym == 'F4':
        Abrir()

    if event.keysym == 'F5':        
        acionamento.MoveManual('x', 1, velText.get())

    if event.keysym == 'F6':
        acionamento.MoveManual('x', 0, velText.get())

    if event.keysym == 'F7':
        acionamento.MoveManual('y', 1, velText.get())

    if event.keysym == 'F8':
        acionamento.MoveManual('y', 0, velText.get())

    if event.keysym == 'F9':
        acionamento.MoveManual('z', 1, velText.get())

    if event.keysym == 'F10':
        acionamento.MoveManual('z', 0, velText.get())

    if event.keysym == 'F11':
        acionamento.AcionaReleManual()

    if event.keysym == 'F12':
        comandos = programa.get("1.0",END).split('\n')
        mx = int(passoXText.get())
        my = int(passoYText.get())
        mz = int(passoZText.get())
        ViewDialog(root, comandos, mx, my, mz).Show()   

root.bind("<KeyPress>", KeyDown)
root.bind("<KeyRelease>", KeyUp)

root.mainloop()