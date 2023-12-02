create database City_Of_Williamston;

use City_of_Williamston;

create table UserInfo(Username varchar(20) NOT NULL, PwHash varbinary(1024) NOT NULL NOT NULL, CDate datetime, PRIMARY KEY(Username));

