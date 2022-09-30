drop TABLE dbo.PPPLoanInfo
GO
drop TABLE PPPBorrower
GO
drop TABLE dbo.CensusInfo
GO
drop TABLE BusinessAgeDescription
GO
drop TABLE Unemployment
GO
drop TABLE BusinessType
GO
drop TABLE PPPLender
GO
drop TABLE DemographicInfo
GO
drop TABLE Industry
GO
drop Table [State]
GO

--Create State Table
CREATE TABLE [State](
    StateID int primary key identity(1,1),
    StateName varchar(30) not null,
    StateAcronym varchar(20) not null,
);
GO

--Create Industry Table
CREATE TABLE Industry(
    IndustryID int primary key identity(1,1),
    IndustryName varchar(100) not null,
);
GO

--Create Demographics Table
CREATE TABLE DemographicInfo(
    DemographicID int primary key identity(1,1),
    Race varchar(50) not null,
    Ethnicity varchar (20) not null,
    Sex varchar(10) not null,
);
GO

--Create PPP Lender Table
CREATE TABLE PPPLender(
    PPPLenderID int primary key identity(1,1),
    ServicingLenderName varchar(100) not null,
    OriginatingLenderName varchar(100) not null,
);
GO

--Create Business Type Table
CREATE TABLE BusinessType(
    BusinessTypeID int primary key identity (1,1),
    BusinessTypeDescription varchar(50) not null,
);
GO

-- --Create Unemployment Table
CREATE TABLE Unemployment(
    UnemploymentID int primary key identity (1,1),
    StateID int not null,
        constraint fk_Unemployment_StateID
        foreign key (StateID)
        references [State](StateID),
    FiledWeekEnded DATE not null,
    ReflectingWeekEnded Date not null,
    InitialClaims int not null,
    ContinuedClaims int not null,
    CoveredEmployment int not null,
    InsuredUnemploymentRate decimal(5,2) not null,
);
GO

--Create Business Age Description Table
CREATE TABLE BusinessAgeDescription(
    BusinessAgeDescID int primary key identity (1,1),
    BusinessAgeDescription varchar(50) not null,
);
GO

--Create Census Info Table
CREATE TABLE CensusInfo(
    CensusID int primary key identity (1,1),
    StateID int not null,
        constraint fk_CensusInfo_StateID
        foreign key (StateID)
        references [State](StateID),
    IndustryID int not null,
        constraint fk_CensusInfo_IndustryID
        foreign key (IndustryID)
        references [Industry](IndustryID),
    DemographicID int not null,
        constraint fk_CensusInfo_DemographicID
        foreign key (DemographicID)
        references [DemographicInfo](DemographicID),
    NumberOfBusinesses int not null,
);
GO

--Create PPP Borrower Table
CREATE TABLE PPPBorrower(
    PPPBorrowerID int primary key identity (1,1),
    BorrowerName varchar(100) not null,
    BusinessAgeDescID int not null,
        constraint fk_PPPBorrower_BusinessAgeDescID
        foreign key (BusinessAgeDescID)
        references [BusinessAgeDescription](BusinessAgeDescID),
    JobsReported decimal(12,2) not null,
    BusinessTypeID int not null,
        constraint fk_PPPBorrower_BusinessTypeID
        foreign key (BusinessTypeID)
        references [BusinessType](BusinessTypeID),
    HubzoneIndicator varchar(3)  not null,
    LMIIndicator varchar(3) not null,
    CensusID int not null,
        constraint fk_PPPBorrower_CensusID
        foreign key (CensusID)
        references [CensusInfo](CensusID)
);
GO

--Create Census Info Table
CREATE TABLE PPPLoanInfo(
    LoanNumber int primary key identity (1,1),
    DateApproved date not null,
    InitialApprovalAmount decimal(12,2) not null,
    LoanStatus varchar(20) not null,
    CurrentApprovalAmount decimal(12,2) not null,
    ForgivenessAmount decimal(12,2) not null,
    ForgivenessDate date not null,
    UTILITIES_PROCEED decimal(12,2) null,
    PAYROLL_PROCEED decimal(12,2) null,
    MORTGAGE_INTEREST_PROCEED decimal(12,2) null,
    RENT_PROCEED decimal(12,2) null,
    REFINANCE_EIDL_PROCEED decimal(12,2) null,
    HEALTHCARE_PROCEED decimal(12,2) null,
    DEBT_INTEREST_PROCEED decimal(12,2) null,
    PPPLenderID int not null,
    constraint fk_CensusInfo_PPPLenderID
    foreign key (PPPLenderID)
    references [PPPLender](PPPLenderID),
    PPPBorrowerID int not null,
        constraint fk_PPPLoanInfo_PPPBorrowerID
        foreign key (PPPBorrowerID)
        references [PPPBorrower](PPPBorrowerID)
);
GO

-- drop TABLE dbo.PPPLoanInfo
-- GO
-- drop TABLE dbo.CensusInfo
-- GO
-- drop TABLE PPPBorrower
-- GO
-- drop TABLE BusinessAgeDescription
-- GO
-- drop TABLE Unemployment
-- GO
-- drop TABLE BusinessType
-- GO
-- drop TABLE PPPLender
-- GO
-- drop TABLE DemographicInfo
-- GO
-- drop TABLE Industry
-- GO
-- drop Table [State]
-- GO