BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "DjangoLivre_transfer" (
	"id"	integer NOT NULL,
	"source_cpf"	varchar(14) NOT NULL,
	"target_cpf"	varchar(14) NOT NULL,
	"value"	real NOT NULL,
	"date"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "DjangoLivre_account" (
	"number"	char(32) NOT NULL,
	"balance"	integer unsigned NOT NULL CHECK("balance" >= 0),
	"account_user_id"	varchar(14) NOT NULL,
	PRIMARY KEY("account_user_id"),
	FOREIGN KEY("account_user_id") REFERENCES "DjangoLivre_client"("cpf") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "DjangoLivre_client" (
	"name"	varchar(255) NOT NULL,
	"cpf"	varchar(14) NOT NULL,
	"phone"	varchar(128) NOT NULL,
	"email"	varchar(255) NOT NULL,
	"creation"	datetime NOT NULL,
	PRIMARY KEY("cpf")
);
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'DjangoLivre','0001_initial','2021-12-01 18:52:48.520263'),
 (2,'contenttypes','0001_initial','2021-12-01 18:52:48.535269'),
 (3,'auth','0001_initial','2021-12-01 18:52:48.566269'),
 (4,'admin','0001_initial','2021-12-01 18:52:48.589262'),
 (5,'admin','0002_logentry_remove_auto_add','2021-12-01 18:52:48.608261'),
 (6,'admin','0003_logentry_add_action_flag_choices','2021-12-01 18:52:48.626274'),
 (7,'contenttypes','0002_remove_content_type_name','2021-12-01 18:52:48.656077'),
 (8,'auth','0002_alter_permission_name_max_length','2021-12-01 18:52:48.680082'),
 (9,'auth','0003_alter_user_email_max_length','2021-12-01 18:52:48.701080'),
 (10,'auth','0004_alter_user_username_opts','2021-12-01 18:52:48.722080'),
 (11,'auth','0005_alter_user_last_login_null','2021-12-01 18:52:48.740077'),
 (12,'auth','0006_require_contenttypes_0002','2021-12-01 18:52:48.751083'),
 (13,'auth','0007_alter_validators_add_error_messages','2021-12-01 18:52:48.766083'),
 (14,'auth','0008_alter_user_username_max_length','2021-12-01 18:52:48.787081'),
 (15,'auth','0009_alter_user_last_name_max_length','2021-12-01 18:52:48.812087'),
 (16,'auth','0010_alter_group_name_max_length','2021-12-01 18:52:48.834083'),
 (17,'auth','0011_update_proxy_permissions','2021-12-01 18:52:48.855082'),
 (18,'auth','0012_alter_user_first_name_max_length','2021-12-01 18:52:48.875077'),
 (19,'sessions','0001_initial','2021-12-01 18:52:48.895085');
INSERT INTO "DjangoLivre_account" ("number","balance","account_user_id") VALUES ('e07056c3a6a446caa6820037c74f3349',5000,'87418806094'),
 ('44cae485c1d34eff83425560f8ffbc5d',5000,'07406238002'),
 ('d2114b4822f242588a3f96c54201ba7c',5000,'09069831007'),
 ('49af258643174f33abe7327a647604dc',5000,'70765419041'),
 ('678daaa335114da884836df00be3cdc0',5000,'24719546005'),
 ('27ad0991033f421487aa61e656ab6ede',5000,'27236236020'),
 ('2924da1692f04dcc8ba8b9b863033b24',5000,'27050561061'),
 ('f2cc5e0a890b45e2b23d0c4adb167bbd',5000,'77656618090'),
 ('bb0b599f1fdb4b998610ed14119779cf',5000,'62222241057'),
 ('9a66a43c284e44b1adfb092c4a0ba97f',5000,'35693789004'),
 ('2050f6b1f4804215b2927ec341147a66',5000,'01855861046'),
 ('4cd774da0e4d4711b84c46d817682ef5',5000,'94137824070'),
 ('69c689f0c2634ceeb4d85d1b4dd893c8',5000,'70610936093'),
 ('b3ca45b108334d6b8de5477c8b006f0c',5000,'15485838049'),
 ('e4b371f95a55488da473ed46d7c7fdba',5000,'10875280030');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry'),
 (2,'auth','permission'),
 (3,'auth','group'),
 (4,'auth','user'),
 (5,'contenttypes','contenttype'),
 (6,'sessions','session'),
 (7,'DjangoLivre','client'),
 (8,'DjangoLivre','account'),
 (9,'DjangoLivre','transfer');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_user','Can add user'),
 (14,4,'change_user','Can change user'),
 (15,4,'delete_user','Can delete user'),
 (16,4,'view_user','Can view user'),
 (17,5,'add_contenttype','Can add content type'),
 (18,5,'change_contenttype','Can change content type'),
 (19,5,'delete_contenttype','Can delete content type'),
 (20,5,'view_contenttype','Can view content type'),
 (21,6,'add_session','Can add session'),
 (22,6,'change_session','Can change session'),
 (23,6,'delete_session','Can delete session'),
 (24,6,'view_session','Can view session'),
 (25,7,'add_client','Can add client'),
 (26,7,'change_client','Can change client'),
 (27,7,'delete_client','Can delete client'),
 (28,7,'view_client','Can view client'),
 (29,8,'add_account','Can add account'),
 (30,8,'change_account','Can change account'),
 (31,8,'delete_account','Can delete account'),
 (32,8,'view_account','Can view account'),
 (33,9,'add_transfer','Can add transfer'),
 (34,9,'change_transfer','Can change transfer'),
 (35,9,'delete_transfer','Can delete transfer'),
 (36,9,'view_transfer','Can view transfer');
INSERT INTO "DjangoLivre_client" ("name","cpf","phone","email","creation") VALUES ('Elias Bernardo Otávio Viana','87418806094','(51) 99605-4822','eliasviana@saa.com.br','2021-12-02 11:10:06.502033'),
 ('Sabrina Débora Pietra Pires','07406238002','(96) 99882-6593','sabrinadeborapietrapires-97@fanger.com.br','2021-12-02 11:15:05.906025'),
 ('Eduardo Danilo Rodrigues','09069831007','(75) 98285-3900','eduardodanilorodrigues-75@lojaprincezinha.com.br','2021-12-02 11:15:45.891095'),
 ('Isabelle Letícia Heloisa dos Santos','70765419041','(69) 98538-2277','iisabelleleticiaheloisadossantos@fingrs.com.br','2021-12-02 11:18:26.434637'),
 ('Ryan Rodrigo Anthony Vieira','24719546005','(61) 98945-8452','ryanrodrigoanthonyvieira_@alstom.com','2021-12-02 11:19:30.010517'),
 ('Noah Enzo Araújo','27236236020','(77) 98772-0168','noahenzoaraujo_@djapan.com.br','2021-12-02 11:20:15.213445'),
 ('Marina Andrea Aparecida Brito','27050561061','(11) 99135-8118','marinaandreaaparecidabrito__marinaandreaaparecidabrito@ovi.com','2021-12-02 11:21:22.081598'),
 ('Heitor Carlos Rafael Baptista','77656618090','(79) 98428-8666','heitorcarlosrafaelbaptista-96@51hotmail.com','2021-12-03 15:09:53.099960'),
 ('Ester Yasmin Luzia Alves','62222241057','(98) 98930-2757','esteryasminluziaalves.esteryasminluziaalves@mtic.net.br','2021-12-03 15:10:58.542697'),
 ('Rebeca Aparecida Emily Pires','35693789004','(61) 98259-2123','rebecaaparecidaemilypires_@lencise.com','2021-12-03 15:11:53.749895'),
 ('Nina Vanessa Peixoto','01855861046','(69) 99309-7383','ninavanessapeixoto-72@agencia10clic.com.br','2021-12-03 15:12:20.912254'),
 ('Francisco Marcos Vinicius da Cunha','94137824070','(82) 98184-3931','ffranciscomarcosviniciusdacunha@andrepires.com.br','2021-12-03 15:13:00.136559'),
 ('Cláudio Vitor Teixeira','70610936093','(65) 99485-9586','claudiovitorteixeira-84@hidrara.com.br','2021-12-03 15:14:13.051365'),
 ('Nina Clara da Paz','15485838049','(84) 99486-9366','ninaclaradapaz-99@vetech.vet.br','2021-12-03 15:14:50.192883'),
 ('Leonardo Cláudio Ramos','10875280030','(86) 98395-4259','leonardoclaudioramos.leonardoclaudioramos@mundivox.com.br','2021-12-03 15:15:55.354646');
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;
