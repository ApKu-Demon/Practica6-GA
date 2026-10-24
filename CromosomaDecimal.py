import random

class CromosomaDecimal(object):
    def __init__(self, genes: int):
        self.n_genes = genes
        self.score = -1.0  # El fitness ahora es un valor flotante fraccionario
        self.max_carga = 0 # Propiedad auxiliar para visualizar M(x) - tiempo maximo de carga
        self.genes = [1] * genes

    def llenar_random_data(self):
        for i in range(self.n_genes):
            # Base Decimal: procesadores del 1 al 3
            valor = random.randint(1, 3)
            self.set_gen(valor, i + 1)

    def get_gen(self, gen: int) -> int:
        return self.genes[gen - 1]

    def set_gen(self, valor: int, gen: int) -> None:
        self.genes[gen - 1] = valor

    @property
    def representacion(self) -> str:
        return "".join(str(g) for g in self.genes)