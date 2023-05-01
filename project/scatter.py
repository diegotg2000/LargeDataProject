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
    html.H1('Average Sentiment per Cluster', style={'marginBottom': '50px'}),
    # Add a button to reload the data
    html.Button('Reload Data', id='reload-button', n_clicks=0, style={'marginBottom': '50px', 'backgroundColor': '#0074D9', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'}),
    # Add a scatter plot to show the average sentiment per cluster
    dcc.Graph(id='sentiment-per-cluster')
])

# Define the callback for the reload button
@app.callback(
    dash.dependencies.Output('sentiment-per-cluster', 'figure'),
    [dash.dependencies.Input('reload-button', 'n_clicks')]
)
def update_sentiment_per_cluster(n_clicks):
    # Reload the data from the CSV file
    df = pd.read_csv('predictions.csv')
    # Compute the average sentiment per cluster
    avg_sentiment = df.groupby('Cluster')['Sentiment'].mean()
    #color_map = {0: 'red', 1: 'blue', 2: 'green'}
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