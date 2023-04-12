CREATE TABLE document (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  classification VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE portion (
  id SERIAL PRIMARY KEY,
  document_id INTEGER REFERENCES document(id),
  text TEXT,
  classification VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO document (title, classification) VALUES ('Operation Plan: Alpha', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (1, 'Mission Objective', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (1, 'Enemy Threat Analysis', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (1, 'Logistics and Resource Allocation', 'SECRET');
INSERT INTO portion (document_id, text, classification) VALUES (1, 'Communication Protocols', 'SECRET');

INSERT INTO document (title, classification) VALUES ('Top Secret Briefing', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (2, 'Security Threat Assessment', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (2, 'National Security Implications', 'TOPSECRET');
INSERT INTO portion (document_id, text, classification) VALUES (2, 'Operational Plan Overview', 'TOPSECRET');

INSERT INTO document (title, classification) VALUES ('Naval Intelligence Report', 'SECRET');
INSERT INTO portion (document_id, text, classification) VALUES (3, 'Vessel Tracking and Identification', 'SECRET');
INSERT INTO portion (document_id, text, classification) VALUES (3, 'Current Naval Deployment Overview', 'SECRET');
INSERT INTO portion (document_id, text, classification) VALUES (3, 'Analysis of Enemy Naval Capabilities', 'TOPSECRET');

INSERT INTO document (title, classification) VALUES ('La La Land Movie Review', 'UNCLASSIFIED');
INSERT INTO portion (document_id, text, classification) VALUES (4, 'La La Land is a romantic musical comedy-drama film directed by Damien Chazelle and starring Emma Stone and Ryan Gosling.', 'UNCLASSIFIED');
INSERT INTO portion (document_id, text, classification) VALUES (4, 'The movie tells the story of Mia, an aspiring actress, and Sebastian, a jazz pianist, who fall in love while pursuing their dreams in Los Angeles.', 'UNCLASSIFIED');
INSERT INTO portion (document_id, text, classification) VALUES (4, 'The movie features beautiful cinematography, catchy songs, and impressive dance numbers that pay tribute to classic Hollywood musicals.', 'UNCLASSIFIED');
INSERT INTO portion (document_id, text, classification) VALUES (4, 'Emma Stone and Ryan Gosling deliver strong performances, and their chemistry on-screen is undeniable.', 'UNCLASSIFIED');
INSERT INTO portion (document_id, text, classification) VALUES (4, 'La La Land is a charming and entertaining movie that is sure to leave you with a smile on your face.', 'UNCLASSIFIED');

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