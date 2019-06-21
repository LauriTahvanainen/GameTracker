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
| Käyttäjä | tarkastella havaintoja erinlaisin suodattimin | tarkastella esimerkiksi yhden lajin havaintoja | X |
| Käyttäjä | päivittää omia tietojani | päivittää muuttuneita tietojani | - |
| Käyttäjä | poistaa oman tilini | irrottautua palvelusta | X |
| Pääkäyttäjä | poistaa tilejä | poistaa tilejä jotka käyttävät palvelua sääntöjenvastaisesti. | X |
| Pääkäyttäjä | poistaa havaintoja | poistaa palvelusta virheellisiä havaintoja. | X | 
| Pääkäyttäjä | lisätä uusia välineitä | mahdollistaa uusien välineiden lisäämisen havaintoihin. | X |
| Pääkäyttäjä | muokata välineitä | muokata virheellisiä välineitä | X |
| Pääkäyttäjä | poistaa välineitä | poistaa virheellisiä välineitä | X |
| Pääkäyttäjä | poistaa eläimiä | poistaa virheellisiä eläimiä| X |
| Pääkäyttäjä | muokata eläimiä | korjata virheellisiä eläimiä | X |

## SQL-Kyselyt

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
    WHERE account.account_id = ?

### Uuden havainnon lisääminen
    INSERT INTO Observation (account_id, date_created, date_modified, date_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info)
    VALUES (Current_Account_id, Current_Timestamp, Current_Timestamp, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    
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

    UPDATE observation SET date_modified=CURRENT_TIMESTAMP, weight=30 WHERE observation.observation_id = OBSERVAATION_ID
