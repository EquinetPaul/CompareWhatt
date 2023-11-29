"""
CompareWhatt
"""
import json
from datetime import timedelta
import pandas as pd
from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go

app = Flask(__name__)

def projection(df : pd.DataFrame, electricity_price: float, theorical_evolution : float):
    """
    Projette les coûts totaux pour chaque produit dans un DataFrame sur une période de 50 ans.

    Paramètres:
    df (pd.DataFrame): DataFrame contenant les données des produits
    electricity_price (float): Le prix de l'électricité par kWh.
    theorical_evolution (float): Evolution théorique du prix du kWh/année

    Retourne:
    pd.DataFrame: Un DataFrame avec les coûts totaux projetés pour chaque produit et chaque jour sur une période de 50 ans.
    """
    start_date = pd.to_datetime('today')
    end_date = start_date + timedelta(days=50*365)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df['Consommation (kWh/annum)'] = df['Consommation (kWh/annum)'].astype(float)
    df['Daily_Consumption'] = df['Consommation (kWh/annum)'] / 365
    rows = []
    for _, row in df.iterrows():
        for date in dates:
            years_passed = (date.year - start_date.year)
            adjusted_electricity_price = float(electricity_price) * ((1 + float(theorical_evolution)) ** years_passed)
            days_passed = (date - start_date).days
            total_price = float(row['Prix de vente']) + row['Daily_Consumption'] * days_passed * adjusted_electricity_price
            rows.append({'Total_Price': total_price, 'Date': date, 'Product': row['id']})    
    final_df = pd.DataFrame(rows)
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    final_df['Date'] = final_df['Date'].dt.strftime('%d/%m/%Y')
    return final_df

def transform_projection(df: pd.DataFrame):
    """
    Transforme les données projetées en une structure JSON adaptée pour la visualisation.

    Paramètres:
    df (pd.DataFrame): DataFrame contenant les données projetées

    Retourne:
    str: Une chaîne JSON représentant les données transformées, adaptée pour la visualisation.
    """
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').astype(str)
    data = []
    for product_id, group in df.groupby('Product'):
        product_data = {
            'label': f'Produit {product_id}',
            'data': group[['Date', 'Total_Price']].to_dict('records'),
        }
        data.append(product_data)
    data_json = json.dumps(data)
    return data_json

def transform_projection_plotly(df: pd.DataFrame):
    """
    Prépare les données pour la visualisation avec Plotly, en formatant les données projetées en traces Plotly.

    Paramètres:
    df (pd.DataFrame): DataFrame contenant les données projetées

    Retourne:
    str: Une chaîne JSON représentant le graphique Plotly, adaptée pour la visualisation interactive.
    """
    data = []
    for product_id, group in df.groupby('Product'):
        trace = go.Scatter(
            x=group['Date'],
            y=group['Total_Price'],
            mode='lines',
            name=f'Produit {product_id}',
            hoverinfo='text', 
            text=group.apply(lambda row: f'Date: {row.Date}, Prix: {row.Total_Price}', axis=1)
        )
        data.append(trace)
    layout = dict(
        title='Comparaison des Prix de Produits',
        xaxis=dict(
            title='Date',
        ),
        yaxis=dict(title='Prix Total'),
    )
    fig = dict(data=data, layout=layout)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Fonction principale et gestionnaire des routes HTTP
    """
    products_data = []
    if request.method == 'POST':
        electricity_price = request.form.get("electricity_price")
        theorical_evolution = request.form.get("theorical_evolution")
        for i in range(1, 6):
            product_price = request.form.get(f'productPrice{i}')
            product_consumption = request.form.get(f'productConsumption{i}')
            if product_price and product_consumption:
                products_data.append({
                    'Prix de vente': product_price,
                    'Consommation (kWh/annum)': product_consumption,
                    'id': i 
                })


        products_df = pd.DataFrame(products_data)
        projection_df = projection(products_df, electricity_price, theorical_evolution)
        # products_df.to_csv("save.csv")
        # projection_to_template = transform_projection(projection_df)
        projection_to_template = transform_projection_plotly(projection_df)
        return render_template('index.html', products=products_data, electricity_price=electricity_price, theorical_evolution=theorical_evolution, chart_data=projection_to_template)
    return render_template('index.html', products=products_data, electricity_price=0.16, theorical_evolution=0.008236)

if __name__ == '__main__':
    app.run(debug=True)
