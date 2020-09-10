import pandas
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
from db import create_connection

def convert_date(output):
    monthyear = output.find(class_='css-tr15v5').find('b').text
    year = monthyear.split(' ')[-1]
    month = monthyear.split(' ')[0]
    if month =='Jan':
        month = '01'
    elif month =='Feb':
        month = '02'
    elif month =='Mrt':
        month = '03'
    elif month =='Apr':
        month = '04'
    elif month =='Mei':
        month = '05'
    elif month =='Jun':
        month = '06'
    elif month =='Jul':
        month = '07'
    elif month =='Aug':
        month = '08'
    elif month =='Sep':
        month = '09'
    elif month =='Okt':
        month = '10'
    elif month =='Nov':
        month = '11'
    elif month =='Dec':
        month = '12'
    else:
        month = '12'
    return f'{year}-{month}-01'


cars = ['BMW','Audi','Volkswagen','Mercedes Benz','Peugeot','Opel','Renault','Toyota','Ford']

def create_model():
    db_file = 'instance/database.db'
    conn = create_connection(db_file)
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM cars;")
    rows = cur.fetchall()
    df = pandas.DataFrame(rows, columns =['id', 'date', 'name','price','brand','type','year','km','fuell','gearbox'])
    df = df[['price','brand','year','km','fuell','gearbox']]
    df['year'] = pandas.to_numeric(df['year'].str[:4])
    df['km'] = pandas.to_numeric(df['km'], errors='coerce')
    df['price'] = pandas.to_numeric(df['price'], errors='coerce')
    df = pandas.get_dummies(df)
    df = df.dropna()

    y = np.array(df['price'])
    df = df.drop(['price'], axis=1)
    x = np.array(df)

    model = LinearRegression().fit(x, y)
    names = [x for x in df.columns]
    pickle.dump(model, open('finalized_model.sav', 'wb'))
    print(names)
    return names

def create_prediction(data, model, names):
    df_predict = pandas.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],columns=names)
    data_clean = [k+'_'+str(v) for k,v in data.items()]

    df_predict.at[0,'year'] = data.get('year')
    df_predict.at[0,'km'] = data.get('km')
    df_predict.at[0,data_clean[2]] = 1
    df_predict.at[0,data_clean[3]] = 1
    df_predict.at[0,data_clean[4]] = 1
    print([x for x in df_predict.columns])
    return model.predict(np.array(df_predict))[0]

if __name__ == '__main__':
    data = {
        'year':2011,
        'km':1000,
        'brand':'audi',
        'fuell':'Benzine',
        'gearbox':'Automatisch'
    }
    names = create_model()
    model = pickle.load(open('instance/finalized_model.sav', 'rb'))
    output = create_prediction(data, model, names)
    print(output)

