# Tietokantarakenne
## Tietokantakaavio
![](https://github.com/LauriTahvanainen/GameTracker/blob/master/documentation/pictures/tietokantarakenne.png)

## Create table-lauseet
##### Account
    CREATE TABLE account (
	    date_created DATETIME, 
	    date_modified DATETIME, 
	    account_id INTEGER NOT NULL, 
	    username VARCHAR(16) NOT NULL, 
	    name VARCHAR(144), 
	    password VARCHAR NOT NULL, 
	    city VARCHAR(144), 
	    age INTEGER, 
	    urole VARCHAR(10), 
	    PRIMARY KEY (account_id), 
	    UNIQUE (username)
    )

    CREATE INDEX ix_account_date_created ON account (date_created)

#### Equipment
    CREATE TABLE equipment (
	  equipment_id INTEGER NOT NULL, 
	  name VARCHAR(44) NOT NULL, 
	  PRIMARY KEY (equipment_id), 
	  UNIQUE (name)
    )

#### Animal
    CREATE TABLE animal (
	    date_created DATETIME, 
	    date_modified DATETIME, 
	    animal_id INTEGER NOT NULL, 
	    name VARCHAR(144) NOT NULL, 
	    lat_name VARCHAR(144), 
	    info VARCHAR, 
	    PRIMARY KEY (animal_id), 
	    UNIQUE (name), 
	    UNIQUE (lat_name)
    )

    CREATE INDEX ix_animal_date_created ON animal (date_created)

#### Observation
    CREATE TABLE observation (
	    date_created DATETIME, 
	    date_modified DATETIME, 
	    observation_id INTEGER NOT NULL, 
	    account_id INTEGER NOT NULL, 
	    date_observed DATETIME NOT NULL, 
	    city VARCHAR(144) NOT NULL, 
	    latitude NUMERIC, 
    	longitude NUMERIC, 
	    animal_id INTEGER NOT NULL, 
	    weight NUMERIC, 
	    sex INTEGER, 
	    observ_type INTEGER, 
	    equipment_id INTEGER, 
	    info VARCHAR(500), 
	    PRIMARY KEY (observation_id), 
	    FOREIGN KEY(account_id) REFERENCES account (account_id), 
	    FOREIGN KEY(animal_id) REFERENCES animal (animal_id), 
	    FOREIGN KEY(equipment_id) REFERENCES equipment (equipment_id) ON DELETE SET NULL
    )


    CREATE INDEX ix_observation_animal_id ON observation (animal_id)
    CREATE INDEX ix_observation_account_id ON observation (account_id)
    CREATE INDEX ix_observation_info ON observation (info)
    CREATE INDEX ix_observation_date_observed ON observation (date_observed)
    CREATE INDEX ix_observation_observ_type ON observation (observ_type)
    CREATE INDEX ix_observation_date_created ON observation (date_created)
    CREATE INDEX ix_observation_equipment_id ON observation (equipment_id)
    CREATE INDEX ix_observation_city ON observation (city)
    CREATE INDEX "obsAndAnimal" ON observation (observ_type, animal_id)
    CREATE INDEX "obsAndDate" ON observation (observ_type, date_observed)
    CREATE INDEX "equipAndAnimal" ON observation (equipment_id, animal_id)
    CREATE INDEX "cityAndAnimal" ON observation (city, animal_id)

## Normalisointi
Kaikki tietokannan taulut ovat ensimmäisessä normaalimuodossa. Taulut _Equipment_ ja _Observation_ ovat myös kolmannessa normaalimuodossa. Taulut _Animal_ ja _Account_ eivät kuitenkaan ole. Taulun _Account_ kohdalla tämä ei aiheuta ongelmia, ja rakenne on toimiva, sillä se ei varsinaisesti lisää toisteisuutta. Itseasiassa, jos ajattelee, että account_id:n lisää käyttäjänimen perään, muodostavat _account_id_ ja _username_ yhdessä pääavaimen, vaikka näin ei virallisesti olekaan. Erillistä pääavainta taulussa tarvitaan kuitenkin viiteavaimen käyttöön _Observation taulussa_.

_Animal_-taulun uniikit sarakkeet aiheuttavat sen, että taulu ei ole edes toisessa normaalimuodossa. Tämä rakenne on kuitenkin sovellusta varten erittäin hyvä, eikä se varsinaisesti lisää toisteisuutta. Jos _Animal_- ja _Account_-taulut normalisoisi, olisi rakenne selvästi monimutkaisempi, eikä se toisi varsinaista lisäarvoa sovellukseen.

## Indeksointi
Sarakkeet joilla on uniikki-rajoite, tai jotka toimivat pääavaimina, tietokannanhallintajärjestelmä indeksoi automaattisesti. Tietokannassa on pyritty indeksoimaan viiteavaimet, rajauksen kohteet, sekä järjestämisen kohteet. Tästä poikkeuksena on __Observation__-taulun sarakkeet _latitude_, _longitude_, _weight_, sekä _sex_. Nämä ovat sarakkeita joiden tieto saatetaan usein jättää havainnosta aluksi tyhjäksi, myöhempää muokkausta varten (esim. ei tunnisteta heti onko kyseessä uros vai naaras). Sarakkeita ei siis indeksoida, sillä niihin tulee liittymään todennäköisesti paljon muokkauksia. __Observation__-tauluun on lisätty myös muutama monisarakkeinen indeksi yleisimpiä rajauksia varten. Näitä ovat esimerkiksi havaintotapa & havaintoaika, sekä kaupunki & eläimen id.
