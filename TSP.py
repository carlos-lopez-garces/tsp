import time
from geom import *
from random import *
from math import *

"""
  ITESM Campus Guadalajara
  Inteligencia Computacional
  Recocido simulado para el problema del TSP en circulo.
  Autor: Carlos Enrique Lopez Garces a01082449  
"""

class TSP:
    
    def __init__(self, n):
        # P son los 100 valores aleatorios que se anadiran al costo de la solucion.
        self.P = []
        self.genP()
        # n es el numero de ciudades.
        self.n = n        
        self.cities = []
        self.generateNCities()
        # distanceMatrix es la matriz de distancias entre cada par de ciudades.
        self.distanceMatrix = []
        self.generateDistanceMatrix()

    """
        Se generan los 100 numeros aleatorios que se anadiran al costo de la solucion.
        Los numeros aleatorios van del 0 al 1, distribuidos uniformemente.
    """
    def genP(self):
        for i in range(0, 100):
            self.P.append(uniform(0,1))    

    """
        Se generan n ciudades sobre la circunferencia de un circulo de radio 1.
        Cada ciudad esta separada de las adyacentes por la misma distancia 2PI/n.
    """
    def generateNCities(self):
        inc = 2*pi/self.n
        ang = 0
        for i in range(self.n):
            x = cos(ang)
            y = sin(ang)
            self.cities.append(Point2D(x, y))
            ang += inc

        self.cities.append(self.cities[0])
        
    """
        Se genera la matriz de distancias entre cada par de ciudades, anadiendo
        los valores aleatorios P[i] y P[j].
    """
    def generateDistanceMatrix(self):
        for i in range(self.n):
            self.distanceMatrix.append([])
            for j in range(self.n):
                self.distanceMatrix[i].append(round(self.cities[i].getDistanceTo(self.cities[j]), 3))
                #self.distanceMatrix[i].append(round(self.cities[i].getDistanceTo(self.cities[j]), 8)+self.P[i]+self.P[j])    

    """
        Se genera una solucion aleatoria, es decir, una secuencia de n ciudades
        en orden aleatorio. Se incluye el retorno a la ciudad origen.
    """
    def generateRandomSolution(self):
        solution = []
        cities = range(0, self.n)
        
        while len(cities) > 0:
            c = choice(cities)
            solution.append(c)
            cities.remove(c)

        solution.append(solution[0])

        return solution


    """
        Se calcula el costo de una solucion, sumando las distancias de una ciudad
        a la siguiente de la secuencia.
    """
    def calculatePathLength(self, solution):
        pathLength = 0
        for i in range(0, len(solution)-1):
            pathLength += self.distanceMatrix[solution[i]][solution[i+1]]
        return pathLength

    """
        La perturbacion consiste en intercambiar de lugar la posicion de dos
        ciudades elegidas de forma aleatoria.
    """
    def perturbSolution(self, perturbedSolution):        
        indexes = range(0, len(perturbedSolution)-1)

        i = choice(indexes)
        j = i       

        while i == j:
            j = choice(indexes)

        pIPlus1 = perturbedSolution[i+1]        
        perturbedSolution[i+1] = perturbedSolution[j]
        perturbedSolution[j] = pIPlus1

        if j == 0:
            perturbedSolution[len(perturbedSolution)-1] = perturbedSolution[0]
        else:
            if (i+1 == len(perturbedSolution)-1):
                perturbedSolution[0] = perturbedSolution[len(perturbedSolution)-1]
        
        return [i, j]        

    """
        Esta funcion define el Cooling Schedule: t/(1+bt). Esta funcion permite
        que la temperatura, cuando es alta, se reduzca rapidamente, mientras que
        cuando es baja, lentamente.
    """
    def lowerT(self, t):
        b = 0.00009
        t = t / (1 + (b * t))
	#print str(t)+"\n"	
        return t

    """
        Esta funcion implementa el algoritmo de recocido simulado.
        El criterio de paro es que la solucion aceptada no haya cambiado durante
        700 iteraciones. Este valor se determino experimentalmente.
        La temperatura desciende cada 5 iteraciones, esto debido a que el cooling
        schedule hace descender la temperatura muy lentamente cuando el valor de t
        es bajo. Si se dieran mas iteraciones, el algoritmo seria mucho mas lento.
    """
    def anneal(self, s0, t0):
        # contador de iteraciones, para controlar descenso de temp. 
        iteration = 1
        # solution es solucion actual, la ultima que fue aceptada.
        solution = s0[:]
        temperature = t0
        # esta variable cuenta el numero de iteraciones en las que no ha cambiado
        # la solucion aceptada.
        iterationsWithoutChange = 0

        # E1 es el costo de la solucion aceptada.
        E1 = self.calculatePathLength(solution)        

        iterations = 0
        # el criterio de paro es que se den 700 iteraciones sin cambio en la solucion.
        while iterationsWithoutChange < 700:
            iterations += 1
            perturbedSolution = solution[:]

            # se perturba la solucion.
            self.perturbSolution(perturbedSolution)
            # E2 es el costo de la solucion perturbada.
            E2 = self.calculatePathLength(perturbedSolution)                        
            # deltaE es la diferencia de costo entre la solucion aceptada y la perturbada.
            deltaE = E2-E1            

            # criterio de metropolis.
            if deltaE <= 0 or exp(-deltaE/temperature) > uniform(0, 1):
                # se acepta la solucion perturbada.
                solution = perturbedSolution
                E1 = E2

                # se reinicia el contador de iteraciones sin cambio en la solucion.
                iterationsWithoutChange = 0
                #print "Costo: "+str(E1)

            # disminuye la temperatura cada 5 iteraciones.
            if iteration%5 == 0:
                temperature = self.lowerT(temperature)
                
            iterationsWithoutChange += 1
            iteration += 1 

        print "tf = "+str(temperature)
        print "---------------------------------------------------"
        print "\nIterations: ",iterations,"\n"
        return solution

    """
        Las funciones definidas a continuacion, son para hacer representacion textual.
    """

    def getTextRep(self):
        textRep = "---------------------------------\n"
        textRep += "Problem: TSP\n---------------------------------\n"
        textRep += "N (number of cities) = "+str(self.n)+"\n\nCoordinates of cities:\n"
        for i in range(0, self.n):
            textRep += "\nC"+str(i)+" = "+self.cities[i].getTextRep()
        return textRep

    def printSolution(self, solution):
        solStr = "Solution (sequence of cities): "
        for i in range(0, len(solution)):
            solStr += "C"+str(solution[i])+","
        solStr += "\b  | Path Length: "+str(self.calculatePathLength(solution))
        print solStr

    def printDistanceMatrix(self):        
        tmp = "\nDistance Matrix:\n\n"
        
        for i in range(self.n):
            tmp += "\tC"+str(i)
        tmp += "\n\n"
        for i in range(self.n):
            tmp += "C"+str(i)+"\t"
            for j in range(self.n):
                tmp += str(self.distanceMatrix[i][j])+"\t"
            tmp += "\n"
        print tmp


# 100 ciudades.
n = 100
# el constructor del objeto se encarga de inicializar la lista de ciudades y la matriz de distancias.
tsp = TSP(n)
# se genera una solucion aleatoria.
solution = tsp.generateRandomSolution()
# se corre el algoritmo y se imprime su solucion.
print "---------------------------------------------------"
print "Solucion TSP"
print "n = 100"
print "t0 = 1000"

start = time.time()
tsp.printSolution(tsp.anneal(solution, 1000))
end = time.time()
elapsed= end - start
print "---------------------------------------------------"
print "\n Tiempo: ",elapsed," segs., o ",elapsed*1000," ms."
