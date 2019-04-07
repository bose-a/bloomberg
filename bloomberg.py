# Dash
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

# Plot.ly
import plotly
import plotly.graph_objs as go

# Other
import math
import random
import json
from collections import deque
from collections import OrderedDict
from distutils.version import LooseVersion
from heapq import nlargest
from operator import itemgetter
import pandas as pd
import jupyter
import jupyter_core
import csv

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Variables
prod = 0
storage = 0
dev = 0
corp = 0
admin = 0
inet = 0
bcloud = 0
apex = 0
feed = 0
one = 0
blank = 0
tdmz = 0
area_list = []
colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}
pcolors = ['#0059b3', '#660000', '#111111', '#0080ff', '#000066', '#666666', 'cc7a00', '#999999', '#006600', '#E1396C', '#FFFFFF', '#D0F9B1']


# Data Dictionary
version_uptime_dict = {}

# Get Data
with open('data.json') as f:
    data = json.load(f)

# Number of different versions
numberofversions = 0
version_list = []
i = 0
buptimes = []
for version in data:
    if 'version' in data[i]:
        version_list.append(version['version'])
        buptimes.append(version['uptime'])
    i += 1
numberofversions = len(set(version_list))

# List that HAS duplicates for averaging uptime
fullversion_list = version_list

# Order version list from oldest to newest
version_list = sorted(version_list, key=LooseVersion, reverse=False)
version_list = list(sorted(set(version_list), key=LooseVersion, reverse=False))
print("Sorted versions; no duplicates: ", version_list)

# Create version dictionary
usedversion = []
i = 0
average = 0
numtimes = 1
mylib = {}
for x in fullversion_list:
    if x in usedversion:
        if mylib[x] != '' and buptimes[i] != '':
            average += int(mylib[x])
            average += int(buptimes[i])
            numtimes += 1
            mylib[x] = (average/numtimes)
    else:
        mylib[x] = buptimes[i]
        usedversion.append(x)
    i += 1
    average = 0
    numtimes = 1
for key in sorted(mylib.keys(), key=LooseVersion, reverse=False):
    # print("%s: %s" % (key, mylib[key]))
    if mylib[key] != '':
        version_uptime_dict[key] = int(mylib[key])
version_uptimes = []
for element in version_uptime_dict:
    version_uptimes.append(version_uptime_dict[element])
print("Version-uptime dict: ", version_uptime_dict)

# Version averages
vau = {}
total = 0
vup = OrderedDict(version_uptime_dict)
i = 0
usedprefix = []
numtimes = 1
for x in version_uptime_dict:
    keys = list(version_uptime_dict.keys())
    values = list(version_uptime_dict.values())
    versionid = keys[i]
    prefix = (((keys[i])).split('.', 1))[0]
    if prefix in usedprefix:
        total += vau[prefix]
        total += version_uptime_dict[x]
        numtimes += 1
        vau[prefix] = total/numtimes
    else:
        vau[prefix] = version_uptime_dict[x]
        usedprefix.append(prefix)
    # print("prefix: ", prefix[0])
    i += 1
    total = 0
    numtimes = 1

# Fill area list from data
for area in data:
    area_list.append(area['area'])

# Area-uptime dictionary
usedarea = []
i = 0
average = 0
numtimes = 1
alib = {}
for x in area_list:
    if 'uptime' in data[i]:
        if x in usedarea:
            if alib[x] != '' and buptimes[i] != '':
                average += int(alib[x])
                average += int(buptimes[i])
                numtimes += 1
                alib[x] = (average/numtimes)
        else:
            alib[x] = buptimes[i]
            usedarea.append(x)
    i += 1
    average = 0
    numtimes = 1
alib_ordered = {}
intuptimeforarea = []
for key in alib:
    if alib[key] != '':
        alib_ordered[key] = (int(alib[key]))
i = 0
dd = OrderedDict(sorted(alib_ordered.items(), key=lambda x: x[1]))
dd = dict(dd)
alib = dd


