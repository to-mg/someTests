"""
# not pass which information should be color-coded
# https://community.plotly.com/t/is-it-possible-to-use-custom-geojson-on-go-choropleth-not-plotly-express/36819/5
"""
import json
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen

df = pd.read_csv('data.csv')
countiesborders = json.load(open("counties.json"))
df = pd.read_csv('https://raw.githubusercontent.com/FBosler/covid19-dash-app/master/functions/data.csv')
URL = 'https://raw.githubusercontent.com/FBosler/covid19-dash-app/master/functions/counties.json'
with urlopen(URL) as response:
    countiesborders = json.load(response)


colorscale = [[0.0, "#CBC2C0"], [0.5, "#CBC7C0"], [1.0, "#C3CBC0"]]
traccia1 = go.Choropleth(
    geojson=countiesborders,
    showscale=False,
    colorscale=colorscale,
    zmin=0, zmax=1,
    z=[0.5]*len(countiesborders['features']),
    locations=df['Landkreis'],
    featureidkey="properties.NAME_3")
df.sort_values(['date', 'Landkreis'], inplace=True)
counties = df['Landkreis'].unique()
prima_data = df.date.min()
inizio = df[df.date == prima_data]['infected']
# ultima_data = df.date.max()
# fine = df[df.date == ultima_data]['infected']
maxval = df.infected.max()
minval = df.infected.min()
traccia2 = go.Scattergeo(
    mode='markers',
    marker=dict(size=inizio, sizemode='area',
                # size=(df.loc[df['Date'] == dt, 'Confirmed'])**(1 / 2.7) + 3,
                opacity=0.6,
                reversescale=True,
                autocolorscale=False,
                line=dict(width=0.5, color='rgba(0, 0, 0)'),
                cmin=minval,
                color=inizio,
                cmax=maxval,
                colorbar_title="Contagiati"),
    geojson=countiesborders, locations=counties,
    featureidkey="properties.NAME_3",)

dates = df.date.unique()
frames = [dict(data=[go.Scattergeo(
    marker=dict(size=df[df.date == date]['infected'],
                color=df[df.date == date]['infected'],
                sizemode="area",),
    name="user")],
    traces=[1],
    name='frame{}'.format(date)) for date in dates]

layout = go.Layout(
    geo=dict(
        showland=False,
        showcountries=False,
        showocean=False,
        showrivers=False,
        showlakes=False,
        showcoastlines=False,
    ),
    title="A title you like",
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None])])]
)

fig = go.Figure(data=[traccia1, traccia2], frames=frames, layout=layout)
fig.update_layout(coloraxis_showscale=False)
open('fig.txt', 'wt').write(str(fig))
fig.update_geos(fitbounds="locations")
fig.show()
