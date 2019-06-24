# Tietokantarakenne
## Tietokantakaavio
![](https://github.com/LauriTahvanainen/GameTracker/blob/master/documentation/pictures/tietokantarakenne.png)
## Normalisointi
Kaikki tietokannan taulut ovat ensimmäisessä normaalimuodossa. Taulut _Equipment_ ja _Observation_ ovat myös kolmannessa normaalimuodossa. Taulut _Animal_ ja _Account_ eivät kuitenkaan ole. Taulun _Account_ kohdalla tämä ei aiheuta ongelmia, ja rakenne on toimiva, sillä se ei varsinaisesti lisää toisteisuutta. Itseasiassa, jos ajattelee, että account_id:n lisää käyttäjänimen perään, muodostavat _account_id_ ja _username_ yhdessä pääavaimen, vaikka näin ei virallisesti olekaan. Erillistä pääavainta taulussa tarvitaan kuitenkin viiteavaimen käyttöön _Observation taulussa_.

Animal taulun uniikin sarakkeet aiheuttavat sen, että taulu ei ole edes toisessa normaalimuodossa. Tämä rakenne on kuitenkin sovellusta varten erittäin hyvä, eikä se varsinaisesti lisää toisteisuutta. Jos _Animal_ ja _Account_ taulut normalisoisi, olisi rakenne selvästi monimutkaisempi, eikä se toisi varsinaista lisätehokkuutta sovellukseen.
