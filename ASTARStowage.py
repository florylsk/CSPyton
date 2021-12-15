from math import comb
import constraint
import sys
from constraint import *
import numpy as np
import pandas as pd
import copy

#Te pasan contenedores, inicial->puerto1->puerto2,descaga o carga de contenedores, busqueda de contenedores del puerto X e ir sacandolos

def carga(altura, costeAcumulado):
    return 10+altura+costeAcumulado

def descarga(altura, costeAcumulado):
    return (10+(altura*2))+costeAcumulado

def navegar(costeAcumulado):
    return 3500+costeAcumulado

class Node:
    def __init__(self,state,parent=None,position=None):
        self.state=state
        self.parent=parent
        self.position=position
        self.g=0
        self.f=0
        self.h=0

    def __eq__(self, other):
        return self.position==other.position

def aStar(start,startPort,end, endPort):
    while(startPort!=endPort):
        pass
    pass



def main():
    #codification: 0=X,1=N,2=E,4=R1,5=S1,6=R2,7=S2
    start=[[1,1,1,1],
          [1,1,1,1],
          [2,2,2,2],
          [0,2,2,0],
          [0,0,0,0]]
    start=Node(state=start)
    end=
    aStar(start,end)










if __name__=="__main__":
    main()
