from math import comb
import constraint
import sys
from constraint import *
import numpy as np
import pandas as pd
import copy
import os

if len(sys.argv) != 4:
    print(sys.argv)
    sys.exit("Invalid amount of arguments to start the program")
path = sys.argv[1]
map_path = sys.argv[2]
container_path = sys.argv[3]

array_mapa=[]
array_contenedores=[]
with open(""+path+"/"+map_path+".txt") as textFile:
    lines = [line.split() for line in textFile]
    array_mapa=lines
    if len(array_mapa)==0:
        print("The map is empty")
        sys.exit()

with open(""+path+"/"+container_path+".txt") as textFile:
    lines = [line.split() for line in textFile]
    array_contenedores=lines
    if len(array_contenedores)==0:
        print("There are no containers")
        sys.exit()


new_array_mapa=[]
MapaShape=np.shape(array_mapa)
for length in range(0,MapaShape[0]):
    new_array_mapa.append([])
#Create the new map array with the cell type, row and column
for row in range(0,MapaShape[0]):
    for column in range(0,MapaShape[1]):
        new_array_mapa[row].append(array_mapa[row][column]+str(row)+str(column))



new_array_contenedores=[]
ContendoresShape=np.shape(array_contenedores)
#create the new container array with merged id,type and port
for row in range(0,ContendoresShape[0]):
    if len(array_contenedores[row])==3:
        new_array_contenedores.append(array_contenedores[row][0]+array_contenedores[row][1]+array_contenedores[row][2])
    elif len(array_contenedores[row])==4:
        new_array_contenedores.append(array_contenedores[row][0] + array_contenedores[row][1] + array_contenedores[row][2]) + array_contenedores[row][3]

print("Array final del mapa")
for row in new_array_mapa:
    print(row)

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
#Constraint so every container has a different location
problem.addConstraint(constraint.AllDifferentConstraint())
##Constraint so theres no floating container
deepestEValue=0
deepestNValue=0
numOfUpperX=0
for row in range(0,newArrMapaShape[0]):
    for column in range(0,newArrMapaShape[1]):
        if 'E' in new_array_mapa[row][column]:
            if int(new_array_mapa[row][column][1])>deepestEValue:
                deepestEValue=int(new_array_mapa[row][column][1])
        elif 'N' in new_array_mapa[row][column]:
            if int(new_array_mapa[row][column][1])>deepestNValue:
                deepestNValue=int(new_array_mapa[row][column][1])
        elif 'X' in new_array_mapa[row][column] and not 'X' in new_array_mapa[row-1][column]:
            numOfUpperX+=1
deepestNonXValue=max(deepestEValue,deepestNValue)
def notFloating(*args):
    contiguousAmount=0
    for x in args:
        for y in args:
            if x!=y:
                if (abs(int(x[1])-int(y[1]))==1 and int(x[2])==int(y[2])) or (abs(int(x[2])-int(y[2]))==1 and int(x[1])==int(y[1])):
                    contiguousAmount+=1
    if contiguousAmount==comb(len(args),2):
        return True

problem.addConstraint(notFloating,new_array_contenedores)

def checkPort2(*args):
    lastRow = False
    for x in args:
        if int(x[1])==deepestNonXValue:
            lastRow = True
    if lastRow == True:
        return True


containersPort2=[]
for _container in new_array_contenedores:
    if len(_container)==3:
        if _container[2]=='2':
            containersPort2.append(_container)
    elif len(_container)==4:
        if _container[3]=='2':
            containersPort2.append(_container)
if len(containersPort2)!=0:
    problem.addConstraint(checkPort2,containersPort2)

solutions=problem.getSolutions()
solutionN=1
#Create output directory and empty files to fill them later
os.makedirs("outputCSP",exist_ok=True)
with open("outputCSP/"+map_path+"-"+container_path+".output", 'w',encoding="utf-8") as f:
    f.write("N??mero de soluciones: "+ str(len(solutions))+"\n")
with open("outputCSP/"+map_path+"-"+container_path+"-pretty.output", 'w',encoding="utf-8") as f:
    pass
#print and write solutions
for solution in solutions:
    contenedores=[]
    celdas=[]
    #Copy final map array to modify it and insert containers in it
    final_map_array=copy.deepcopy(new_array_mapa)
    #Create dataframe to store pairs of container:cell
    dataframe=pd.DataFrame.from_dict(solution,orient="index",columns=['Cell'])
    dataframe.reset_index(level=0,inplace=True)
    dataframe.columns=['Container','Cell']
    #Write txt file
    tmpStr = '{'
    for index, row in dataframe.iterrows():
        if len(row['Container'])==3:
            tmpStr += row['Container'][0] + ': (' + row['Cell'][2] +', '+ row['Cell'][1] + '), '
        else:
            tmpStr += row['Container'][0] +row['Container'][1] +': (' + row['Cell'][2] + ', ' + row['Cell'][1] + '), '
    tmpStr += '}\n'
    with open("outputCSP/"+map_path+"-"+container_path+".output", 'a') as f:
        f.write(tmpStr)
    #Fill cell map with the containers
    for row in range(0,newArrMapaShape[0]):
        for column in range(0,newArrMapaShape[1]):
            for index,dfrow in dataframe.iterrows():
                if final_map_array[row][column]==dfrow["Cell"]:
                    final_map_array[row][column]=dfrow["Container"]
    #Remove container and port from the container name
    for row in range(0,newArrMapaShape[0]):
        for column in range(0,newArrMapaShape[1]):
            if len(final_map_array[row][column])==3:
                final_map_array[row][column]=final_map_array[row][column][0]
            else:
                final_map_array[row][column] = final_map_array[row][column][0]+final_map_array[row][column][1]
    #Print solution
    prettyStr = "Solution Nr."+str(solutionN)+"\n"
    for row in final_map_array:
        prettyStr+=str(row)+"\n"
    prettyStr+="------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"+"\n"
    with open("outputCSP/"+map_path+"-"+container_path+"-pretty.output", 'a') as f:
        f.write(prettyStr)
    solutionN += 1




