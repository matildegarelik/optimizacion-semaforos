import random
import math

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

    print(mejor_aptitud)
            
    return mejor, mejor_aptitud,fitness

def ordenar_y_sumar(individuos, fitness_normalizado):
    combinados = list(zip(fitness_normalizado, individuos))
    combinados.sort()
    fitness_ordenado, individuos_ordenado = zip(*combinados)

    fitness_ordenado = [0] + list(fitness_ordenado)
    suma_acumulada = [fitness_ordenado[i] + fitness_ordenado[i+1] for i in range(len(fitness_ordenado)-1)]
    return suma_acumulada, individuos_ordenado

def seleccionar(individuos, fitness, tipo='RULETA', cantidad=10):
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

def mutar(cruza):
    punto_mutacion = int(random.uniform(0,len(cruza)))
    mutacion = (
        cruza[:punto_mutacion] + 
        ('0' if cruza[punto_mutacion] == '1' else '1') + 
        cruza[punto_mutacion + 1:]
    )
    return mutacion

def reproducir(individuos):
    # CANTIDAD HIJOS = PADRES SI ES PAR O IMPAR. SI ES IMPAR SE AGREGA COMO HIJO UN PADRE MUTADO
    hijos = []
    for i in range(0,len(individuos), 2):
        individuo1 = individuos[i]
        individuo2 = individuos[i+1] if i+1 < len(individuos) else None
        if individuo2:
            cruza1, cruza2 = cruzar(individuo1, individuo2)
            mutacion1 = mutar(cruza1)
            mutacion2 = mutar(cruza2)
            hijos.append(mutacion1)
            hijos.append(mutacion2)
        else:
            mutacion = mutar(individuo1)
            hijos.append(mutacion)
    return hijos

def generar_nueva_generacion(progenitores, fitness_prog, hijos, cantidad_poblacion,tipo='REEMPLAZO TOTAL',mejor_individuo=None):
    if tipo == 'REEMPLAZO TOTAL':
        return hijos
    if tipo == 'REEMPLAZO CON BRECHA':
        # elegir 0.2 mejores progenitores y agregar a hijos
        progenitores_supervivientes,_ = seleccionar(progenitores, fitness_prog, cantidad=math.ceil(0.2 * cantidad_poblacion), tipo='RULETA')
        return hijos + progenitores_supervivientes
    if tipo =='ELITISMO':
        hijos.append(mejor_individuo)
        return hijos

def entrenar(funcion_aptitud,cantidad_poblacion=6,tipo_reemplazo='REEMPLAZO TOTAL',max_it=100,aptitud_requerida=-0.55, longitud=10,imprimir=True):
    # SE USA UNA LONGITUD DE 14 PARA TENER SUFICIENTES BITS PARA REPRESENTAR X e Y
    individuos = inicializar_poblacion(longitud, cantidad=cantidad_poblacion)
    mejor_individuo, mejor_aptitud, fitness = evaluar(funcion_aptitud,individuos)
    
    progreso = [mejor_individuo]
    it=0
    while (mejor_aptitud < aptitud_requerida) and (it < max_it):

        # GENERAR NUEVA POBLACION
        if(tipo_reemplazo=='REEMPLAZO TOTAL'):
            cantidad_padres = cantidad_poblacion
        elif(tipo_reemplazo=='REEMPLAZO CON BRECHA'):
            cantidad_padres = math.floor(0.8 * cantidad_poblacion)
        elif(tipo_reemplazo=='ELITISMO'):
            cantidad_padres = cantidad_poblacion-1
            #individuos.remove(mejor_individuo)

        progenitores, fitness_prog = seleccionar(individuos, fitness, cantidad=cantidad_padres, tipo='VENTANA')

        hijos = reproducir(progenitores)
        #reemplazo
        individuos = generar_nueva_generacion(progenitores, fitness_prog, hijos, cantidad_poblacion,tipo=tipo_reemplazo,mejor_individuo=mejor_individuo)

        #EVALUAR
        mejor_individuo, mejor_aptitud, fitness = evaluar(funcion_aptitud,individuos)
        progreso.append(mejor_individuo)
        if imprimir:
            print(f"Iteración {it} - Mejor Aptitud: {mejor_aptitud}")
        it+=1

    return mejor_individuo, it, progreso, mejor_aptitud
    
