DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS OrganizationUser;
DROP TABLE IF EXISTS Owner;
DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Repository;
DROP TABLE IF EXISTS File;
DROP TABLE IF EXISTS Issue;
DROP TABLE IF EXISTS Contributor;
DROP TABLE IF EXISTS RepositoryQueue;

CREATE TABLE Owner (
    name varchar(255),
    followers int,
    PRIMARY KEY (name)
);


CREATE TABLE User (
	name varchar(255),
    following int,
    PRIMARY KEY (name),
    FOREIGN KEY (name) REFERENCES Owner(name)
);

CREATE TABLE Organization (
	name varchar(255),
    PRIMARY KEY (name),
    FOREIGN KEY (name) REFERENCES Owner(name)
);


CREATE TABLE OrganizationUser (
    user_name varchar(255),
    organization_name varchar(255),
    PRIMARY KEY (user_name, organization_name),
    FOREIGN KEY (user_name) REFERENCES User(name),
    FOREIGN KEY (organization_name) REFERENCES Organization(name)
);


CREATE TABLE Repository (
	name varchar(255),
    stars int,
    owner varchar(255),
    PRIMARY KEY (name, owner),
    FOREIGN KEY (owner) REFERENCES Owner(name)
);


CREATE TABLE File (
    name varchar(255),
    language varchar(255),
    path varchar(255),
    repo_name varchar(255),
    owner varchar(255),
    PRIMARY KEY (path, repo_name, owner),
    FOREIGN KEY (repo_name, owner) REFERENCES Repository(name, owner)
);


CREATE TABLE Issue (
	id int AUTO_INCREMENT,
    check_id varchar(255),
    start_line int,
    end_line int,
    category varchar(255),
    impact varchar(255),
    repo_name varchar(255),
    owner varchar(255),
    path varchar(255),
    PRIMARY KEY (id, repo_name, owner, path),
    FOREIGN KEY (path, repo_name, owner) REFERENCES File(path, repo_name, owner)
);


CREATE TABLE Contributor (
    user_name varchar(255),
    repo_name varchar(255),
    owner varchar(255),
    PRIMARY KEY (user_name, repo_name, owner),
    FOREIGN KEY (user_name) REFERENCES User(name),
    FOREIGN KEY (repo_name, owner) REFERENCES Repository(name, owner)
);


CREATE TABLE RepositoryQueue (
    github_url varchar(255) CHECK (github_url LIKE 'https://github.com/%'),
    date_inserted datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (github_url)
);
