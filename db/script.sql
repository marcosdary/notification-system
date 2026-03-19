create type type_send as enum (
	'REGISTER', 
	'PASSWORD_CHANGE', 
	'PASSWORD_RESET', 
	'TWO_FACTOR_AUTH'
);

create type status as enum (
	'PENDING',
	'DONE',
	'ERROR',
	'REJECTED'
);

create table notifications (
	"idSend" varchar(255) primary key,
	"info" text not null,
	"typeSend" type_send not null,
	"status" status not null,
	"responseServer" text default 'No response',
	"createdAt" timestamp default current_timestamp,
	"endIn" timestamp default current_timestamp
);

drop table notifications;

select * from notifications;
drop type type_send;
