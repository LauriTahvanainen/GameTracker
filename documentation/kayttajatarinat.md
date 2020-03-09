# Käyttäjätarinat

| Kun olen... | haluan... | jotta voin.. | Toteutettu |
| :-----------: | :---------: | :----------: | :----------: |
| Käyttäjä | rekisteröityä palveluun ja kirjautua käyttäjätililleni | käyttää palvelua, havaintojen tekemiseen ja toisten havaintojen tarkastelemiseen. | X |
| Käyttäjä | vaihtaa salasanani | parantaa tilini turvallisuutta. | X |
| Käyttäjä | luoda uuden havainnon | seurata eläinhavaintojani. | X |
| Käyttäjä | poistaa havaintojani | korjata virheellisen havainnon, jos en jaksa muokata vanhaa havaintoa. | X |
| Käyttäjä | muokata havaintojani | korjata virheellisiä havaintojani. | X |
| Käyttäjä | lisätä uusia eläimiä | lisätä havaintoja joissa on löytämättömiä/harvinaisia/tietokannassa olemattomia eläimiä. | X |
| Käyttäjä | tarkastella havaintojani | nähdä kokonaiskuvan omista havainnoistani | X |
| Käyttäjä | tarkastella muiden havaintoja | nähdä kokonaiskuvan kaikista havainnoista | X |
| Käyttäjä | tarkastella havaintoja erilaisin suodattimin | tarkastella esimerkiksi yhden lajin havaintoja | X |
| Käyttäjä | päivittää omia tietojani | päivittää muuttuneita tietojani | X |
| Käyttäjä | poistaa oman tilini | irrottautua palvelusta | X |
| Käyttäjä | nähdä tilastoja havainnoista | saada nopeasti dataa havaintomäärien mittasuhteista | X |
| Pääkäyttäjä | poistaa tilejä | poistaa tilejä jotka käyttävät palvelua sääntöjenvastaisesti. | X |
| Pääkäyttäjä | poistaa havaintoja | poistaa palvelusta virheellisiä havaintoja. | X | 
| Pääkäyttäjä | lisätä uusia välineitä | mahdollistaa uusien välineiden lisäämisen havaintoihin. | X |
| Pääkäyttäjä | poistaa välineitä | poistaa virheellisiä välineitä | X |
| Pääkäyttäjä | poistaa eläimiä | poistaa virheellisiä eläimiä| X |
| Pääkäyttäjä | muokata eläimiä | korjata virheellisiä eläimiä | X |
| Pääkäyttäjä | tilastoja sovelluksen käytöstä | näen miten käyttäjät käyttävät sovellusta | X |
| KESKEN |
| Pääkäyttäjä | muokata välineitä | muokata virheellisiä välineitä | - |
| Käyttäjä | rajata näytettäviä havaintoja kartalta | tarkastella tietyn alueen havaintoja helposti | - |
| Käyttäjä | saada havaintooni automaattisesti havaintopaikan sään havaintoajalla | syöttää havaintoja helpommin | - |


## SQL-Kyselyt
Joitain yksinkertaisia ja muiden kyselyiden kanssa samanlaisia kyselyitä, kuten yksinkertaisia INSERT, UPDATE ja DELETE kyselyitä, ei käydä tässä läpi.

### Rekisteröityminen
    INSERT INTO Account VALUES (username, name, password, city, age) VALUES (?, ?, ?, ?, ?)

### Kirjautuminen
Kirjautuessa haetaan käyttäjä-olio tietyllä käyttäjänimellä.


    SELECT account.account_id AS account_account_id, 
    account.username AS account_username, 
    account.name AS account_name,
    account.password AS account_password,
    account.city AS account_city,
    account.age AS account_age,
    account.urole AS account_urole
    FROM account
    WHERE account.name = SYÖTETTY_KÄYTTÄJÄNIMI

