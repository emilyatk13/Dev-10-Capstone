# Paycheck Protection Programs (PPP): Loan decision analysis led by data

As the global pandemic COVID 19 hit the U.S. Economy in 2019, the United States government implemented an unprecedented and large-scale solution to keep businesses (and by extension, their employees) afloat. The Paycheck Protection Program (PPP), which ran from March 2020 through April 2021, allowed businesses to take out loans backed by the federal government. The government intended for these loans to keep businesses solvent and employees on their payroll during the span of the pandemic.
We seek to provide an analysis that the government can apply should there ever be a need to implement something like the Paycheck Protection Program again. We will start with some exploratory research, aiming to understand what this program looked like in practice. In order to contextualize the impact of the PPP, we will also analyze contemporaneous unemployment data. From there, we will implement predictive modeling of data from the PPP to determine key factors in forecasting which borrowers will pay their loans. Our main questions that will guide this research are below.

## Essential Questions
1. What types of business owners (gender, race, geography) received Payment Protection Plan loans? 
2. Which industries (based on Census NAICS codes) received the largest amount of loans?
3. How did businesses in each state and industry use the loans they received?  
4. Was the quantity of loans given proportional to the demographic breakdown of business in each state/industry?
5. Which businesses in each state/industry paid off their loans? Which businesses had their loans forgiven?
6. Who were the top lenders to businesses in each state and industry?
7. What is the relationship between the number of PPP loans given by state and that state’s unemployment numbers?
8. Based on predictive modeling analysis, how likely is a particular business to pay back their loan?

## Table of Contents
- [Datasets](#Datasets)
- [Project Structure](#Project-Structure)
- [Data Structure & ETL](#data-structure--etl)
- [SQL Database](#SQL-Database)


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
![DataPlatform-Page-1 drawio](https://user-images.githubusercontent.com/104226913/192575526-b12ce4d0-dd1c-46cc-be9b-426d1a910c20.png)
*Diagram outlining the data processing pipeline and necessary components.*

## Data Structure & ETL
A comprehensive guide of our ETL process can be found at [INSERT LINK TO REPEATABLEETLREPORT.PDF], All data has been collected from U.S. Government agencies to ensure credibility. Information regarding the PPP has been obtained from the Small Business Administration. Information regarding the Business/Business Owner Demographics have been obtained from the Census Annual Business Survey. Information regarding Uemployment has been obtained from the Department of Labor Statistics. More information on these datasets can be found [here](#Datasets).

After retrieving all relevant data for our research from these U.S. departments, we then begin the process of transformation to populate our SQL database. Our transformation of the data utilized Python Pandas & Apache Spark. General Transformation practices included removing null values, dropping unnecessary columns, removing aggregations already present so as to not skew our results, converting data into an appropriate type, and renaming columns for clarity. For the PPP datasets, we made the decision to combine the 13 csv files into a larger single csv so as it could be called upon more reliably. With transformation of the data completed, we then deploy all the data into our SQL Database through the use of Spark Databricks. 


**Static Data Stream** <br>
![DataFlow Diagram drawio (2)](https://user-images.githubusercontent.com/104226913/192000149-b6e06fd3-0e6a-4860-8f0a-8bc1d0a499c8.png)<br>
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
  10. `PPPLoanInfo`: This table
![ERD drawio (5)](https://user-images.githubusercontent.com/104226913/193344060-02c9fcb8-198a-4dd3-8985-231f168f81b2.png)
*ERD of the SQL database structure.*
