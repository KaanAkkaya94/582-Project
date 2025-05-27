DROP TABLE IF EXISTS admins;
use Fastmeds;

create table admins (
    adminID int key,
    foreign key (adminID) references users(userID)
);

insert into admins 
	values 
    (1);