# Paycheck Protection Programs (PPP): Loan decision analysis led by data

As the global pandemic COVID 19 hit the U.S. Economy in 2019, the United States government implemented an unprecedented and large-scale solution to keep businesses (and by extension, their employees) afloat. The Paycheck Protection Program (PPP), which ran from March 2020 through April 2021, allowed businesses to take out loans backed by the federal government. The government intended for these loans to keep businesses solvent and employees on their payroll during the span of the pandemic.
We seek to provide an analysis that the government can apply should there ever be a need to implement something like the Paycheck Protection Program again. We will start with some exploratory research, aiming to understand what this program looked like in practice. In order to contextualize the impact of the PPP, we will also analyze contemporaneous unemployment data. From there, we will implement predictive modeling of data from the PPP to determine key factors in forecasting which borrowers will pay their loans. Our main questions that will guide this research are below.

## Essential Questions
1. What types of business owners (gender, race, geography) received Paycheck Protection Program loans? 
2. Which industries (based on Census NAICS codes) received the largest amount of loans?
3. How did businesses in each state and industry use the loans they received?  
4. Was the quantity of loans given proportional to the demographic breakdown of business in each state/industry?
5. Which businesses in each state/industry paid off their loans? Which businesses had their loans forgiven?
6. Who were the top lenders to businesses in each state and industry?
7. What is the relationship between the number of PPP loans given by state and that state’s unemployment numbers?
8. Based on predictive modeling analysis, how likely is a particular business to pay back their loan?

