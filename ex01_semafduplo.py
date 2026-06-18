#OP.DUP.SEM.01
#Declaração de variáveis

import multiprocessing
import random
import time

pistas = None
semaforo = None


def iniciar(p, s):
    global pistas
    global semaforo

    pistas = p
    semaforo = s


def aviao(id):
    global pistas
    global semaforo

    with semaforo:
        pista = random.choice(["NORTE", "SUL"])

        if pista == "NORTE" and pistas[0] == 1:
            pista = "SUL"

        elif pista == "SUL" and pistas[1] == 1:
            pista = "NORTE"

        if pista == "NORTE":
            pistas[0] = 1
        else:
            pistas[1] = 1

        print(f"\nAviao {id} manobrando na pista {pista}")
        time.sleep(random.uniform(0.3, 0.7))

        print(f"Aviao {id} taxiando na pista {pista}")
        time.sleep(random.uniform(0.5, 1.0))

        print(f"Aviao {id} decolando pela pista {pista}")
        time.sleep(random.uniform(0.6, 0.8))

        print(f"Aviao {id} afastando da area pela pista {pista}")
        time.sleep(random.uniform(0.3, 0.8))

        print(f"Aviao {id} concluiu a decolagem pela pista {pista}")

        if pista == "NORTE":
            pistas[0] = 0
        else:
            pistas[1] = 0

        print(f"Pista {pista} liberada")


def main():

    with multiprocessing.Manager() as manager:

        pistas = manager.Array("i", [0, 0])

        semaforo = manager.Semaphore(2)

        processos = []

        for i in range(12):
            processos.append(i + 1)

        with multiprocessing.Pool(processes=12,initializer=iniciar, initargs=(pistas, semaforo)) as pool:
            pool.map(aviao, processos)


if __name__ == "__main__":
    main()

#Fim