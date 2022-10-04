import numpy as np
import pandas as pd
import pymssql

from config2 import database
from config2 import username
from config2 import password
from config2 import server

# import SQL database tables
from config2 import Statetable
from config2 import Industrytable
from config2 import Demographictable
from config2 import PPPLoanInfotable
from config2 import PPPLendertable

from config2 import PPPBorrowertable
from config2 import CensusInfotable
from config2 import Unemploymenttable

# Data Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Map Data - - - - - - - - - - - - - - - - - - - - - - - - - -

# Data for Map of Percent of Loans Received Nationally
def data_0():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)

        cursor = conn.cursor()
        query_0 = f"""
        SELECT 
        S.StateName, S.StateAcronym,
        PL.LoanNumber
        FROM {CensusInfotable} as C
        INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        INNER JOIN {PPPLoanInfotable} AS PL ON PB.PPPBorrowerID = PL.PPPBorrowerID
        INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
        """
        State_to_Loan = pd.read_sql(query_0, conn)
    except Exception as e:
        print(e)
    State_to_Loan = State_to_Loan.groupby(["StateName", "StateAcronym"], as_index=False)["LoanNumber"].count()
    State_to_Loan = State_to_Loan[State_to_Loan["StateName"] != "Unanswered"]
    Total_Loans_Quantity = State_to_Loan["LoanNumber"].sum()
    State_to_Loan["Percent of Loans"] = round((State_to_Loan["LoanNumber"] / Total_Loans_Quantity) * 100,2)
    return State_to_Loan
# Final table : State_to_Loan 

# Data for Map of Dollar Amount of Loans Received Nationally
def data_8():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)

        cursor = conn.cursor()
        query_0 = f"""
        SELECT 
        S.StateName, S.StateAcronym,
        SUM(CAST(PL.CurrentApprovalAmount AS BIGINT)) AS CurrentApprovalAmount
        FROM {CensusInfotable} as C
        INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        INNER JOIN {PPPLoanInfotable} AS PL ON PB.PPPBorrowerID = PL.PPPBorrowerID
        INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
        GROUP BY S.StateName, S.StateAcronym
        """
        State_to_Loan_Cash = pd.read_sql(query_0, conn)
    except Exception as e:
        print(e)
    State_to_Loan_Cash = State_to_Loan_Cash[State_to_Loan_Cash["StateName"] != "Unanswered"]
    State_to_Loan_Cash["CurrentApprovalAmount Billions"] = round((State_to_Loan_Cash["CurrentApprovalAmount"] / 1_000_000_000),2).astype(str) + "B"
    return State_to_Loan_Cash
# Final table : State_to_Loan_Cash

# Data for Map of Percent of Borrowers per Businesses
def data_9():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)

        cursor = conn.cursor()
        query_0 = f"""
        SELECT 
        S.StateName, S.StateAcronym, 
        SUM(C.NumberOfBusinesses) as NumberOfBusinesses,
        COUNT(PB.BorrowerName) AS NumberofBorrowers
        FROM {CensusInfotable} as C
        INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
        GROUP BY S.StateName, S.StateAcronym
        ORDER BY S.StateName
        """
        Borrwers_to_Businesses = pd.read_sql(query_0, conn)
    except Exception as e:
        print(e)
    Borrwers_to_Businesses["Percent of Borrowers per Businesses"] = round(Borrwers_to_Businesses["NumberofBorrowers"] / Borrwers_to_Businesses["NumberOfBusinesses"] * 100, 2)
    return Borrwers_to_Businesses
# Final table : Borrwers_to_Businesses

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



# PPP Borrower Breakdown - - - - - - - - - - - - - - - - - - 

# Data for Bar Chart of Demographics of who Recieved loans 
def data_1():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)

        cursor = conn.cursor()
        query_1 = f"""
        SELECT 
        D.Sex, D.Race, I.IndustryName, S.StateName,
        PL.LoanNumber
        FROM {CensusInfotable} as C
        INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        INNER JOIN {PPPLoanInfotable} AS PL ON PB.PPPBorrowerID = PL.PPPBorrowerID
        INNER JOIN {Demographictable} AS D ON C.DemographicID = D.DemographicID
        INNER JOIN {Industrytable} AS I ON C.IndustryID = I.IndustryID
        INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
        """
        Demographic_to_Loan = pd.read_sql(query_1, conn)
    except Exception as e:
        print(e)

    Demographic_to_Loan_group = Demographic_to_Loan.groupby(["Race", "Sex", "IndustryName", "StateName"], as_index= False)["LoanNumber"].count()
    Demographic_to_Loan_group = Demographic_to_Loan_group[Demographic_to_Loan_group["Sex"] != "Unanswered"]
    Demographic_to_Loan_group["Race"] = Demographic_to_Loan_group["Race"].replace("Unanswered", "Other")
    Demographic_to_Loan_group["Race"] = Demographic_to_Loan_group["Race"].replace("Black or African American", "Black")
    Total_Loans_Quantity = Demographic_to_Loan_group["LoanNumber"].sum()
    Demographic_to_Loan_group["Percent of Loans"] = round((Demographic_to_Loan_group["LoanNumber"] / Total_Loans_Quantity) * 100,2)
    return Demographic_to_Loan_group