## Table of Contents
- [Reporting](#Reporting)
- [Datasets](#Datasets)
- [Project Structure](#Project-Structure)
- [Data Structure & ETL](#data-structure--etl)
- [SQL Database](#SQL-Database)
- [Machine Learning](#Machine-Learning)
- [Visualization](#Visualization)
- [Dash Deployment](#Dash-Deployment)
- [Heroku](#Heroku)
- [Results](#Results)


## Reporting
The procedures and findings of this project can be found in one of several reports found under [/ProjectSpecifications/](/ProjectSpecifications/) directories. Summaries of the reports are the following:

 1. [ExecutiveSummary.pdf](ProjectSpecifications/ExecutiveSummary.pdf): Description of the high-level aims of the project, including introduction to project, key questions, datasets, and sources.
 2. [ProjectManagementPlan.xlsx](ProjectSpecifications/ProjectManagementPlan.xlsx): Excel table with teammembers breakdown of daily/hourly assignments from start to finish.
 3. [DataSources.pdf](ProjectSpecifications/DataSources.pdf): PDF citing data sources. 
 4. [DataPlatformDiagram.png](ProjectSpecifications/DataPlatformDiagram.png): Diagram outlining the data processing pipeline and necessary components.
 5. [DataFlowDiagram.png](ProjectSpecifications/DataFlowDiagram.png): Diagram outlining the sequence of data transformation.
 6. [RepeatableETLReport.pdf](ProjectSpecifications/RepeatableETLReport.pdf): In-depth description of ETL process to get from extracting raw data, cleaning/transforming in databricks, and loading into the SQL database.
 7. [ProjectTechnicalReport](ProjectSpecifications/ProjectTechnicalReport.pdf): Full explanation and summary of the project, including structure, methods, results, and recommendations.
 8. [VisualizationsNapkinsAndFeedback.pdf](ProjectSpecifications/VisualizationsNapkinsAndFeedback.pdf): Napkin drawing and feedback from group 1 for our visualizations.
 9. [DashboardNapkinsAndFeedback.pdf](ProjectSpecifications/DashboardNapkinsAndFeedback.pdf): Napkin drawing abd feedback from group 1 for our dashboard.
 
 All coding for our cleaning, transoformation, loading, and amchine learning model can be found under the [/code/](/code/) directory. All code for our dashboard can be found under the [/DashBoard/](/DashbBoard/) directory. 


## Datasets
**Small Business Administration**. (July 4, 2022). Paycheck Protection Program - Freedom of Information Act. Retrieved
September 19, 2022 from data.sba.gov website: https://data.sba.gov/dataset/ppp-foia
- The Small Business Administration provides data on the government Paycheck Protection Program initialized in 2020. Data provided here can be downloaded in CSV format. Due to the large size of the overall file, SBA has broken the data down into 13 CSV files that can then be remerged.

**United States Census Bureau**. (October 28, 2021). Annual Business Survey. Retrieved September 20, 2022 from
www.census.gov website: https://www.census.gov/data/developers/data-sets/abs.html
- The United States Census Bureau conducts an Annual Business Survey to provide select economic and demographic information for businesses and business owners. The Company Summary API provides data for employer businesses by sector, sex, ethnicity, race, veteran status, years in business, receipts size of firm, and employment size of firm for states within the U.S.

**United States Department of Labor**. (July 7, 2022). Unemployment Insurance Weekly Claims Data. Retrieved September
20, 2022 from oui.doleta.gov website: https://oui.doleta.gov/unemploy/claims.asp
- The United States Department of Labor Employment & Training Administration updates weekly claims for Unemployment Insurance. The Department of Labor tracks both Initial Claims (new claims) as well as Continued Claims to track the number of persons claiming unemployment benefits. Claims information can be accessed at a National or State level for a specified year range which can then be output either as an HTML webpage, Excel document, or XML document.

## Project Structure
![DataPlatformDiagram](https://user-images.githubusercontent.com/104226913/194190924-dd83e4a5-e8ae-49f6-b779-7d6a181f5159.png)
*Diagram outlining the data processing pipeline and necessary components.*

## Data Structure & ETL
A comprehensive guide of our ETL process can be found at [here](ProjectSpecifications/RepeatableETLReport.pdf), All data has been collected from U.S. Government agencies to ensure credibility. Information regarding the PPP has been obtained from the Small Business Administration. Information regarding the Business/Business Owner Demographics have been obtained from the Census Annual Business Survey. Information regarding Uemployment has been obtained from the Department of Labor Statistics. More information on these datasets can be found [here](#Datasets).

After retrieving all relevant data for our research from these U.S. departments, we then begin the process of transformation to populate our SQL database. Our transformation of the data utilized Python Pandas & Apache Spark. General Transformation practices included removing null values, dropping unnecessary columns, removing aggregations already present so as to not skew our results, converting data into an appropriate type, and renaming columns for clarity. For the PPP datasets, we made the decision to combine the 13 csv files into a larger single csv so as it could be called upon more reliably. With transformation of the data completed, we then deploy all the data into our SQL Database through the use of Spark Databricks. 


**Static Data Stream** <br>
![DataFlowDiagram](https://user-images.githubusercontent.com/104226913/194191035-bf00e8c8-8695-4d0a-aaa7-ced9d7fbb630.png)<br>
*Diagram outlining the sequence of data transformation.*

**Unemployment Data Stream** <br>
![Data_Stream drawio](https://user-images.githubusercontent.com/104226913/191998353-b38502ee-bfcc-446a-a7a0-3c6b89621907.png)

## SQL Database
This SQL Database is hosted on Microsoft Azure SQL Database. An Entity Relationship Diagram has been provided at the end of this section for clarity and can also be found at the end of this section. The combination of the following tables serve to create our database:
  1. `State`: This table contains the `StateName` and `StateAcronym` for the U.S. Both name and acronym have been included to ensure that each dataset can communicate properly.
  2. `Industry`: This table contains the `IndustryName` for each category of industry within the North American Industry Classification System (NAICS) used within the Census Data.
  3. `DemographicInfo`: This table contains the `Race`, `Ethnicity`, and `Sex` for business owners within the U.S. Column names for this table have been standardized to work with both the Census and PPP data, as there were discrepencies in the naming conventions from each dataset.
  4. `BusinessAgeDescription`: This table contains the `BusinessAgeDescription` showing the amount of time a business has been operating at the time of application for the PPP loan.
  5. `BusinessType`: This table contains the `BusinessTypeDescription` that provides the organizational structure of the business applying for the PPP loan.
  6. `Unemployment`: This table provides information from the Department of Labor Unemployment Claims dataset. This table includes: a `StateID` foreign key referenceing the `State` table, `FiledWeekEnded` date that references the end-date of a week for Unemployment Insurance (UI) claims being filed, `ReflectingWeekEnded` date that references the end-date of a week for UI claims that are being counted in the dataset, `InitialClaims` that represents the number of new UI claims in a given week, `ContinuedClaims` that references the number of UI claims that have been filed in a previous week and are still receiving benefits, `CoveredEmployment` which represents the number of individuals that could be eligible for UI in a given week, and `InsuredUnemploymentRate` which references the number of continued claims divided by the total covered employment of a given week.
  7. `CensusInfo`: This table contains a `StateID` foreign key referencing the `State` table, an `IndustryID` foreign key referencing the `Industry` table, a `DemographicID` foreign key referencing the `DemographicInfo` table, and the `NumberOfBusinesses` that references the total number of businesses that are located wihin a particular `CensusID`.
  8. `PPPBorrower`: This table contains information from the PPP dataset including: `BorrowerName` representing the name of the individual or business that applied for the loan, `CensusID` foreign key referencing the `CensusInfo` table, `BusinessAgeDescID` foreign key referencing the `BusinessAgeDescription` table, `JobsReported` which represents the number of employees within the applicants business, `BusinessTypeID` foreign key referencing the `BusinessType` table, `HubzoneIndicator` which represents whether a business is within a 'Historically Underutilized Business Zone', and `LMIIndicator` which represents whether the business classifies within a 'Low-and-Moderate Income' community.
  9. `PPPLender`: This table contains information from the PPP dataset including: `ServicingLenderName` which represents the institution that currently holds the loan given to a particular business, and `OriginatingLenderName` which represents the institution that initally held the loan at the time of loan approval.
  10. `PPPLoanInfo`: This table contains information from the PPP dataset for loan specifc information including: `DateApproved`, `InitialApprovalAmount`, `LoanStatus` to show whether it has been paid in-full or in Exemption 4 status, `CurrentApprovalAmount` if the amount received from the loan differed from the initial approval amount, `ForgivenessAmount`/`ForgivenessDate` if any portion of the loan was forgiven, a list of categories for how the funds from the loan were used (`UTILITIES_PROCEED`, `PAYROLL_PROCEED`, `MORTGAGE_INTEREST_PROCEED`,`RENT_PROCEED`,`REFINANCE_EIDL_PROCEED`, `HEALTHCARE_PROCEED`,`DEBT_INTEREST_PROCEED`), a `PPPBorrowerID` foreign key referencing the `PPPBorrower` table, and a `PPPLenderID` foreign key referencing the `PPPLender` table.
![ERD drawio (5)](https://user-images.githubusercontent.com/104226913/193344060-02c9fcb8-198a-4dd3-8985-231f168f81b2.png)
*ERD of the SQL database structure.*


## Machine Learning
Throughout our analysis of the PPP data, we anchored our focus around what happened during the loan program. Who received the loans, how did they use it, was there a connection to unemployment rates? For machine learning, we shifted from focusing on what the loan program was like in practice to how to optimize future implementation of a similar program. Our group created a model that predicts whether or not a borrower will pay back their loan based on key information including the industry, age of the business, and the demographics of the owner. We ran an algorithm with 'K Nearest Neighbors' using sklearn with the goal of producing the fewest false positives as lenders are risk averse. Should the United States ever run such a program again, the implementation of our model would allow them to select borrowers most likely to pay back their loans. Our full Machine Learning code with information comments can be found [here](code/PPP_ml_implementation.ipynb). 

## Visualization


The visualizations in the dashboard are created using both Plotly Express and Plotly Graph Objects. Plotly Express is used for it's native integration with Dash, a product created by Plotly. For any visualizations made outside of the Dash environment we have imported them as PNG files to be placed within the layout of the Dash page. For the graphs dynamically updated on pages, we chose to take the user’s dropdown input to call the relevant information from the Pandas DataFrames, which we then transformed into Plotly visualizations.

## Dash Deployment

For our dashboard, we utilized Plotly’s Dash in combination with Bootstrapping to create a viewable webpage. Dropdown menus, interactive graphs, and pre-run visuals then populate using Dash's Python library. For deployment of the dashboard, download all files as-is from the DashBoard folder. Inside the DashBoard folder, there is a folder called DashBoard-data. Do not unpack this folder, leave the folder as-is inside the DashBoard folder. The dashboard requires a config.py file with sensitive information. Please contact the owner of this github and request access. The config.py file contains all SQL table databases and variables for your own SQL username, SQL password, server, and port connected to the entire database.

To deploy the dashboard, run the DashBoard_Code.py file using the terminal command `python DashBoard_Code.py` in the root folder, do not closed the terminal, then copy and paste the url given to you in the terminal to a web broweser. The url should be `http://127.0.0.1:8050/` and will only run if the application is open and active in the terminal.

## Heroku

From our dashboard we utilized the cloud platorm Heroku to create a web app allowing easier access to our dahsboard at any time using the link: https://ppp-loans-dashboard.herokuapp.com/. Heroku is a cloud platform that lets companies and developers build, deliver, monitor and scale apps which is the fastest way to go from idea to URL, bypassing all those infrastructure headaches. 
To help set up this app we used the <a herf =https://www.youtube.com/c/CharmingData>Charming Data</a> Youtube channel instructional video <a herf=https://www.youtube.com/watch?v=b-M2KQ6_bM4>Deploy your First App with Heroku and Dash Plotly</a> which provided helpful step-by-step procedures to enable the web app.

## Results
You can find the results to this capstone project in three areas:

[ProjectTechnicalReport](ProjectSpecifications/ProjectTechnicalReport.pdf): Full explanation and summary of the project, including structure, methods, results, and recommendations.<br>
DashBoard_Code.py: Run this file in a Python interpreter from the root folder to view this projects supporting Dashboard.<br>
https://ppp-loans-dashboard.herokuapp.com/: Click on this link at anytime to bypass the setup of the dashboard and view the application using Heroku.
