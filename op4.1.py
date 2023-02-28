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
        plt.title("")
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


xy_gen(1000, True, True, False)