# Compute how many IDs have each area
areas = 0
for i in range(len(area_list)):
    if area_list[i] == "prod":
        prod += 1
        areas += 1
    elif area_list[i] == "storage":
        storage += 1
        areas += 1
    elif area_list[i] == "dev":
        dev += 1
        areas += 1
    elif area_list[i] == "corp":
        corp += 1
        areas += 1
    elif area_list[i] == "inet":
        inet += 1
        areas += 1
    elif area_list[i] == "apex":
        apex += 1
        areas += 1
    elif area_list[i] == "feed":
        feed += 1
        areas += 1
    elif area_list[i] == "admin":
        admin += 1
        areas += 1
    elif area_list[i] == "1":
        one += 1
        areas += 1
    elif area_list[i] == "":
        blank += 1
        areas += 1
    elif area_list[i] == "bcloud":
        bcloud += 1
        areas += 1
    elif area_list[i] == "tdmz":
        tdmz += 1
        areas += 1
    else:
        print("Look here! ", area_list[i])

blabels = list(alib.keys())
bvalues = list(alib.values())

# Highest and Lowest Uptimes
utimes = []
for key in version_uptimes:
    if key != '':
        utimes.append(int(key))
utimes = sorted(utimes)
versions_byvalue = OrderedDict(sorted(version_uptime_dict.items(), key=itemgetter(1), reverse=True))
i = 0
highest_uptimes = {}
# Highest
for x in range(4):
    key = list(versions_byvalue.keys())[i]
    val = list(versions_byvalue.values())[i]
    highest_uptimes[key] = val
    i += 1
i = len(versions_byvalue)-1
lowest_uptimes = {}
# Lowest
for x in reversed(range(4)):
    key = list(versions_byvalue.keys())[i]
    val = list(versions_byvalue.values())[i]
    lowest_uptimes[key] = val
    i -= 1

# Calculate percentages of each area; round to nearest tenth
prod_perc = prod / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; prod_perc = round(prod_perc, 1)
stor_perc = storage / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; stor_perc = round(stor_perc, 1)
dev_perc = dev / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; dev_perc = round(dev_perc, 1)
corp_perc = corp / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; corp_perc = round(corp_perc, 1)
inet_perc = inet / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; inet_perc = round(inet_perc, 1)
admin_perc = admin / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; admin_perc = round(admin_perc, 2)
bcloud_perc = bcloud / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; bcloud_perc = round(bcloud_perc, 2)
one_perc = one / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; one_perc = round(one_perc, 2)
blank_perc = blank / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; blank_perc = round(blank_perc, 2)
feed_perc = feed / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; feed_perc = round(feed_perc, 2)
apex_perc = apex / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; apex_perc = round(apex_perc, 2)
tdmz_perc = tdmz / (prod + storage + dev + corp + inet + admin + bcloud + one + blank + feed + apex + tdmz) * 100; tdmz_perc = round(tdmz_perc, 2)

# Graphs and tables preparation
pchart_values = [prod_perc, stor_perc, dev_perc, corp_perc, inet_perc, admin_perc, bcloud_perc, one_perc, blank_perc, feed_perc, apex_perc, tdmz_perc]
filter_columns = {'Area', 'Version', 'Uptime', 'Hostname'}
tabledata = {}
tabledata = data

# Area, Version, Uptime, and Hostname arrays for table use
index_arr = []; area_arr = []; version_arr = []; uptime_arr = []; hostname_arr = []
i = 0
for x in data:
    area_arr.append(data[i]['area'])
    i += 1
i = 0
for x in data:
    if 'version' in data[i]:
        version_arr.append(data[i]['version'])
    else:
        version_arr.append("N/A")
    i += 1
i = 0
for x in data:
    if 'uptime' in data[i]:
        uptime_arr.append(data[i]['uptime'])
    else:
        uptime_arr.append("N/A")
    i += 1
