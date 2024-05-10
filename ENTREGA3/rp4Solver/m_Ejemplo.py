'''
Model: All or nothing (2 state variables)
Objective: Profit Maximization
'''

def Starting_State():    
    s1=1
    s2=1
    s=(s1,s2)    
    return s

def Action_Set(s):
    (s1,s2)=s    
    if s2==0: AS=['myself']    
    else: AS=[0,1,2,3]       
    return AS

def Event_Set(s,a):
    (s1,s2)=s
    if a==0: ES=['se']
    if a>0: ES=['bueno','malo']            
    return ES

def Transition_Equations(s,a,e):
    (s1,s2)=s
    sn1=s1+1
    if a==0: sn2=s2    
    if s2>0 and e=='bueno': 
        sn2=0
    if s2>0 and e=='malo':
        sn2=1
    sn=(sn1,sn2)
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