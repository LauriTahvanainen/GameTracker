# Sovelluksen rajoitteet, puuttuvat ominaisuudet sekä jatkokehitysidoita

## Rajoitteet
- Havaintojen listaaminen on tällä hetkellä rakennettu niin, että käyttäjän poiston yhteydessä on mahdotonta jättää käyttäjän havaintoja tietokantaan. Tämä olisi tarpeellinen toiminnallisuus, jotta dataa ei menetettäisi. Käyttäjä voisi esimerkiksi itse valita, poistetaanko hänen havaintonsakin, vai jätetäänkö ne muiden käyttäjien tarkasteltavaksi.
- Havaintojen sijainnin rajaaminen havaintojen tarkastelussa tapahtuu syöttämällä koordinaatit lomakkeeseen. Tämä on varsin kömpelöä, ja parempi ratkaisu olisi, jos käyttäjä voisi rajata suoraan kartasta haluamansa havainnot.
- Eläinten ja käyttäjien tarkastelussa olisi hyvä olla hakukenttä, jotta tietyn eläimen tai käyttäjän hakeminen olisi mahdollisimman nopeaa. (Filttereissä on tavallaan hakukenttä)
- Välineitä ei voi muokata, vaan vain poistaa. Jos järjestelmässä on paljon havaintoja, mahdollisesti kaikilla välineillä, niin välineen poistamisesta saattaa koitua ongelma, jos uusien välineiden lisäämistä ei tee tarkasti. Saattaa nimittäin käydä niin, että väline poistetaan, jolloin sen omaavat havainnot muuttavat väline arvon NULL-arvoksi, mutta jos lisätään huolimattomasti uusi, eri niminen, väline, niin tämä uusi väline saattaa saada saman id:n kuin aikaisemmin poistettu väline. Näin ollen havainnot joissa oli poistettu väline, saattavat saada aivan uuden, tarkoittamattoman välineen liitetyksi havaintoon.

## Puuttuvat ominaisuudet
Kokonaisuudesaan suuri osa suunniteltuista toiminnallisuuksista saatiin toteutettua.
- Eläinten ja käyttäjien listaamiseen olisi hyvä toteuttaa etsimistoiminto. Tämä helpottaisi erityisesti pääkäyttäjän toimintaa.
- Käyttäjän, eläimen ja näiden poistamisien myötä havaintojen poistamisessa ei saatu toimimaan tietokannan automaattista 'cascade'/ON DELETE poistoa, vaan poistaminen tehdään erikseen.
- Uutta havaintoa ei voi lisätä, jos järjestelmässä ei ole eläimiä tai välineitä. Käytettävyyden kannalta havainnonlisäämisnäkymään olisi hyvä lisätä nappi, josta pääsee siirtymään lisäämään eläimiä (ja havaintoja pääkäyttäjän kohdalla), jos näitä ei järjestelmässä ole.
-Välineen muokkaaminen.

## Jatkokehitysideoita
- Kartassa voisi jokaisella eläimellä olla oma merkkinsä.
- Kuvan lisääminen havaintoon.
- Kommenttien lisääminen havaintoon.
- Salasanan palauttamistoiminto.
- Visuaaliset tilastot
