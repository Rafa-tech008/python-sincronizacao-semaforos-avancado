#OP.DUP.SEM.02
#Declaração de variáveis

import multiprocessing
import random
import time

portas = None
tocha = None
pedra = None
porta_certa = None
semaforo = None


def iniciar(p, pe, t, pc, s):
    global portas
    global pedra
    global tocha
    global porta_certa
    global semaforo

    portas = p
    pedra = pe
    tocha = t
    porta_certa = pc
    semaforo = s


def cavaleiro(id):
    global portas
    global pedra
    global tocha
    global porta_certa
    global semaforo

    distancia = 0
    print(f"Cavaleiro {id} iniciou a caminhada")

    while distancia < 2000:
        velocidade = random.randint(2, 4)
        if tocha.value == id:
            velocidade += 2
        if pedra.value == id:
            velocidade += 2

        distancia += velocidade

        if distancia > 2000:
            distancia = 2000

        print(f"Cavaleiro {id} | Velocidade: {velocidade} m | Distancia: {distancia} m")
        time.sleep(0.05)

        if distancia >= 500:
            with semaforo:
                if tocha.value == -1:
                    tocha.value = id
                    print(f"Cavaleiro {id} pegou a tocha")

        if distancia >= 1500:
            with semaforo:
                if pedra.value == -1 and tocha.value != id:
                    pedra.value = id
                    print(f"Cavaleiro {id} pegou a pedra")

    with semaforo:
        print(f"\nCavaleiro {id} chegou nas portas")
        qtd = len(portas)

        escolha = random.randint(0, qtd - 1)
        print(f"Cavaleiro {id} escolheu a porta {portas[escolha]}")

        if portas[escolha] == porta_certa.value:
            print(f"Cavaleiro {id} encontrou a saida")
        else:
            print(f"Cavaleiro {id} foi devorado pelo monstro")
        portas.pop(escolha)


def main():

    with multiprocessing.Manager() as manager:

        portas = manager.list([1, 2, 3, 4])
        pedra = manager.Value("i", -1)
        tocha = manager.Value("i", -1)
        porta_certa = manager.Value("i", random.randint(1, 4))

        semaforo = manager.Semaphore(1)

        lista = []

        for i in range(4):
            lista.append(i + 1)

        with multiprocessing.Pool(processes=4, initializer=iniciar, initargs=(portas, pedra, tocha, porta_certa, semaforo)) as pool:
            pool.map(cavaleiro, lista)


if __name__ == "__main__":
    main()

#Fim