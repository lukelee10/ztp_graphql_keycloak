CREATE TABLE records (
  id SERIAL PRIMARY KEY,
  data TEXT,
  clearance VARCHAR(50)
);

INSERT INTO records (data, clearance) VALUES ('This is top secret data', 'TOPSECRET');
INSERT INTO records (data, clearance) VALUES ('This is confidential data', 'CONFIDENTIAL');
INSERT INTO records (data, clearance) VALUES ('This is secret data', 'SECRET');
INSERT INTO records (data, clearance) VALUES ('This is unclassified data', 'UNCLASSIFIED');

CREATE TABLE users (
    EmployeeNumber varchar(8) not null,
    UserName varchar(20),
    EmailAddress varchar(50),
    GivenName varchar(30),
    Surname varchar(50),
    Name varchar(70),
    DistinguishedName varchar(70),
    Clearance varchar(4),
    Company varchar(60),
    Nationality varchar(3),
    SCI varchar(30),
    ACTIVE varchar(1),
    NTK varchar(40),
    MemberOf varchar(60),
    Department varchar(60),
    Title varchar(40)
);

COPY users FROM '/tables/users.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE financials (
  identifierNFN VARCHAR(8),
  Classification VARCHAR(50),
  SCI VARCHAR(30),
  NTKoverall VARCHAR(40),
  ReleaseableTo VARCHAR(20),
  DateCreate VARCHAR(22),
  DateCreateNTKkey VARCHAR(30),
  Country VARCHAR(20),
  CountryNTKkey VARCHAR(30),
  Agency VARCHAR(20),
  AgencyNTKkey VARCHAR(30),
  FiscalYear VARCHAR(4),
  FiscalYearNTKkey VARCHAR(30),
  Project VARCHAR(40),
  ProjectNTK VARCHAR(30),
  OfficeBranch VARCHAR(10),
  OfficeBranchNTKkey VARCHAR(30),
  Organization VARCHAR(50),
  OrganzationNTKkey VARCHAR(30),
  DollarAmount VARCHAR(20),
  DollarNTKkey VARCHAR(30),
  Category VARCHAR(10),
  CategoryNTKkey VARCHAR(30),
  Justification VARCHAR(180),
  JustidicationNTKkey VARCHAR(30),
  FinancialStatementTitle VARCHAR(180),
  FinancialTitleNTKkey VARCHAR(30),
  FinancialForm VARCHAR(180),
  FinancialFormNTKkey VARCHAR(30),
  Comments VARCHAR(180),
  CommentsNTKkey VARCHAR(30),
  RecentActivity VARCHAR(180),
  RecentActivityNTKkey VARCHAR(30)
);

COPY financials FROM '/tables/financials.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE ntk (
    ntkkey VARCHAR(10),
    classification VARCHAR(12),
    ntkgroups VARCHAR(50)
);

COPY ntk FROM '/tables/ntk.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE nag (
    NAGKey VARCHAR(8),
    Value VARCHAR(60),
    Policy VARCHAR(30),
    ProfileDes VARCHAR(80),
    OwnerProducer VARCHAR(3),
    sci VARCHAR(25),
    accessList VARCHAR(180)
);

COPY nag FROM '/tables/nag.csv' DELIMITER ',' CSV HEADER;