i = 0
for x in data:
    hostname_arr.append(data[i]['hostname'])
    i += 1
i = 0

# Create Dash application
app = dash.Dash()

# Layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'width': '100%', 'max-width': 100000, 'height': '100%'}, children=[

    # Title
    html.Div(children=[
        html.H2('Bloomberg', style={'textAlign': 'left', 'color': '#e6e6e6', 'margin-left': 24})
    ], className="row", style={'backgroundColor': colors['background']}),

    # Subtitle
    html.Div(children=[
        html.H4('Server Metrics', style={'textAlign': 'center', 'color': colors['text']})
    ], className="row"),

    # Graphs
    html.Div(children=[

        # Pie
        html.Div(children=[
            html.H5("Percentage Breakdown by Area", style={'textAlign': 'center', 'color': '#e6e6e6'}),
            dcc.Graph(id='area-percentages',
                figure={
                    'data': [
                        go.Pie(
                            labels=["Products", "Storage", "Development", "Corporate", "inet", "admin", "bcloud", "1", "n/a", "feed", "apex", "tdmz"],
                            values=pchart_values,
                            textfont=dict(size=13, color='#bfbfbf'),
                            marker=dict(colors=pcolors, line=dict(color='#bfbfbf', width=1))
                            ),
                    ],
                    'layout': {
                        'title': '',
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'textfont': dict(color='rgb(204,204,204', size=15),
                        'marker': dict(colors=pcolors,
                                       line=dict(color='#FFFFFF', width=1)
                                       ),
                        'legend': dict(
                                font=dict(
                                    size=11,
                                    color='#bfbfbf'
                                )
                        ),
                        # 'width': 500
                    }
                })
        ], className="col s6", style={'backgroundColor': colors['background']}),

        # Scatter
        html.Div(children=[
            html.H5("Version and Average Uptime", style={'textAlign': 'center', 'color': '#e6e6e6'}),
            dcc.Graph(id='scatter1',
                figure={
                    'data' : [
                        go.Scatter(
                            x=list(version_list),
                            y=list(version_uptimes),
                            name='Scatter',
                            mode='markers',
                            marker=dict(
                                color='#FF8C00',
                                size=9
                            )
                        )
                    ],
                    'layout': {
                        'title': '',
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'xaxis': dict(range=[0, 50], title='Version from oldest to newest', color='bfbfbf', font='Menlo', fontsize=11, animate=False, autorange=True),
                        'yaxis': dict(range=[50, 3000], title='Uptime', color='bfbfbf', font='Menlo', fontsize=11, animate=False, autorange=True),
                        'margin': {'l': 50, 'r': 1, 't': 45, 'b': 1}
                    }
                })
        ], className="col s6", style={'backgroundColor': colors['background']}),

    ], className="row"),

    # Bar and Tables
    html.Div(children=[

        # Bar Graph
        html.Div(children=[
            html.H5("Area and Uptime", style={'textAlign': 'center', 'color': '#e6e6e6'}),
            dcc.Graph(id='bargraph2',
                      figure={
                          'data': [
                              go.Bar(
                                  x=bvalues,
                                  y=blabels,
                                  orientation='h'
                              ),
                          ],
                          'layout': {
                              'title': dict(text='Area and Average Uptime', font=dict(color='#e6e6e6'), size=21),
                              'plot_bgcolor': colors['background'],
                              'paper_bgcolor': colors['background'],
                              'xaxis': dict(tickangle=0, color='rgb(204, 204, 204', title='Area'),
                              'yaxis': dict(color='rgb(204, 204, 204', title='Uptime'),
                              'orientation': 'horizantal',
                              # 'margin': {'l': 50, 'r': 50, 't': 50, 'b': 75}
                          }
                      })
        ], className="col s1", style={'backgroundColor': colors['background'],
                                      'margin-top': 0,
                                      'padding': 0,
                                      'width': 600}
        ),
        # Highest Uptimes
        html.Div(children=[
                html.H5("Highest Uptimes", style={'textAlign': 'center', 'color': '#e6e6e6', 'margin-left': 10}),
                dcc.Graph(id='tablegod',
                          figure={
                              'data': [
                                  go.Table(
                                      header=dict(values=['Version', 'Uptime'], fill=dict(color='#111111'),
                                                  font=dict(color=colors['text'], size=13), align=['left'] * 5),
                                      cells=dict(values=[list(highest_uptimes.keys()), list(highest_uptimes.values())],
                                                 fill=dict(color='#111111'), font=dict(color=colors['text'], size=13),
                                                 align=['left'] * 5)
                                      # textfont=dict(size=13, color='#bfbfbf'),
                                      # marker=dict(colors=pcolors, line=dict(color='#bfbfbf', width=1))
                                  ),
                              ],
                              'layout': {
                                  'title': dict(text='Highest Average Uptimes', font=dict(color=colors['text'])),
                                  'plot_bgcolor': colors['background'],
                                  'paper_bgcolor': colors['background'],
                                  'width': 300,
                                  'height': 300
                                  # 'textfont': dict(color='rgb(204,204,204', size=15),
                                  # 'marker': dict(colors=pcolors,
                                  # line=dict(color='#FFFFFF', width=1)
                                  # )
                              }
                          })
            ], className="col s1", style={'padding': 0, 'width': 400}),

        # Lowest Uptimes
        html.Div(children=[
                html.H5("Lowest Uptimes", style={'textAlign': 'center', 'color': '#e6e6e6', 'margin-left': 40}),
                dcc.Graph(id='ganesh',
                          figure={
                              'data': [
                                  go.Table(
                                      header=dict(values=['Version', 'Uptime'], fill=dict(color='#111111'),
                                                  font=dict(color=colors['text'], size=13), align=['left'] * 5),
                                      cells=dict(values=[list(lowest_uptimes.keys()), list(lowest_uptimes.values())],
                                                 fill=dict(color='#111111'), font=dict(color=colors['text'], size=13),
                                                 align=['left'] * 5)
                                      # textfont=dict(size=13, color='#bfbfbf'),
                                      # marker=dict(colors=pcolors, line=dict(color='#bfbfbf', width=1))
                                  ),
                              ],
                              'layout': {
                                  'title': dict(text='Lowest Average Uptimes', font=dict(color=colors['text'])),
                                  'plot_bgcolor': colors['background'],
                                  'paper_bgcolor': colors['background'],
                                  'width': 300,
                                  'height': 300,
                                  'line': dict(color=colors['text']),
                                  # 'textfont': dict(color='rgb(204,204,204', size=15),
                                  # 'marker': dict(colors=pcolors,
                                  # line=dict(color='#FFFFFF', width=1)
                                  # )
                              }
                          })
            ], className="col s1", style={'padding': 0})

    ], className="row", style={'padding': 60}),

    # Column Dropdown
    html.Div(children=[
        dcc.Dropdown(
            id='column-filter',
            options=[
                {'label': 'Area', 'value': 'area'},
                {'label': 'Version', 'value': 'version'},
                {'label': 'Uptime', 'value': 'uptime'},
                {'label': 'Hostname', 'value': 'hostname'}
            ],
            multi=True,
            value=['area', 'version', 'uptime'],
            style={'backgroundColor': '#000000', 'width': '80%', 'height': 20, 'text': dict(color='#FFFFFF')}
        )
    ], style={'margin-left': 490}),

    # Filter search Bar
    html.Div(children=[
        dcc.Input(
            id='version-search',
            value='',
            type='text',
            style={'color': colors['text'], 'width': 800, 'margin-top': 24}
        ),
    ], style={'margin-left': 470}),

    # Table 3
    html.Div(className="row", style={'margin-left': 430}, id='big', children=html.Div(id='confidence', className="col s5")),

], className="row")


