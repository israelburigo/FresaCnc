from tkinter import*
from math import *

class PontoD(object):
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
    def Set(self, p):
        self.X = p.X
        self.Y = p.Y
        self.Z = p.Z

class ViewDialog(object):
    def __init__(self, parent, comandos, mx, my, mz):

        self.Dialog = Toplevel(parent, bg = "red")
        self.Dialog.title('3D')
        self.Dialog.geometry("500x500+100+100")        
        self.Parent = parent
        self.Canvas = Canvas(self.Dialog, bg = 'black')
        self.Canvas.pack(fill='both', expand=True)

        self.Origem = PontoD(50,50,0)
        self.ListaPontos = []

        self.IsMouseDown = False

        self.Dialog.bind("<Button-1>", self.MouseDown)
        self.Dialog.bind("<ButtonRelease-1>", self.MouseUp)
        self.Dialog.bind("<B1-Motion>", self.MouseMove)
                
        self.MontaPontos(comandos, mx, my, mz)        
        self.Move()
        self.Desenha()

    def MouseDown(self, mouse):        
        self.IsMouseDown = True         
        self.Origem.X = mouse.x
        self.Origem.Y = mouse.y             

    def MouseUp(self, mouse):
         self.IsMouseDown = False

    def MouseMove(self, mouse):
         if not self.IsMouseDown: 
             return                  
         self.RotateZ(0.05)
         self.RotateX(0.05)
         self.Desenha()

    def Desenha(self):
        pAnt = self.ListaPontos[0]
        self.Canvas.delete(ALL)
        for i in range(1, len(self.ListaPontos)):
            p = self.ListaPontos[i]
            self.Canvas.create_line(pAnt.X, pAnt.Y, p.X, p.Y, fill = 'white', width = 1)
            pAnt = p

    def Show(self):		
        self.Dialog.wait_window()

    def MontaPontos(self, comandos, mx, my, mz):

        pontoAnterior = PontoD(0,0,0)

        for i in range(0,len(comandos)):
            try:        
                comando = comandos[i]                

                if not (comando[0] in ['+', '-']):
                    raise

                if len(comando) != 12:                
                    raise
            
                x = int(comando[0:4]) + pontoAnterior.X
                y = int(comando[4:8]) + pontoAnterior.Y
                z = int(comando[8:12]) + pontoAnterior.Z
                self.ListaPontos.append(PontoD(x * mx, y * my, z * mz))
                pontoAnterior.Set(self.ListaPontos[-1])

            except:
                pass

        return

    def RotateZ(self, rad):        
        r = [[0,0,0],[0,0,0],[0,0,0]]
        r[0][0] = cos(rad)
        r[0][1] = -sin(rad)
        r[0][2] = 0
        r[1][0] = sin(rad)
        r[1][1] = cos(rad)
        r[1][2] = 0
        r[2][0] = 0
        r[2][1] = 0
        r[2][2] = 1
        self.Calc(r)

    def RotateX(self, rad):        
        r = [[0,0,0],[0,0,0],[0,0,0]]
        r[0][0] = 1
        r[0][1] = 0
        r[0][2] = 0
        r[1][0] = 0
        r[1][1] = cos(rad)
        r[1][2] = -sin(rad)
        r[2][0] = 0
        r[2][1] = sin(rad)
        r[2][2] = cos(rad)
        self.Calc(r)
        
    def Move(self):
        for p in self.ListaPontos:
            p.X += self.Origem.X
            p.Y += self.Origem.Y
            p.Z += self.Origem.Z       

    def Calc(self, r):        
        for p in self.ListaPontos:
            x = p.X - self.Origem.X
            y = p.Y - self.Origem.Y
            z = p.Z - self.Origem.Z
            p.X = r[0][0] * x + r[0][1] * y + r[0][2] * z
            p.Y = r[1][0] * x + r[1][1] * y + r[1][2] * z
            p.Z = r[2][0] * x + r[2][1] * y + r[2][2] * z
            p.X += self.Origem.X
            p.Y += self.Origem.Y
            p.Z += self.Origem.Z
            
        