# Final table : Demographic_to_Loan_group 

# Data for Bar Chart of Top 10 Industries 
def data_2():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)

        cursor = conn.cursor()
        query_2 = f"""
        SELECT I.IndustryName, S.StateName, SUM(PL.CurrentApprovalAmount)
        FROM {CensusInfotable} as C
        INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
        INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        INNER JOIN {PPPLoanInfotable} AS PL ON PB.PPPBorrowerID = PL.PPPBorrowerID
        INNER JOIN {Industrytable} AS I ON C.IndustryID = I.IndustryID
        GROUP BY I.IndustryName, S.StateName
        """
        Industry_to_LoanAmount = pd.read_sql(query_2, conn)
    except Exception as e:
        print(e)

    Industry_to_LoanAmount_ = Industry_to_LoanAmount
    Industry_to_LoanAmount_["Cummulative Loan Amount ($)"] = Industry_to_LoanAmount_[""]
    Industry_to_LoanAmount_ = Industry_to_LoanAmount_.drop("", axis=1).reset_index().drop("index",axis=1)
    Industry_to_LoanAmount_["Cummulative Loan Amount ($)"] = Industry_to_LoanAmount_["Cummulative Loan Amount ($)"].astype(float)
    Industry_to_LoanAmount_["Cummulative Loan Amount Billions"] = round(Industry_to_LoanAmount_["Cummulative Loan Amount ($)"]/1_000_000_000, 2).astype(str) +"B"
    Industry_to_LoanAmount_ = Industry_to_LoanAmount_.sort_values(by = "Cummulative Loan Amount ($)", ascending = False)
    Industry_to_LoanAmount_ = Industry_to_LoanAmount_[Industry_to_LoanAmount_["IndustryName"] != "Other Services (except Public Administration)"]
    return Industry_to_LoanAmount_
# Final table : Industry_to_LoanAmount_ 

# Data for loan spending breakdown
def data_3():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)
        cursor = conn.cursor()
        query1 = f'''SELECT sum(cast(UTILITIES_PROCEED as bigint)) as UTILITIES_PROCEED,
            sum(cast(PAYROLL_PROCEED as bigint)) as PAYROLL_PROCEED,
            sum(cast(MORTGAGE_INTEREST_PROCEED as bigint)) as MORTGAGE_INTEREST_PROCEED,
            sum(cast(RENT_PROCEED as bigint)) as RENT_PROCEED,
            sum(cast(REFINANCE_EIDL_PROCEED as bigint)) as REFINANCE_EIDL_PROCEED, 
            sum(cast(HEALTHCARE_PROCEED as bigint)) as HEALTHCARE_PROCEED,
            sum(cast(DEBT_INTEREST_PROCEED as bigint)) as DEBT_INTEREST_PROCEED, 
            StateName, 
            StateAcronym, 
            IndustryName 
            FROM {PPPLoanInfotable} 
            join {PPPBorrowertable} on PPPLoanInfo.PPPBorrowerID = PPPBorrower.PPPBorrowerID 
            join {CensusInfotable} on PPPBorrower.CensusID = CensusInfo.CensusID 
            join {Statetable} on CensusInfo.StateID = State.StateID 
            join {Industrytable} on CensusInfo.IndustryID = Industry.IndustryID
            group by StateName, StateAcronym, IndustryName'''
        df1 = pd.read_sql(query1, conn)
    except Exception as e:
        print(e)
    df2 = df1.melt(['StateName', 'StateAcronym', 'IndustryName'], var_name='Category', value_name='Total')
    total_proceeds = df2["Total"].sum()
    df2["Percent"] = round(df2["Total"] / total_proceeds * 100, 2)
    df2["Category"] = df2["Category"].apply(lambda x : x[:-8].replace('_', ' ').title())
    df2["Breakdown"] = np.where(df2["Category"]=='Payroll', 'Payroll', 'Other')
    return df2
