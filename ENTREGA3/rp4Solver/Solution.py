import sys
import os

current_dir=os.getcwd()
is_ipynb=False
try:
    sys.path.append(f'{current_dir}\ENTREGA3')
    from MARKOVIANAS import Markov_Model
    is_ipynb=False
except ImportError as e:
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(f'{parent_dir}\ENTREGA3')
    from MARKOVIANAS import Markov_Model
    is_ipynb=True

ford_matrix,ford_last_stdv = Markov_Model.sendInfoToAnalize("Ford3",is_ipynb)
NIO_matrix,NIO_last_stdv = Markov_Model.sendInfoToAnalize("NIO3",is_ipynb)


#S1-Día de la Inversión (0,1,2....)
#S2-Dinero de la inversión en el día S1 (100,101,102...)
#S3-Empresa en la que esta la inversión en el día S1 (Ford,Nio)

# Bajar = 0 ; Subir = 1

def Starting_State():    
    s1=1
    s2="Ford"
    s3=100
    s4 = 100
    s5 = 1
    s6 = 1
    s=(s1,s2,s3,s4,s5,s6)
    return s

#Si el dinero llega a 0, no puedo invertir
#Si la acción subio el día anterior, se mantiene
#Si la acción bajo el día anterior, se cambia

def Action_Set(s):
    (s1,s2,s3,s4,s5,s6)=s  
    if s1 >= 4: AS=['myself']    
    else: AS=['Cambio','Mantengo']       
    return AS

def Event_Set(s,a):
    (s1,s2,s3,s4,s5,s6)=s
    if s1 >= 4: ES=['se']
    # Bajar = 0 ; Subir = 1
    else: ES=[(0,0),(0,1),(1,0),(1,1)]            
    return ES

def Transition_Equations(s,a,e):
    (s1,s2,s3,s4,s5,s6)=s   
    sn1=s1+1
    if ((a == 'Mantengo' and s2 == 'Ford') or (a=='Cambio' and s2 == 'Nio')):
        sn2 = "Ford"
    elif ((a == 'Mantengo' and s2 == 'Nio') or (a=='Cambio' and s2 == 'Ford')):
        sn2 = "Nio"
    
    if (e == (1,0) or e == (1,1)):
        sn3 = s3 * (1 + ford_last_stdv)
    elif (e == (0,0) or e == (0,1)):
        sn3 = s3 * (1 - ford_last_stdv)

    if (e == (0,1) or e == (1,1)):
        sn4 = s4 * (1 + NIO_last_stdv)
    elif (e == (0,0) or e == (1,0)):
        sn4 = s4 * (1 - NIO_last_stdv)
    
    if (e == (1,0) or e == (1,1)):
        sn5 = 1
    elif (e == (0,0) or e == (0,1)):
        sn5 = 0

    if (e == (0,1) or e == (1,1)):
        sn6 = 1
    elif (e == (0,0) or e == (1,0)):
        sn6 = 0

    sn=(sn1,sn2,sn3,sn4,sn5,sn6)
        
    return sn

def Constraints(s,a,sn,L):
    (sn1,sn2,sn3,sn4,sn5,sn6)=sn
    Ct=(sn1<=4)
    return Ct

def Transition_Probabilities(s,a,e):
    (s1,s2,s3,s4,s5,s6)=s
    if e == (1,1):
        p = ford_matrix[1][s5] * NIO_matrix[1][s6]
    elif e == (1,0):    
        p = ford_matrix[1][s5] * NIO_matrix[0][s6]
    elif e == (0,1):
        p = ford_matrix[0][s5] * NIO_matrix[1][s6]
    elif e == (0,0):
        p = ford_matrix[0][s5] * NIO_matrix[0][s6] 
    return p
    
def Action_Contribution(s,a):
    (s1,s2,s3,s4,s5,s6)=s
    if a=="Mantengo": ca=0
    if a=="Cambio" and s2 == 'Ford': ca=s3*0.01
    if a=="Cambio" and s2 == 'Nio': ca=s4*0.01
    return ca

def Event_Contribution(s,a,e):
    (s1,s2,s3,s4,s5,s6)=s
    if ((e == (1,0) or e == (1,1)) and s2 == 'Ford'): ce=s3*ford_last_stdv
    if ((e == (0,0) or e == (0,1)) and s2 == 'Ford'): ce=-s3*ford_last_stdv
    if ((e == (0,1) or e == (1,1)) and s2 == 'Nio'): ce=s4*NIO_last_stdv
    if ((e == (0,0) or e == (1,0)) and s2 == 'Nio'): ce=-s4*NIO_last_stdv
    return ce

def Quality_Function(m,p,ca,ce,V_sn):
    Q_s_a=ca+sum(p[i]*(ce[i]+V_sn[i]) for i in range(0,m))
    return Q_s_a

def Optimal_Value_Function(Q_s_a):
    V_s=max(Q_s_a)
    return V_s

def Boundary_Condition(s):    
    V_s=0
    return V_s