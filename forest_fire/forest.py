import numpy as np
import random 
from tqdm import tqdm
from scipy.spatial.distance import jensenshannon
import pickle
import time
from scipy.stats import wasserstein_distance


class forest_cl():

    def __init__(s,N,rho,p,f):
        s.N = N
        s.rho = rho 
        s.p = p 
        s.f = f 
        s.forest = np.random.choice([0, 1], size=N, p=[1-s.rho,s.rho])
        s.distribution = np.zeros(int(5*p/f))
        s.cluster_compute()
        s.burn_distribution = []
        s.divergence_history = []


    def cluster_compute(s):
        index=0
        s.distribution = np.zeros(int(5*s.p/s.f))
        while index <len(s.forest):
            
            if s.forest[index]==1:
                size = index
                while  index <len(s.forest) and s.forest[index] == 1:
                    index+=1
                
                size = index-size
                s.distribution[size] +=1

            else:
                index += 1
        return

    def get_cluster_size(s,i):

        if s.forest[i] == 0:
            return 0

        cluster_size =1      
        
        t=i-1
        while t>0 and s.forest[t]==1:
            cluster_size +=1
            t=t-1

        t=i+1
        while t<s.N and s.forest[t]==1:
            cluster_size +=1
            t=t+1
        
        return cluster_size

    def burn(s,i):

        if s.forest[i] == 0:
            return

        s.forest[i] = 0
        cluster_size =1

        #burn left
        t= i-1
        while t>0 and s.forest[t]==1:
            s.forest[t]=0
            cluster_size +=1
            t=t-1

        #burn right
        t=i+1
        while t<s.N and s.forest[t]==1:
            s.forest[t]=0
            cluster_size +=1
            t=t+1
        
        #reudce distribution entry 
        s.distribution[cluster_size] -=1
        s.burn_distribution.append(cluster_size)

        return

    def plant(s,i):
        if s.forest[i] == 0:
            s.forest[i] = 1
            s.distribution[s.get_cluster_size(i)] += 1

        return

    def js_divergence(s,a,b):
        return jensenshannon(a,b)
        # return wasserstein_distance(a,b)






    def update(s,iterations=10**7,clear=False):

        if clear:
            s.divergence_history = []

        s.previous = np.array(s.distribution,copy=True)
        scale = int(s.p/s.f)
        for iter in tqdm(range(iterations//scale)):
 
            for _ in range(scale):
                i = int(np.random.rand()*s.N)
                if s.forest[i] == 0:
                    s.plant(i)

            i = int(np.random.rand()*s.N)
            if s.forest[i] == 1:
                s.burn(i)        

            if  iter%(10**5//scale)==0:
                div = s.js_divergence(s.previous,s.distribution)
                s.divergence_history.append(div)
                s.previous = np.array(s.distribution,copy=True)

        return 


    def store(s,file='forest'+str(int(time.time()))+'.pkl'):
        with open(file, 'wb') as f: 
            pickle.dump(s.forest, f)

        return

    def load(s,file):
        with open(file, 'rb') as f: 
            s.forest = pickle.load(f)
        s.cluster_compute()
        return    