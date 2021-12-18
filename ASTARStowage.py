import sys
import numpy as np
import copy
import os
import timeit


if len(sys.argv) != 4:
    print(sys.argv)
    sys.exit("Invalid amount of arguments to start the program")
path = sys.argv[1]
map_path = sys.argv[2]
container_path = sys.argv[3]
with open("" + path + "/" + map_path + ".txt") as textFile:
    lines = [line.split() for line in textFile]
    mapa = lines
    if len(mapa) == 0:
        print("The map is empty")
        sys.exit()

with open("" + path + "/" + container_path + ".txt") as textFile:
    lines = [line.split() for line in textFile]
    array_contenedores = lines
    if len(array_contenedores) == 0:
        print("There are no containers")
        sys.exit()
mapaShape = np.shape(mapa)
containers=[]

class Node:
    def __init__(self,state,parent=None,position=0,g=0,h=0,move='start'):
        self.state=state
        self.parent=parent
        self.position=position
        self.g=g
        self.h=h
        self.f=self.g+self.h
        self.move=move

    def equals(self, other):
         if other is None:
             return False
         return np.array_equal(self.state,other.state) and other.f==self.f

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
                            if mapa[row+1][column]!='X':
                                continue
                            container.fila=row
                            container.columna=column
                            #using deepcopy so the copy doesnt share same memory pointer
                            cargar=copy.deepcopy(self.state)
                            #remove first container from the available containers
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(10+container.fila+1),move='CargarContainer-'+str(container._id)+container.tipo+str(container.puerto)+"-EnPos-"+str(container.fila)+str(container.columna))
                        else:
                            #for container in loaded containers
                            continueFlag=False
                            for c in self.state[1]:
                                #if container already lodaded in that position continue the for loop
                                if c.fila==row and c.columna==column:
                                    continueFlag=True
                            if continueFlag:
                                continue
                            firstFlag=False
                            secondFlag=False
                            for c in self.state[1]:
                                if c.fila==row+1 and c.columna==column:
                                    firstFlag=True
                            if mapa[row + 1][column] == 'X':
                                secondFlag=True
                            if firstFlag==False and secondFlag==False:
                                continue
                            container.fila = row
                            container.columna = column
                            cargar = copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar, parent=self, position=self.position + 1, g=self.g + 1,h=self.h+(10+container.fila+1), move='CargarContainer-' +str(container._id)+container.tipo+str(container.puerto)+"-EnPos-"+str(container.fila)+str(container.columna))
                elif container.tipo=='R':
                    if mapa[row][column] == 'E':
                        # if no loaded containers yet
                        if len(self.state[1])==0:
                            if mapa[row+1][column]!='X':
                                continue
                            container.fila=row
                            container.columna=column
                            cargar=copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(10+container.fila+1),move='CargarContainer-'+str(container._id)+container.tipo+str(container.puerto)+"-EnPos-"+str(container.fila)+str(container.columna))
                        else:
                            #for container in loaded containers
                            continueFlag=False
                            for c in self.state[1]:
                                #if container already lodaded in that position continue the for loop
                                if c.fila==row and c.columna==column:
                                    continueFlag=True
                            if continueFlag:
                                continue
                            container.fila = row
                            container.columna = column
                            cargar = copy.deepcopy(self.state)
                            cargar[0].pop(0)
                            cargar[1].append(container)
                            return Node(cargar, parent=self, position=self.position + 1, g=self.g + 1,h=self.h+(10+container.fila+1), move="CargarContainer-" +str(container._id)+container.tipo+str(container.puerto)+"-EnPos-"+str(container.fila)+str(container.columna))


    def descargar(self):
        #cant unload on first port
        if self.state[4]==0 or len(self.state[1])==0:
            return None
        #retrieve first available container from loaded containers list
        _container = self.state[1][0]
        if self.state[4]==1:
            #if theres no more containers to unload to port 1
            if sum(c.puerto == 1 for c in self.state[1])==0:
                return None
            descargar=copy.deepcopy(self.state)
            descargar[1].pop(0)
            descargar[2].append(_container)
            return Node(descargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(15+2*_container.fila),move="DescargarContainer-"+str(_container._id)+_container.tipo+str(_container.puerto))
        if self.state[4]==2:
            if sum(c.puerto == 2 for c in self.state[1])==0:
                return None
            descargar=copy.deepcopy(self.state)
            descargar[1].pop(0)
            descargar[3].append(_container)
            return Node(descargar,parent=self,position=self.position+1,g=self.g+1,h=self.h+(15+2*_container.fila),move="DescargarContainer-"+str(_container._id)+_container.tipo+str(_container.puerto))


    def navegar(self):
        if self.state[4]==2:
            return None
        #if port is 1
        if self.state[4]==0:
            #if theres still containers to load in port 0
            if len(self.state[0])!= 0:
                return None
            navegar=copy.deepcopy(self.state)
            navegar[4]=1
            return Node(navegar,parent=self,position=self.position+1,g=self.g+1,h=self.h+3500,move="NavegarA-"+str(navegar[4]))
        #if port is 2
        if self.state[4]==1:
            #if theres still containers to unload in port 1
            if sum(c.puerto == 1 for c in self.state[1])!=0:
                return None
            navegar = copy.deepcopy(self.state)
            navegar[4] = 2
            return Node(navegar, parent=self, position=self.position + 1, g=self.g + 1, h=self.h + 3500,move="NavegarA-" + str(navegar[4]))


    def doAll(self,graph):
        cargar=self.cargar()
        cargar=None if graph.isClosed(cargar) else cargar
        descargar=self.descargar()
        descargar=None if graph.isClosed(descargar) else descargar
        navegar=self.navegar()
        navegar=None if graph.isClosed(navegar) else navegar
        #should work but doesn't currently
        # graph.closeNode(self)
        # graph.openNode(cargar)
        # graph.openNode(descargar)
        # graph.openNode(navegar)
        tmpList= [cargar, descargar, navegar]
        return tmpList

    def print(self):
        if self.parent is None:
            with open("outputASTAR/" + map_path + "-" + container_path + ".output", 'a') as f:
                f.write("Start\n")
            return
        with open("outputASTAR/" + map_path + "-" + container_path + ".output", 'a') as f:
            f.write(self.move+"\n")
        return self.parent.print()

