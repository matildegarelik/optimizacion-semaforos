import random
import math
from datetime import datetime
import csv
import time

def inicializar_poblacion(longitud, cantidad):
   return [''.join(random.choice('01') for _ in range(longitud)) for _ in range(cantidad)]

def calcular_porcentajes(vector):
    suma_absoluta = sum(valor for valor in vector)
    porcentajes = [(valor / suma_absoluta) for valor in vector]
    return porcentajes

def evaluar(funcion_aptitud,individuos):
    mejor = individuos[0]
    mejor_aptitud=funcion_aptitud(mejor)
    fitness=[]
    for individuo in individuos:
        f=funcion_aptitud(individuo)
        fitness.append(f)
        if f > mejor_aptitud: 
            mejor_aptitud = f
            mejor = individuo
        
    return mejor, mejor_aptitud,fitness

def ordenar_y_sumar(individuos, fitness_normalizado):
    combinados = list(zip(fitness_normalizado, individuos))
    combinados.sort()
    fitness_ordenado, individuos_ordenado = zip(*combinados)

    fitness_ordenado = [0] + list(fitness_ordenado)
    suma_acumulada = [fitness_ordenado[i] + fitness_ordenado[i+1] for i in range(len(fitness_ordenado)-1)]
    return suma_acumulada, individuos_ordenado

def seleccionar(individuos, fitness, tipo='VENTANA', cantidad=10):
    progenitores =[]
    fitness_prog=[]
    if tipo =='RULETA':
        fitness_normalizado = calcular_porcentajes(fitness)
        suma_acumulada, individuos = ordenar_y_sumar(individuos, fitness_normalizado)
        i =0
        while i<cantidad:
            n = random.uniform(0,1)
            idx=0
            for v,valor in enumerate(suma_acumulada): # buscar menor indice de suma_acumulada cuyo valor sea mayor a n
                if n >= valor:
                    idx =v-1
                    break
            progenitores.append(individuos[idx])
            fitness_prog.append(fitness[idx])
            i+=1
    elif tipo == 'VENTANA':
        fitness_normalizado = calcular_porcentajes(fitness)
        _, individuos = ordenar_y_sumar(individuos, fitness_normalizado)

        # tamaño inicial  ventana
        ventana = len(individuos)
        while len(progenitores) < cantidad:
            indice_seleccionado = random.randint(0, ventana - 1)
            progenitores.append(individuos[indice_seleccionado])
            fitness_prog.append(fitness[indice_seleccionado])

            # reducir el tamaño de la ventana para las siguientes selecciones
            ventana -= 1

    #@TODO: METODO COMPETENCIAS
    return progenitores,fitness_prog

def cruzar(individuo1, individuo2):
    punto_cruza = int(random.uniform(0,len(individuo1)))
    cruza1 = individuo1[:punto_cruza] + individuo2[punto_cruza:]
    cruza2 = individuo2[:punto_cruza] + individuo1[punto_cruza:]
    return cruza1, cruza2

def mutar(cruza, tasa_mutacion):
    mutacion = cruza
    for i in range(0,5):
        if random.uniform(0,1) < tasa_mutacion:
            punto_mutacion = int(random.uniform(0,len(cruza)))
            mutacion = (
                mutacion[:punto_mutacion] + 
                ('0' if cruza[punto_mutacion] == '1' else '1') + 
                mutacion[punto_mutacion + 1:]
            )
    

    return mutacion

def reproducir(individuos, tasa_mutacion):
    # CANTIDAD HIJOS = PADRES SI ES PAR O IMPAR. SI ES IMPAR SE AGREGA COMO HIJO UN PADRE MUTADO
    hijos = []
    for i in range(0,len(individuos), 2):
        individuo1 = individuos[i]
        individuo2 = individuos[i+1] if i+1 < len(individuos) else None
        if individuo2:
            cruza1, cruza2 = cruzar(individuo1, individuo2)
            mutacion1 = mutar(cruza1, tasa_mutacion)
            mutacion2 = mutar(cruza2, tasa_mutacion)
            hijos.append(mutacion1)
            hijos.append(mutacion2)
        else:
            mutacion = mutar(individuo1, tasa_mutacion)
            hijos.append(mutacion)
    return hijos

def generar_nueva_generacion(progenitores, fitness_prog, hijos, cantidad_poblacion, tipo_seleccion, mejor_individuo=None, tasa_supervivencia=0.2):
    # elegir 0.2 mejores progenitores y agregar a hijos
    progenitores_supervivientes,_ = seleccionar(progenitores, fitness_prog, cantidad=math.ceil(tasa_supervivencia * cantidad_poblacion), tipo=tipo_seleccion)
    hijos.append(mejor_individuo)
    return hijos + progenitores_supervivientes
    

def entrenar(funcion_aptitud,cantidad_poblacion=6,tipo_seleccion = 'VENTANA', max_it=100,aptitud_requerida=-0.55, 
            tasa_mutacion=0.1, longitud=10,imprimir=True, params_aptitud=None, tasa_supervivencia=0.2):
    fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"results/output_{fecha_hora_actual}.csv"
    start_time = time.time()
    individuos = inicializar_poblacion(longitud, cantidad=cantidad_poblacion)
    mejor_individuo, mejor_aptitud, fitness = evaluar(funcion_aptitud,individuos)
    
    progreso = [mejor_individuo]
    it=0

    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(["Iteracion", "Mejor Aptitud", "Velocidad promedio", "Tiempo espera promedio"])
        
        # Guardar la primera iteración en el archivo CSV
        avg_speed, avg_waiting_time = params_aptitud(mejor_individuo)
        escritor_csv.writerow([it, mejor_aptitud, avg_speed,avg_waiting_time])

        while (mejor_aptitud < aptitud_requerida) and (it < max_it):

            # GENERAR NUEVA POBLACION: REEMPLAZO CON BRECHA Y ELITISMO
            cantidad_padres = math.floor((1-tasa_supervivencia) * cantidad_poblacion)
            
            progenitores, fitness_prog = seleccionar(individuos, fitness, cantidad=cantidad_padres, tipo=tipo_seleccion)

            hijos = reproducir(progenitores, tasa_mutacion)
            #reemplazo
            individuos = generar_nueva_generacion(progenitores, fitness_prog, hijos, cantidad_poblacion,tipo_seleccion=tipo_seleccion, mejor_individuo=mejor_individuo, tasa_supervivencia=tasa_supervivencia)

            #EVALUAR
            mejor_individuo, mejor_aptitud, fitness = evaluar(funcion_aptitud,individuos)
            progreso.append(mejor_individuo)

            # Guardar la iteración actual y mejor aptitud en el archivo CSV
            avg_speed, avg_waiting_time = params_aptitud(mejor_individuo)
            escritor_csv.writerow([it + 1, mejor_aptitud, avg_speed,avg_waiting_time])

            if imprimir:
                print(f"Iteración {it} - Mejor Aptitud: {mejor_aptitud} - Solución: {mejor_individuo} - Tiempo: {time.time()-start_time}s")
            it+=1

    tiempo =time.time()-start_time
    return mejor_individuo, it, progreso, mejor_aptitud, tiempo
    
