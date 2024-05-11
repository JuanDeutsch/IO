import pandas as pd
import numpy as np

def __dataPreparationForMarkov(database_name,is_ipynb):
    #SE IMPORTA EL CSV
    if is_ipynb:
        data = pd.read_csv(f'../CSV/{database_name}.csv')
    else:
        data = pd.read_csv(f'ENTREGA3/CSV/{database_name}.csv')
    #SE BORRAN LAS COLUMNAS QUE NO SE USARAN
    data = data.drop(columns=['Open', 'High', 'Low', 'Close','Volume'])
    #SE DETERMINAN LOS CAMBIOS ENTRE REGISTROS
    percentage = [0,]
    for i in range(1, len(data)):
        percent = (data['Adj Close'][i] - data['Adj Close'][i-1]) / data['Adj Close'][i-1]
        percentage.append(percent)
    data.insert(2, 'Change %', percentage)
    #SE HALLA LA DESVIACIÓN MOVIL
    std_dev = [0,] * 20
    for i in range(21, len(percentage) + 1):
        standar_dev = np.std(percentage[i-20:i])
        std_dev.append(standar_dev)
    data.insert(3, 'std dev', std_dev)
    #SE RECUPERA LA ULTIMA DESVIACIÓN MOVIL
    last_stdv_case = data['std dev'][len(data)-1]
    #SE ESTABLECEN LOS ESTADOS PARA CADA REGISTRO
    states = [0,] * 20
    for j in range(20, len(percentage)):
        change = percentage[j]
        if change > 0:
            state = "S"
        elif change <= 0:
            state = "B"
        states.append(state)
    data.insert(4, 'Current State', states)

    next_state_column = []
    for i in range(len(data)-1):
        next_state_column.append(data['Current State'][i+1])

    previows_state_column = [0]
    for i in range(1, len(data)-1):
        previows_state_column.append(data['Current State'][i-1])

    data = data.drop(data.index[-1])
    data.insert(5, 'Next State', next_state_column)
    data.insert(4, 'Previous State', previows_state_column)
    data_trim=data.iloc[21:]
    return last_stdv_case, data_trim[['Current State', 'Next State']]

def __markovModel(data):
    #PROBABILIDAD OBSERVADA
    states=np.unique(data['Current State'])
    states_mapping = {}
    for i,state in enumerate(states):
        states_mapping[state]=i

    #PROBABILIDAD ESPERADA
    transition_matrix = np.zeros(((len(states_mapping)), len(states_mapping)))
    for i in range(len(data)):
        transition_matrix[states_mapping[data.iloc[i]['Current State']], states_mapping[data.iloc[i]['Next State']]] += 1
    for i in range(len(transition_matrix)):
        transition_matrix[i] = transition_matrix[i] / sum(transition_matrix[i])
    return transition_matrix

def sendInfoToAnalize(database_name,is_ipynb):
    last_stdv,prepared_data=__dataPreparationForMarkov(database_name,is_ipynb)
    transition_matrix =__markovModel(prepared_data)
    return transition_matrix, last_stdv