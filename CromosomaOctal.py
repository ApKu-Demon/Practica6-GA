import random

class CromosomaOctal(object):
    def __init__(self, genes: int):
        self.n_genes: int = genes
        self.score: int = -1
        # Usamos una lista donde cada índice es la columna y el valor (0-7) la fila
        self.genes = [0] * genes

    def llenar_random_data(self):
        for i in range(self.n_genes):
            # Base octal: valores del 0 al 7
            valor = random.randint(0, 7)
            self.set_gen(valor, i + 1)

    def get_gen(self, gen: int) -> int:
        return self.genes[gen - 1]

    def set_gen(self, valor: int, gen: int) -> None:
        self.genes[gen - 1] = valor

    @property
    def representacion(self) -> str:
        # Devuelve el cromosoma como un string continuo para fácil visualización
        return "".join(str(g) for g in self.genes)