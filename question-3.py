import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies



# Importation de la base de données
ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=';')
ratp_trie = ratp.sort_values(by = ['Trafic'], ascending=False).head(10)
ratp_trafic = ratp[["Station", "Trafic"]]

grp = ratp.groupby("Ville").agg({"Trafic": "sum"}).sort_values("Trafic", ascending=False).head(10)
print(grp)

# Importation de la base de données
idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=';')
idf_trie = idf.groupby('exploitant')['nom'].count().reset_index()


# Create bar chart of number of stations per exploitant
exploitant_stations = idf['exploitant'].value_counts()
bar_fig = px.bar(x=exploitant_stations.index, y=exploitant_stations.values)
bar_fig.update_layout(xaxis_title ="Exploitant", yaxis_title="Trafic")
# Create bar chart of number of stations per ligne
ligne_stations = idf['ligne'].value_counts()
ligne_fig = px.bar(x=ligne_stations.index, y=ligne_stations.values)
ligne_fig.update_layout(xaxis_title ="Nom", yaxis_title="Trafic")
options_ratp = [{'label' : v, 'value' : v} for v in ratp['Réseau'].unique()]
options_autres = [{'label' : v, 'value' : v}for v in idf['exploitant'].unique()]



app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Exercice 1"),
    dcc.Dropdown(id = 'drop-exercice1', options = options_ratp),
    html.Div(children=[
    dcc.Graph(id='bar-chart', figure=px.bar(ratp_trafic.sort_values(by="Trafic", ascending=False).head(10), x="Station",y="Trafic")),
    dcc.Graph(id = 'pie-chart',figure = px.pie(grp, values='Trafic', names=grp.index))
    ], style={'display':'flex'})
,
    html.H1("Exercice 2"),
    dcc.Dropdown(id = 'drop-exercice2', options = options_autres),
    html.Div(children=[
    dcc.Graph(id='exploitant-stations', figure=bar_fig),
    dcc.Graph(id='ligne-stations', figure=ligne_fig)
    ]),
    ])

@app.callback(
    dependencies.Output('bar-chart','figure'),
    dependencies.Input('drop-exercice1','value')
)
def upddate_graph(category):
    if category is None:
        df_filtered = ratp_trie
    else:
        df_filtered = ratp_trie[ratp_trie['Réseau'] == category].head(10)
    return px.bar(df_filtered, x = 'Station', y = 'Trafic')

@app.callback(
    dependencies.Output('exploitant-stations', 'figure'),
    dependencies.Input('drop-exercice2', 'value')
)

def upddate_graph(category):
    if category is None:
        df_filtered = idf_trie
    else:
        df_filtered = idf_trie[idf_trie['exploitant'] == category]
    return px.bar(df_filtered, x = 'exploitant', y = 'nom')


if __name__ == "__main__":
    app.run_server(debug=True)