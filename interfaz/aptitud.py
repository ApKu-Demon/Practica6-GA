from abc import ABC, abstractmethod
from typing import List, Dict
from CromosomaBin import CromosomaBinario

class Aptitud(ABC):
    @abstractmethod
    def evaluar_poblacion(self, poblacion: List[CromosomaBinario], var: Dict):
        """interfaz encargada para darle un score a la poblacion"""
        pass

class AptitudMochila(Aptitud):
    def evaluar_poblacion(self, poblacion: List[CromosomaBinario], var: Dict):
        for cromosoma in poblacion:
            peso_total: int = 0
            valor_total: int = 0
            pesos: List[int] = var["pesos"]
            valores: List[int] = var["valores"]
            capacidad_maxima: int = var["capacidad"]
            factor_penalizacion: int = 70 # %

            # recorrer los genes
            for i in range(1, cromosoma.n_genes + 1):
                if cromosoma.get_bits(i) == 1:
                    peso_total += pesos[i-1]
                    valor_total += valores[i-1]

            # asignar el score
            if peso_total > capacidad_maxima:
                penalizacion = (peso_total - capacidad_maxima) * factor_penalizacion
                score = valor_total - penalizacion
                cromosoma.score = max(0, score)
            else:
                cromosoma.score = valor_total
            
class AptitudOchoReinas(Aptitud):
    def evaluar_poblacion(self, poblacion: List, var: Dict):
        for cromosoma in poblacion:
            conflictos = 0
            # Evaluar todos los pares posibles de reinas (combinaciones)
            for i in range(1, cromosoma.n_genes + 1):
                for j in range(i + 1, cromosoma.n_genes + 1):
                    fila_i = cromosoma.get_gen(i)
                    fila_j = cromosoma.get_gen(j)
                    col_i = i
                    col_j = j
                    
                    # Checar conflictos en la misma fila (mismo valor)
                    if fila_i == fila_j:
                        conflictos += 1
                    # Checar conflictos en diagonales (diferencia de filas == diferencia de columnas)
                    elif abs(fila_i - fila_j) == abs(col_i - col_j):
                        conflictos += 1
            
            # f(x) = 28 - c(x)
            cromosoma.score = 28 - conflictos
            
class AptitudTareas(Aptitud):
    def evaluar_poblacion(self, poblacion: List, var: Dict):
        tiempos = var["tiempos"]
        
        for cromosoma in poblacion:
            # Diccionario para sumar la carga de cada procesador
            cargas = {1: 0, 2: 0, 3: 0}
            
            for i in range(1, cromosoma.n_genes + 1):
                procesador = cromosoma.get_gen(i)
                # Sumamos el tiempo de la tarea actual al procesador asignado
                cargas[procesador] += tiempos[i - 1]
                
            # M(x) es el tiempo maximo de carga entre los procesadores
            m_x = max(cargas.values())
            
            # f(x) = 1 / (1 + M(x))
            cromosoma.score = 1.0 / (1.0 + m_x)
            cromosoma.max_carga = m_x
                
                
                