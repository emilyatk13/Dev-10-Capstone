import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import dash_html_components as html
import pandas as pd
import numpy as np
import base64

# Data - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Heat_Map_Percent_Loans_Received_Quantity = pd.read_csv("./DashBoard/DashBoard_Data/Heat_Map_Percent_Loans_Received_Quantity.csv", sep = ',', header = 0)
Bar_Chart_Demographics_Percent_Loans_Received = pd.read_csv("./DashBoard/DashBoard_Data/Bar_Chart_Demographics_Percent_Loans_Received.csv", sep = ',', header = 0)
Unemployment_data = pd.read_csv("./DashBoard/DashBoard_Data/Unemployment_data.csv", sep = ',', header = 0)
Heat_Map_Dollar_Amount_of_Loans_Received = pd.read_csv("./DashBoard/DashBoard_Data/Heat_Map_Dollar_Amount_of_Loans_Received.csv", sep = ',', header = 0)
Heat_Map_Percent_of_Borrwers_to_Businesses = pd.read_csv("./DashBoard/DashBoard_Data/Heat_Map_Percent_of_Borrwers_to_Businesses.csv", sep = ',', header = 0)


# Graphs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
from DashBoard.Graph_Functions import createFig_Map_Loans_Precent_by_State
from DashBoard.Graph_Functions import createFig_Bar_Race_Demographics
from DashBoard.Graph_Functions import createFig_BarH_Top_Industries
from DashBoard.Graph_Functions import CreateDonutChart
from DashBoard.Graph_Functions import CreateSpendingCategoryBarChart
from DashBoard.Graph_Functions import createFig_Stacked_Cluster_PPP_vs_Census
from DashBoard.Graph_Functions import createFig_bar_Top_Lenders
from DashBoard.Graph_Functions import createFig_Map_Unemployment_Claims
from DashBoard.Graph_Functions import createFig_Scatter_Unemployment_Loans
from DashBoard.Graph_Functions import createFig_Map_Loans_Dollar_Amount_by_State
from DashBoard.Graph_Functions import createFig_Map_Percent_of_Borrwers_to_Businesses
from DashBoard.Graph_Functions import ConfusionMatrix


# DashBoard - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# link fontawesome 
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR, FA])
server = app.server

mygraph_maps = dcc.Graph(figure={})
dropdown_maps = dcc.Dropdown(options=['Percent of Received PPP Loans (%)', 'Cumulative Amount of PPP Loans Received ($)', 'Percent of Borrowers per Businesses by State (%)'],
                        value='Percent of Received PPP Loans (%)',  # initial value displayed when page first loads
                        clearable=False,
                        style = {"color": "'#DCE4E6'"})


State_Names = list(set(Bar_Chart_Demographics_Percent_Loans_Received["StateName"]))
State_Names.sort()
State_List = ["Nation"] + State_Names

Industry_Names = list(set(Bar_Chart_Demographics_Percent_Loans_Received["IndustryName"]))
Industry_Names.sort()
Industry_List = ["All Industries"] + Industry_Names

image_filename = './DashBoard/qrcode.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())





