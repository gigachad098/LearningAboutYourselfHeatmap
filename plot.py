import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as graph


class ParsedCSV:
    def __init__(self, csv):
        self.csvarray = csv
        self.csvcopy = csv
        self.app = dash.Dash('MyApp')
        self.recommededvaluedict = {'Steps': 10000, 'Fat': 65, 'Carbs': 300,
                                    'Protein': 50, 'Sodium': 2.4, 'Fiber': 25, 'Calories': 2000}
        self.fig = make_subplots(rows=1, cols=1)
        daysofweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.fig.update_xaxes(title_text="Food Category", tickvals=list(range(7)), ticktext=list(self.recommededvaluedict.keys()))
        self.fig.update_yaxes(title_text='Day of the Week', tickvals=list(range(7)), ticktext=daysofweek)
        self.csvarray = self.setCSVValues()
        self.heatmap_trace = graph.Heatmap(z=self.csvarray)
        self.fig.add_trace(self.heatmap_trace)
        self.app.layout = html.Div([
            dcc.Graph(id='graph', figure=self.fig),
            html.Div([
                dcc.Dropdown(
                    id='choose-value',
                    options=[
                        {'label': 'Steps', 'value': 'Steps'},
                        {'label': 'Fat', 'value': 'Fat'},
                        {'label': 'Carbs', 'value': 'Carbs'},
                        {'label': 'Protein', 'value': 'Protein'},
                        {'label': 'Sodium', 'value': 'Sodium'},
                        {'label': 'Fiber', 'value': 'Fiber'},
                        {'label': 'Calories', 'value': 'Calories'}
                    ],
                    value='Steps'
                ),
                dcc.Input(id='dailyvalue', type='number', value=1),
                html.Button('Update Value', id='update-button', n_clicks=0)
            ]),
        ])
        self.app.callback(
            Output('graph', 'figure'),
            [Input('update-button', 'n_clicks')],
            [dash.dependencies.State('choose-value', 'value'),
             dash.dependencies.State('dailyvalue', 'value')]
        )(self.setRecommendedValues)

    def setRecommendedValues(self, n_clicks, choosevalue, dailyvalue):
        if n_clicks == 0:
            return self.fig
        self.recommededvaluedict.update({choosevalue: dailyvalue})
        newtrace = self.setCSVValues()
        self.fig.update_traces(z=newtrace)
        return self.fig

    def setCSVValues(self):
        templist = []
        for col in self.csvcopy:
            temprow = []
            i = 0
            for key in self.recommededvaluedict.items():
                temprow.append(float(col[i])/key[1])
                i += 1
            templist.append(temprow)
        return templist


def parsecsv(file):
    vallist = []
    with open(file, 'r') as f:
        for i in range(7):
            vallist.append(f.readline().split(","))
    f.close()
    return vallist


def main(filepath):
    parser = ParsedCSV(parsecsv(filepath))
    parser.app.run_server()


main('./data.csv')
