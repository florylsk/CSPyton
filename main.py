from constraint import *
import sys
from constraint import *
#Todo
# if len(sys.argv) != 4:
#     sys.exit("Invalid amount of arguments to start the program")
#
# path = sys.argv[1]
# map_path = sys.argv[2]
# container_path = sys.argv[3]

array_mapa=[]
array_contenedores=[]
#TODO: cambiar esto para que use map_path
with open("mapa.txt") as textFile:
    lines = [line.split() for line in textFile]
    array_mapa=lines
    for line in lines:
        print(line)

#TODO: cambiar esto para que use container_path
with open("contenedores.txt") as textFile:
    lines = [line.split() for line in textFile]
    array_contenedores=lines
    for line in lines:
        print(line)


problem = Problem()
problem.addVariables('S',['E','N'])
problem.addVariables('R',['E'])


def validPosition(a):
   if a != "X":
        return True
problem.addConstraint(validPosition, ('S'))
problem.addConstraint(validPosition, ('R'))
print(problem.getSolutions())