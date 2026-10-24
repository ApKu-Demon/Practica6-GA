from abc import ABC, abstractmethod
from CromosomaBin import CromosomaBinario
import random
from typing import List

class Mutacion(ABC):
    @abstractmethod
    def mutacion_poblacion(self, poblacion: List[CromosomaBinario]):
        pass

class MutacionFlip(Mutacion):
    def __init__(self, probabilidad: float):
        super().__init__()
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion: List[CromosomaBinario]):
        max_valor = 2**poblacion[0].gen_width - 1
        for crom in poblacion:
            for i in range(1, crom.n_genes + 1):
                prob_gen = random.random() # de 0 al 1
                if prob_gen < self.prob:
                    valor = crom.get_bits(i)
                    # mutación flip
                    valor = valor ^ max_valor
                    crom.set_bits(valor, i)
                    
class MutacionOctal(Mutacion):
    def __init__(self, probabilidad: float):
        super().__init__()
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion: List):
        for crom in poblacion:
            for i in range(1, crom.n_genes + 1):
                prob_gen = random.random() # de 0 a 1
                if prob_gen < self.prob:
                    # Mutación octal: asignamos un nuevo valor aleatorio de 0 a 7
                    nuevo_valor = random.randint(0, 7)
                    crom.set_gen(nuevo_valor, i)
                    
class MutacionDecimal(Mutacion):
    def __init__(self, probabilidad: float):
        super().__init__()
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion: List):
        for crom in poblacion:
            for i in range(1, crom.n_genes + 1):
                if random.random() < self.prob:
                    # Asignar un procesador diferente aleatorio del 1 al 3
                    crom.set_gen(random.randint(1, 3), i)
                    
                    
                    