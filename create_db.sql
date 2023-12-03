create database City_Of_Williamston;

use City_of_Williamston;

create table UserInfo(Username varchar(20) NOT NULL, PwHash varbinary(1024) NOT NULL NOT NULL, CDate datetime, PRIMARY KEY(Username));

-- holds text data for the cms community page
create table cmsCommunityPage (
  number int auto_increment primary key,
  size varchar(10) not null,
  content text
  );

insert into cmsCommunityPage (size,content)
values ('h1','Sample Title'),
('h3','Sample Heading'),
('p','Sample Text');
