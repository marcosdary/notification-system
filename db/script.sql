create type send_type as enum (
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

create table email_notification (
	"idEmail" varchar(255) primary key,
	"recipientEmail" varchar(400) not null,
	
	"sendType" send_type not null,
	"status" status not null,
	
	"providerResponse" text default 'No response',
	"createdAt" timestamp default current_timestamp,
	"processedAt" timestamp default current_timestamp
);

drop table email_notification;

delete from email_notification where "idEmail" = '5436d192-610b-459b-b976-57f44f6e4bbe';

select * from email_notification;
drop type send_type;
