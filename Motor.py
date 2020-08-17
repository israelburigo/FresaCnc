import time	
import threading as th
import RPi.GPIO as GPIO
import math as math

class Motor(object):
    
    def __init__(self, pulso, sentido):
        self.PinoPulso = pulso
        self.PinoSentido = sentido
        self.Sinal = False		
        GPIO.setup(self.PinoPulso, GPIO.OUT)		
        GPIO.setup(self.PinoSentido, GPIO.OUT)
        self.PinoPwm = None

    def Direcao(self, passos):
        GPIO.output(self.PinoSentido, 1 if passos > 0 else 0)
        return

