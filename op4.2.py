import numpy as np
import matplotlib.pyplot as plt


def xy_gen(N, prnt=False, plot=False, save=False):
    x_verdier = np.random.rand(N)
    y_verdier = np.random.rand(N)
    R_verdier = np.sqrt(x_verdier**2+y_verdier**2)
    R_verdier_filtra = R_verdier[R_verdier <= 1]
    n = len(R_verdier_filtra)
    pi = 4*n/N

    if prnt:
        print(
            'total antall punkt N og total antall punk inennfor n er:\n N=%i n=%i' % (N, n), pi)

    if plot:
        plt.figure(0)
        plt.scatter(x_verdier[R_verdier <= 1],
                    y_verdier[R_verdier <= 1], c="red")
        plt.title("kommer ikke på noe vittig")
        plt.xlabel("x-akse")
        plt.ylabel("y-akse")
        plt.gca().set_xlim(0, 1)
        plt.gca().set_ylim(0, 1)
        plt.gca().set_aspect("equal", adjustable="box")

        if save:
            plt.draw()
            plt.savefig("op4.1.jpg")
        else:
            plt.show()

    return pi


def M_forsøk(M, N=1000, hist=False, binST=0.01):
    pi_vekt = []

    for i in range(1, M):
        pi = xy_gen(N)
        pi_vekt.append(pi)

    middelverdi = np.mean(pi_vekt)
    std = np.std(pi_vekt)
    usikkerhet_std = std/np.sqrt(2*(M-1))
    print(middelverdi, std, usikkerhet_std)

    if hist:
        binner = np.arange(start=np.min(pi_vekt),
                           stop=np.max(pi_vekt), step=binST)
        max_verdi = M/10
        plt.hist(pi_vekt, bins=binner, color="red")
        plt.vlines(middelverdi, 0, max_verdi, linestyle="--", color="blue")
        plt.vlines(middelverdi-std, 0, max_verdi,
                   linestyle='--', color='black')
        plt.vlines(middelverdi+std, 0, max_verdi,
                   linestyle='--', color='black')
        plt.legend(["histogram=rød", "middelverdi=blå",
                   "1std=svart"], loc="upper right")
        plt.show()

    return [middelverdi, std, usikkerhet_std]


M_forsøk(1000, 10000, True, 0.005)