app.layout = html.Div(children=[
    html.H1(children='Paycheck Protection Program (PPP) Loans', style={'textAlign': 'center', 'font-size': '50px', 'text-decoration': 'underline', 'margin-bottom':25, 'margin-top':25}),
    html.H3(children="PPP Dash Introduction",  style={'textAlign': 'center', 'font-size': '30px', 'margin-bottom':5, 'margin-top':35}),
    html.P(children=
    """
    As the global pandemic COVID-19 hit the U.S. Economy in 2019, the United States government implemented an unprecedented and large-scale solution to keep businesses(and by the extension, their employees, afloat).
    The Paycheck Protection Program(PPP), which ran from March 2020 through April 2021, allowed businesses to take out loans backed by the federal government.
    The government intended for these loans to keep businesses solvent and employees on their payroll during the span of the pandemic.
    """,
    style = {'display': 'inline-block', 'margin':200, 'margin-bottom':5, 'font-size': '20px', 'margin-top':5,'textAlign': 'center'}),
    html.P(children=
    dcc.Markdown("""
    This interactive dashboard is a visual representation of the PPP data released from https://data.sba.gov/dataset/ppp-foia.
    We also take a look at Unemployment numbers and census breakdowns during this time period with data released from https://www.bls.gov/ and https://www.census.gov/, respectively.
    What do the borrowers/businesses owners look like?
    Where did the loans go to? Who gave out these loans?
    Check out the differences between state and/or industries.
    Follow the money and see where it goes. We encourage you to draw your own conclusions.
    The bottom of this dashboard displays our machine learning loan decision analysis, which the government can apply
    should there ever be a need to implement something like PPP again.
    """),
    style = {'display': 'inline-block', 'margin':200, 'margin-bottom':25, 'font-size': '20px', 'margin-top':5,'textAlign': 'center'}),
    # 3 Maps - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    html.Div(className = "container", children=[
    html.H2(children='National PPP Overview', style={'textAlign': 'center', 'font-size': '40px'}),
    html.Div(className = "container", children=[dropdown_maps, mygraph_maps])

    ]),
    # Demographics Breakdown Graphs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    html.Div(className = "container", children=[
    html.H2(children='PPP Borrower Breakdown', style={'textAlign': 'center', 'font-size': '40px', 'margin-bottom':20, 'margin-top':30}),
        html.Div([
            dcc.Dropdown(options=State_List,
                        value='Nation',  # initial value displayed when page first loads
                        clearable=False,
                        id = "state-dropdown")
                  ]),
        html.Div([
            dcc.Dropdown(options=Industry_List,
                        value='All Industries',  # initial value displayed when page first loads
                        clearable=False,
                        id = "industry-dropdown")
                  ]), 
        html.Div([
            dcc.Graph(id="graph1", style={'width': '50%', 'height': '60vh', 'display': 'inline-block'}),
            dcc.Graph(id="graph2", style={'width': '50%', 'height': '60vh', 'display': 'inline-block'})
                ]),
        html.Div([
            dcc.Dropdown(options=["Payroll and Other Utilities", "Other Utilities In-Depth Look"],
                        value="Payroll and Other Utilities",  # initial value displayed when page first loads
                        clearable=False,
                        style = {'width': '100%', 'textAlign':'right'},
                        id = "utilities-dropdown"),
            dcc.Graph(id="graph3", style={'width': '33.33%', 'height': '60vh', 'display': 'inline-block'}),
            dcc.Graph(id="graph4", style={'width': '33.33%', 'height': '60vh', 'display': 'inline-block'}),
            dcc.Graph(id="graph5", style={'width': '33.33%', 'height': '60vh', 'display': 'inline-block'}),
                ]),

    ]),

    # Unemployment Graphs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    html.Div(className = "container", children=[
    html.H2(children='National Unemployment Overview', style={'textAlign': 'center', 'font-size': '40px', 'margin-bottom':20, 'margin-top':30}),
        dcc.Graph(
            id='Scatter Plot of Loans',
            figure=createFig_Scatter_Unemployment_Loans(Unemployment_data),
            style={'width': '40%', 'height': '60vh', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id='Map of Unemployment',
            figure=createFig_Map_Unemployment_Claims(Unemployment_data),
            style={'width': '60%', 'height': '60vh', 'display': 'inline-block'}
        )
    ]),


    # ML Graphs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    html.Div(className = "container", children=[
    html.H2(children=' Loan Decision Analysis (ML)', style={'textAlign': 'center', 'font-size': '40px', 'margin-bottom':20, 'margin-top':30}),
        dcc.Graph(
            id='ML Confusion Matrix',
            figure=ConfusionMatrix(),
            style={'width': '100%', 'height': '40vh', 'display': 'inline-block', 'align':'center'}
        ),
    html.P(children=
    dcc.Markdown("""
    Throughout our analysis of the PPP data, we anchored our focus around what happened during the loan program.
    Who received the loans, how did they use it, was there a connection to unemployment rates? For machine learning, we shifted from focusing on what the loan program was like in practice to how to optimize future implementation of a similar program.
    Our group created a model that predicts whether or not a borrower will pay back their loan based on key information including the industry, age of the business, and the demographics of the owner.
    We ran an algorithm with K Nearest Neighbors with the goal of producing the fewest false positives as lenders are risk averse. The confusion matrix, seen above, demonstrates the results. A key for interpreting the results is as follows:
    """), style={'font-size': '20px', 'margin':50, 'margin-top':15, 'margin-bottom':15,}),

    html.P(children=
    dcc.Markdown("""
    True positive (TP): The algorithm accurately predicts that a borrower will pay back their loan  
    False positive (FP): The algorithm inaccurately predicts that a borrower will pay back their loan  
    False negative (FN): The algorithm inaccurately predicts that a borrower will not pay back their loan  
    True negative (TN): The algorithm accurately predicts that a borrower will not pay back their loan  
    """), style={'font-size': '20px', 'margin':50, 'margin-top':5, 'margin-bottom':25,'textAlign': 'center'}),
    dbc.Container([
    dcc.Markdown("""
    Presicion $= \\frac{TP}{TP + FP} = 0.93$ &emsp;&emsp; Sensitivity $= \\frac{TP}{TP + FN} = 0.92$  
    """, mathjax=True)], style={'font-size': '25px', 'margin':50, 'margin-top':5, 'margin-bottom':15,'textAlign': 'center'}),
    dbc.Container([
    dcc.Markdown("""
    $F_1$-score $= \\frac{2 \\times Precision \\times Recall}{Presicion + Recall} = 0.93$ &emsp;&emsp; Accuracy $= \\frac{TP + TN}{TP + TN + FP + FN} = 0.88$
    """, mathjax=True)], style={'font-size': '25px', 'margin':50, 'margin-top':15, 'margin-bottom':65,'textAlign': 'center'})
    ]),

    # Conclusion - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    html.Div(className = "container", children=[
    html.H3(children="PPP Dash Conclusion",  style={'textAlign': 'center', 'font-size': '40px', 'margin-bottom':5, 'margin-top':75, 'text-decoration': 'underline'}),
    html.P(children=
    dcc.Markdown("""
    We hope you found this interactive dashboard intuitive and informative in your exploration.
    Please see our technical report and explore our project GitHub (https://github.com/emilyatk13/dev-10-capstone) for a thorough discussion of these results.
    This capstone project is the creation of Adam Brewer, Emily Atkinson, Nolan Thomas, and Stephanie Leiva in coordination with the Dev 10 Bootcamp.
    """),
    style = {'display': 'inline-block', 'margin':200, 'font-size': '20px', 'margin-bottom':20, 'margin-top':15,'textAlign': 'center'}),
    html.H4(children="Scan to view our Github",  style={'textAlign': 'center', 'font-size': '25px', 'margin-bottom':5, 'margin-top':25}),
    html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'10%', 'width':'10%',}), style={'textAlign': 'center', 'margin-bottom':50})
    ])

])


