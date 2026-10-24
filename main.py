import random
from GA import GA
from CromosomaBin import CromosomaBinario
from CromosomaOctal import CromosomaOctal
from CromosomaDecimal import CromosomaDecimal

# Interfaces
from interfaz.aptitud import AptitudMochila, AptitudOchoReinas, AptitudTareas
from interfaz.seleccion import SeleccionTorneo, SeleccionRuleta
from interfaz.reproduccion import ReproduccionUnCruce, ReproduccionUnCruceOctal, ReproduccionUnCruceDecimal
from interfaz.mutacion import MutacionFlip, MutacionOctal, MutacionDecimal

def sum_pesos_test(pesos, cromosoma):
    s = 0
    for i in range(cromosoma.n_genes):
        if cromosoma.get_bits(i+1) == 1:
            s += pesos[i]
    return s

if __name__ == "__main__":
    
    MODO_EJECUCION = "TAREAS"  # MOCHILA, REINAS, TAREAS
    
    variables = {}
    gaparams = {}
    cant_ind = 100

    if MODO_EJECUCION == "MOCHILA":
        print("--- EJECUTANDO PROBLEMA DE LA MOCHILA ---")
        variables["pesos"] = [random.randint(1, 5) for _ in range(32)]
        variables["valores"] = [random.randint(10, 100) for _ in range(32)]
        variables["capacidad"] = 120 #kg
        
        num_genes = 32
        clase_cromosoma = CromosomaBinario
        
        gaparams["Aptitud"] = AptitudMochila()
        gaparams["Seleccion"] = SeleccionTorneo(3)
        gaparams["Reproduccion"] = ReproduccionUnCruce(num_genes)
        gaparams["Mutacion"] = MutacionFlip(0.05)
        gaparams["por_remplazo"] = 0.5
        
    elif MODO_EJECUCION == "REINAS":
        print("--- EJECUTANDO PROBLEMA DE LAS 8 REINAS ---")
        num_genes = 8
        clase_cromosoma = CromosomaOctal
        
        gaparams["Aptitud"] = AptitudOchoReinas()
        gaparams["Seleccion"] = SeleccionTorneo(3)
        gaparams["Reproduccion"] = ReproduccionUnCruceOctal(num_genes)
        gaparams["Mutacion"] = MutacionOctal(0.05)
        gaparams["por_remplazo"] = 0.5
        
    if MODO_EJECUCION == "TAREAS":
        print("--- EJECUTANDO PROBLEMA DE BALANCEO DE TAREAS ---")
        variables["tiempos"] = [8, 5, 7, 3, 6, 4]  # Tiempos de T1 a T6
        num_genes = 6
        clase_cromosoma = CromosomaDecimal
        
        gaparams["Aptitud"] = AptitudTareas()
        gaparams["Seleccion"] = SeleccionRuleta()
        gaparams["Reproduccion"] = ReproduccionUnCruceDecimal(num_genes)
        gaparams["Mutacion"] = MutacionDecimal(0.05)
        gaparams["por_remplazo"] = 0.5

    # Instanciamos el algoritmo pasando la clase de cromosoma correcta
    algoritmoGA = GA(cant_ind, num_genes, gaparams, clase_cromosoma)
    algoritmoGA.buscar_solucion(1e-4, variables)
    
    # Imprimir resultados dependiendo del modo
    print("\nResultados:")
    solucion = sorted(algoritmoGA.poblacion, key=lambda c: c.score, reverse=True)
    
    for i, cromosoma in enumerate(solucion[:15]):
        if MODO_EJECUCION == "MOCHILA":
            print(f"[{i:4d}] {cromosoma.bits:032b} Score: {cromosoma.score} -> {sum_pesos_test(variables['pesos'], cromosoma)} kg")
        elif MODO_EJECUCION == "REINAS":
            conflictos = 28 - cromosoma.score
            print(f"[{i:4d}] {cromosoma.representacion:<15} Score: {cromosoma.score} ({conflictos} conflictos)")
        else:
            print(f"[{i:4d}] {cromosoma.representacion:<10} Score f(x): {cromosoma.score:.5f} -> Carga M(x): {cromosoma.max_carga} unidades")

