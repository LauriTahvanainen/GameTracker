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
Painamalla yläpalkin `Havainnot`, käyttäjä siirtyy havaintojen valikkoon, josta voi siirtyä edelleen havaintojen lisäämiseen painamalla `Lisää havainto`, omien havaintojen tarkastelemiseen painamalla `Tarkastele omia havaintoja`, tai tarkastelemaan kaikkia havaintoja painamalla `Tarkastele kaikkia havaintoja`.

### Lisää havainto
Havainnon lisäämisnäkymässä avautuu lomake, jonka yläreunassa on nappi `Eikö havaittua eläintä löydy? Siirry tästä lisäämään uusi eläin!`. Tästä napista voi siirtyä lisäämään uusia eläimiä. 

Havaintojen lisäämislomakkeessa valitaan eläin valikosta, joka avautuu valikkoa painamalla. Havainnon aika annetaan muodossa __01-01-2019 22:22__. Havaintoon on myös mahdollista syöttää kaupunki, leveys- sekä pituusasteet, paino (kilogrammoina)
, sukupuoli, havaintotapa, havaintoväline, sekä muita tietoja. Sukupuolen vaihtoehtoja on *uros*, *naaras*, *muu*, *ei tiedossa*. Havaintotapoja on neljä: *Saalis*, *Näköhavainto*, *Kiinnotto*, *Onnettomuus*. Välineitä on lukuisia. Muita tietoja kohtaan voi syöttää 500 merkin verran sanallista tietoa havainnosta.

### Tarkastele omia havaintoja
`Tarkastele omia havaintoja`-linkkiä painamalla avautuu näkymä, jossa näkyy listana käyttäjän kaikki omat havainnot. Listan yläpuolella on kaksi nappia: `Rajaa näytettäviä havaintoja` ja `Näytä kaikki`. `Rajaa näytettäviä havaintoja`-nappia painamalla käyttäjälle avautuu lomake, jonka avulla näytettäviä omia havaintoja voi rajata. Rajauksen voi kohdistaa kaikkiin havainnnon tietokohteisiin. Rajatun haun suorittaminen tapahtuu painamalla nappia `Hae`. Kaikki omat havainnot saa taas näkymään painamalla `Näytä kaikki`.

#### Muokkaus ja poistaminen
Jos käyttäjällä on oikeus muokata havaintoa tai poistaa se, näkyy listatun havainnon oikeassa reunassa napit: `Poista` ja `Muokkaa`. Muokkausnäkymässä käyttäjälle näytetään lähes samanlainen näkymä kuin havainnon lisäämisessä, mutta lomakkeen kentät on täytetty muokattavan havainnon tiedoilla. Muokkaus vahvistetaan napista `Suorita havainnon muokkaus`.

### Tarkastele kaikkia havaintoja
`Tarkastele omia havaintoja` avaa samanlaisen näkymän kuin omien havaintojen tarkastelu, mutta lisäksi havainnoista näytetään havaitsijan käyttäjänimi. Käyttäjänimeä painamalla voi siirtyä tarkastelemaan havaitsijan tietoja, sekä kaikkia hänen havaintojaan. Näytettävien havaintojen rajaus toimii jokaisessa havaintojen-tarkastelu-näkymässä samalla tavalla.

Jos leveys ja pituusasteet on annettu, voi jommankumman numerosta painamalla avata uudelle välilehdelle Open Street Map:n havainnon koordinaateilla.

## Eläimet
Eläimet-valikko sisältää linkin `Lisää eläin`, jota painamalla voi siirtyä lisäämään uusia eläimiä, sekä linkin `Tarkastele eläimiä`, josta voi siirtyä tarkastelemaan kaikkia eläimiä.

### Lisää eläin
Uuden eläimen lisääminen tapahtuu syöttämällä lomakkeeseen eläimen suomenkielinen nimi, latinankielinen nimi, sekä url-osoite, josta eläimestä voi saada lisätietoa.

