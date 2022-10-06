import plotly.express as px
import pandas as pd
import pymssql
import seaborn as sns
import plotly.graph_objects as go
import os

# If we are in production, make sure we DO NOT use the debug mode
if os.environ.get('ENV') == 'production':
    # Heroku gives us an environment variable called DATABASE_URL when we add a postgres database
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    database =  os.environ.get('DATABASE')
    username =  os.environ.get('USERNAME')
    password =  os.environ.get('PASSWORD')
    server =  os.environ.get('SERVER')
else:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-heroku'
    # import SQL database connection strings
    from DashBoard.config2 import database
    from DashBoard.config2 import username
    from DashBoard.config2 import password
    from DashBoard.config2 import server

def unit_labeler(x):
    result = ''
    dollar_units = [["k", 1_000], ["M", 1_000_000], ["B", 1_000_000_000]]
    if(x < 1_000):
        result = str(x)
    elif(x < 1_000_000):
        result = str(round(x / dollar_units[0][1], 2))
        if(result[-2:] == '.0'):
            result = str(result)[:-2]
        result += dollar_units[0][0]
    elif(x < 1_000_000_000):
        result = str(round(x / dollar_units[1][1], 2))
        if(result[-2:] == '.0'):
            result = str(result)[:-2]
        result += dollar_units[1][0]
    else:
        result = str(round(x / dollar_units[2][1], 2))
        if(result[-2:] == '.0'):
            result = str(result)[:-2]
        result += dollar_units[2][0]
    return result