FlaskLogin suorittaa samaa kyselyä, mutta account_id:llä.
SQLalchemy suorittaa kaikkien taulujen yhteydessä saman tyyppisen haun kuin yllä, kun kutsutaan _TaulunNimi.query.get(Taulu.id)_
### Uuden havainnon lisääminen
    INSERT INTO Observation (account_id, date_created, date_modified, date_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info)
    VALUES (Current_Account_id, Current_Timestamp, Current_Timestamp, havainto_aika, kaupunki, leveysaste, pituusaste, eläin_id, paino, sukupuoli, hvaintotyyppi, väline_id, lisätietoja)
    
Muiden tietokohteiden lisääminen tapahtuu samaan tapaan.
    
### Havaintojen tarkasteleminen ja rajaaminen
Havaintojen listaukseen ja rajaukseen käytetään samaa kyselyä, rajatessa kyselyyn vain lisätään filttereitä. Flask-muokkaa myös kyselyä sivutuksen takia. Tässä esitetään kysely ilman sivutuksen aiheuttamia muutoksia
    
Tarkastelu

    SELECT observation.observation_id AS observation_observation_id,
    observation.account_id AS observation_account_id,
    observation.date_created AS observation_date_created,
    observation.date_modified AS observation_date_modified,
    observation.date_observed AS observation_date_observed,
    observation.city AS observation_city,
    observation.latitude AS observation_latitude,
    observation.longitude AS observation_longitude,
    observation.animal_id AS observation_animal_id, 
    observation.weight AS observation_weight, 
    observation.sex AS observation_sex,
    observation.observ_type AS observation_observ_type, 
    observation.equipment_id AS observation_equipment_id, 
    observation.info AS observation_info,
    animal.animal_id AS animal_animal_id,
    animal.name AS animal_name, 
    animal.lat_name AS animal_lat_name,
    animal.info AS animal_info,
    equipment.name AS equipment_name,
    account.account_id AS account_account_id, 
    account.username AS account_username,
    account.name AS account_name,
    account.password AS account_password,
    account.city AS account_city,
    account.age AS account_age,
    account.urole AS account_urole 
    FROM observation
    LEFT OUTER JOIN animal ON animal.animal_id = observation.animal_id
    LEFT OUTER JOIN equipment ON equipment.equipment_id = observation.equipment_id
    LEFT OUTER JOIN account ON account.account_id = observation.account_id 
    GROUP BY observation.observation_id, animal.animal_id, equipment.equipment_id, account.account_id
    ORDER BY observation.date_observed DESC
    
Rajaus lisää samaan kyselyyn vain filttereitä ohjelmallisesti sen mukaan onko filtterilomakkeen kentässä syötettä. Esimerkiksi rajaus jossa rajataan kaupungin (Helsinki, Espoo), käyttäjän (test) ja havaintotyypin (Saalis=0) mukaan:

    SELECT observation.observation_id AS observation_observation_id,
    observation.account_id AS observation_account_id,
    observation.date_created AS observation_date_created,
    observation.date_modified AS observation_date_modified,
    observation.date_observed AS observation_date_observed,
    observation.city AS observation_city,
    observation.latitude AS observation_latitude,
    observation.longitude AS observation_longitude,
    observation.animal_id AS observation_animal_id, 
    observation.weight AS observation_weight, 
    observation.sex AS observation_sex,
    observation.observ_type AS observation_observ_type, 
    observation.equipment_id AS observation_equipment_id, 
    observation.info AS observation_info,
    animal.animal_id AS animal_animal_id,
    animal.name AS animal_name, 
    animal.lat_name AS animal_lat_name,
    animal.info AS animal_info,
    equipment.name AS equipment_name,
    account.account_id AS account_account_id, 
    account.username AS account_username,
    account.name AS account_name,
    account.password AS account_password,
    account.city AS account_city,
    account.age AS account_age,
    account.urole AS account_urole 
    FROM observation
    LEFT OUTER JOIN animal ON animal.animal_id = observation.animal_id
    LEFT OUTER JOIN equipment ON equipment.equipment_id = observation.equipment_id
    LEFT OUTER JOIN account ON account.account_id = observation.account_id
    WHERE account.username = test AND observation.city IN (Helsinki, Espoo) AND observation.observ_type IN (0)
    GROUP BY observation.observation_id, animal.animal_id, equipment.equipment_id, account.account_id
    ORDER BY observation.date_observed DESC
    
