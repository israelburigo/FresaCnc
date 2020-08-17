
from math import*

def Comprimento(x, y, z):
    return sqrt(x * x + y * y + z * z)

def Reparte(x1, x2, y1, y2, z1, z2, dist):

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    comprimento = Comprimento(dx, dy, dz)
    
    maxDistance = sqrt(3 * dist * dist)

    if(comprimento < maxDistance):
        return [(dx, dy, dz)]

    fator = comprimento / maxDistance
    qntPontos = round(fator)
    
    fxyz = (dx / fator, dy / fator, dz / fator)

    ultimoPonto = (x1, x2, z1)

    novosPontos = []
    novosPontos.append(ultimoPonto)

    i = 1
    while i < qntPontos:
        i+=1
        novoPonto = (ultimoPonto[0] + fxyz[0],
                     ultimoPonto[1] + fxyz[1],
                     ultimoPonto[2] + fxyz[2])

        novosPontos.append(novoPonto)

        ultimoPonto = (novoPonto[0], novoPonto[1], novoPonto[2])

    return novosPontos;