# Map: Percent of Loans Nationally
def createFig_Map_Loans_Precent_by_State(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    fig = go.Figure(data=go.Choropleth(
    locations =df["StateAcronym"],
    z = df["Percent of Loans"].astype(float),
    colorscale = "Blues",
    colorbar_title = "Percent of<br>Loans Received",
    text = df["StateName"],
    marker_line_color = "black",
    locationmode = "USA-states"))

    fig.update_layout(
    title_text = 'Percent of Loans Received by State',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig


# Bar Chart: Race Demographics
def createFig_Bar_Race_Demographics(df, state, industry):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    sns.set_theme(style='whitegrid')
    # Defining Custom Colors
    colours = {
        "Male": "#0C3B5D",
        "Female": "#FCB94D",
    }
    fig = px.bar(df, x="Race", y="Percent of Loans",
     color="Sex",
     barmode="group",
     color_discrete_map=colours,
     title=f"Percent of Quantity of Loans Received by Race and Sex<br><sup>Location: {state}<br>Industry: {industry}</sup>",
     text = "Percent of Loans")
    
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Bar Chart: Top Industries
def createFig_BarH_Top_Industries(df, state):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    df["Cummulative Loan Amount ($) Units"] = df["Cummulative Loan Amount ($)"].apply(lambda x : unit_labeler(x))
    fig = px.bar(df, x = 'Cummulative Loan Amount ($)', y = 'IndustryName',
                color = 'IndustryName',
                category_orders = {'Industry':list(df["IndustryName"])},
                color_discrete_sequence = ["#4863A0",
                                            "#2B3856",
                                            "#342D7E",
                                            "#0041C2",
                                            "#488AC7",
                                            "#3BB9FF"],
                text = df["Cummulative Loan Amount ($) Units"],
                title = f"Top 5 Industries<br><sup>Location: {state}</sup>"
    )
    fig.update_layout(showlegend=False)
    fig.update_layout(yaxis_title=None)
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Donut Plot: How Borrowers Used their Loans
def CreateDonutChart(df, state, industry):
    fig = px.pie(df, values='Total', names='Breakdown', color_discrete_sequence=['#292F68', '#28A9A9'], labels = {'Breakdown': 'Category ', 'Total':'Total Spent ($) '})

    fig.update_traces(textposition='outside', textinfo='percent+label',hole=.6)
    fig.update_layout(title = f'How Borrowers Spent PPP Money<br><sup>Location: {state}<br>Industry: {industry}</sup>')
    fig.update_layout(yaxis_title=None)
    fig.update_layout(plot_bgcolor = '#DCE4E6', paper_bgcolor = '#DCE4E6')
    return fig

# Bar Chart: Other Utitlies use chart
def CreateSpendingCategoryBarChart(df, state, industry):
    sns.set_theme(style='whitegrid')
    breakdown_other = df[df['Breakdown'] != 'Payroll'].copy()
    breakdown_other = breakdown_other.groupby(["Category"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
    breakdown_other = breakdown_other.rename(columns = {"Total":"PPP Money Spent ($)"})
    breakdown_other["PPP Money Spent ($) Units"] = breakdown_other["PPP Money Spent ($)"].apply(lambda x : unit_labeler(x))
    fig = px.bar(breakdown_other, y='Category', x='PPP Money Spent ($)', color='Category',
                color_discrete_sequence = ["#342D7E",
                                            "#488AC7",
                                            "#151B8D",
                                            "#659EC7",
                                            "#43BFC7"],
                orientation='h',
                hover_data=[breakdown_other.Category, breakdown_other['PPP Money Spent ($)']],
                text = "PPP Money Spent ($) Units"
                )
    fig.update_layout(plot_bgcolor = '#DCE4E6',
                    title = f'How Borrowers Spent PPP Money:<br>Other Utilities Breakdown<br><sup>Location: {state}<br>Industry: {industry}</sup>')
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_traces(width=0.75)
    fig.update_layout(yaxis_title=None, yaxis = dict(domain=[0, .93]))
    fig.update_traces(showlegend = False)
    return fig

# Stacked Cluster Bar Chart: PPP vs. Census Percent of Race per Sex
def createFig_Stacked_Cluster_PPP_vs_Census(df, state, industry):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    sns.set_theme(style='whitegrid')
    # Defining Custom Colors
    fig = go.Figure()

    fig.update_layout(
        title=go.layout.Title(
            text=f"PPP vs Census: Percent of Race per Sex<br><sup>Bars in chart will be empty when data is not available for specific filter<br>Location: {state}<br>Industry: {industry}</sup>"),

        xaxis=dict(title_text="Race"),
        yaxis=dict(title_text="Percent Of Race"),   
        barmode="stack",
    )

    colors = ["#FCB94D", "#0C3B5D"]
    for r, c in zip(df.Sex.unique(), colors):
        plot_df = df[df.Sex == r]
        fig.add_trace(
            go.Bar(x=[plot_df.Race, plot_df.Origin], y=plot_df.PercentOfRace, name=r, marker_color=c,
            text = plot_df['PercentOfRace']))
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Map: Percent of Unemployment Claims
def createFig_Map_Unemployment_Claims(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    fig = go.Figure(data=go.Choropleth(
    locations =df["State Acronym"],
    z = df["Percentage of Total Unemployment Claims"].astype(float),
    colorscale = "Blues",
    colorbar_title = "Percent of<br>Unemployment<br>Claims",
    text = df["State"],
    marker_line_color = "black",
    locationmode = "USA-states"))
    fig.update_layout(
    title_text = 'Percent of Unemployment Claims from 3/2020 - 4/2021 by State',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig


# Scatter Plot: Quantity of PPP Loans vs Total Unemployment Claims for States
def createFig_Scatter_Unemployment_Loans(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    fig = px.scatter(df, x="Total Unemployment Claims", y="Total PPP Loans",hover_name = "State", size='Total Loan Amount ($)', color='Region')
    fig.update_layout(
    title_text = 'Number of PPP Loans vs Total Unemployment Claims<br>from 3/2020 - 4/2021 by State',
    autosize=True
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Bar Chart: Top Lenders
def createFig_bar_Top_Lenders(df, state, industry):
    df["Number of Loans Given Units"] = df["Number of Loans Given"].apply(lambda x : unit_labeler(x))
    fig = px.bar(df.sort_values(by='Number of Loans Given', ascending=False), x='Number of Loans Given', y='Lender Name', orientation='h',
    title= f'Top 5 Lenders<br><sup>Location: {state}<br>Industry: {industry}</sup>', hover_name='Lender Name', color = "Lender Name", 
                    color_discrete_sequence = ["#151B8D",
                                                "#6960EC",
                                                "#659EC7",
                                                "#A0CFEC",
                                                "#43BFC7"],
                                                text = "Number of Loans Given Units")
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(yaxis_title=None)
    fig.update_layout(showlegend=False)
    return fig


# Map: Dollar Amount of Loans Nationally
def createFig_Map_Loans_Dollar_Amount_by_State(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    fig = go.Figure(data=go.Choropleth(
    locations =df["StateAcronym"],
    z = (round(df["CurrentApprovalAmount"]/1_000_000_000, 2)).astype(float),
    colorscale = "Blues",
    colorbar_title = "Loans Received in<br>Billions of Dollars",
    text = df["StateName"],
    marker_line_color = "black",
    locationmode = "USA-states"
    ))

    fig.update_layout(
    title_text = 'Loans Received by State in Billions of Dollars',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor= '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig


# Map: Percent of Borrowers per Businesses
def createFig_Map_Percent_of_Borrwers_to_Businesses(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    fig = go.Figure(data=go.Choropleth(
    locations =df["StateAcronym"],
    z = df["Percent of Borrowers per Businesses"],
    colorscale = "Blues",
    colorbar_title = "Percent of Borrowers<br>per Businesses<br>by State",
    text = df["StateName"],
    marker_line_color = "black",
    locationmode = "USA-states"
    ))

    fig.update_layout(
    title_text = 'Percent of Borrowers who received PPP Loans per Total Number of Businesses by State',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig

def ConfusionMatrix():
        c_m = [ [576, 647], 
        [7951, 546]  ]
        fig = go.Figure(data=go.Heatmap(z=c_m,
                        text = [['False Negative (647)', 'True Negative (576)'],
                                ['True Positive (7951)', 'False Positive (546)', ]],
                        texttemplate = "%{text}",
                        colorscale = 'Blues',
                        hoverongaps = True,
                        xgap = 5,
                        ygap = 5
                        )
        )
        fig.update_traces(hovertemplate='%{text}')
        fig.update_layout(title ='Machine Learning Confusion Matrix',
                        xaxis_title = 'Actual Label',
                        yaxis_title = 'Predicted Label')
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = 'black')
        fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
        return fig