import plotly.express as px
import pandas as pd
import pymssql
import seaborn as sns
import plotly.graph_objects as go

# import SQL database connection strings
from config2 import database
from config2 import username
from config2 import password
from config2 import server

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
    title_text = 'Percent of Loans Revieved by State',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig


# Bar Chart: Race Demographics
def createFig_Bar_Race_Demographics(df):
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
     title="Percent of Quantity of Loans Received by Race and Sex",
     text = "Percent of Loans")
    
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Bar Chart: Top Industries
def createFig_BarH_Top_Industries(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()

    fig = px.bar(df, x = 'Cummulative Loan Amount ($)', y = 'IndustryName',
                color = 'IndustryName',
                category_orders = {'Industry':list(df["IndustryName"])},
                color_discrete_sequence = ["#4863A0",
                                            "#2B3856",
                                            "#342D7E",
                                            "#0041C2",
                                            "#488AC7",
                                            "#3BB9FF"],
                text = df["Cummulative Loan Amount Billions"],
                title = "Top 5 Industries"
    )
    fig.update_layout(showlegend=False)
    fig.update_layout(yaxis_title=None)
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Donut Plot: How Borrowers Used their Loans
def CreateDonutChart(df):
    fig = px.pie(df, values='Total', names='Breakdown', color_discrete_sequence=['#292F68', '#28A9A9'], labels = {'Breakdown': 'Category ', 'Total':'Total Spent ($) '})

    fig.update_traces(textposition='outside', textinfo='percent+label',hole=.6)
    fig.update_layout(title = 'How Borrowers Spent PPP Money')
    fig.update_layout(yaxis_title=None)
    fig.update_layout(plot_bgcolor = '#DCE4E6', paper_bgcolor = '#DCE4E6')
    return fig

# Bar Chart: Other Utitlies use chart
def CreateSpendingCategoryBarChart(df):
    sns.set_theme(style='whitegrid')
    breakdown_other = df[df['Breakdown'] != 'Payroll'].copy()
    breakdown_other = breakdown_other.groupby(["Category"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
    fig = px.bar(breakdown_other, y='Category', x='Total', color='Category',
                color_discrete_sequence = ["#342D7E",
                                            "#488AC7",
                                            "#151B8D",
                                            "#659EC7",
                                            "#43BFC7"],
                orientation='h',
                hover_data=[breakdown_other.Category, breakdown_other.Total]
                )
    fig.update_layout(plot_bgcolor = '#DCE4E6',
                    legend=dict(title='Category'),
                    height = 676,
                    showlegend=True,
                    title = dict(text = 'How Borrowers Spent PPP Money<br>(with Payroll removed)')
                    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(showlegend=False)
    fig.update_traces(width=0.75)
    fig.update_layout(yaxis_title=None)
    return fig

# Stacked Cluster Bar Chart: PPP vs. Census Percent of Race per Sex
def createFig_Stacked_Cluster_PPP_vs_Census(df):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    # wanted figure
    sns.set_theme(style='whitegrid')
    # Defining Custom Colors
    fig = go.Figure()

    fig.update_layout(
        title=go.layout.Title(
            text="PPP vs Census: Percent of Race per Sex"),

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
    title_text = 'Percent of Unemployment Claims from 4/2020 - 3/2021 by State',
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
    title_text = 'Number of PPP Loans vs Total Unemployment Claims from 4/2020 - 3/2021 by State',
    autosize=True
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    return fig


# Bar Chart: Top Lenders
def createFig_bar_Top_Lenders(df):
    fig = px.bar(df.sort_values(by='Number of Loans Given', ascending=False), x='Number of Loans Given', y='Lender Name', orientation='h',
    title= 'Top 5 Lenders', hover_name='Lender Name', text_auto=' .2s', color = "Lender Name", 
                    color_discrete_sequence = ["#151B8D",
                                                "#6960EC",
                                                "#659EC7",
                                                "#A0CFEC",
                                                "#43BFC7"])
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
    title_text = 'Loans Revieved by State in Billions of Dollars',
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
    title_text = 'Percent of Borrowers who recieved PPP Loans per Total Number of Businesses by State',
    geo_scope='usa', # limite map scope to USA
    )
    fig.update_layout(paper_bgcolor = '#DCE4E6', plot_bgcolor = '#DCE4E6')
    fig.update_layout(geo=dict(bgcolor= '#DCE4E6'))
    return fig

