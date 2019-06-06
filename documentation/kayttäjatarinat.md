# Käyttäjätarinat

| Kun olen... | haluan... | jotta voin.. | Toteutettu |
| :-----------: | :---------: | :----------: | :----------: |
| Käyttäjä | rekisteröityä palveluun ja kirjautua käyttäjätililleni | käyttää palvelua, havaintojen tekemiseen ja toisten havaintojen tarkastelemiseen. | X |
| Käyttäjä | vaihtaa salasanani | parantaa tilini turvallisuutta. | X |
| Käyttäjä | luoda uuden havainnon | seurata eläinhavaintojani. | X |
| Käyttäjä | poistaa havaintojani | korjata virheellisen havainnon, jos en jaksa muokata vanhaa havaintoa. | - |
| Käyttäjä | muokata havaintojani | korjata virheellisiä havaintojani. | - |
| Käyttäjä | lisätä uusia eläimiä | lisätä havaintoja joissa on löytämättömiä/harvinaisia/tietokannassa olemattomia eläimiä. | X |
| Käyttäjä | päivittää eläimiä | korjata virheellisiä eläimiä | - |
| Käyttäjä | tarkastella havaintojani | nähdä kokonaiskuvan omista havainnoistani | X |
| Käyttäjä | tarkastella muiden havaintoja | nähdä kokonaiskuvan kaikista havainnoista | - |
| Käyttäjä | tarkastella havaintoja erinlaisin suodattimin | tarkastella esimerkiksi yhden lajin havaintoja | - |
| Käyttäjä | päivittää omia tietojani | päivittää muuttuneita tietojani | - |
| Käyttäjä | poistaa oman tilini | irrottautua palvelusta | X |
| Pääkäyttäjä | poistaa tilejä | poistaa tilejä jotka käyttävät palvelua sääntöjenvastaisesti. | - |
| Pääkäyttäjä | poistaa havaintoja | poistaa palvelusta virheellisiä havaintoja. | - | 
| Pääkäyttäjä | lisätä uusia välineitä | mahdollistaa uusien välineiden lisäämisen havaintoihin. | - |
| Pääkäyttäjä | muokata välineitä | muokata virheellisiä välineitä | - |
| Pääkäyttäjä | poistaa välineitä | poistaa virheellisiä välineitä | - |
| Pääkäyttäjä | poistaa eläimiä | poistaa virheellisiä eläimiä| - |

## SQL-Kyselyt

### Rekisteröityminen
    INSERT INTO Account VALUES (username, name, password, city, age) VALUES (?, ?, ?, ?, ?)

### Kirjautuminen
Kirjautuessa haetaan käyttäjä-olio tietyllä käyttäjänimellä.


    SELECT account.account_id AS account_account_id, account.username
    AS account_username, account.name
    AS account_name, account.password
    AS account_password, account.city 
    AS account_city, account.age
    AS account_age FROM account
    WHERE account.account_id = ?

### Uuden havainnon lisääminen
    INSERT INTO Observation (account_id, date_created, date_modified, date_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info)
    VALUES (Current_Account_id, Current_Timestamp, Current_Timestamp, ?, ?, ?, ?, ?, ?, ?, ?, ?)
