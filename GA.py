import random
import copy
from typing import Dict, List
from CromosomaBin import CromosomaBinario
from interfaz.aptitud import AptitudMochila
from interfaz.seleccion import SeleccionTorneo
from interfaz.reproduccion import ReproduccionUnCruce
from interfaz.mutacion import MutacionFlip

class GA(object):
    def __init__(self, num_inv: int, num_genes: int, hyperparams: Dict, clase_cromosoma):
        self.poblacion: List[clase_cromosoma] = [clase_cromosoma(num_genes) for i in range(num_inv)]
        self.num_inv: int = num_inv
        self.hyperparams: Dict = hyperparams
        self.evaluar = hyperparams["Aptitud"]
        self.seleccion = hyperparams["Seleccion"]
        self.reproduccion = hyperparams["Reproduccion"]
        self.mutacion = hyperparams["Mutacion"]
        self.num_remplazo = int(hyperparams["por_remplazo"] * num_inv)
        
        # inicializar
        for i in range(num_inv):
            self.poblacion[i].llenar_random_data()

    def buscar_solucion(self, tolerancia: float, var: Dict):
        avg_tol: float = 99999999.99
        sum_score_prev: float = 0
        sum_score: float = 1
        generacion: int = 1
        mating_pool = None
        generacion_inicial: List = copy.deepcopy(self.poblacion)
        generacion_nueva: List = None
        fail: bool = False
        fail_count: int = 0
        fail_score: float = 0.0

        while not fail:
            self.evaluar.evaluar_poblacion(self.poblacion, var)
            sum_scores: float = sum([cromosoma.score for cromosoma in self.poblacion])
            sum_scores /= self.num_inv
            
            # Prevenir division entre 0
            if sum_score == 0: sum_score = 0.0001
            avg_tol = abs(sum_scores - sum_score_prev) / sum_score
            sum_score_prev = sum_scores

            if (generacion + 1) % 100 == 0:
                print(f"generacion {generacion:04d} avg_err: {avg_tol:.5f} avg_score: {sum_scores:.5f}")

            if fail_score == avg_tol:
                fail_count += 1
            else:
                fail_count = 0

            if fail_count >= 10:
                fail = True
                break

            if avg_tol < tolerancia:
                break

            fail_score = avg_tol
            self.poblacion = sorted(self.poblacion, key=lambda c: c.score, reverse=True)
            mating_pool = self.seleccion.seleccion_poblacion(self.poblacion)
            generacion_nueva = copy.deepcopy(self.poblacion[:self.num_remplazo])
            self.reproduccion.reproduccion_poblacion(generacion_nueva, mating_pool, self.num_inv)
            self.mutacion.mutacion_poblacion(generacion_nueva)

            generacion += 1
            self.poblacion = copy.deepcopy(generacion_nueva)


