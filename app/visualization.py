import dash
from dash import html, dash_table, Input, Output
import pandas as pd
from sqlalchemy import create_engine
import os

app = dash.Dash(__name__)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL)

df = pd.read_sql("SELECT * FROM countries", engine)

app.layout = html.Div([
    html.H2("Countries"),

    html.Div([
        # Leva strana: tabela
        html.Div([
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict('records'),
                sort_action="native",
                row_selectable="single",
                selected_rows=[],
                page_size=10,
                style_table={'overflowX': 'auto', 'minWidth': '0px'},
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '100px',  
                    'maxWidth': '200px',  
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'flag_desc'},
                        'maxWidth': '250px',    
                        'whiteSpace': 'normal', 
                    }
                ],
            )
        ], style={'flex': '2', 'marginRight': '20px', 'minWidth': '0px'}),

        # Desna strana: zastava
        html.Div(id='flag-container', style={'flex': '1', 'textAlign': 'center'})
    ], style={'display': 'flex'})
])

# Callback za prikaz zastave
@app.callback(
    Output('flag-container', 'children'),
    Input('data-table', 'derived_virtual_data'),
    Input('data-table', 'derived_virtual_selected_rows')
)
def update_flag(rows, selected_rows):
    if selected_rows is None or len(selected_rows) == 0:
        return html.Div("Select a country to see its flag.")

    selected_row = selected_rows[0]
    selected_data = rows[selected_row]

    flag_url = selected_data.get('flag_png')
    country_name = selected_data.get('country_name', 'Unknown')

    if flag_url:
        return html.Div([
            html.H4(f"Flag of {country_name}"),
            html.Img(src=flag_url, style={'height': '100px'})
        ])
    else:
        return html.Div(f"No flag URL available for {country_name}.")

# Pokretanje aplikacije
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')