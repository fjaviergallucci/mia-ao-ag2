import itertools
from IPython.display import display
import matplotlib.pyplot as plt
import random
from time import time
import math

_COSTES = [[11, 12, 18, 40],    #agente 0
           [14, 15, 13, 22],    #agente 1
           [11, 17, 19, 23],    #agente 2
           [17, 14, 20, 28]]    #agente 3

# _COSTES = [[1, 2, 3, 4],    #agente 0
#            [5, 6, 7, 8],    #agente 1
#            [9, 10, 11, 12],    #agente 2
#            [13, 14, 15, 16]]    #agente 3

# Calculo del valor de una solucion parcial
#   index = tarea
#   value = agente
def valor(s, costes):
    valor = 0
    for i in range(len(s)):
        valor += costes[s[i]][i]
    return valor


# print(valor((3, 2, 0, 1), _COSTES))
# print()


# Coste inferior para soluciones parciales
#  (1,3,) Se asigna la tarea 1 al agente 0 y la tarea 3 al agente 1
#   index = agente
#   value = tarea
def CI(s, costes):
    valor = 0
    # Valores establecidos
    for i in range(len(s)):
        valor += costes[i][s[i]]

    # Estimacion
    for i in range(len(s), len(costes)):
        values = [costes[j][i] for j in range(len(s), len(costes))]
        aux = min(values)
        valor += aux
    return valor

# print(CI((3,), _COSTES))
# print()

def CS(s, costes):
    valor = 0
    # Valores establecidos
    for i in range(len(s)):
        valor += costes[i][s[i]]

    # Estimacion
    for i in range(len(s), len(costes)):
        values = [costes[j][i] for j in range(len(s), len(costes))]
        aux = max(values)
        valor += aux
    return valor


# print(CS((3,), _COSTES))
# print()

# Genera tantos hijos como como posibilidades haya para la siguiente elemento de la tupla
# (0,) -> (0,1), (0,2), (0,3)
def crear_hijos(nodo, n):
    hijos = []
    for i in range(n):
        if i not in nodo:
            hijos.append({'s': nodo + (i,)})
    return hijos


# print(crear_hijos((3, 2, 0, 1), 4))
# print()


def ramificacion_y_poda(costes):
    # Construccion iterativa de soluciones(arbol). En cada etapa asignamos un agente(ramas).
    # Nodos del grafo  { s:(1,2),CI:3,CS:5  }
    # print(COSTES)
    dimension = len(costes)
    mejor_solucion = tuple(i for i in range(len(costes)))
    CotaSup = valor(mejor_solucion, costes)
    #print("Cota Superior:", CotaSup)

    nodos = []
    nodos.append({'s': (), 'ci': CI((), costes)})

    iteracion = 0

    while(len(nodos) > 0):
        iteracion += 1

        nodo_prometedor = [min(nodos, key=lambda x:x['ci'])][0]['s']
        #print("Nodo prometedor:", nodo_prometedor)

        # Ramificacion
        # Se generan los hijos
        hijos = crear_hijos(nodo_prometedor, dimension)
        HIJOS = [{'s': x['s'], 'ci':CI(x['s'], costes)}
                 for x in hijos]

        # Revisamos la cota superior y nos quedamos con la mejor solucion si llegamos a una solucion final
        NODO_FINAL = [x for x in HIJOS if len(x['s']) == dimension]
        if len(NODO_FINAL) > 0:
            #print("\n********Soluciones:",  [x for x in HIJOS if len(x['s']) == DIMENSION  ] )
            if NODO_FINAL[0]['ci'] < CotaSup:
                CotaSup = NODO_FINAL[0]['ci']
                mejor_solucion = NODO_FINAL

        # Poda
        HIJOS = [x for x in HIJOS if x['ci'] < CotaSup]

        # Añadimos los hijos
        nodos.extend(HIJOS)

        # Eliminamos el nodo ramificado
        nodos = [x for x in nodos if x['s'] != nodo_prometedor]

    print("La solucion final es:", mejor_solucion, " en ",
          iteracion, " iteraciones", " para dimension: ", dimension)

# ramificacion_y_poda(_COSTES)
# print()

def fuerza_bruta(costes):
    mejor_valor = 10e10
    mejor_solucion = ()

    for s in list(itertools.permutations(range(len(costes)))):
        valor_tmp = valor(s, costes)
        if valor_tmp < mejor_valor:
            mejor_valor = valor_tmp
            mejor_solucion = s

    print(f'La mejor solucion es : {mejor_solucion}. Con valor: {mejor_valor}')

# fuerza_bruta(_COSTES)
# print()

def generate_costs(dimension):
    return [[random.randint(1, 20) for _ in range(dimension)] for _ in range(dimension)]


dimension = []
tiempo_fuerza_bruta = []
tiempo_ramificaion_poda = []

for i in range(5, 12):
    _COSTES = generate_costs(i)
    # display(_COSTES)
    dimension.append(i)

    start_time = time()
    ramificacion_y_poda(_COSTES)
    end_time = time()
    tiempo_ramificaion_poda.append(end_time - start_time)

    start_time = time()
    fuerza_bruta(_COSTES)
    end_time = time()
    tiempo_fuerza_bruta.append(end_time - start_time)

    print(f'Ramificacion y Poda tiempo total {end_time - start_time} con {i} dimensiones')
    print(f'Fuerza brutal tiempo total {end_time - start_time} con {i} dimensiones\n')


plt.plot(dimension, tiempo_ramificaion_poda, label="Ramificacion y poda")
plt.plot(dimension, tiempo_fuerza_bruta, label="Fuerza bruta")
plt.xlabel("Dimensiones")  # add X-axis label
plt.ylabel("Tiempo ejecucion")  # add Y-axis label
plt.title("Tiempo x Nº dimensiones")  # add title
plt.grid()
plt.legend()
plt.show()

