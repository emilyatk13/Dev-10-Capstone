# Paycheck Protection Programs (PPP): Loan decision analysis led by data

As the global pandemic COVID 19 hit the U.S. Economy in 2019, the United States government implemented an unprecedented and large-scale solution to keep businesses (and by extension, their employees) afloat. The Paycheck Protection Program (PPP), which ran from March 2020 through April 2021, allowed businesses to take out loans backed by the federal government. The government intended for these loans to keep businesses solvent and employees on their payroll during the span of the pandemic.
We seek to provide an analysis that the government can apply should there ever be a need to implement something like the Paycheck Protection Program again. We will start with some exploratory research, aiming to understand what this program looked like in practice. In order to contextualize the impact of the PPP, we will also analyze contemporaneous unemployment data. From there, we will implement predictive modeling of data from the PPP to determine key factors in forecasting which borrowers will pay their loans. Our main questions that will guide this research are below.

## Essential Questions
1. Our team will analyze three datasets to answer the following questions:
2. What types of business owners (gender, race, geography) received Payment Protection Plan loans? 
3. Which industries (based on Census NAICS codes) received the largest amount of loans?
4. How did businesses in each state and industry use the loans they received?  
5. Was the quantity of loans given proportional to the demographic breakdown of business in each state/industry?
6. Which businesses in each state/industry paid off their loans? Which businesses had their loans forgiven?
7. Who were the top lenders to businesses in each state and industry?
8. What is the relationship between the number of PPP loans given by state and that state’s unemployment numbers?
9. Based on predictive modeling analysis, how likely is a particular business to pay back their loan?

## Table of Contents
- [Datasets](#Datasets)
- [Project Structure](#Project-Structure)


## Datasets
**Small Business Administration**. (July 4, 2022). Paycheck Protection Program - Freedom of Information Act. Retrieved
September 19, 2022 from data.sba.gov website: https://data.sba.gov/dataset/ppp-foia

  The Small Business Administration provides data on the government Paycheck Protection Program initialized in
  2020. Data provided here can be downloaded in CSV format. Due to the large size of the overall file, SBA has
  broken the data down into 13 CSV files that can then be remerged.

**United States Census Bureau**. (October 28, 2021). Annual Business Survey. Retrieved September 20, 2022 from
www.census.gov website: https://www.census.gov/data/developers/data-sets/abs.html

  The United States Census Bureau conducts an Annual Business Survey to provide select economic and
  demographic information for businesses and business owners. The Company Summary API provides data for
  employer businesses by sector, sex, ethnicity, race, veteran status, years in business, receipts size of firm, and
  employment size of firm for states within the U.S.

**United States Department of Labor**. (July 7, 2022). Unemployment Insurance Weekly Claims Data. Retrieved September
20, 2022 from oui.doleta.gov website: https://oui.doleta.gov/unemploy/claims.asp

  The United States Department of Labor Employment & Training Administration updates weekly claims for
  Unemployment Insurance. The Department of Labor tracks both Initial Claims (new claims) as well as Continued
  Claims to track the number of persons claiming unemployment benefits. Claims information can be accessed at
  a National or State level for a specified year range which can then be output either as an HTML webpage, Excel
  document, or XML document.
