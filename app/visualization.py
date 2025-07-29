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
    html.H2("Countries", style={'textAlign': 'center', 'marginBottom': '30px', 'fontFamily': 'Arial, sans-serif'}),

    html.Div([
        html.Div([
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict('records'),
                sort_action="native",
                row_selectable="single",
                selected_rows=[],
                page_size=10,
                style_table={
                    'overflowX': 'auto',
                    'minWidth': '100%',
                },
                style_header={
                    'backgroundColor': '#004080',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '16px',
                    'fontFamily': 'Arial, sans-serif',
                    'border': 'none',
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'minWidth': '120px',
                    'maxWidth': '300px',
                    'whiteSpace': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'borderBottom': '1px solid #ddd',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'flag_desc'},
                        'maxWidth': '300px',
                        'whiteSpace': 'normal',
                    }
                ],
                style_data_conditional=[
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': '#BFD7FF',
                        'border': '1px solid #004080',
                        'color': '#004080',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#f9f9f9',
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'white',
                    },
                    {
                        'if': {'state': 'active'},  # hover
                        'backgroundColor': '#D6E8FF',
                        'border': '1px solid #004080',
                    }
                ],
                tooltip_delay=500,
                tooltip_duration=None,
            )
        ], style={
            'flex': '9',
            'padding': '20px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'backgroundColor': 'white',
            'maxHeight': '80vh',
            'overflowY': 'auto'
        }),

        # Desna strana: zastava - zauzima oko 10% širine i stoji na vrhu
        html.Div(id='flag-container', style={
            'flex': '1',
            'textAlign': 'center',
            'padding': '10px',
            'marginLeft': '20px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'borderRadius': '12px',
            'backgroundColor': '#f4f6f8',
            'maxHeight': '150px',   # malo manja visina
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'flex-start',
            'alignItems': 'center',
            'position': 'sticky',
            'top': '20px'           
        }),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'maxWidth': '1200px',
        'margin': '0 auto',
        'alignItems': 'flex-start' 
    })
])


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')