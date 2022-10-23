
import pandas as pd
import numpy as np
import re




def extract(datasetName = 'madrid_idealista.csv'):
    dataframe = pd.read_csv(datasetName)
    return dataframe



#función que evalua si un parámetro de 2 casas distintas coincide
def eqParam(house_1, house_2, param):
    return 1 if house_1[param] == house_2[param] else 0

#función que evalua si 2 casas están en la misma calle
def eqStreet(house_1, house_2, i):
    pattern = re.compile(r'calle\s[^,]+')
    if ( bool(re.search(pattern, house_1)) and bool(re.search(pattern, house_2)) ):
        if ( bool(re.search(pattern.findall(house_1)[0], house_2 )) ):
            return 1
        else:
            return 0
    else:
        return 0  



def transform(dataframe, house_reference = 0):
    
    #Establezco como referencia la casa que a seleccionado el usuario
    ref = dataframe.iloc[house_reference]
    
    #Utilizo una función de utilidad para asignar un valor a cada casa en función de las semejanzas con la casa seleccionada por el usuario
    newCol = list()
    for index, row in dataframe.iterrows():
        
        #Para evaluar si las casa correspondiente a la iteración del bucle está en la misma calle que la de referencia
        same_street = eqStreet(ref['Address'], row['Address'], index)
        
        #Función de utilidad
        score = (same_street*0.6 + row['Price'] - ref['Price'])/(-600) + abs(row['Squared_meters'] - ref['Squared_meters'])/(-15) + eqParam(row, ref, 'Type')*1 + eqParam(row, ref, 'Distric')*0.5 + (1 if row['Pool'] else 0)*0.15 + (1 if row['Furniture'] else 0)*0.35 + eqParam(row, ref, 'Exterior')*0.2 + (1 if row['Elevator'] else -2)*row['Floor']*0.02
        newCol.append(score)
        
        #PONDERACIONES:
        #type 1
        #ascensor 0.1*floor
        #distric 0.4
        #pool 0.15
        #amueblada 0.35
        #jardín 0.2
        #sqm 15 1
        #misma calle 0.5
    
    #Normalizo la nueva columna 'score'
    minim = min(newCol)
    newCol = [(i+abs(minim)) for i in newCol]
    rg = max(newCol) - min(newCol)
    newCol = [np.round(i/rg,3) for i in newCol]

    dataframe['score'] = newCol
    
    dataframe = dataframe.sort_values(by='score', ascending=False)
    
    return dataframe



def load(dataframe, house_reference):
    
    print('REFERENCIA:')
    print(ordered_house_df.loc[[house_reference],['Distric','Type','Price','Squared_meters','Furniture','score']],'\n')
    print('10 MEJORES RECOMENDACIONES:')
    #print(dataframe.iloc[:20])
    print(ordered_house_df.iloc[:11].loc[:,['Distric','Type','Price','Squared_meters','Furniture','score']].drop(house_reference))
    #display(ordered_house_df.loc[:,['Distric','Type','Price','Squared_meters','Floor','Furniture','Exterior','Pool','Elevator','score']])
    return None





if __name__ == '__main__':
    house_df = extract()
    house_reference = 100
    ordered_house_df = transform(house_df, house_reference)
    load(ordered_house_df, house_reference)