# Final table : df2 

# Data for Stacked cluster graph to show proportions of PPP to Census data
def data_4():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)
        cursor = conn.cursor()
        query2 = f"select DISTINCT D.Race, D.Sex, B.BorrowerName, I.IndustryName, S.StateName \
            from {PPPBorrowertable} B \
            join {CensusInfotable} C on B.CensusID = C.CensusID \
            join {Demographictable} D on C.DemographicID = D.DemographicID \
            join {Industrytable} I on I.IndustryID = C.IndustryID \
            join {Statetable} S on S.StateID = C.StateID \
            where race NOT LIKE '%Unanswered%'"
        query3 = f"select D.Race, D.Sex, C.NumberOfBusinesses, I.IndustryName, S.StateName \
            from {CensusInfotable} C \
            join {Demographictable} D on C.DemographicID = D.DemographicID \
            join {Industrytable} I on I.IndustryID = C.IndustryID \
            join {Statetable} S on S.StateID = C.StateID \
            where D.Race NOT LIKE '%Unanswered%' "
        df2 = pd.read_sql(query2, conn)
        df3 = pd.read_sql(query3, conn)
    except Exception as e:
        print(e)
    #count the number of borrower names for each race and sex. 
    PPPDemo = df2.groupby(["Race", "Sex", "IndustryName", "StateName"], as_index= False)["BorrowerName"].count()
    #exclude any unanswered sex.
    PPPDemo = PPPDemo[PPPDemo["Sex"] != "Unanswered"]
    #sum up value for each sex.
    temp = PPPDemo.groupby(["Race"], as_index= False)["BorrowerName"].sum()
    #put tables together.
    PPPDemo = pd.merge(temp, PPPDemo, on='Race')
    #appropriately rename columns.
    PPPDemo.rename(columns = {'BorrowerName_x':'TotalRace','BorrowerName_y':'TotalRacePerSex'}, inplace = True)
    # #create percentage column, rounded by 2 decimals.
    PPPDemo["PercentOfRace"] = round((PPPDemo['TotalRacePerSex']/PPPDemo['TotalRace']) * 100, 2)
    #sum NumberOfBusinesses instead of count. each line represents # of people that fit all catories. # of Race A of Sex B in State C in Industry D. 
    CensusDemo = df3.groupby(["Race", "Sex", "IndustryName", "StateName"], as_index= False)["NumberOfBusinesses"].sum()
    #exclude any unanswered sex.
    CensusDemo = CensusDemo[CensusDemo["Sex"] != "Unanswered"]
    #exclude any race that is aslo not included in PPP
    CensusDemo = CensusDemo[CensusDemo["Race"] != "American Indian and Alaska Native"]
    CensusDemo = CensusDemo[CensusDemo["Race"] != "Native Hawaiian and Other Pacific Islander"]
    #sum up value for each sex.
    temp2 = CensusDemo.groupby(["Race"], as_index= False)["NumberOfBusinesses"].sum()
    #put tables together.
    CensusDemo = pd.merge(temp2, CensusDemo, on='Race')
    #appropriately rename columns.
    CensusDemo.rename(columns = {'NumberOfBusinesses_x':'TotalRace','NumberOfBusinesses_y':'TotalRacePerSex'}, inplace = True)
    #create percentage column, rounded by 2 decimals.
    CensusDemo["PercentOfRace"] = round((CensusDemo['TotalRacePerSex']/CensusDemo['TotalRace']) * 100, 2)
    PPPCopy = PPPDemo.copy()
    CensusCopy = CensusDemo.copy()
    #add origin column to both tables w/ appropriate origins
    PPPCopy['Origin'] = 'PPP'
    CensusCopy['Origin'] = 'Census'
    #concatenate tables. Should work perfectly if all column names alighn.
    PPPCensusDemo= pd.concat([CensusCopy, PPPCopy])
    PPPCensusDemo["Race"] = PPPCensusDemo["Race"].replace("Black or African American", "Black")
    return PPPCensusDemo
# Final table : PPPCensusDemo 