### Tarkastele eläimiä
Näkymässä näkyy kaikki eläimet listattuna.

## Käyttäjätili
Käyttäjätili-valikko sisältää linkit `Vaihda salasana`, `Vaihda käyttäjänimi`, `Tarkastele omia käyttäjätietoja` sekä `Poista käyttäjätili`,.

### Vaihda salasana
`Vaihda salasana`-näkymässä on lomake, jossa käyttäjä voi vaihtaa tilinsä salasanan syöttämällä lomakkeeseen vanhan salasanansa, sekä uuden salasanan kaksi kertaa. Vaihto tapahtuu painamalla nappia `Vaihda salasana`. Järjestelmä ilmoittaa vaihdon lopputuloksesta.

### Vaihda käyttäjänimi
`Vaihda käyttäjänimi`-näkymä on hyvin samankaltainen kuin salasananvaihtonäkymä, mutta siinä on vain yksi syötekenttä: Uusi käyttäjänimi. Vaihtaminen tapahtuu painamalla `Vaihda käyttäjänimi`.

### Tarkastele omia käyttäjätietoja
Näkymä listaa käyttäjälle hänen käyttäjätietonsa.

### Poista käyttäjätili
Käyttäjätilin poistaminen onnistuu painamalla nappia `Poista käyttäjäsi`, ja painamalla `OK` varmistus-dialogissa. Käyttäjätilin poistaminen poistaa sekä käyttäjätiedot, että käyttäjän luomat havainnot.


# Pääkäyttäjä
Pääkäyttäjällä on muutama käyttäjältä puuttuva ominaisuus. Näitä ovat: Välineiden luominen ja poistaminen, sekä kaikkien käyttäjien ja heidän tietojensa listaaminen. Linkkien: `Havainnot`, `Eläimet` ja `Käyttäjätili` lisäksi pääkäyttäjän yläpalkissa on linkit `Välineet` ja `Listaa käyttäjät`. Pääkäyttäjällä on mahdollisuus poistaa tai muokata jokaista havaintoa, poistaa käyttäjätilejä käyttäjätilien listausnäkymästä tai käyttäjän havaintojen listausnäkymästä, sekä mahdollisuus muokata ja poistaa eläimiä.

## Eläimen muokkaus ja poistaminen
Pääkäyttäjä näkee `Tarkastele eläimiä näkymässä` jokaisen eläimen vieressä napin `Muokkaa tai poista`. Tästä napista avautuu havainnonmuokkauksen tyylinen näkymä, siis eläimenlisäyslomake, mutta täytettynä muokattavan eläimen tiedoilla. Muokkaus tapahtuu painamalla `Suorita muokkaus`. Eläimen voi samassa näkymässä poistaa painamalla `Poista eläin`

## __POISTAMISESTA__
HUOM! Käyttäjän poistaminen poistaa myös kaikki käyttäjän havainnot.
HUOM! Eläimen poistaminen poistaa myös kaikki sen eläimen omaavat havainnot!

## Välineet
`Välineet` linkistä pääkäyttäjä pääsee välineiden valikkoon, josta voi siirtyä lisäämään välineen painamalla `Lisää väline`, tai tarkastelemaan ja poistamaan välineitä painamalla `Tarkastele ja poista välineitä`.

### Lisää väline
Lisää väline lomakkeeseen syötetään välinen nimi, ja painetaan `Lisää väline`, jolloin väline lisätään tietokantaan. Järjestelmä ilmoittaa lisäämisestä ja myös siitä, jos lisäys ei onnistunut, esimerkiksi koska väline oli jo järjestelmässä.

### Tarkastele ja poista välineitä
Näkymä listaa kaikki välineet vierellään checkbox-elementti. Pääkäyttäjä voi halutessaan poistaa välineitä valitsemalla poistettavat välineet rustaamalla välineiden vieressä olevan checkboxin, ja painamalla `Poista valitut`. Tällöin välineet, joiden viereinen checkbox oli rustattu, poistetaan.
