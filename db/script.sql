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

create type status_webhook as enum (
	'PENDING',
	'SUCCESS',
	'FAILED',
	'RETRYING',
	'DEAD_LETTER'
);

create table email_notification (
	"idEmail" varchar(255) primary key,
	"recipientEmail" varchar(400) not null,
	
	"sendType" send_type not null,
	"status" status_email not null,
	
	"actionLink" varchar(500),
    "code" varchar(10),
    "token" varchar(400),
    "expiresAt" integer,
	
	"providerResponse" text default 'No response',
	"createdAt" timestamp default current_timestamp,
	"processedAt" timestamp default current_timestamp
);

create table webhook (
	"idWebhook" varchar(255) primary key,
	"status" status_webhook not null,
	"response" text,
	"createdAt" timestamp default current_timestamp,
	"processedAt" timestamp default current_timestamp
);


drop table email_notification;