# Data bar chart of top lenders
def data_6():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)
        cursor = conn.cursor()
        query2 = f"""SELECT S.StateName, S.StateAcronym, I.IndustryName, L.ServicingLenderName, COUNT(CAST(LI.LoanNumber AS BIGINT)) AS LoanNumber
        FROM {CensusInfotable} AS C
        JOIN {Statetable} AS S ON C.StateID = S.StateID
        JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        JOIN {PPPLoanInfotable} AS LI ON PB.PPPBorrowerID = LI.PPPBorrowerID
        JOIN {PPPLendertable} AS L ON LI.PPPLenderID = L.PPPLenderID
        JOIN {Industrytable} AS I ON C.IndustryID = I.IndustryID
        GROUP BY S.StateName, S.StateAcronym, I.IndustryName, L.ServicingLenderName"""
        df2 = pd.read_sql(query2, conn)
    except Exception as e:
        print(e)
    #lender = df2.groupby(['ServicingLenderName', 'IndustryName', 'StateName'], as_index = False)['LoanNumber'].count()
    lender = df2.sort_values(by='LoanNumber', ascending=False)
    lender = lender.drop("StateAcronym", axis = 1)
    lender = lender.rename(columns={'LoanNumber': 'Number of Loans Given', 'ServicingLenderName' : 'Lender Name'})
    return lender
# Final table : lender 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



# Unemploymnet - - - - - - - - - - - - - - - - - - - - - - -

# Data for all Unemploymnet Data based Graphs
def data_5():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)
        cursor = conn.cursor()
        query_2 = f"""
            SELECT S.StateName, S.StateAcronym,
            SUM(CAST(U.ContinuedClaims AS BIGINT)) AS ContinuedClaims, 
            SUM(CAST(PL.CurrentApprovalAmount AS BIGINT)) AS CurrentApprovalAmount, 
            COUNT(CAST(PL.LoanNumber AS BIGINT)) AS LoanNumber
            FROM {CensusInfotable} as C
            INNER JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
            INNER JOIN {PPPLoanInfotable} AS PL ON PB.PPPBorrowerID = PL.PPPBorrowerID
            INNER JOIN {Statetable} AS S ON C.StateID = S.StateID
            INNER JOIN {Unemploymenttable} AS U ON S.StateID = U.StateID
            WHERE CONVERT(datetime, U.ReflectingWeekEnded) > CONVERT(datetime, '04-21-2020') AND CONVERT(datetime, U.FiledWeekEnded) < CONVERT(datetime, '3-31-2021')
            GROUP BY S.StateName, S.StateAcronym
        """
        Unemployment_to_Loan = pd.read_sql(query_2, conn)
    except Exception as e:
        print(e)
    #transforming columns to add percentages
    Unemployment_to_Loan_ = Unemployment_to_Loan
    Unemployment_total = Unemployment_to_Loan_["ContinuedClaims"].sum()
    Unemployment_to_Loan_["Percent Unemployed"] = round(((Unemployment_to_Loan_["ContinuedClaims"] / Unemployment_total) * 100), 2)
    states = {
        'AK': 'West',
        'AL': 'South',
        'AR': 'South',
        'AZ': 'West',
        'CA': 'West',
        'CO': 'West',
        'CT': 'Northeast',
        'DC': 'Northeast',
        'DE': 'South',
        'FL': 'South',
        'GA': 'South',
        'HI': 'West',
        'IA': 'Midwest',
        'ID': 'West',
        'IL': 'Midwest',
        'IN': 'Midwest',
        'KS': 'Midwest',
        'KY': 'South',
        'LA': 'South',
        'MA': 'Northeast',
        'MD': 'Northeast',
        'ME': 'Northeast',
        'MI': 'Midwest',
        'MN': 'Midwest',
        'MO': 'Midwest',
        'MS': 'South',
        'MT': 'West',
        'NC': 'South',
        'ND': 'Midwest',
        'NE': 'Midwest',
        'NH': 'Northeast',
        'NJ': 'Northeast',
        'NM': 'West',
        'NV': 'West',
        'NY': 'Northeast',
        'OH': 'Midwest',
        'OK': 'South',
        'OR': 'West',
        'PA': 'Northeast',
        'RI': 'Northeast',
        'SC': 'South',
        'SD': 'Midwest',
        'TN': 'South',
        'TX': 'South',
        'UT': 'West',
        'VA': 'South',
        'VT': 'Northeast',
        'WA': 'West',
        'WI': 'Midwest',
        'WV': 'South',
        'WY': 'West'
    }
    Unemployment_to_Loan['Region'] = Unemployment_to_Loan['StateAcronym'].map(states)
    #rename columns for graph titles
    Unemployment_to_Loan.rename(columns={'StateName': 'State', 'StateAcronym': 'State Acronym', 'ContinuedClaims':'Total Unemployment Claims', 'CurrentApprovalAmount': 'Total Loan Amount ($)', 'LoanNumber':'Total PPP Loans', 'Percent Unemployed':'Percentage of Total Unemployment Claims'}, inplace=True)
    return Unemployment_to_Loan
