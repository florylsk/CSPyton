from math import comb
import constraint
import sys
from constraint import *
import numpy as np
import pandas as pd
import copy

#Te pasan contenedores, inicial->puerto1->puerto2,descaga o carga de contenedores, busqueda de contenedores del puerto X e ir sacandolos
mapa=    [['N','N','N','N'],
          ['N','N','N','N'],
          ['E','N','N','E'],
          ['X','E','E','X'],
          ['X','X','X','X']]
mapaShape=np.shape(mapa)
class Node:
    def __init__(self,state,parent=None,position=None,g=0,h=0,move='start'):
        self.state=state
        self.parent=parent
        self.position=position
        self.g=g
        self.h=h
        self.f=g+h
        self.move=move

    def __eq__(self, other):
        return self.position==other.position

    #accion para cargar un contenedores disponible en el mapa
    def cargar(self):
        #if no available containers to deploy or port isnt 0 return empty node
        if len(self.state[0])==0 or self.state[4]!=0:
            return None
        #get first container available
        container=self.state[0][0]
        #traverse map
        for row in range(0, mapaShape[0]):
            for column in range(0, mapaShape[1]):
                if container.tipo=='S':
                    if mapa[row][column] == 'N' or mapa[row][column] == 'E':
                        # if no loaded containers yet
                        if len(self.state[1])==0:
                            container.fila=row
                            container.columna=column
                            #using deepcopy so the copy doesnt share same memory pointer
                            cargar=copy.deepcopy(self.state)
                            #remove first container from the available containers
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(10+container.fila+1),move='CargarContainer-'+container.id+container.tipo+container.puerto+"-EnPos-"+container.fila+container.columna)
                        else:
                            #for container in loaded containers
                            for c in self.state[1]:
                                #if container already lodaded in that position continue the for loop
                                if c.fila==row and c.columna==column:
                                    continue
                            container.fila = row
                            container.columna = column
                            cargar = copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar, parent=self, position=self.position + 1, g=self.g + 1,h=self.h+(10+container.fila+1), move='CargarContainer-' + container.id + container.tipo + container.puerto + "-EnPos-" + container.fila + container.columna)
                elif container.tipo=='R':
                    if mapa[row][column] == 'E':
                        # if no loaded containers yet
                        if len(self.state[1])==0:
                            container.fila=row
                            container.columna=column
                            cargar=copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(10+container.fila+1),move='CargarContainer-'+container.id+container.tipo+container.puerto+"-EnPos-"+container.fila+container.columna)
                        else:
                            #for container in loaded containers
                            for c in self.state[1]:
                                #if container already lodaded in that position continue the for loop
                                if c.fila==row and c.columna==column:
                                    continue
                            container.fila = row
                            container.columna = column
                            cargar = copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar, parent=self, position=self.position + 1, g=self.g + 1,h=self.h+(10+container.fila+1), move="CargarContainer-" + container.id + container.tipo + container.puerto + "-EnPos-" + container.fila + container.columna)


    def descargar(self):
        #cant unload on first port
        if self.state[4]==0 or len(self.state[1])==0:
            return None
        if self.state[4]==1:
            #if theres no more containers to unload to port 1
            if sum(c.puerto == 1 for c in self.state[1])==0:
                return None
            _container = self.state[1][0]
            descargar=copy.deepcopy(self.state)
            descargar[1].pop(0)
            descargar[2].append(_container)
            return Node(descargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(15+2*_container.row),move="DescargarContainer-"+_container.id+_container.tipo+_container.puerto)
        if self.state[4]==2:
            if sum(c.puerto == 2 for c in self.state[1])==0:
                return None
            _container = self.state[1][0]
            descargar=copy.deepcopy(self.state)
            descargar[1].pop(0)
            descargar[3].append(_container)
            return Node(descargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(15+2*_container.row),move="DescargarContainer-"+_container.id+_container.tipo+_container.puerto)


    def navegar(self):
        if self.state[4]==2:
            return None
        if self.state[4]==0:
            #if theres still containers to load in port 0
            if len(self.state[0])!= 0:
                return None
            navegar=copy.deepcopy(self.state)
            navegar[4]=1
            return Node(navegar,parent=self,position=self.position+1,g=self.g+1,h=self.h+3500,move="NavegarA-"+navegar[4])




        if self.state[4]==1:
            #if theres still containers to unload in port 1
            if sum(c.puerto == 1 for c in self.state[1])!=0:
                return None
            navegar = copy.deepcopy(self.state)
            navegar[4] = 2
            return Node(navegar, parent=self, position=self.position + 1, g=self.g + 1, h=self.h + 3500,
                        move="NavegarA-" + navegar[4])


class Container:


    def __init__(self,id,tipo,puerto,fila=-1,columna=-1):
        self.id=id
        self.tipo=tipo
        self.puerto=puerto
        self.fila=fila
        self.columna=columna


class AStar:
    def __init__(self,start,end):
        self.start=start
        self.end=end
        self.mapa=mapa
        self.open=[]
        self.closed=[]

    def solve(self):



def main():
    #estado=contenedoresDisponibles,contenedoresCargados,contenedoresDescargados1,contenedoresDescargados2,puertoActual
    container1=Container(1,'S',1)
    container2=Container(2,'S',1)
    container3=Container(3,'S',1)
    container4=Container(4,'R',2)
    container5=Container(5,'R',2)


    _start=[
           [container1,container2,container3,container4,container5],
            [],
           [],
           [],
           0
           ]
    start=Node(state=_start)
    _end=[
           [],
            [],
           [container1,container2,container3],
           [container4,container5],
           2
           ]
    end=None(state=_end)
    solver=AStar(start,end)
    solver.solve()










if __name__=="__main__":
    main()