# 'Percent of Recieved PPP Loans (%)', 'Cumulative Amount of PPP Loans Recieved ($)', 'Percent of Borrowers per Businesses by State'

# Maps
@app.callback(
    Output(mygraph_maps, component_property='figure'),
    Input(dropdown_maps, component_property='value')
)
def update_graph_maps(user_input):  # function arguments come from the component property of the Input
    if user_input == 'Percent of Received PPP Loans (%)':
        fig = createFig_Map_Loans_Precent_by_State(Heat_Map_Percent_Loans_Received_Quantity)

    elif user_input == 'Cumulative Amount of PPP Loans Received ($)':
        fig = createFig_Map_Loans_Dollar_Amount_by_State(Heat_Map_Dollar_Amount_of_Loans_Received)

    elif user_input == 'Percent of Borrowers per Businesses by State (%)':
        fig = createFig_Map_Percent_of_Borrwers_to_Businesses(Heat_Map_Percent_of_Borrwers_to_Businesses)

    return fig



# Demographics
@app.callback(
    Output("graph1", 'figure'),
    Input("state-dropdown",  'value'),
    Input("industry-dropdown", 'value')
)
def update_graph_demo(user_input_1, user_input_2):  # function arguments come from the component property of the Input
    state = user_input_1
    industry = user_input_2
    Bar_Chart_Demographics_Percent_Loans_Received = pd.read_csv("./DashBoard/DashBoard_Data/Bar_Chart_Demographics_Percent_Loans_Received.csv", sep = ',', header = 0)
    
    if(state == "Nation" and industry == "All Industries"):
        # Bar Chart Demographics
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("IndustryName", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("StateName", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.groupby(["Race", "Sex"], as_index = False)["Percent of Loans"].sum()
        fig_1 = createFig_Bar_Race_Demographics(Bar_Chart_Demographics_Percent_Loans_Received, state, industry)

    elif(state == "Nation" and industry != "All Industries"):
        # Bar Chart Demographics
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("StateName", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("Percent of Loans", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received[Bar_Chart_Demographics_Percent_Loans_Received["IndustryName"] == industry]
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.groupby(["Race", "Sex"], as_index = False)["LoanNumber"].sum()
        total_demo_loans = Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"].sum()
        Bar_Chart_Demographics_Percent_Loans_Received["Percent of Loans"] = round(Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"] / total_demo_loans * 100, 2)
        fig_1 = createFig_Bar_Race_Demographics(Bar_Chart_Demographics_Percent_Loans_Received, state, industry)

    elif(state != "Nation" and industry == "All Industries"):
        # Bar Chart Demographics
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("IndustryName", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("Percent of Loans", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received[Bar_Chart_Demographics_Percent_Loans_Received["StateName"] == state]
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.groupby(["Race", "Sex"], as_index = False)["LoanNumber"].sum()
        total_demo_loans = Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"].sum()
        Bar_Chart_Demographics_Percent_Loans_Received["Percent of Loans"] = round(Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"] / total_demo_loans * 100, 2)
        fig_1 = createFig_Bar_Race_Demographics(Bar_Chart_Demographics_Percent_Loans_Received, state, industry)

    else:
        # Bar Chart Demographics
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.drop("Percent of Loans", axis = 1)
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received[Bar_Chart_Demographics_Percent_Loans_Received["StateName"] == state]
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received[Bar_Chart_Demographics_Percent_Loans_Received["IndustryName"] == industry]
        Bar_Chart_Demographics_Percent_Loans_Received = Bar_Chart_Demographics_Percent_Loans_Received.groupby(["Race", "Sex"], as_index = False)["LoanNumber"].sum()
        total_demo_loans = Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"].sum()
        Bar_Chart_Demographics_Percent_Loans_Received["Percent of Loans"] = round(Bar_Chart_Demographics_Percent_Loans_Received["LoanNumber"] / total_demo_loans * 100, 2)
        fig_1 = createFig_Bar_Race_Demographics(Bar_Chart_Demographics_Percent_Loans_Received, state, industry)


    return fig_1

def add_missing_data(records):
    Race_list = ["Asian", "Black", "White"]
    Sex_list = ["Male", "Female"]
    Origin_list = ["PPP", "Census"]
    Record_Master_list = []
    for race in Race_list:
        for sex in Sex_list:
            for origin in Origin_list:
                record = {'Race': race, 'TotalRacePerSex': 0, 'Sex':sex, 'Origin':origin}
                Record_Master_list.append(record)

    matser_record_index = []
    for i, m_record in enumerate(Record_Master_list):
        match = 0
        for record in records:
            temp_record = record.copy()
            temp_m_record = m_record.copy()
            del temp_record["TotalRacePerSex"]
            del temp_m_record["TotalRacePerSex"]
            equal = temp_record == temp_m_record
            if(equal):
                match+=1
        if(match == 0):
            matser_record_index.append(i)

    for record_index in matser_record_index:
        records.append(Record_Master_list[record_index])
    return records

# PPP vs Census
@app.callback(
    Output("graph2", 'figure'),
    Input("state-dropdown", 'value'),
    Input("industry-dropdown", 'value')
)
def update_graph_PPPvCensus(user_input_1, user_input_2):  # function arguments come from the component property of the Input
    state = user_input_1
    industry = user_input_2
    Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = pd.read_csv("./DashBoard/DashBoard_Data/Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.csv", sep = ',', header = 0)
    
    if(state == "Nation" and industry == "All Industries"):
        # Stacked Cluster Proportion PPP vs Census
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("IndustryName", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("StateName", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin","Sex","TotalRace"], as_index = False)['TotalRacePerSex'].sum()
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = round((Cluster_Stacked_Bar_Chart_Demographics_PPP_Census['TotalRacePerSex']/Cluster_Stacked_Bar_Chart_Demographics_PPP_Census['TotalRace']) * 100, 2)
        fig_2 = createFig_Stacked_Cluster_PPP_vs_Census(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census, state, industry)

    elif(state == "Nation" and industry != "All Industries"):
        # Stacked Cluster Proportion PPP vs Census
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("StateName", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("PercentOfRace", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["IndustryName"] == industry]
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin","Sex"], as_index = False)["TotalRacePerSex"].sum()
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin"], as_index = False)["TotalRacePerSex"].sum()[["TotalRacePerSex"]]
        double = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[["RacePerSexPerSurveyTotals"]]
        double = double.iloc[np.arange(len(double)).repeat(2)].dropna().reset_index().drop("index", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = double
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = round(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["TotalRacePerSex"] / Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] * 100, 2)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"].fillna(0)
        fig_2 = createFig_Stacked_Cluster_PPP_vs_Census(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census, state, industry)

    elif(state != "Nation" and industry == "All Industries"):
        # Stacked Cluster Proportion PPP vs Census
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("IndustryName", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop("PercentOfRace", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["StateName"] == state]
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin","Sex"], as_index = False)["TotalRacePerSex"].sum()
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin"], as_index = False)["TotalRacePerSex"].sum()[["TotalRacePerSex"]]
        double = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[["RacePerSexPerSurveyTotals"]]
        double = double.iloc[np.arange(len(double)).repeat(2)].dropna().reset_index().drop("index", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = double
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = round(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["TotalRacePerSex"] / Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] * 100, 2)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"].fillna(0)
        fig_2 = createFig_Stacked_Cluster_PPP_vs_Census(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census, state, industry)

    else:
         # Stacked Cluster Proportion PPP vs Census
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop(["PercentOfRace", "TotalRace"], axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["StateName"] == state]
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["IndustryName"] == industry]
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.drop(["IndustryName", "StateName"], axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = pd.DataFrame.from_records(add_missing_data(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.to_dict('records'))).sort_values(by = ["Race", "Origin", "Sex"], ascending=True)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.sort_values(by = ["Race", "Origin", "Sex"], ascending=True)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin","Sex"], as_index = False)["TotalRacePerSex"].sum()
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.groupby(["Race", "Origin"], as_index = False)["TotalRacePerSex"].sum()[["TotalRacePerSex"]]
        double = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census[["RacePerSexPerSurveyTotals"]]
        double = double.iloc[np.arange(len(double)).repeat(2)].dropna().reset_index().drop("index", axis = 1)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] = double
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = round(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["TotalRacePerSex"] / Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["RacePerSexPerSurveyTotals"] * 100, 2)
        Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"] = Cluster_Stacked_Bar_Chart_Demographics_PPP_Census["PercentOfRace"].fillna(0)
        fig_2 = createFig_Stacked_Cluster_PPP_vs_Census(Cluster_Stacked_Bar_Chart_Demographics_PPP_Census, state, industry)


    return fig_2


def label_break(list_labels):

    def find(str, ch):
        for i, ltr in enumerate(str):
            if ltr == ch:
                yield i

    new_labels = []
    for label in list_labels:
        spacers = list(find(label, ' '))
        length = len(spacers)
        if(length == 0):
            new_labels.append(label)
            continue
        label_weights = []
        for spacer in spacers:
            label_weights.append(abs(len(label[:spacer]) - len(label[spacer + 1:])))
        choosen_space = 1000
        desired_space_index = 0
        for i, weight in enumerate(label_weights):
            if(choosen_space > weight): 
                choosen_space = weight
                desired_space_index = i
        desired_break_location = spacers[desired_space_index]
        label = label[:desired_break_location] + "<br>" + label[desired_break_location + 1:]
        new_labels.append(label)
    return new_labels


# Top 5 Industries
@app.callback(
    Output("graph3", 'figure'),
    Input("state-dropdown", 'value')
)
def update_graph_top_industry(user_input_1):  # function arguments come from the component property of the Input
    state = user_input_1
    Bar_Chart_Top_10_Industries = pd.read_csv("./DashBoard/DashBoard_Data/Bar_Chart_Top_10_Industries.csv", sep = ',', header = 0)
    if(state == "Nation"):
        Industry_to_LoanAmount_ = Bar_Chart_Top_10_Industries.drop("StateName", axis = 1)
        Industry_to_LoanAmount_ = Industry_to_LoanAmount_.groupby(["IndustryName"], as_index = False)["Cummulative Loan Amount ($)"].sum().sort_values(by = "Cummulative Loan Amount ($)", ascending = False)
        Industry_to_LoanAmount_["Cummulative Loan Amount Billions"] = round(Industry_to_LoanAmount_["Cummulative Loan Amount ($)"]/1_000_000_000, 2).astype(str) +"B"
        Industry_to_LoanAmount_ = Industry_to_LoanAmount_.head(5)
        Industry_to_LoanAmount_["IndustryName"] = label_break(list(Industry_to_LoanAmount_["IndustryName"]))
        fig_3 = createFig_BarH_Top_Industries(Industry_to_LoanAmount_, state)
    else: 
        Industry_to_LoanAmount_ = Bar_Chart_Top_10_Industries[Bar_Chart_Top_10_Industries["StateName"] == state]
        Industry_to_LoanAmount_ = Industry_to_LoanAmount_.head(5)
        Industry_to_LoanAmount_["IndustryName"] = label_break(list(Industry_to_LoanAmount_["IndustryName"]))
        fig_3 = createFig_BarH_Top_Industries(Industry_to_LoanAmount_, state)

    return fig_3


# Top 5 Lenders
@app.callback(
    Output("graph4", 'figure'),
    Input("state-dropdown", 'value'),
    Input("industry-dropdown", 'value')
)
def update_graph_top_lender(user_input_1, user_input_2):  # function arguments come from the component property of the Input
    state = user_input_1
    industry = user_input_2
    Top_Lender_data = pd.read_csv("./DashBoard/DashBoard_Data/Top_Lender_data.csv", sep = ',', header = 0)
    lender = Top_Lender_data
    if(state == "Nation" and industry == "All Industries"):
        lender_ = lender.drop("IndustryName", axis = 1)
        lender_ = lender_.drop("StateName", axis = 1)
        lender_ = lender_.groupby(["Lender Name"], as_index = False)["Number of Loans Given"].sum().sort_values(by= "Number of Loans Given", ascending = False)
        lender_ = lender_.head(5)
        lender_["Lender Name"] = label_break(list(lender_["Lender Name"]))
        fig_4 = createFig_bar_Top_Lenders(lender_, state, industry)

    elif(state == "Nation" and industry != "All Industries"):
        lender_ = lender[lender["IndustryName"] == industry]
        lender_ = lender_.drop("StateName", axis = 1)
        lender_ = lender_.groupby(["Lender Name"], as_index = False)["Number of Loans Given"].sum().sort_values(by= "Number of Loans Given", ascending = False)
        lender_ = lender_.head(5)
        lender_["Lender Name"] = label_break(list(lender_["Lender Name"]))
        fig_4 = createFig_bar_Top_Lenders(lender_, state, industry)

    elif(state != "Nation" and industry == "All Industries"):
        lender_ = lender[lender["StateName"] == state]
        lender_ = lender_.drop("IndustryName", axis = 1)
        lender_ = lender_.groupby(["Lender Name"], as_index = False)["Number of Loans Given"].sum().sort_values(by= "Number of Loans Given", ascending = False)
        lender_ = lender_.head(5)
        lender_["Lender Name"] = label_break(list(lender_["Lender Name"]))
        fig_4 = createFig_bar_Top_Lenders(lender_, state, industry)

    else: 
        lender_ = lender[lender["StateName"] == state]
        lender_ = lender_[lender_["IndustryName"] == industry]
        lender_ = lender_.groupby(["Lender Name"], as_index = False)["Number of Loans Given"].sum().sort_values(by= "Number of Loans Given", ascending = False)
        lender_ = lender_.head(5)
        lender_["Lender Name"] = label_break(list(lender_["Lender Name"]))
        fig_4 = createFig_bar_Top_Lenders(lender_, state, industry)

    return fig_4


# Utilites Breakdown
@app.callback(
    Output("graph5", 'figure'),
    Input("state-dropdown", 'value'),
    Input("industry-dropdown", 'value'),
    Input("utilities-dropdown", 'value'),
    
)
def update_graph_top_industry(user_input_1, user_input_2, user_input_3):  # function arguments come from the component property of the Input
    state = user_input_1
    industry = user_input_2
    utility = user_input_3
    Plot_Utilities = pd.read_csv("./DashBoard/DashBoard_Data/Plot_Utilities.csv", sep = ',', header = 0)
    df_utilities = Plot_Utilities
    if(utility == "Payroll and Other Utilities"):
        if(state == "Nation" and industry == "All Industries"):
            df_utilities = df_utilities.drop(["StateName", "StateAcronym", "IndustryName"], axis = 1)
            fig_5 = CreateDonutChart(df_utilities, state, industry)

        elif(state == "Nation" and industry != "All Industries"):
            df_utilities = df_utilities.drop(["StateAcronym","StateName"], axis = 1)
            df_utilities = df_utilities[df_utilities["IndustryName"] == industry]
            fig_5 = CreateDonutChart(df_utilities, state, industry)

        elif(state != "Nation" and industry == "All Industries"):
            df_utilities = df_utilities.drop(["IndustryName"], axis = 1)
            df_utilities = df_utilities[df_utilities["StateName"] == state]
            fig_5 = CreateDonutChart(df_utilities, state, industry)

        else: 
            df_utilities = df_utilities[df_utilities["IndustryName"] == industry]
            df_utilities = df_utilities[df_utilities["StateName"] == state]
            fig_5 = CreateDonutChart(df_utilities, state, industry)
    else:
        if(state == "Nation" and industry == "All Industries"):
            df_utilities = df_utilities.drop(["StateName", "StateAcronym", "IndustryName"], axis = 1)
            df_utilities = df_utilities.groupby(["Breakdown", "Category", "Percent"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
            fig_5 = CreateSpendingCategoryBarChart(df_utilities, state, industry)

        elif(state == "Nation" and industry != "All Industries"):
            df_utilities = df_utilities.drop(["StateName","StateAcronym"], axis = 1)
            df_utilities = df_utilities[df_utilities["IndustryName"] == industry]
            df_utilities = df_utilities.groupby(["Breakdown", "Category", "Percent"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
            fig_5 = CreateSpendingCategoryBarChart(df_utilities, state, industry)

        elif(state != "Nation" and industry == "All Industries"):
            df_utilities = df_utilities.drop(["IndustryName"], axis = 1)
            df_utilities = df_utilities[df_utilities["StateName"] == state]
            df_utilities = df_utilities.groupby(["Breakdown", "Category", "Percent"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
            fig_5 = CreateSpendingCategoryBarChart(df_utilities, state, industry)

        else: 
            df_utilities = df_utilities[df_utilities["IndustryName"] == industry]
            df_utilities = df_utilities[df_utilities["StateName"] == state]
            df_utilities = df_utilities.groupby(["Breakdown", "Category", "Percent"], as_index = False)["Total"].sum().sort_values(by="Total", ascending = False)
            fig_5 = CreateSpendingCategoryBarChart(df_utilities, state, industry)

    return fig_5

if __name__ == '__main__':
    app.run_server(debug=True)