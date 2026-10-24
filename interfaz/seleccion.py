import random
from abc import ABC, abstractmethod
from typing import List
from CromosomaBin import CromosomaBinario

class Seleccion(ABC):
    @abstractmethod
    def seleccion_poblacion(self, poblacion: List[CromosomaBinario], participantes: int=3) -> List[CromosomaBinario]:
        pass

class SeleccionTorneo(Seleccion):
    def __init__(self, participantes=3) -> None:
        super().__init__()
        self.participantes = participantes

    def seleccion_poblacion(self, poblacion: List[CromosomaBinario]) -> List[CromosomaBinario]:
        ganadores = []
        for i in range(len(poblacion)):
            competidores = random.sample(poblacion, self.participantes)
            ganador = max(competidores, key=lambda cromosoma: cromosoma.score)
            ganadores.append(ganador)
        return ganadores
    
class SeleccionRuleta(Seleccion):
    def seleccion_poblacion(self, poblacion: List, participantes: int=0) -> List:
        mating_pool = []
        suma_fitness = sum(c.score for c in poblacion)
        
        # Seleccionamos un número de padres igual al tamaño de la población
        for _ in range(len(poblacion)):
            r = random.uniform(0, suma_fitness)
            acumulado = 0.0
            for cromosoma in poblacion:
                acumulado += cromosoma.score
                if acumulado >= r:
                    mating_pool.append(cromosoma)
                    break
                    
        return mating_pool
    
    
    