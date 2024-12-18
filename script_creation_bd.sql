-- SQLite
-- Création des tables
CREATE TABLE joueur (
    pseudo_joueur VARCHAR(50) PRIMARY KEY,
    nom_joueur VARCHAR(50)
);

CREATE TABLE ressources (
    id_ressource INTEGER PRIMARY KEY,
    prix_matieres_prem REAL,
    prix_loyer INTEGER,
    salaire INTEGER,
    depenses_persos INTEGER,
    energie INTEGER

);

CREATE TABLE entreprise (
    id_entreprise INTEGER PRIMARY KEY,
    pseudo_joueur VARCHAR(50),
    id_ressource INTEGER,

    nom_entreprise VARCHAR(30),
    benefice_total INTEGER,
    score INTEGER,
    nombre_salaries INTEGER,
    mois_en_cours INTEGER,
    prix_plat INTEGER,
    note_totale INTEGER,

    FOREIGN KEY (pseudo_joueur) REFERENCES joueur (pseudo_joueur),
    FOREIGN KEY (id_ressource) REFERENCES joueur (id_ressource)
);

-- Différents prix de ressources en fonction des mois
INSERT INTO ressources (id_ressource, prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie)
VALUES 
    (1,   5, 2000, 2500, 1500, 200),
    (2, 5.5, 2000, 2500, 1500, 200),
    (3, 5.5, 2000, 2500, 1500, 400);

/*
réinitialiser la BD:

DELETE from entreprise;
DELETE from joueur;

*/