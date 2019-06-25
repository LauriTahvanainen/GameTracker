# Tietokantarakenne
## Tietokantakaavio
![](https://github.com/LauriTahvanainen/GameTracker/blob/master/documentation/pictures/tietokantarakenne.png)
## Normalisointi
Kaikki tietokannan taulut ovat ensimmäisessä normaalimuodossa. Taulut _Equipment_ ja _Observation_ ovat myös kolmannessa normaalimuodossa. Taulut _Animal_ ja _Account_ eivät kuitenkaan ole. Taulun _Account_ kohdalla tämä ei aiheuta ongelmia, ja rakenne on toimiva, sillä se ei varsinaisesti lisää toisteisuutta. Itseasiassa, jos ajattelee, että account_id:n lisää käyttäjänimen perään, muodostavat _account_id_ ja _username_ yhdessä pääavaimen, vaikka näin ei virallisesti olekaan. Erillistä pääavainta taulussa tarvitaan kuitenkin viiteavaimen käyttöön _Observation taulussa_.

_Animal_-taulun uniikit sarakkeet aiheuttavat sen, että taulu ei ole edes toisessa normaalimuodossa. Tämä rakenne on kuitenkin sovellusta varten erittäin hyvä, eikä se varsinaisesti lisää toisteisuutta. Jos _Animal_- ja _Account_-taulut normalisoisi, olisi rakenne selvästi monimutkaisempi, eikä se toisi varsinaista lisäarvoa sovellukseen.

## Indeksointi
Sarakkeet joilla on uniikki-rajoite, tai jotka toimivat pääavaimina, tietokannanhallintajärjestelmä indeksoi automaattisesti. Tietokannassa on pyritty indeksoimaan viiteavaimet, rajauksen kohteet, sekä järjestämisen kohteet. Tästä poikkeuksena on __Observation__-taulun sarakkeet _latitude_, _longitude_, _weight_, sekä _sex_. Nämä ovat sarakkeita joiden tieto saatetaan usein jättää havainnosta aluksi tyhjäksi, myöhempää muokkausta varten (esim. ei tunnisteta heti onko kyseessä uros vai naaras). Sarakkeita ei siis indeksoida, sillä niihin tulee liittymään todennäköisesti paljon muokkauksia. __Observation__-tauluun on lisätty myös muutama monisarakkeinen indeksi yleisimpiä rajauksia varten. Näitä ovat esimerkiksi havaintotapa & havaintoaika, sekä kaupunki & eläimen id.
