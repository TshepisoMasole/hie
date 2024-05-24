from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__, suppress_callback_exceptions=True)

# Load data
fun = pd.read_csv('FunOlympics.csv')

colors = {
    'background': '#192841',
    'text': '#FFFFFF',
    'navbar': '#3B9EBF',
    'dropdown_background': '#6FC0DB',
    'dropdown_text': 'black',
    'header_text': '#83aff0'
}

# 'Date' and 'Time' columns to datetime conversion
fun['DateTime'] = pd.to_datetime(fun['Date'] + ' ' + fun.get('Time', ''))

# Number of unique countries
unique_countries = fun['Country'].unique()

# Total site visits per country
site_visits_per_country = fun.groupby(['Country', 'Sports'])['Site_Visits'].sum().reset_index()

# Options for unique sports
unique_sports = fun['Sports'].unique()

# Scatter Plot
scatter_fig = px.scatter(fun, x="Country", y="Views", hover_name="Country",
                         title="Viewership per country in every sporting event")

scatter_fig.update_traces(marker=dict(color='#00BFFF'))  # Very bright blue color

scatter_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Histogram
histogram_fig = px.histogram(fun, x="Country", y="Views")

histogram_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Bar Chart
bar_fig = px.bar(fun, x="Sports", y="Views", color="Gender", barmode="group")

bar_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Choropleth Map
def generate_choropleth(selected_sport):
    filtered_data = site_visits_per_country[site_visits_per_country['Sports'] == selected_sport]
    choropleth_fig = px.choropleth(
        filtered_data,
        locations='Country',
        locationmode='country names',
        color='Site_Visits',
        hover_name='Country',
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f'Site Visits per Country for {selected_sport}'
    )
    choropleth_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return choropleth_fig

app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[

    

    html.H1("FunOlympics Dashboard", style={'textAlign': 'center', 'color': colors['header_text'], 'fontSize': '48px'}),
    
    dcc.Tabs(id="tabs", value='scatter', children=[
        dcc.Tab(label='Scatter Plot', value='scatter', style={'backgroundColor': colors['navbar']}),
        dcc.Tab(label='Bar Graph', value='bar', style={'backgroundColor': colors['navbar']}),
        dcc.Tab(label='Histogram', value='histogram', style={'backgroundColor': colors['navbar']}),
        dcc.Tab(label='Area Chart', value='area', style={'backgroundColor': colors['navbar']}),  
        dcc.Tab(label='Choropleth Map', value='choropleth', style={'backgroundColor': colors['navbar']}),
    ]),

    html.Div(id='graphs-container', style={'padding': '20px'}),
])

@app.callback(
    Output('graphs-container', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    dropdown_style = {
        'backgroundColor': colors['dropdown_background'],
        'color': colors['dropdown_text'],
        'fontWeight': 'bold'
    }
    
    if tab == 'scatter':
        return html.Div([
            dcc.Dropdown(
                id='sporting-dropdown',
                options=[{'label': sport, 'value': sport} for sport in fun['Sports'].unique()],
                value='athletics',
                clearable=False,
                style=dropdown_style
            ),
            dcc.Graph(id='scatter-graph', figure=scatter_fig, style={'height': '70vh'})
        ])
    elif tab == 'bar':
        return html.Div([
            dcc.Dropdown(
                id='sports-dropdown',
                options=[{'label': sport, 'value': sport} for sport in fun['Sports'].unique()],
                value='athletics',
                clearable=False,
                style=dropdown_style
            ),
            dcc.Graph(id='example-graph-2', style={'height': '70vh'})
        ])
    elif tab == 'histogram':
        return html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in fun['Country'].unique()],
                value='China',
                style=dropdown_style
            ),
            dcc.Graph(id='histogram',  style={'height': '70vh'})
        ])
    elif tab == 'area':
        return html.Div([
            dcc.Dropdown(
                id='sport-dropdown',
                options=[{'label': sport, 'value': sport} for sport in fun['Sports'].unique()],
                value='athletics',
                clearable=False,
                style=dropdown_style
            ),
            dcc.Graph(id='area-chart', style={'height': '70vh'})
        ])
    elif tab == 'choropleth':
        return html.Div([
            dcc.Dropdown(
                id='Sport-dropdown',
                options=[{'label': sport, 'value': sport} for sport in unique_sports],
                value=unique_sports[0],
                clearable=False,
                style=dropdown_style
            ),
            dcc.Graph(id='choropleth-graph', style={'height': '70vh'})
        ])

# Callback function to update Scatter Graph
@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('sporting-dropdown', 'value')]
)
def update_scatter(selected_sport):
    filtered_fun = fun[fun['Sports'] == selected_sport]
    scatter_fig = px.scatter(filtered_fun, x="Country", y="Views", title=f"Viewership for {selected_sport} in Every Country", hover_name="Country")

    scatter_fig.update_traces(marker=dict(color='#FF3131'))  # Very bright blue color

    scatter_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return scatter_fig

# Callback function to update histogram
@app.callback(
    Output('example-graph-2', 'figure'),
    [Input('sports-dropdown', 'value')]
)
def update_bar(selected_sport):
    filtered_fun = fun[fun['Sports'] == selected_sport]
    grouped_fun = filtered_fun.groupby('Country', as_index=False).agg({'Views': 'sum'})

    updated_figure = px.bar(grouped_fun, x="Country", y="Views",barmode="group", title=f"Viewership for {selected_sport} in Every Country")

    updated_figure.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return updated_figure

# Callback to update the area chart 
@app.callback(
    Output('area-chart', 'figure'),
    [Input('sport-dropdown', 'value')]
)
def update_area_chart(selected_sport):
    filtered_fun = fun[fun['Sports'] == selected_sport]
    
    # Create area chart
    area_fig = px.area(filtered_fun, x="DateTime", y='Views', title=f'Viewership Distribution for {selected_sport} over a period of days and time',
                       labels={'Views': 'Total Viewership', 'DateTime': 'Date and Time'}, hover_data={'DateTime': '|%B %d, %Y %H:%M', 'Views': True})
    
    area_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return area_fig

# Callback function to update bar chart
@app.callback(
    Output('histogram', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_histogram(selected_countries):
    filtered_fun = fun[fun['Country'] == selected_countries]

    hist_figure = px.histogram(filtered_fun, x="Sports", y="Views", color="Gender", barmode="group",
                        title="Viewership by Gender in every sporting event in each country")

    hist_figure.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return  hist_figure

# Callback to update choropleth map 
@app.callback(
    Output('choropleth-graph', 'figure'),
    [Input('Sport-dropdown', 'value')]
)
def update_choropleth(selected_sport):
    return generate_choropleth(selected_sport)



if __name__ == '__main__':
    app.run_server(debug=True)


