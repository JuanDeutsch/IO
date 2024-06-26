import sys
import os

#A-->Empresa Inicial
A=1
B=2
#FORD-->1
#NIO-->2
#TOYOTA-->3
#HONDA--4

enterprise_dic={1:"Ford",2:"NIO",3:"Toyota",4:"Honda"}
A=enterprise_dic[A]
B=enterprise_dic[B]


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

#Establece Diccionario con todas las desviaciones y matrices de transición
ford_matrix,ford_last_stdv = Markov_Model.sendInfoToAnalize("Ford3",is_ipynb)
NIO_matrix,NIO_last_stdv = Markov_Model.sendInfoToAnalize("NIO3",is_ipynb)
toyota_matrix,toyota_last_stdv = Markov_Model.sendInfoToAnalize("Toyota3",is_ipynb)
honda_matrix,honda_last_stdv = Markov_Model.sendInfoToAnalize("Honda3",is_ipynb)

enterprise_transition_matrix={"Ford":ford_matrix,
                              "NIO":NIO_matrix,
                              "Toyota":toyota_matrix,
                              "Honda":honda_matrix}
enterprise_last_stdv={"Ford":round(ford_last_stdv,4),
                      "NIO":round(NIO_last_stdv,4),
                      "Toyota":round(toyota_last_stdv,4),
                      "Honda":round(honda_last_stdv,4)}

#Código para obtener todas las matrices y desviaciones y hacerlas estáticas
"""for i,empresa in enumerate(enterprise_last_stdv.keys()):
    print(f'{empresa}:\nMatriz:\n{enterprise_transition_matrix[empresa]}\nDesviacion:\n{enterprise_last_stdv[empresa]}')"""


def Starting_State():  
    s1=1
    s2=A
    s3=100
    s4 = 100
    s5 = 1
    s6 = 1
    s=(s1,s2,s3,s4,s5,s6)
    return s

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
    if ((a == 'Mantengo' and s2 == A) or (a=='Cambio' and s2 == B)):
        sn2 = A
    elif ((a == 'Mantengo' and s2 == B) or (a=='Cambio' and s2 == A)):
        sn2 = B
    
    if (e == (1,0) or e == (1,1)):
        sn3 = round(s3 * (1 + enterprise_last_stdv[A]),4)
    elif (e == (0,0) or e == (0,1)):
        sn3 = round(s3 * (1 - enterprise_last_stdv[A]),4)

    if (e == (0,1) or e == (1,1)):
        sn4 = round(s4 * (1 + enterprise_last_stdv[B]),4)
    elif (e == (0,0) or e == (1,0)):
        sn4 = round(s4 * (1 - enterprise_last_stdv[B]),4)
    
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
        p = enterprise_transition_matrix[A][s5][1] * enterprise_transition_matrix[B][s6][1]
    elif e == (1,0):    
        p = enterprise_transition_matrix[A][s5][1] * enterprise_transition_matrix[B][s6][0]
    elif e == (0,1):
        p = enterprise_transition_matrix[A][s5][0] * enterprise_transition_matrix[B][s6][1]
    elif e == (0,0):
        p = enterprise_transition_matrix[A][s5][0] * enterprise_transition_matrix[B][s6][0]
    return p
    
def Action_Contribution(s,a):
    (s1,s2,s3,s4,s5,s6)=s
    if a=="Mantengo": ca=0
    if a=="Cambio" and s2 == A: ca=-s3*0.01
    if a=="Cambio" and s2 == B: ca=-s4*0.01
    return ca

def Event_Contribution(s,a,e):
    (s1,s2,s3,s4,s5,s6)=s
    if ((e == (1,0) or e == (1,1)) and s2 == A): ce=s3*enterprise_last_stdv[A]
    if ((e == (0,0) or e == (0,1)) and s2 == A): ce=-s3*enterprise_last_stdv[A]
    if ((e == (0,1) or e == (1,1)) and s2 == B): ce=s4*enterprise_last_stdv[B]
    if ((e == (0,0) or e == (1,0)) and s2 == B): ce=-s4*enterprise_last_stdv[B]
    return ce

def Quality_Function(m,p,ca,ce,V_sn):
    Q_s_a=ca+sum(p[i]*(ce[i]+V_sn[i]) for i in range(0,m))
    return Q_s_a

def Optimal_Value_Function(Q_s_a):
    V_s=max(Q_s_a)
    return V_s

def Boundary_Condition(s):      
    (s1,s2,s3,s4,s5,s6)=s
    if s1 >= 4 and s2 == A: V_s= s3
    elif s1 >= 4 and s2 == B: V_s= s4
    else: V_s=0
    return V_s