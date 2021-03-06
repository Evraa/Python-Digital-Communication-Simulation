import math
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc


def generateRandomProcess(elementCount):
    '''
    This function returns random process of streaming bits 0 an 1.
    eg. [1, 0, 0, 1,....]
    '''
    XofT = []
    for _ in range(elementCount):
        XofT.append(math.floor(0.5 + random.uniform(0, 1)))
    return XofT


def generatePulses(X_T, width):
    '''
    This Function generates +ve and -ve pulses g(t)
    '''
    GofT = []
    for i in range(len(X_T)):
        if X_T[i] == 1:
            for _ in range(10*width):
                GofT.append(1)
        else:
            for _ in range(10*width):
                GofT.append(-1)

    return GofT


def generateTimeSteps(elementCount, width):
    '''
    This function returns time steps where output is desired
    '''
    return np.linspace(0, elementCount, 10*width*elementCount, endpoint=False)


def plotGraphs(arr1, arr2, title, label1, label2, i):

    plt.subplot(2, 1, i)
    plt.plot(arr1, arr2)
    plt.title(title)
    plt.ylabel(label1)
    plt.xlabel(label2)

    return


def matchedFilter(idx, G_t_n):
    """
    idx: 0 .. unit energy
    idx: 1 .. convolve with delta(1)
    idx: 2 .. matched filter root(3)
    """
    if (idx == 1):
        h_t = 1
        conv = np.convolve(G_t_n, h_t, 'same')
        return conv
    elif (idx == 0):
        h_t = np.ones([10])
        conv = np.convolve(G_t_n, h_t, 'same')
        return conv
    else:
        h_t = []
        for i in range(10):
            h_t.append(i*math.sqrt(3))
        conv = np.convolve(G_t_n, h_t, 'same')
        return conv

def decode(Y_t, count, T):
    """
    This function decodes the outcome of the mathced filter at samples T
    we pass the count as it's the indicator where T lies
    """
    # Lambda is zero, since P(0) == P(1)
    L = 0
    out_t = []
    # for i in range (0,2*count):
    #     if (i%2 != 0):
    #         #ODDs
    #         idx = (i*10)-1
    #         peakValue = Y_t[idx]
    #         if peakValue > L:
    #             out_t.append(1)
    #         else:
    #             out_t.append(0)
    for i in range(1, 1+count):

        idx = (i*10)-1
        peakValue = Y_t[idx]
        if peakValue > L:
            out_t.append(1)
        else:
            out_t.append(0)
    return out_t


def findError(out_t, X_ts):
    """
    This function returns the error between two arrays
    """
    out_t = np.array(out_t)
    X_ts = np.array(X_ts)
    assert out_t.size == X_ts.size
    return out_t.size - np.count_nonzero(out_t == X_ts)


def AWGN(length, mean_noise, variance):
    # Generate AWGN with SNR = 1/Eb_No[0] and SNR = 1/Eb_N0[n] to show the difference
    # Generate noise samples
    return np.random.normal(mean_noise, np.sqrt(variance), length)


if __name__ == "__main__":
    ###VARIABLES###
    Eb_No_dB_Min = -10  # min E/No alowed in db
    Eb_No_dB_Max = 20  # max E/No alowed in db
    Eb_No_dB = np.arange(Eb_No_dB_Min, Eb_No_dB_Max+1)
    # Linearize Eb/N0
    Eb_No = 10**(Eb_No_dB/10.0)

    Pe = []  # Probability of error
    BER = []  # Bit error rate
    count = 300  # no of tests/time steps
    T = 1  # Width of each pulse

    # Generate random 0/1 samples
    X_t = generateRandomProcess(count)
    # Generate g(t) where 0--> -A and 1--> A
    G_t = generatePulses(X_t, T)
    # Generate time steps with count*T elements
    T_s = generateTimeSteps(count, T)

    plt.rcParams["figure.figsize"] = (20,20)
    
    plt.plot(T_s, G_t)
    plt.title("Original Signal")
    plt.ylabel("Volts")
    plt.xlabel("Time")
    plt.ylim(-2, 2)
    plt.savefig("Original Signal")
    #plt.show()
    plt.clf()

    for i in range(3):
        # MAIN LOOP 1:
        # Matched filter is h(t) = delta(t)
        for E_N0 in Eb_No:
            # Generate AWGN
            var = (1/E_N0)/2
            W_t = AWGN(len(G_t), 0, var)
            # add the noise with the appropriate SNR
            G_t_n = G_t + W_t
            # Test the outcome with no matched filter h(t) = delta(t)
            # Type 1 : h(t) = delta(t), ie no Matched filter
            Y_t = matchedFilter(i, G_t_n)

            # NOTE: Y_t is doubled in size now!
            out_t = decode(Y_t, count, T)
            err = findError(out_t, X_t)
            BER.append(err/count)
            Pe.append(0.5*erfc(1/math.sqrt((1/E_N0))))

        #Plot the output signal
        out_t_pulses = generatePulses(out_t, T)
        plt.subplot(2,1,1)
        plt.plot(T_s, out_t_pulses)
        plt.title("Received Signal")
        plt.ylabel("Volts")
        plt.xlabel("Time")
        plt.ylim(-2, 2)
        #Plot BRE and Pe
        plt.subplot(2,1,2)
        plt.semilogy(Eb_No_dB, BER,'-s')
        plt.semilogy(Eb_No_dB, Pe,'g',linewidth=2)
        plt.grid(True)
        plt.legend(('BER','PE'))
        plt.xlabel('Eb/No (dB)')
        plt.ylabel('BER')
        title = ""
        if (i == 0):
            title+= "BER with MF: Unit Energy"
        elif i==1:
            title+="BER with MF: delta(t)"
        else:
            title += "BER with MF: sqrt(3)"
        plt.title(title)
        plt.show()
        #plt.savefig("Receiver"+str(i))
        plt.clf()
        BER.clear()
        Pe.clear()

