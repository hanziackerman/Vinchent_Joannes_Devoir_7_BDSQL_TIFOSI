-- Création de la base de données
DROP DATABASE IF EXISTS tifosi;
CREATE DATABASE tifosi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tifosi;

-- Création de l'utilisateur avec les droits
CREATE USER IF NOT EXISTS 'tifosi'@'localhost' IDENTIFIED BY 'TifosiPass2024!';
GRANT ALL PRIVILEGES ON tifosi.* TO 'tifosi'@'localhost';
FLUSH PRIVILEGES;

-- Création des tables
CREATE TABLE marque (
    id_marque INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE boisson (
    id_boisson INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    id_marque INT NOT NULL,
    FOREIGN KEY (id_marque) REFERENCES marque(id_marque)
) ENGINE=InnoDB;

CREATE TABLE ingredient (
    id_ingredient INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE focaccia (
    id_focaccia INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    prix DECIMAL(5,2) NOT NULL CHECK (prix > 0)
) ENGINE=InnoDB;

CREATE TABLE menu (
    id_menu INT PRIMARY KEY AUTO_INCREMENT,
    prix DECIMAL(5,2) NOT NULL CHECK (prix > 0)
) ENGINE=InnoDB;

CREATE TABLE client (
    id_client INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    code_postal VARCHAR(5) NOT NULL
) ENGINE=InnoDB;

-- Tables de relations
CREATE TABLE comprend (
    id_focaccia INT,
    id_ingredient INT,
    quantite INT NOT NULL CHECK (quantite > 0),
    PRIMARY KEY (id_focaccia, id_ingredient),
    FOREIGN KEY (id_focaccia) REFERENCES focaccia(id_focaccia),
    FOREIGN KEY (id_ingredient) REFERENCES ingredient(id_ingredient)
) ENGINE=InnoDB;

CREATE TABLE est_constitue (
    id_menu INT,
    id_focaccia INT,
    PRIMARY KEY (id_menu, id_focaccia),
    FOREIGN KEY (id_menu) REFERENCES menu(id_menu),
    FOREIGN KEY (id_focaccia) REFERENCES focaccia(id_focaccia)
) ENGINE=InnoDB;

CREATE TABLE contient (
    id_menu INT,
    id_boisson INT,
    PRIMARY KEY (id_menu, id_boisson),
    FOREIGN KEY (id_menu) REFERENCES menu(id_menu),
    FOREIGN KEY (id_boisson) REFERENCES boisson(id_boisson)
) ENGINE=InnoDB;

CREATE TABLE achete (
    id_client INT,
    id_menu INT,
    date_achat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_client, id_menu, date_achat),
    FOREIGN KEY (id_client) REFERENCES client(id_client),
    FOREIGN KEY (id_menu) REFERENCES menu(id_menu)
) ENGINE=InnoDB; 