# Final table : Unemployment_to_Loan 

# Data for Map of Percent of Unforgiven Loans
def data_7():
    # pull queies from SQL database
    try:
        conn = pymssql.connect(server,username, password,database)
        cursor = conn.cursor()
        query2 = f"""SELECT S.StateName, S.StateAcronym, L.ServicingLenderName, I.IndustryName, COUNT(CAST(LI.LoanNumber AS BIGINT)) AS LoanNumber, LI.LoanStatus
        FROM {CensusInfotable} AS C
        JOIN {Statetable} AS S ON C.StateID = S.StateID
        JOIN {PPPBorrowertable} AS PB ON C.CensusID = PB.CensusID
        JOIN {PPPLoanInfotable} AS LI ON PB.PPPBorrowerID = LI.PPPBorrowerID
        JOIN {PPPLendertable} AS L ON LI.PPPLenderID = L.PPPLenderID
        JOIN {Industrytable} AS I ON C.IndustryID = I.IndustryID
        GROUP BY S.StateName, S.StateAcronym, I.IndustryName, L.ServicingLenderName, LI.LoanStatus"""
        df2 = pd.read_sql(query2, conn)
        df2
    except Exception as e:
        print(e)
    maps = df2.groupby(['LoanStatus', 'StateAcronym', 'StateName'], as_index = False)['LoanNumber'].count()
    maps = maps.sort_values(by='LoanNumber', ascending=False)
    maps = maps[maps['LoanStatus'] == 'Exemption 4']
    maps_unpaid_total = maps['LoanNumber'].sum()
    maps['LoanNumber'] = maps['LoanNumber'].astype(float)
    maps['Percentage'] = round(((maps['LoanNumber']/maps_unpaid_total) * 100), 2)
    maps2 = maps.groupby(['StateAcronym', 'StateName'], as_index=False)['Percentage'].sum()
    maps2.sort_values(by='Percentage')
    return maps2
# Final table : maps2 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Data to Export - - - - - - - - - - - - - - - - - - - - - - - - - 
Heat_Map_Percent_Loans_Received_Quantity = data_0()
Bar_Chart_Demographics_Percent_Loans_Received = data_1()
Bar_Chart_Top_10_Industries = data_2()
Plot_Utilities = data_3()
Cluster_Stacked_Bar_Chart_Demographics_PPP_Census = data_4()
Unemployment_data = data_5()
Top_Lender_data = data_6()
Heat_Map_Unforgiven_Loans = data_7()
Heat_Map_Dollar_Amount_of_Loans_Received = data_8()
Heat_Map_Percent_of_Borrwers_to_Businesses = data_9()

Heat_Map_Percent_Loans_Received_Quantity.to_csv("DashBoard/DashBoard_Data/Heat_Map_Percent_Loans_Received_Quantity.csv", sep=',', encoding='utf-8', index=False)
Bar_Chart_Demographics_Percent_Loans_Received.to_csv("DashBoard/DashBoard_Data/Bar_Chart_Demographics_Percent_Loans_Received.csv", sep=',', encoding='utf-8', index=False)
Bar_Chart_Top_10_Industries.to_csv("DashBoard/DashBoard_Data/Bar_Chart_Top_10_Industries.csv", sep=',', encoding='utf-8', index=False)
Plot_Utilities.to_csv("DashBoard/DashBoard_Data/Plot_Utilities.csv", sep=',', encoding='utf-8', index=False)
Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.to_csv("DashBoard/DashBoard_Data/Cluster_Stacked_Bar_Chart_Demographics_PPP_Census.csv", sep=',', encoding='utf-8', index=False)
Unemployment_data.to_csv("DashBoard/DashBoard_Data/Unemployment_data.csv", sep=',', encoding='utf-8', index=False)
Top_Lender_data.to_csv("DashBoard/DashBoard_Data/Top_Lender_data.csv", sep=',', encoding='utf-8', index=False)
Heat_Map_Unforgiven_Loans.to_csv("DashBoard/DashBoard_Data/Heat_Map_Unforgiven_Loans.csv", sep=',', encoding='utf-8', index=False)
Heat_Map_Dollar_Amount_of_Loans_Received.to_csv("DashBoard/DashBoard_Data/Heat_Map_Dollar_Amount_of_Loans_Received.csv", sep=',', encoding='utf-8', index=False)
Heat_Map_Percent_of_Borrwers_to_Businesses.to_csv("DashBoard/DashBoard_Data/Heat_Map_Percent_of_Borrwers_to_Businesses.csv", sep=',', encoding='utf-8', index=False)


