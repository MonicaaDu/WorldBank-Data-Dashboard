import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
import requests
from collections import OrderedDict

# default list of all countries of interest
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'),
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'),
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN')])

def graph(country = country_default):
    countries = list(country.values())
    countries = [x.lower() for x in countries]
    country_filter = ';'.join(countries)

    # World Bank indicators of interest for pulling data
    indicators = ['AG.LND.ARBL.HA.PC', 'SP.RUR.TOTL.ZS', 'SP.RUR.TOTL.ZS', 'AG.LND.FRST.ZS']

    data_frames = [] # stores the data frames with the indicator data of interest
    urls = [] # url endpoints for the World Bank API

    # pull data from World Bank API and clean the resulting json
    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/' + country_filter +\
        '/indicators/' + indicator + '?date=1990:2015&per_page=1000&format=json'
        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()[1]
        except:
            print('could not load data ', url)

        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        data_frames.append(data)

    # first chart plots arable land from 1990 to 2015 in top 10 economies
    # as a line chart
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    df_one = df_one[(df_one['date'] == '2015') | (df_one['date'] == '1990')]
    df_one.sort_values('value', ascending=False, inplace=True)

    country_list = df_one.country.unique().tolist()

    for country in country_list:
        x_val = df_one[df_one['country']== country].date.tolist()
        y_val = df_one[df_one['country']== country].value.tolist()
        graph_one.append(
              go.Scatter(
                 x = x_val,
                 y = y_val,
                 mode = 'lines',
                 name = country
              )
         )

    layout_one = dict(
           title = 'Change in Hectares Arable Land <br> per Person 1990 to 2015',
           xaxis = dict(title = 'Year', autotick = False, tick0 = 1990, dtick = 25),
           yaxis = dict(title = 'Hectares')
     )

    # second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df_one.sort_values('value', ascending=False, inplace=True)
    df_one = df_one[df_one['date'] == '2015']

    graph_two.append(
          go.Bar(
          x = df_one.country.tolist(),
          y = df_one.value.tolist(),
          )
    )

    layout_two = dict(title = 'Hectares Arable Land per Person in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Hectares per person')
    )

    # third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df_three = pd.DataFrame(data_frames[1])
    df_three = df_three[(df_three['date'] == '2015') | (df_three['date'] == '1990')]

    df_three.sort_values('value', ascending=False, inplace=True)

    for country in country_list:
        x_val = df_three[df_three['country'] == country].date.tolist()
        y_val =  df_three[df_three['country'] == country].value.tolist()
        graph_three.append(
               go.Scatter(
                  x = x_val,
                  y = y_val,
                  mode = 'lines',
                 name = country
               )
        )

    layout_three = dict(title = 'Change in Rural Population <br> (Percent of Total Population)',
                   xaxis = dict(title = 'Year', autotick=False, tick0=1990, dtick=25),
                   yaxis = dict(title = 'Percent')
    )

    # fourth chart shows rural population vs arable land as percents
    graph_four = []
    df_four_a = pd.DataFrame(data_frames[2])
    df_four_a = df_four_a[['country', 'date', 'value']]

    df_four_b = pd.DataFrame(data_frames[3])
    df_four_b = df_four_b[['country', 'date', 'value']]

    df_four = df_four_a.merge(df_four_b, on=['country', 'date'])
    df_four.sort_values('date', ascending=True, inplace=True)

    plotly_default_colors = plotly.colors.DEFAULT_PLOTLY_COLORS

    for i, country in enumerate(country_list):
        current_color = []
        x_val = df_four[df_four['country'] == country].value_x.tolist()
        y_val = df_four[df_four['country'] == country].value_y.tolist()
        years = df_four[df_four['country'] == country].date.tolist()
        country_label = df_four[df_four['country'] == country].country.tolist()

        text = []
        for country, year in zip(country_label, years):
            text.append(str(country) + ' ' + str(year))

        graph_four.append(
            go.Scatter(
            x = x_val,
            y = y_val,
            mode = 'lines+markers',
            text = text,
            name = country,
            textposition = 'top center'
          )
         )

    layout_four = dict(title = '% of Population that is Rural versus <br> % of Land that is Forested <br> 1990-2015',
                xaxis = dict(title = '% Population that is Rural', range=[0,100], dtick=10),
                yaxis = dict(title = '% of Area that is Forested', range=[0,100], dtick=10),
                )

        # append all charts
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
