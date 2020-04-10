import numpy as np
import matplotlib.pyplot as plt
import random, math
from scipy.special import erfc




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
    idx: 1 .. convolve with delta(1)
    idx: 2 .. matched filter root(3)
    """
    if (idx == 1):
        h_t = 1
        conv = np.convolve(G_t_n,h_t,'same')
        return conv
    elif (idx == 0):
        h_t = np.ones([10])
        conv = np.convolve(G_t_n,h_t,'same')
        return conv




def decode(Y_t,count,T):
    """
    This function decodes the outcome of the mathced filter at samples T
    we pass the count as it's the indicator where T lies
    """
    #Lambda is zero, since P(0) == P(1)
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
    for i in range (1,1+count):
    
        idx = (i*10)-1
        peakValue = Y_t[idx]
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


def AWGN(length,mean_noise,variance):
    #Generate AWGN with SNR = 1/Eb_No[0] and SNR = 1/Eb_N0[n] to show the difference
    # Generate noise samples
    return np.random.normal(mean_noise, np.sqrt(variance), length)
    
if __name__ == "__main__":
    ###VARIABLES###
    Eb_No_dB_Min = -10 #min E/No alowed in db
    Eb_No_dB_Max = 20 #max E/No alowed in db
    Eb_No_dB = np.arange(Eb_No_dB_Min,Eb_No_dB_Max+1)
    #Linearize Eb/N0
    Eb_No = 10**(Eb_No_dB/10.0)  

    Pe = [] #Probability of error
    BER = [] #Bit error rate
    count = 100000 # no of tests/time steps
    T = 1 #Width of each pulse

    #Generate random 0/1 samples 
    X_t = generateRandomProcess(count)
    #Generate g(t) where 0--> -A and 1--> A
    G_t = generatePulses (X_t,T)
    #Generate time steps with count*T elements
    T_s = generateTimeSteps(count,T)

    #MAIN LOOP 1:
    #Matched filter is h(t) = delta(t)
    for E_N0 in Eb_No:
        #Generate AWGN
        var = (1/E_N0)/2
        W_t = AWGN(len(G_t),0,var)
        #add the noise with the appropriate SNR
        G_t_n = G_t + W_t
        #Test the outcome with no matched filter h(t) = delta(t)
        #Type 1 : h(t) = delta(t), ie no Matched filter
        Y_t = matchedFilter(1,G_t_n)
        
        #NOTE: Y_t is doubled in size now!
        out_t = decode(Y_t,count,T)
        err = findError(out_t,X_t)
        BER.append(np.sum(err)/count)
        Pe.append(0.5*erfc(1/math.sqrt((1/E_N0))))

    plt.semilogy(Eb_No_dB, Pe,'r',linewidth=2)
    plt.semilogy(Eb_No_dB, BER,'-s')
    plt.grid(True)
    plt.legend(('analytical','simulation'))
    plt.xlabel('Eb/No (dB)')
    plt.ylabel('BER')
    plt.show()

    




