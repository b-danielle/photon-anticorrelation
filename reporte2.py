import matplotlib.pyplot as plt
import math
from math import sqrt
from numpy import array, savetxt
import numpy as np
import sys




def experimento(v):

    import numpy as np
    import math
    from random import random   

    
    serie_i=[] 

    serie_it=[]  
    serie_ir=[]  

    serie_t=[]   
    serie_r=[]   

    NN=v 
    
    N=5000 
    NQ=5000 
    ff=float(N)/float(NN)    
    ffQ=float(NQ)/float(NN)  
    
    
    r1 = np.random.random(size = (NN))
    r2 = np.random.random(size = (NN))
    rc = np.random.random(size = (NN))
    dharray =np.random.random(size = (NN))

    ffarray = np.full(NN,ff)
    ffQarray=np.full(NN,ffQ)
    div_haz=np.full(NN,.5)
    
    compare_t = np.less(r1,ffarray)     
    serie_t = compare_t.astype(int)   
    
    compare_r = np.less(r2,ffarray)     
    serie_r = compare_r.astype(int)   
    
    
    compare_i = np.less(rc, ffQarray)
    serie_i = compare_i.astype(int)    
        
    
    compare_it = np.greater(dharray,div_haz) 
    compare_it_inv=np.invert(compare_it)    
    
    aux1 = compare_it.astype(int)
    aux2 = compare_it_inv.astype(int)      
    
    serie_it=np.multiply(aux1, serie_i)      
    serie_ir = np.multiply(aux2, serie_i)    
            
    serie_T = serie_t + serie_it             
    serie_R = serie_r + serie_ir           
    
    unos_t = np.count_nonzero(serie_T)
    unos_r = np.count_nonzero(serie_R)       


    double_coincidence2D = np.multiply(serie_T,serie_R)  
    nc = np.count_nonzero(double_coincidence2D)
    
    triple_coincidence3D = np.multiply(serie_i,double_coincidence2D)
    nc123 = np.count_nonzero(triple_coincidence3D)
    
    double_coincidence3D_13 = np.multiply(serie_T,serie_i)
    nc13 = np.count_nonzero(double_coincidence3D_13)
    
    double_coincidence3D_23 = np.multiply(serie_R,serie_i)
    nc23 = np.count_nonzero(double_coincidence3D_23)          
    
    unos_i=np.count_nonzero(serie_i)          
    
    g2=(float(nc))/(float(unos_t)*float(unos_r))*(NN)   
    g3=(float(nc123)/(float(nc13)*float(nc23)))*float(unos_i)
    
    
    
    return [float(g2),float(g3)] 



def muestra(NN,Nexp):
    g_2d=[]
    g_3d=[]
    avg2=0
    avg3=0 
    var_g2=0
    var_g3=0
    Ninv=1.0/float(Nexp)
    for i in range(Nexp):     
            [g2,g3]=experimento(NN) 
            g_2d.append(float(g2))
            g_3d.append(float(g3))   
            avg2 = avg2 + (float(g2)*Ninv)
            avg3 = avg3 + (float(g3)*Ninv)   
    
    g2cuad=0
    g3cuad=0
    for i in range(Nexp):
        g2cuad=g2cuad + (float(g_2d[i]))**2
        g3cuad=g3cuad + (float(g_3d[i]))**2
    mucuad2=(avg2**2)*(float(Nexp))
    mucuad3=(avg3**2)*(float(Nexp))
    vg2diff=mucuad2-g2cuad        
    vg3diff=mucuad3-g3cuad       
    var_g3=float(vg3diff)
    var_g2=float(vg2diff)
    std_g2=(math.sqrt(abs(var_g2)*(Ninv)))
    std_g3=(math.sqrt(abs(var_g2)*(Ninv)))
    return[avg2,std_g2,avg3,std_g3]



t1=np.linspace(500000,5000000,20) 
                                   
g2=[]
stdg2=[]
g3=[]
stdg3=[]

for i in range(20):                 
    [a,b,c,d]=muestra(int(t1[i]),20)
    g2.append(a)                     
    stdg2.append(b)                 
    g3.append(c)                     
    stdg3.append(d)


t3=np.reciprocal(t1) 

plt.rcParams['legend.fontsize'] = 18     
fig = plt.figure()

ax = fig.gca()
fig.set_size_inches(18.5, 10.5)
   

ax.set_xlabel(r'$\tau$',fontsize=18)
ax.set_ylabel('Correlación',fontsize=18)

plt.errorbar(t3, g2, yerr=stdg2,elinewidth=2, label='$\sigma$')
plt.errorbar(t3, g3, yerr=stdg3,elinewidth=2, label='$\sigma$')

ax.legend()

plt.show()
fig.savefig('plot.png', dpi=600)


from numpy import array, savetxt
datos=np.column_stack((t3,g2,stdg2,g3,stdg3))
savetxt('datos.txt', datos, delimiter=',',header="tau,g2,stdg2,g3,stdg3", fmt='%f')
