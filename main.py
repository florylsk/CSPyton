from math import comb
import constraint
import sys
from constraint import *
import numpy as np
import pandas as pd
import copy

#Todo
# if len(sys.argv) != 4:
#     sys.exit("Invalid amount of arguments to start the program")
# path = sys.argv[1]
# map_path = sys.argv[2]
# container_path = sys.argv[3]

array_mapa=[]
array_contenedores=[]
#TODO: cambiar esto para que use map_path
with open("mapa.txt") as textFile:
    lines = [line.split() for line in textFile]
    array_mapa=lines

#TODO: cambiar esto para que use container_path
with open("contenedores.txt") as textFile:
    lines = [line.split() for line in textFile]
    array_contenedores=lines

new_array_mapa=[]
MapaShape=np.shape(array_mapa)
for length in range(0,MapaShape[0]):
    new_array_mapa.append([])
#Create the new map array with the cell type, row and column
for row in range(0,MapaShape[0]):
    for column in range(0,MapaShape[1]):
        new_array_mapa[row].append(array_mapa[row][column]+str(row)+str(column))

print("Array final del mapa")
for row in new_array_mapa:
    print(row)

new_array_contenedores=[]
ContendoresShape=np.shape(array_contenedores)
#create the new container array with merged id,type and port
for row in range(0,ContendoresShape[0]):
    new_array_contenedores.append(array_contenedores[row][0]+array_contenedores[row][1]+array_contenedores[row][2])
print("Array final de contenedores")
print(new_array_contenedores)

problem = Problem()

dominioE=[]
dominioN=[]
newArrMapaShape=np.shape(new_array_mapa)
#Create the domain array searching for Es and Ns
for row in range(0,newArrMapaShape[0]):
    for column in range(0,newArrMapaShape[1]):
        if 'E' in new_array_mapa[row][column]:
            dominioE.append(new_array_mapa[row][column])
        elif 'N' in new_array_mapa[row][column]:
            dominioN.append(new_array_mapa[row][column])

#Add variables and their domains to the solution
for variable in new_array_contenedores:
    if 'S' in variable:
        problem.addVariable(variable,dominioN+dominioE)
    elif 'R' in variable:
        problem.addVariable(variable,dominioE)
problem.addConstraint(constraint.AllDifferentConstraint())
##Constraint so theres no floating container
deepestEValue=0
deepestNValue=0
for row in range(0,newArrMapaShape[0]):
    for column in range(0,newArrMapaShape[1]):
        if 'E' in new_array_mapa[row][column]:
            if int(new_array_mapa[row][column][1])>deepestEValue:
                deepestEValue=int(new_array_mapa[row][column][1])
        elif 'N' in new_array_mapa[row][column]:
            if int(new_array_mapa[row][column][1])>deepestNValue:
                deepestNValue=int(new_array_mapa[row][column][1])
deepestNonXValue=max(deepestEValue,deepestNValue)
def notFloating(*args):
    lastRow=False
    for x in args:
        if int(x[1])==deepestNonXValue:
            lastRow=True
    contiguousAmount=0
    for x in args:
        for y in args:
            if x!=y:
                if (abs(int(x[1])-int(y[1]))==1 and int(x[2])==int(y[2])) or (abs(int(x[2])-int(y[2]))==1 and int(x[1])==int(y[1])) :
                    contiguousAmount+=1

    if lastRow == True and contiguousAmount==comb(len(args),2):
        return True
problem.addConstraint(notFloating,new_array_contenedores)





print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("Solucion final")
solutions=problem.getSolutions()
solutionN=1
for solution in solutions:
    print("Solution Nr. "+str(solutionN))
    solutionN+=1
    #Copy final map array to modify it and insert containers in it
    final_map_array=copy.deepcopy(new_array_mapa)
    #Create dataframe to store pairs of container:cell
    dataframe=pd.DataFrame.from_dict(solution,orient="index",columns=['Cell'])
    dataframe.reset_index(level=0,inplace=True)
    dataframe.columns=['Container','Cell']
    #Fill cell map with the containers
    for row in range(0,newArrMapaShape[0]):
        for column in range(0,newArrMapaShape[1]):
            for index,dfrow in dataframe.iterrows():
                if final_map_array[row][column]==dfrow["Cell"]:
                    final_map_array[row][column]=dfrow["Container"]
    #Remove container and port from the container name
    for row in range(0,newArrMapaShape[0]):
        for column in range(0,newArrMapaShape[1]):
            final_map_array[row][column]=final_map_array[row][column][0]
    #Print solution
    for row in final_map_array:
        print(row)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


