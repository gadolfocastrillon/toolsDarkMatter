#import pandas as pd
import funcion_l as lik
#from scipy.optimize import differential_evolution
import numpy as np
import time

def diccionario(x_):
    # Definición de parámetros base
    data = {
        'MAp': 3., 
        'mphi': 1,
        'Mchi1': 0.1,
        'angle': 1e-4,
        'gX': 0.1182,
        'epsilon': 0.1,
        'ff': 0.10
    }
    
    global delta_rel_deseado, alphaD,R 
    gx = np.sqrt(4*np.pi*alphaD)
    
    # Asignación de valores a partir del punto x_ en el espacio de parámetros
    Mx1 = 10**x_[0]      # Masa Mx1
    Ms2 = 10**x_[1]      # Masa mphi
    epsilon = 10**x_[2]   # epsilon

    # Cálculo de parámetros dependientes
    MAp = R * Mx1
    vphi = MAp / (2 * gx)
    
    # Calculamos ff (yf) para obtener el delta relativo deseado
    # Sabemos que: Mx2 = Mx1 + 2*f*vphi
    # Y queremos: (Mx2 - Mx1)/Mx1 = delta_rel_deseado
    # Por lo tanto: 2*f*vphi/Mx1 = delta_rel_deseado
    # Despejando f:
    yf = (delta_rel_deseado * Mx1) / (2 * vphi)
    #yf = (delta_deseado) / (2*vphi)
    
    # Ahora calculamos Mx2 según la relación del programa
    Mx2 = Mx1 + 2 * yf * vphi
    
    theta = 5e-4  # Ángulo de mezcla fijo
    
    # Verificación del delta relativo (para debug)
    delta_rel_actual = (Mx2 - Mx1)/Mx1
    if not np.isclose(delta_rel_actual, delta_rel_deseado, rtol=1e-4):
        print(f"Advertencia: Delta relativo actual {delta_rel_actual:.4f} difiere del deseado {delta_rel_deseado:.4f}")
    
    # Actualización del diccionario
    data.update({
        'MAp': MAp,
        'mphi': Ms2,
        'Mchi1': Mx1,
        'angle': theta,
        'gX': gx,
        'epsilon': epsilon,
        'ff': yf
    })
    
    return data

def de_scan(bounds, tamanio, nombre_='datos.txt'):
    x = [] 
    start_time = time.time()

    def objective(x_):
        ob = lik.Likelihood(diccionario(x_))
        datos = ob.get_datos()
        x.append(datos)

    # Corregido: mchi1_log
    mchi1_values = np.random.uniform(bounds[0][0], bounds[0][1], tamanio)
    mchi1_linear = 10**mchi1_values
    
    # Corregido: mphi basado en mchi1
    factores = np.random.uniform(1.0, 2.0, tamanio)
    mphi_linear = mchi1_linear * factores # Definición de mphi_linear
    mphi_values = np.log10(mphi_linear)
    
    # Epsilon
    epsilon_values = np.random.uniform(bounds[1][0], bounds[1][1], tamanio)
    
    vector = np.column_stack([mchi1_values, mphi_values, epsilon_values])
    print("Vectores aleatorios generados")

    for i in range(tamanio):
        objective(vector[i])
    
    
    sltns = 0
    try:
        if x:
            with open(nombre_, mode='w', encoding='utf-8') as f:
                # 1. Extraer las cabeceras (nombres de las claves del primer diccionario)
                cabeceras = list(x[0].keys())
                f.write(",".join(cabeceras) + "\n")
                
                # 2. Iterar sobre los resultados, filtrar y escribir
                for fila in x:
                    # Filtro manual para Omega
                    valor_omega = fila.get('Omega', 0)
                    
                    if 0.11 <= valor_omega <= 0.13:
                        # Convertir cada valor a string y unir por comas
                        linea = ",".join([str(fila[col]) for col in cabeceras])
                        f.write(linea + "\n")
                        sltns += 1
            
            print(f"Datos almacenados con éxito en {nombre_}")
            print(f"El tamaño de los datos filtrados es: {sltns}")
        else:
            print("No se generaron datos en la lista x")

    except Exception as e:
        print(f"Los datos no han podido ser almacenados. Error: {e}")

    return sltns


if __name__ == '__main__': 
    from math import log
    
    # 1. Alineación correcta de variables (4 espacios o 1 tab constante)
    delta_rel_deseado = 0.1
    alphaD = 0.1
    R = 3

    # 2. Definición de Bounds
    epsilonMin = log(1e-6, 10)
    epsilonMax = log(1e-2, 10)
    mmin = 1e-3
    mmax = 1e-1
    mchi1Min = log(mmin, 10)
    mchi1Max = log(mmax, 10)
    
    tamanio_data = 1000000
    
    bounds = [(mchi1Min, mchi1Max), (epsilonMin, epsilonMax)]

    archivo = 'ard_results.txt'
    print(f"Running de_scan en {archivo}") 
    
    tO = time.time()
    sltns = de_scan(bounds, tamanio_data, nombre_=archivo)
    
    de_time = (time.time() - tO) / 3600 
    
    linea = f"sltns = {sltns} y la cantidad de horas fue {de_time:.2f}"
    with open('nohup.out', 'w') as f:
        f.write(linea + '\n')