### Havainnon muokkaaminen
Muokkaus tapahtuu hyvin yksinkertaisella kyselyllä. Esimerkkinä havainnon painon päivittäminen. Päivittäessä date_modified päivittyy automaattisesti.

    UPDATE observation SET date_modified=CURRENT_TIMESTAMP, weight=30 WHERE observation.observation_id = OBSERVATION_ID
    
### Käyttäjätietojen päivittäminen
Tämäkin päivityskysely on varsin yksinkertainen. Muut päivityskyselyt ovat yhtä yksinkertaisia.

    UPDATE account SET date_modified=CURRENT_TIMESTAMP, name='testi', city='testi', age=1983 WHERE account.account_id = current_user.account_id
    

### Käyttäjätilin poistaminen

    DELETE FROM account WHERE account_id = current_user.account_id
    
Samaan tapaan id:n mukaan tapahtuu myös kaikki muu poistaminen, paitsi välineiden poistaminen, joka tehdään ryhmäpoistona nimen mukaan.

### Välineiden poistaminen
Esimerkkinä kolmen välineen poistaminen

    DELETE FROM equipment WHERE equipment.name IN (Kiikarit, test, Kirves)


### Tilastot
Tilastot sivulla käyttäjälle ja pääkäyttäjälle näytetään erilaisia tilastoja. Monet näistä hauista ovat hyvin samanlaisia, kuten eniten ja vähiten käytettyjen välineiden hakeminen, eikä kaikkia siten käydä läpi.

#### Eniten havaintoja tehneet 10 käyttäjää

    SELECT Account.account_id, Account.username, COUNT(Observation.observation_id) AS count FROM Observation
    LEFT JOIN Account ON Observation.account_id = Account.account_id
    GROUP BY Account.account_id
    ORDER BY count DESC
    LIMIT 10
    
#### 10 nolla havaintoa tehnyttä käyttäjää, tilin luomispäivän mukaan järjestettynä

    SELECT Account.account_id, Account.username, Account.date_created FROM Account
    LEFT JOIN Observation ON Observation.account_id = Account.account_id
    GROUP BY Account.account_id
    HAVING COUNT(Observation.observation_id) = 0
    ORDER BY Account.date_created ASC
    LIMIT 10
    
#### 10 eniten havaittua eläintä ja eläimen keskimääräinen paino havainnoissa

    SELECT Animal.animal_id, Animal.name, Animal.lat_name, Animal.info, COUNT(Observation.observation_id) as count,     
    AVG(Observation.weight) as avg FROM Animal
    LEFT JOIN Observation ON (Animal.animal_id = Observation.animal_id)
    GROUP BY Animal.animal_id
    ORDER BY count DESC, Animal.name
    LIMIT 10
    
#### 10 metsästetyintä eläintä (Ei löydä eläimiä, joihin ei liity yhtään havaintoa tyyppiä saalis)    
    
    SELECT Animal.animal_id, Animal.name, Animal.lat_name, Animal.info, COUNT(Observation.observation_id) as count, 
    AVG(Observation.weight) as avg FROM Animal"
    LEFT JOIN Observation ON (Animal.animal_id = Observation.animal_id)
    WHERE Observation.observ_type = 0
    GROUP BY Animal.animal_id
    ORDER BY count DESC, Animal.name
    LIMIT 10
    
#### 10 eniten käytettyä välinettä

    SELECT Equipment.equipment_id, Equipment.name, COUNT(Observation.observation_id) as count FROM Equipment
    LEFT JOIN Observation ON (Equiment.equipment_id = Observation.equipment_id)
    GROUP BY Equipment.equipment_id
    ORDER BY count DESC, Equipment.name
    LIMIT 10"