class Container:


    def __init__(self,_id,tipo,puerto,fila=-1,columna=-1):
        self._id=_id
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


    def isClosed(self,node):
        if node is None:
            return True
        for _node in self.closed:
            if _node.equals(node):
                return True
        return False


    def closeNode(self,node):
        if node is None:
            return True
        self.open.remove(node)
        for _node in self.closed:
            if _node.equals(node):
                self.closed.append(node)
                return


    def openNode(self,node):
        if node is None:
            return
        self.open.append(node)


    def solve(self):
        self.open.append(self.start)
        currentNode=None
        while len(self.open)!=0:
            currentNode=self.open[0]
            self.open.pop(0)
            self.closed.append(currentNode)
            if currentNode.state is not None:
                if currentNode.equals(self.end):
                    break
            adjNodes=currentNode.doAll(self)
            for node in adjNodes:
                if node in self.closed:
                    continue
                if node in self.open:
                    continue
                if node is not None:
                    self.open.append(node)
        os.makedirs("outputASTAR", exist_ok=True)
        with open("outputASTAR/" + map_path + "-" + container_path + ".output", 'w', encoding="utf-8") as f:
            pass
        with open("outputASTAR/" + map_path + "-" + container_path + "-statistics.stat", 'w', encoding="utf-8") as f:
            f.write("Total g:"+str(currentNode.g)+"\nTotal h:"+str(currentNode.h)+"\nTotal f:"+str(currentNode.f)+"\n")
        currentNode.print()



def main():
    startTime = timeit.default_timer()
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    for c in array_contenedores:
        if len(c)==3:
            containers.append(Container(_id=int(c[0]),tipo=c[1],puerto=int(c[2])))
        else:
            containers.append(Container(_id=int(c[0]+c[1]), tipo=c[2], puerto=int(c[3])))
    contenedoresPuerto1=lambda _c:_c.puerto==1,containers
    contenedoresPuerto2=lambda _c:_c.puerto==2,containers

    # Estado=[contenedoresDisponibles,contenedoresCargados,contenedoresDescargados1,contenedoresDescargados2,puertoActual]
    _start=[
           containers,
            [],
           [],
           [],
           0
           ]
    start=Node(state=_start)
    _end=[
           [],
            [],
           contenedoresPuerto1,
           contenedoresPuerto2,
           2
           ]
    end=Node(state=_end)
    solver=AStar(start,end)
    solver.solve()
    stopTime = timeit.default_timer()
    with open("outputASTAR/" + map_path + "-" + container_path + "-statistics.stat", 'a', encoding="utf-8") as f:
        f.write("Runtime:"+str(stopTime-startTime)+" Seconds")
    #write output reversed since node writing is recursive
    readLines=[]
    with open("outputASTAR/" + map_path + "-" + container_path + ".output", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            readLines.append(line)
    readLines.reverse()
    with open("outputASTAR/" + map_path + "-" + container_path + ".output", 'w', encoding="utf-8") as f:
        for line in readLines:
            f.write(line)
if __name__=="__main__":
    main()
