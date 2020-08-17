from Motor import*
import RPi.GPIO as GPIO
import time	
import threading

class Acionamento(object):
    """description of class"""
    def __init__(self, **kwargs):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.Acionado = False        

        self.Velocidade = 0.000001
        self.PassosX = 1
        self.PassosY = 1
        self.PassosZ = 1
        self.Rele = 21

        self.AcumPassos = [0,0,0]

        GPIO.setup(self.Rele, GPIO.OUT)

        self.MotorX = Motor(24, 25)
        self.MotorY = Motor(16, 20)
        self.MotorZ = Motor(8, 12)

        return super().__init__(**kwargs)

    def AcionaManual(self):        
        self.AcionadoManual = True
        while self.AcionadoManual:
            self.WaitStep(self.Velocidade)
            GPIO.output(self.MotorManual.PinoPulso, 1)
            self.WaitStep(self.Velocidade)
            GPIO.output(self.MotorManual.PinoPulso, 0)                 

    def MoveManual(self, motor, dir, v):

        if self.Acionado:
            return

        self.Velocidade = int(v) * 0.000001

        if motor == 'x': 
            self.MotorX.Direcao(dir)  
            self.MotorManual = self.MotorX

        if motor == 'y': 
            self.MotorY.Direcao(dir)
            self.MotorManual = self.MotorY            

        if motor == 'z': 
            self.MotorZ.Direcao(dir)
            self.MotorManual = self.MotorZ            
     
        thread = threading.Thread(target = self.AcionaManual)
        thread.daemon = True 
        thread.start()

    def AcionaRele(self, value):
        GPIO.output(self.Rele, value)
        return

    def AcionaReleManual(self):
        if self.Acionado: return

        if GPIO.input(self.Rele):
            GPIO.output(self.Rele, 0)
        else:
            GPIO.output(self.Rele, 1)

    def WaitStep(self, tempo):
        t = time.time() + tempo
        while time.time() < t:
            continue 

    def RecalculaFatores(self, pMaior):
        self.FatorX = self.PassosX / pMaior
        self.FatorY = self.PassosY / pMaior
        self.FatorZ = self.PassosZ / pMaior

    def Retorna(self, v, mpx, mpy, mpz):

        self.Velocidade = int(v) * 0.000001
        self.PassosZ = (self.AcumPassos[2] * int(mpz))*-1
        self.MotorZ.Direcao(self.PassosZ)
        self.PassosZ = abs(self.PassosZ)
        self.FatorZ = 1        

        incZ = 0
        while self.PassosZ > 0:
            incZ += self.FatorZ if self.PassosZ > 0 else 0
            if incZ >= 1:
                incZ -= 1
                self.PassosZ -= 1                
                GPIO.output(self.MotorZ.PinoPulso, 1)

            self.WaitStep(self.Velocidade)            
            GPIO.output(self.MotorZ.PinoPulso, 0)
            self.WaitStep(self.Velocidade)

        self.Anda(self.AcumPassos[0]*-1, self.AcumPassos[1]*-1, 0, v, mpx, mpy, mpz)

        self.AcumPassos[0] = 0
        self.AcumPassos[1] = 0
        self.AcumPassos[2] = 0


    def Anda(self, px, py, pz, v, mpx, mpy, mpz):

        self.AcumPassos[0] += px
        self.AcumPassos[1] += py
        self.AcumPassos[2] += pz

        self.Velocidade = int(v) * 0.000001
        self.PassosX = px * int(mpx)
        self.PassosY = py * int(mpy)
        self.PassosZ = pz * int(mpz)

        self.MotorX.Direcao(self.PassosX)
        self.MotorY.Direcao(self.PassosY)
        self.MotorZ.Direcao(self.PassosZ)

        self.PassosX = abs(self.PassosX)
        self.PassosY = abs(self.PassosY)
        self.PassosZ = abs(self.PassosZ)

        self.FatorX = 1
        self.FatorY = 1
        self.FatorZ = 1

        if self.PassosX  == 0 and self.PassosY == 0 and self.PassosZ == 0: 
            return

        if self.PassosX >= self.PassosY and self.PassosX >= self.PassosZ:
            self.RecalculaFatores(self.PassosX)

        if self.PassosY > self.PassosX and self.PassosY >= self.PassosZ:
            self.RecalculaFatores(self.PassosY)

        if self.PassosZ > self.PassosY and self.PassosZ > self.PassosX:
            self.RecalculaFatores(self.PassosZ)

        incX = 0
        incY = 0
        incZ = 0

        while self.PassosX > 0 or self.PassosY > 0 or self.PassosZ > 0:

            incX += self.FatorX if self.PassosX > 0 else 0
            incY += self.FatorY if self.PassosY > 0 else 0
            incZ += self.FatorZ if self.PassosZ > 0 else 0

            if incX >= 1:
                incX -= 1
                self.PassosX -= 1                
                GPIO.output(self.MotorX.PinoPulso, 1)

            if incY >= 1:
                incY -= 1
                self.PassosY -= 1                
                GPIO.output(self.MotorY.PinoPulso, 1)

            if incZ >= 1:
                incZ -= 1
                self.PassosZ -= 1                
                GPIO.output(self.MotorZ.PinoPulso, 1)

            self.WaitStep(self.Velocidade)
            GPIO.output(self.MotorX.PinoPulso, 0)
            GPIO.output(self.MotorY.PinoPulso, 0)
            GPIO.output(self.MotorZ.PinoPulso, 0)
            self.WaitStep(self.Velocidade)
        
        return

