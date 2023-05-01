import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('predictions.csv')

# Define the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'textAlign': 'center', 'fontFamily': 'Arial', 'padding': '50px'}, children=[
    # Add a title to the app
    html.H1('News article sentiment analysis', style={'marginBottom': '50px'}),
    # Add a button to reload the data
    html.Button('Reload Data', id='reload-button', n_clicks=0, style={'marginBottom': '50px', 'backgroundColor': '#0074D9', 'color': 'white', 'border': 'none', 'padding': '10px 20px','borderRadius': '5px'}),
    # Add a row with the best and worst articles
    html.Div(children=[
        # Add a column for the best article
        html.Div(children=[
            # Add a title to the column
            html.H2('Most positive article', style={'marginBottom': '10px'}),
            # Add the title of the best article
            html.P(id='best-article-title', style={'fontSize': '18px', 'fontWeight': 'bold', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '50%', 'paddingRight': '20px'}),
        # Add a column for the worst article
        html.Div(children=[
            # Add a title to the column
            html.H2('Most negative article', style={'marginBottom': '10px'}),
            # Add the title of the worst article
            html.P(id='worst-article-title', style={'fontSize': '18px', 'fontWeight': 'bold', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '50%', 'paddingLeft': '20px'})
    ], style={'marginBottom': '50px'}),
    # Add a row with the graph
    html.Div(children=[
        dcc.Graph(id='sentiment-per-cluster', style={'marginTop': '20px', 'width': '100%'})
    ])
])




# Define the callback for the reload button
@app.callback(
    [dash.dependencies.Output('sentiment-per-cluster', 'figure'),
    dash.dependencies.Output('best-article-title', 'children'),
    dash.dependencies.Output('worst-article-title', 'children')],
    [dash.dependencies.Input('reload-button', 'n_clicks')]
)
def update_sentiment_per_cluster(n_clicks):
    # Reload the data from the CSV file
    df = pd.read_csv('predictions.csv')
    if len(df) == 0:
        return None, '--', '--'
    # Best title
    best_title = df.loc[df['Sentiment'].idxmax(), 'Title']
    # Worst title
    worst_title = df.loc[df['Sentiment'].idxmin(), 'Title']
    # Get graph
    graph = give_graph(df)
    return graph, best_title, worst_title


def give_graph(df):
    # Create a scatter plot showing the average sentiment per cluster
    df["Cluster"] = df["Cluster"].astype(str)
    fig = px.scatter(df, x=df.index, y='Sentiment', color="Cluster", color_discrete_sequence=["red", "green", "blue"], color_continuous_scale = px.colors.sequential.Bluered,  size_max=20)
    # Set the title of the chart 
    fig.update_layout(title='Average Sentiment per Cluster', xaxis_title='Article Index', yaxis_title='Sentiment', plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5')
    # Return the updated chart
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False, port=8050)

    #continuous_colorscale=px.colors.sequential.Viridis