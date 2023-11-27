from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def projection(df : pd.DataFrame, electricity_price):
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    products_data = []
    if request.method == 'POST':
        for i in range(1, 6):
            product_price = request.form.get(f'productPrice{i}')
            product_consumption = request.form.get(f'productConsumption{i}')
            if product_price and product_consumption:
                products_data.append({
                    'Prix de vente': product_price,
                    'Consommation (kWh/annum)': product_consumption,
                    'id': i  # Ajouter un identifiant pour chaque produit
                })

    return render_template('index.html', products=products_data)

if __name__ == '__main__':
    app.run(debug=True)
