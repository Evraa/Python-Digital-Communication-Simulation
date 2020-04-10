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
        if X_T[i] == 1:
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


def matchedFilter(idx,G_t_n):
    """
    idx: 0 .. unit energy
    idx: 1 .. no matched filter
    idx: 2 .. matched filter root(3)
    """
    if (idx == 1):
        return G_t_n


def decode(Y_t,count,T):
    """
    This function decodes the outcome of the mathced filter at samples T
    we pass the count as it's the indicator where T lies
    """
    L = 0
    out_t = []
    for i in range (1,1+count):
        peakValue = Y_t[9*i]
        if peakValue > L:
            out_t.append(1)
        else:
            out_t.append(0)
    return out_t
    
def findError(out_t,X_ts):
    """
    This function returns the error between two arrays
    """
    if (len(out_t) != len(X_ts)):
        print ("Not similar length!")
        return 0
    err = []
    for i in range(len(out_t)):
        if out_t[i] != X_ts[i]:
            err.append(1)
    return err
if __name__ == "__main__":
    ###VARIABLES###
    Eb_No_dB_Min = -10 #min E/No alowed in db
    Eb_No_dB_Max = 20 #max E/No alowed in db
    Eb_No_dB = np.arange(Eb_No_dB_Min,Eb_No_dB_Max+1)
    #Linearize Eb/N0
    Eb_No = 10**(Eb_No_dB/10.0)  

    Pe = [] #Probability of error
    BER = [] #Bit error rate
    count = 50 # no of tests/time steps
    T = 1 #Width of each pulse

    #Generate random 0/1 samples 
    X_t = generateRandomProcess(count)
    #Generate g(t) where 0--> -A and 1--> A
    G_t = generatePulses (X_t,T)
    #Generate time steps with count*T elements
    T_s = generateTimeSteps(count,T)
    #Add signal X to the graph
    plotGraphs(T_s,G_t,"Signal","Voltage","Time",1)
    #Generate AWGN with SNR = 1/Eb_No[0] and SNR = 1/Eb_N0[n] to show the difference
    # Generate noise samples
    mean_noise = 0
    variance = (1/Eb_No[0])/2
    W_t = np.random.normal(mean_noise, np.sqrt(variance), len(G_t))
    #W_t = np.random.normal(mean_noise, np.sqrt(1/Eb_No[len(Eb_No)-1]*2), len(G_t))
    #Add noise to the signal
    G_t_n = G_t + W_t
    #Add noisy graph to the graph, then show
    plotGraphs(T_s,G_t_n,"Signal with noise","Voltage","Time",2)
    #Show the graph
    #plt.show()

    '''
    After plotting Where W_t variance is (1/Eb_No[len(Eb_No)-1])/2 then (1/Eb_No[0])/2
    You'll find that the first case gives better outcome (less noise)
    since it has the least variance (0.005)
    '''
    #Test the outcome with no matched filter h(t) = delta(t)
    Y_t = matchedFilter(1,G_t_n)
    out_t = decode(Y_t,count,T)
    err = findError(out_t,X_t)

    

