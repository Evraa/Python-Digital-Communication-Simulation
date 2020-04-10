import numpy as np
import matplotlib.pyplot as plt
import random, math





def generateRandomProcess(elementCount):
    '''
    This function returns random process of streaming bits 0 an 1.
    eg. [1, 0, 0, 1,....]
    '''    
    XofT = []
    for _ in range (elementCount):
        XofT.append(math.floor(0.5 + random.uniform(0, 1)))
    return XofT

def generatePulses (X_T,width):
    '''
    This Function generates +ve and -ve pulses g(t)
    '''
    GofT = []
    for i in range (len(X_T)):
        if X_T[i] == 0:
            for _ in range (10*width):
                GofT.append(1)
        else:
            for _ in range (10*width):
                GofT.append(-1)

    return GofT

def generateTimeSteps (elementCount,width):
    '''
    This function returns time steps where output is desired
    '''
    return np.linspace(0, elementCount, 10*width*elementCount, endpoint=False)

def plotGraphs (arr1, arr2, title, label1, label2,i):
    
    plt.subplot(2,1,i)
    plt.plot(arr1, arr2)
    plt.title(title)
    plt.ylabel(label1)
    plt.xlabel(label2)
    
    return


if __name__ == "__main__":
    ###VARIABLES###
    SNR_MIN = -10 #min SNR alowed in db
    SNR_MAX = 20 #max SNR alowed in db
    Eb_No_dB = np.arange(SNR_MIN,SNR_MAX+1)
    SNR = 10**(Eb_No_dB/10.0)  # linear SNR
    Pe = [] #Probability of error
    BER = [] #Bit error rate
    count = 50 # no of tests
    T = 1 #Width of each pulse

    #Generate random 0/1 samples
    X_t = generateRandomProcess(count)
    #Generate g(t) where 0--> -A and 1--> A
    G_t = generatePulses (X_t,T)
    #Generate time steps with count*T elements
    T_s = generateTimeSteps(count,T)
    #Add signal X to the graph
    plotGraphs(T_s,G_t,"Signal","Voltage","Time",1)
    #Generate additive gaussian white noise with snr = -10, SNR[0] then snr = 20, SNR[len(SNR)-1] to show the difference
    # Generate noise samples
    mean_noise = 0
    #W_t = np.random.normal(mean_noise, np.sqrt(1/SNR[0]), len(G_t))
    W_t = np.random.normal(mean_noise, np.sqrt(1/SNR[len(SNR)-1]), len(G_t))
    #Add noise to the signal
    G_t_n = G_t + W_t
    #Add noisy graph to the graph, then show
    plotGraphs(T_s,G_t_n,"Signal with noise","Voltage","Time",2)

    #Show the graph
    plt.show()