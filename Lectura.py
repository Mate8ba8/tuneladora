from dash import Dash, html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server= app.server

#Base de datos
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://cagomezj:1234@cluster0.lg8bsx8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sensores.sensor_1
result = 0

# Declarar data_dist fuera de la función para evitar el UnboundLocalError
data_dist = []

# App layout
app.layout = dbc.Container([
    html.H1("Asentamiento Tuneladora", style={'text-align': 'center'}),
    html.H6("ANDRES FELIPE DIAZ MAZORCA-20231579057", style={'text-align': 'rigth'}),
    html.H6("JUAN DANIEL SANDOVAL LIZARAZO-20231579041", style={'text-align': 'rigth'}),
    html.H6("NESTOR JAVIER FLOREZ ALBINO-20231579058", style={'text-align': 'rigth'}),
    html.H6("MATEO BOHORQUEZ ANGULO-20222579010", style={'text-align': 'rigth'}),
    html.Hr(),
    html.Div([
        html.Div([
            html.H3("Descripción"),
            html.P("Una tuneladora es una máquina para cavar túneles subterráneos. Para medir los asentamientos durante la excavación en tiempo real, se utilizan sensores, los cuales proporcionan datos continuos que se transmiten a una base de datos subida a Mongo, permitiendo la detección temprana de cambios en el suelo. Los sistemas de alerta temprana que se emiten por medio de estos sensores nos ayudara a saber cuando deberemos a implementar una lechada. La integración con tecnologías de visualización ofrece representaciones visuales en tiempo real, mejorando la supervisión y la seguridad del proceso de construcción del túnel.", style={'text-align': 'left'})
        ], style={'float': 'left', 'width': '50%'}),

        html.Div([
            html.H3("Innovación"),
            html.P("Una tuneladora es una máquina para cavar túneles subterráneos. Para medir los asentamientos durante la excavación en tiempo real, se utilizan sensores, los cuales proporcionan datos continuos que se transmiten a una base de datos subida a Mongo, permitiendo la detección temprana de cambios en el suelo. Los sistemas de alerta temprana que se emiten por medio de estos sensores nos ayudara a saber cuando deberemos a implementar una lechada. La integración con tecnologías de visualización ofrece representaciones visuales en tiempo real, mejorando la supervisión y la seguridad del proceso de construcción del túnel.", style={'text-align': 'right'})
        ], style={'float': 'right', 'width': '50%'})
    ]),
    html.Hr(),
    html.H4("TUNELADORA A ESCALA", style={'text-align': 'center'}),
    html.Img(src= "https://ingenieriaenlared.files.wordpress.com/2013/01/ingenieria-en-la-red-bertha-tbm.jpg?w=400"),
    html.H4(id='distancia-actual', style={'text-align': 'center'}),
    dcc.Graph(id='asentamiento'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # en milisegundos, actualiza cada 1 segundo
        n_intervals=0
    ),
    html.Div(id='alerta-texto', style={'text-align': 'center', 'margin-top': '10px'})

])

@app.callback(
    [Output('asentamiento', 'figure'),
     Output('distancia-actual', 'children'),
     Output('alerta-texto', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def consultar(n):
    
    # Utilizar la variable global data_dist
    global data_dist , result , db
    result = db.find_one(sort=[('updated_at', -1)])
    distancia = int(result['distancia'])
    data_dist.append(distancia)
    
    # Crear el objeto de figura de Plotly
    fig = go.Figure(data=[go.Scatter(y=data_dist, mode='lines+markers')])
    
     # Agregar una línea horizontal en y=5
    fig.add_shape(
        type="line",
        x0=0,
        x1=len(data_dist),
        y0=1600,
        y1=1600,
        line=dict(color="red", width=2),
    )
    
    # Agregar un texto según la condición
    if distancia >= 1600:
        alerta_texto = html.Span("KEEP CLAM BUT THERE IS A PROBLEM", style={'color': 'red', 'font-size': '50px'})
    else:
        alerta_texto = html.Span("DON'T WORRY", style={'color': 'green', 'font-size': '50px'})
    
    
    # Formatear la distancia para mostrarla en el H1
    distancia_texto = f"El asentamiento fue: {distancia} cm"
    
    return fig, distancia_texto,alerta_texto


if __name__ == "__main__":
    app.run_server(debug=True)

    