@app.callback(
    Output(component_id='big', component_property='children'),
    [dash.dependencies.Input(component_id='column-filter', component_property='value'),
     dash.dependencies.Input(component_id='version-search', component_property='value')]
)
def filter_table(input_data, vsearch_input):

    table_columns = []
    version_arr_F = []
    area_arr_F = []
    uptime_arr_F = []
    hostname_arr_F = []

    def filter_vsearch(v_input):
        i = 0
        for x in version_arr:
            if version_arr[i].startswith(v_input):
                version_arr_F.append(version_arr[i])
                area_arr_F.append(area_arr[i])
                uptime_arr_F.append(uptime_arr[i])
                hostname_arr_F.append(hostname_arr[i])
            i += 1
    def filter_asearch(v_input):
        i = 0
        for x in area_arr:
            if v_input in area_arr[i]:
                version_arr_F.append(version_arr[i])
                area_arr_F.append(area_arr[i])
                uptime_arr_F.append(uptime_arr[i])
                hostname_arr_F.append(hostname_arr[i])
            i += 1
    def filter_usearch(v_input):
        i = 0
        for x in uptime_arr:
            if v_input in uptime_arr[i]:
                version_arr_F.append(version_arr[i])
                area_arr_F.append(area_arr[i])
                uptime_arr_F.append(uptime_arr[i])
                hostname_arr_F.append(hostname_arr[i])
            i += 1
    def filter_hsearch(v_input):
        i = 0
        for x in hostname_arr:
            if v_input in hostname_arr[i]:
                version_arr_F.append(version_arr[i])
                area_arr_F.append(area_arr[i])
                uptime_arr_F.append(uptime_arr[i])
                hostname_arr_F.append(hostname_arr[i])
            i += 1

    if vsearch_input != "":
        print("Starting v filter")
        if '.' in vsearch_input:
            filter_vsearch(vsearch_input)
        if vsearch_input.isnumeric() == False:
            filter_asearch(vsearch_input)
            filter_hsearch(vsearch_input)
        if vsearch_input.isnumeric() == True:
            filter_usearch(vsearch_input)
        i = 0
        # Only display filtered columns
        for z in input_data:
            if input_data[i] == 'area':
                table_columns.append(area_arr_F)
            if input_data[i] == 'version':
                table_columns.append(version_arr_F)
            if input_data[i] == 'uptime':
                table_columns.append(uptime_arr_F)
            if input_data[i] == 'hostname':
                table_columns.append(hostname_arr_F)
            i += 1
    else:
        i = 0
        for z in input_data:
            if input_data[i] == 'area':
                table_columns.append(area_arr)
            if input_data[i] == 'version':
                table_columns.append(version_arr)
            if input_data[i] == 'uptime':
                table_columns.append(uptime_arr)
            if input_data[i] == 'hostname':
                table_columns.append(hostname_arr)
            i += 1

    table_data = go.Table(
        header=dict(values=input_data, fill=dict(color='#111111'),
                    font=dict(color=colors['text'], size=13), align=['left'] * 5),
        cells=dict(values=table_columns,
                   fill=dict(color='#111111'), font=dict(color=colors['text'], size=13),
                   align=['left'] * 5)
    ),

    return html.Div(
        dcc.Graph(
            id='confidence',
            animate=False,
            figure={'data': table_data,
                    'layout': {'title': dict(text='Data', font=dict(color=colors['text'])),
                               'plot_bgcolor': 'rgba(191, 191, 191, 0.3)',
                               'paper_bgcolor': colors['background'],
                               'width': 900,
                               'height': 600
                               }
                    },
            config={'displayModeBar': False}
        )
    )


# Materialize css
external_css = ["https://cdn.jsdelivr.net/gh/bose-a/bloom-css/my.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

# Materialize javascript
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

# Run Web Application
if __name__ == '__main__':
    app.run_server(debug=True)
# End
