import constraint
from constraint import *
import sys
from constraint import *
import numpy as np
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
for len in range(0,MapaShape[0]):
    new_array_mapa.append([])

for row in range(0,MapaShape[0]):
    for column in range(0,MapaShape[1]):
        new_array_mapa[row].append(array_mapa[row][column]+str(row)+str(column))

print("Array final del mapa")
for row in new_array_mapa:
    print(row)

new_array_contenedores=[]
ContendoresShape=np.shape(array_contenedores)
for row in range(0,ContendoresShape[0]):
    new_array_contenedores.append(array_contenedores[row][0]+array_contenedores[row][1]+array_contenedores[row][2])
print("Array final de contenedores")
print(new_array_contenedores)

problem = Problem()

dominioE=[]
dominioN=[]
newArrMapaShape=np.shape(new_array_mapa)
for row in range(0,newArrMapaShape[0]):
    for column in range(0,newArrMapaShape[1]):
        if 'E' in new_array_mapa[row][column]:
            dominioE.append(new_array_mapa[row][column])
        elif 'N' in new_array_mapa[row][column]:
            dominioN.append(new_array_mapa[row][column])

for variable in new_array_contenedores:
    if 'S' in variable:
        problem.addVariable(variable,dominioN+dominioE)
    elif 'R' in variable:
        problem.addVariable(variable,dominioE)
problem.addConstraint(constraint.AllDifferentConstraint())
print("------------------------------------------------------------------------------------------------------------------------------------------------")
print("Solucion final")
print(problem.getSolution())