from flask import Flask, request, render_template
from util import create_prediction
import pickle
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        print(request.form.get('Brand'))
        data = {
            'year':int(request.form.get('Year')),
            'km':int(request.form.get('Kilometers')),
            'brand':request.form.get('Brand').lower(), 
            'fuell':request.form.get('Fuel'), 
            'gearbox':request.form.get('Gearbox')
        }
        print(data)
        names = ['year', 'km', 'brand_audi', 'brand_bmw', 'brand_ford', 'brand_mercedes-benz', 'brand_opel', 'brand_peugeot', 'brand_renault', 'brand_toyota', 'brand_volkswagen', 'fuell_-/- (Brandstof)', 'fuell_Benzine', 'fuell_CNG', 'fuell_Diesel', 'fuell_Elektrisch', 'fuell_Elektro/Benzine', 'fuell_Elektro/Diesel', 'fuell_Ethanol', 'fuell_LPG', 'fuell_Overig', 'fuell_Waterstof', 'gearbox_-/- (Transmissie)', 'gearbox_Automatisch', 'gearbox_Half/Semi-automaat', 'gearbox_Handgeschakeld']
        model = pickle.load(open('instance/finalized_model.sav', 'rb'))
        output = create_prediction(data=data, model=model, names=names)
        output = round(output, 2)
    return render_template('index.html', output=output)
    