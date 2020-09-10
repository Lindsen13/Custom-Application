import requests
from bs4 import BeautifulSoup
import pandas
from db import create_connection, insert_data, main as clear_database
from util import convert_date, cars

clear_database()

db_file = 'instance/database.db'
conn = create_connection(db_file)

for car in cars:
    try:
        car = car.lower().replace(' ','-')
        url = f'https://www.autotrader.nl/auto/{car}/'
        output = requests.get(url)
        soup = BeautifulSoup(output.text, 'html.parser')
        types = []
        for type in soup.find_all('ul')[-6].find_all('li'):
            types.append(type.text)
        print(f'types detected for {car}: {str(types)}')
        for type in types:
            type = type.lower().replace(' ','-').replace('!','').replace('ka/ka+','ka-ka-plus')
            for year in range(1995,2021):
                try:
                    url = f'https://www.autotrader.nl/auto/{car}/{type}/?fregfrom={year}&fregto={year}'
                    output = requests.get(url)
                    soup = BeautifulSoup(output.text, 'html.parser')
                    max_page = int(soup.find(class_='page-nave__desktop').find_all('li')[-1].text)
                    cars_query = []
                    for p in range(1,max_page+1):
                        url = f'https://www.autotrader.nl/auto/{car}/{type}/?fregfrom={year}&fregto={year}&page={p}'
                        output = requests.get(url)
                        soup = BeautifulSoup(output.text, 'html.parser')
                        for output in soup.find_all(class_='css-kshabm'):
                            new_car = {
                                'name':output.find(class_='css-63oe3q').text, 
                                'price':output.find(class_='price').find('span').text.replace('€ ','').replace(',-','').replace('.',''),
                                'brand':car,
                                'type':type,
                                'year':convert_date(output),
                                'km':output.find_all('span')[4].find('b').text.replace(' km','').replace('.',''),
                                'fuell':output.find(class_='css-ort0ib').find_all('li')[0].text,
                                'gearbox':output.find(class_='css-ort0ib').find_all('li')[1].text
                                }
                            cars_query.append(tuple([value for key, value in new_car.items()]))
                        print(f'scraped {str(p)} pages for {car}. ({url})')
                    output = insert_data(conn, cars_query)
                except:
                    print(f'Couldnt process all info for {car}, {year}.')
    except:
        continue

cur = conn.cursor()
cur.execute("SELECT * FROM cars;")
rows = cur.fetchall()
df = pandas.DataFrame(rows, columns =['id', 'date', 'name','price','brand','type','year','km','fuell','gearbox'])
df.to_csv('instance/output.csv', index=False)