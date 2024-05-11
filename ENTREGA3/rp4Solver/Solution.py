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

ford_matrix,Ford_last_stdv = Markov_Model.sendInfoToAnalize("Ford3",is_ipynb)
NIO_matrix,NIO_last_stdv = Markov_Model.sendInfoToAnalize("NIO3",is_ipynb)

print(ford_matrix)

#S1-Día de la Inversión (0,1,2....)
#S2-Dinero de la inversión en el día S1 (100,101,102...)
#S3-Empresa en la que esta la inversión en el día S1 (Ford,Nio)

empresas=["Ford","Nio"]

def Starting_State():    
    s1=1
    s2=100
    s3=empresas[0]
    s=(s1,s2,s3)    
    return s

#Si el dinero llega a 0, no puedo invertir
#Si la acción subio el día anterior, se mantiene
#Si la acción bajo el día anterior, se cambia

def Action_Set(s):
    (s1,s2,s3)=s    
    if s2<=0: AS=['myself']    
    else: AS=['Cambio','Mantengo']       
    return AS

def Event_Set(s,a):
    (s1,s2,s3)=s
    ES=['Sube','Baja']            
    return ES

def Transition_Equations(s,a,e):
    (s1,s2,s3)=s    
    sn1=s1+1
    if a=='Cambio': sn2=s2-(s2*0.10)
    if e=='Baja' and s3=='Ford': 
        sn3='Nio'
    elif e=='Baja' and s3=='Nio':
        sn3='Ford'

    """Aqui voy porque estoy buscando como traer la desviación estándar"""
    if s2>0 and e=='malo':
        sn2=1
    sn=(sn1,sn2,sn3)
    return sn

def Constraints(s,a,sn,L):
    (sn1,sn2)=sn
    Ct=(sn1<=4)
    return Ct

def Transition_Probabilities(s,a,e):
    (s1,s2)=s
    if a==0: p=1    
    if a>0 and e=='malo': p=0.5**a
    if a>0 and e=='bueno': p=1-(0.5**a)    
    return p
    
def Action_Contribution(s,a):
    if a==0: ca=0
    if a>0: ca=300+(100*a)
    return ca

def Event_Contribution(s,a,e):
    ce=0 
    return ce

def Quality_Function(m,p,ca,ce,V_sn):
    Q_s_a=ca+sum(p[i]*(ce[i]+V_sn[i]) for i in range(0,m))
    return Q_s_a

def Optimal_Value_Function(Q_s_a):
    V_s=min(Q_s_a)
    return V_s

def Boundary_Condition(s):    
    (s1,s2)=s
    if (s1==4 and s2==1): V_s=1600
    else: V_s=0
    return V_s