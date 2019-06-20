# Käyttäjä
## Rekisteröityminen
Rekisteröitymiseen siirrytään etusivun oikeasta yläreunasta painamalla `Luo uusi käyttäjä`. Avautuneeseen lomakkeeseen syötetään käyttäjänimi, salasana kaksi kertaa, nimi, kaupunki, sekä syntymävuosi. Kaikki paitsi kaupunki ovat pakollisia tietoja. Luominen tapahtuu painamalla `Luo käyttäjä` nappia. Järjestelmä ilmoittaa onnistuneesta rekisteröitymisestä.

## Kirjautuminen
Kirjautumiseen siirrytään etusivun oikeasta yläreunasta painamalla `Kirjaudu`. Avautuneeseen lomakkeeseen syötetään käyttäjänimi, sekä salasana, ja painetaan `Kirjaudu sisään`-nappia. Jos kirjautuminen onnistuu, ilmoittaa järjestelmä tästä käyttäjälle, ja käyttäjälle avautuu uudenlainen kotisivu. Kirjautumisen epäonnistumisesta ilmoitetaan myös käyttäjälle.

## Uloskirjautuminen
Uloskirjautuminen tapahtuu painamalla oikeassa yläreunassa sijaitsevaa `Kirjaudu ulos`-nappia.

## Toiminnot
Kirjautunut käyttäjä näkee yläpalkissa kolme uutta linkkiä: `Havainnot`, `Eläimet` ja `Käyttäjätili`. Näitä painamalla voi siirtyä kunkin ominaisuuden valikkoon, mistä voi siirtyä yksittäisiin näitä aihealueita koskeviin toimintoihin.

## Havainnot
Painamalla yläpalkin `Havainnot`, käyttäjä siirtyy havaintojen valikkoon, josta voi siirtyä edelleen havaintojen lisäämiseen painamalla `Lisää havainto`, tai omien havaintojen tarkastelemiseen painamalla `Näytä omat havainnot`.

### Lisää havainto
Havainnon lisäämisnäkymässä avautuu lomake, jonka yläreunassa on nappi `Eikö havaittua eläintä löydy? Siirry tästä lisäämään uusi eläin!`. Tästä napista voi siirtyä lisäämään uusia eläimiä. 

Havaintojen lisäämislomakkeessa valitaan eläin valikosta, joka avautuu valikkoa painamalla. Havainnon aika annetaan muodossa __01-01-2019 22:22__. Havaintoon on myös mahdollista syöttää kaupunki, leveys- sekä pituusasteet, paino (kilogrammoina)
, sukupuoli, havaintotapa, havaintoväline, sekä muita tietoja. Sukupuolen vaihtoehtoja on *uros*, *naaras*, *muu*, *ei tiedossa*. Havaintotapoja on neljä: *Saalis*, *Näköhavainto*, *Kiinnotto*, *Onnettomuus*. Välineitä on lukuisia. Muita tietoja kohtaan voi syöttää 500 merkin verran sanallista tietoa havainnosta.

### Näytä omat havainnot
`Näytä omat havainnot`-linkkiä painamalla avautuu näkymä, jossa näkyy listana käyttäjän kaikki omat havainnot. Listan yläpuolella on kaksi nappia: `Rajaa näytettäviä havaintoja` ja `Näytä kaikki`. `Rajaa näytettäviä havaintoja`-nappia painamalla käyttäjälle avautuu lomake, jonka avulla näytettäviä omia havaintoja voi rajata. Rajauksen voi kohdistaa kaikkiin havainnnon tietokohteisiin. Rajatun haun suorittaminen tapahtuu painamalla nappia `Hae`. Kaikki omat havainnot saa taas näkymään painamalla `Näytä kaikki`

## Eläimet
Eläimet-valikko sisältää linkin `Lisää eläin`, jota painamalla voi siirtyä lisäämään uusia eläimiä.

### Lisää eläin
Uuden eläimen lisääminen tapahtuu syöttämällä lomakkeeseen eläimen suomenkielinen nimi, latinankielinen nimi, sekä url-osoite, josta eläimestä voi saada lisätietoa.

## Käyttäjätili
Käyttäjätili-valikko sisältää linkit `Vaihda salasana`, `Poista käyttäjätili`, sekä `Tarkastele omia käyttäjätietoja`.

### Vaihda salasana
`Vaihda salasana` näkymässä on lomake, jossa käyttäjä voi vaihtaa tilinsä salasanan syöttämällä lomakkeeseen vanhan salasanansa, sekä uuden salasanan kaksi kertaa. Vaihto tapahtuu painamalla nappia `Vaihda salasana`. Järjestelmä ilmoittaa vaihdon lopputuloksesta.

### Poista käyttäjätili
Käyttäjätilin poistaminen onnistuu painamalla nappia `Poista käyttäjäsi`, ja painamalla `OK` varmistus-dialogissa. Käyttäjätilin poistaminen poistaa sekä käyttäjätiedot, että käyttäjän luomat havainnot.

### Tarkastele omia käyttäjätietoja
Näkymä listaa käyttäjälle hänen käyttäjätietonsa.

# Pääkäyttäjä
Pääkäyttäjällä on muutama käyttäjältä puuttuva ominaisuus. Näitä ovat: Välineiden luominen ja poistaminen, sekä kaikkien käyttäjien ja heidän tietojensa listaaminen. Linkkien: `Havainnot`, `Eläimet` ja `Käyttäjätili` lisäksi pääkäyttäjän yläpalkissa on linkit `Välineet` ja `Listaa käyttäjät`. 

## Välineet
`Välineet` linkistä pääkäyttäjä pääsee välineiden valikkoon, josta voi siirtyä lisäämään välineen painamalla `Lisää väline`, tai tarkastelemaan ja poistamaan välineitä painamalla `Tarkastele ja poista välineitä`.

### Lisää väline
Lisää väline lomakkeeseen syötetään välinen nimi, ja painetaan `Lisää väline`, jolloin väline lisätään tietokantaan. Järjestelmä ilmoittaa lisäämisestä ja myös siitä, jos lisäys ei onnistunut, esimerkiksi koska väline oli jo järjestelmässä.

### Tarkastele ja poista välineitä
Näkymä listaa kaikki välineet vierellään checkbox-elementti. Pääkäyttäjä voi halutessaan poistaa välineitä valitsemalla poistettavat välineet rustaamalla välineiden vieressä olevan checkboxin, ja painamalla `Poista valitut`. Tällöin välineet, joiden viereinen checkbox oli rustattu, poistetaan.
