create type send_type as enum (
	'REGISTER', 
	'PASSWORD_CHANGE', 
	'PASSWORD_RESET', 
	'TWO_FACTOR_AUTH'
);


create type status_email as enum (
	'PENDING',
	'DONE',
	'ERROR',
	'REJECTED'
);


create table email_notification (
	"id_email" varchar(255) primary key,
	"recipient_email" varchar(400) not null,
	
	"send_type" send_type not null,
	"status" status_email not null,
	
	"action_link" varchar(500),
    "code" varchar(10),
    "token" varchar(400),
    "expires_at" integer,
	
	"provider_response" text default 'No response',
	"created_at" timestamp default current_timestamp,
	"processed_at" timestamp default current_timestamp
);



drop table email_notification;

