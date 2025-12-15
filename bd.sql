create database sante_mentale;
use sante_mentale;

create table utilisateur(
id_utilisateur int auto_increment primary key,
prenom varchar(50),
nom varchar(50),
adresse_mail varchar(100),
mdp text
);

create table tracking(
id int auto_increment primary key,
date_mood date,
hydratation int,
activite int,
sommeil int,
id_utilisateur int,
humeur varchar(10),
foreign key(id_utilisateur) references utilisateur(id_utilisateur)
);


create table resolutions(
id int auto_increment primary key,
intitule varchar(255),
checked boolean default null,
date_fixee date,
id_utilisateur int,
foreign key(id_utilisateur) references utilisateur(id_utilisateur)
);


