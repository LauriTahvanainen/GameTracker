# Sovelluksen rajoitteet, puuttuvat ominaisuudet sekä jatkokehitysidoita

## Rajoitteet
- Havaintojen listaaminen on tällä hetkellä rakennettu niin, että käyttäjän poiston yhteydessä on mahdotonta jättää käyttäjän havaintoja tietokantaan. Tämä olisi tarpeellinen toiminnallisuus, jotta dataa ei menetettäisi. Käyttäjä voisi esimerkiksi itse valita, poistetaanko hänen havaintonsakin, vai jätetäänkö ne muiden käyttäjien tarkasteltavaksi.
- Havaintojen lisääminen on hieman rajoittunut käytettävyyden ja saavutettavuuden kannalta. Päivämäärän ja koordinaattien lisääminen käsin on ymmärrettävästi käyttäjälle paljon raskaampaa kuin, jos hän voisi käyttää päivämäärän- ja ajanvalitsinta, sekä karttaa.


## Puuttuvat ominaisuudet
Kokonaisuudesaan suuri osa suunniteltuista toiminnallisuuksista saatiin toteutettua.
- Päivämäärän- ja ajanvalitsin
- Eläinten ja käyttäjien listaamiseen olisi hyvä toteuttaa etsimistoiminto. Tämä helpottaisi erityisesti pääkäyttäjän toimintaa.
- Käyttäjän, eläimen ja näiden poistamisien myötä havaintojen poistamisessa ei saatu toimimaan tietokannan automaattista 'cascade'/ON DELETE poistoa, vaan poistaminen tehdään erikseen.

## Jatkokehitysideoita
- Havainnollistamisen kannalta sovellukseen olisi erittäin hyvä upottaa kartta. Kartan avulla havaintojen tarkastelusta saataisiin visuualisempaa, ja karttaa voitaisiin myös käyttää havainnon lisäämisessä. Käytettävyyden kannalta havainnon koordinaattien lisääminen kartalta on paljon mielekkäämpää, kuin syöttää suoraan havainnon koordinaatit numeerisessa muodossa.
- Kartassa voisi jokaisella eläimellä olla oma merkkinsä.
- Kuvan lisääminen havaintoon.
- Kommenttien lisääminen havaintoon.
- Salasanan palauttamistoiminto.
