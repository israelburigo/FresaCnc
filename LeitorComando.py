
cNONE = 0
cGOSUB = 1
cCOORDS = 2
cRELE_ON = 3
cRELE_OFF = 4
cFIM = 999


import re

class LeitorComando(object):
    
    def __init__(self):
        return

    def LeGoSub(self, linha, linhas):
        s  = '+' + linha[7:].upper()

        for i in range(0, len(linhas)):
            l = linhas[i].upper()
            if l == s:
                return (cGOSUB, i + 1)
        return None

    def Le(self, index, linha, linhas):
        if linha[:6].upper() == '+GOSUB':
            return self.LeGoSub(linha, linhas)

        if re.match('[+-][0-9]{3}[+-][0-9]{3}[+-][0-9]{3}', linha):
            return (cCOORDS, (int(linha[0:4]), int(linha[4:8]), int(linha[8:12])) )

        if linha[:4].upper() == '+FIM':
            return (cFIM, cNONE)

        if linha[:5].upper() == '+RELE':
            return (cRELE_ON, cNONE)

        if linha[:5].upper() == '-RELE':
            return (cRELE_OFF, cNONE)
