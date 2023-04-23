import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Importation de la base de données
ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=';')
ratp_trafic = ratp[["Station", "Trafic"]]

grp = ratp.groupby("Ville").agg({"Trafic": "sum"}).sort_values("Trafic", ascending=False).head(10)
print(grp)

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Exercice 1"),
    html.Div(children=[
    dcc.Graph(id='bar-chart',figure=px.bar(ratp_trafic.sort_values(by="Trafic", ascending=False).head(10), x="Station",y="Trafic")),
    dcc.Graph(id = 'pie-chart',figure = px.pie(grp, values='Trafic', names=grp.index))
    ], style={'display':'flex'})

    ])


if __name__ == "__main__":
    app.run_server(debug=True)