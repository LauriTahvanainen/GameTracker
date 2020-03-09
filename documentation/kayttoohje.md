# Käyttäjä
## Rekisteröityminen
Rekisteröitymiseen siirrytään etusivun oikeasta yläreunasta painamalla `Luo uusi käyttäjä`. Avautuneeseen lomakkeeseen syötetään käyttäjänimi, salasana kaksi kertaa, nimi, kaupunki, sekä syntymävuosi. Kaikki paitsi kaupunki ovat pakollisia tietoja. Luominen tapahtuu painamalla `Luo käyttäjä` nappia. Järjestelmä ilmoittaa onnistuneesta rekisteröitymisestä.

## Kirjautuminen
Kirjautumiseen siirrytään etusivun oikeasta yläreunasta painamalla `Kirjaudu`. Avautuneeseen lomakkeeseen syötetään käyttäjänimi, sekä salasana, ja painetaan `Kirjaudu sisään`-nappia. Jos kirjautuminen onnistuu, ilmoittaa järjestelmä tästä käyttäjälle, ja käyttäjälle avautuu uudenlainen kotisivu. Kirjautumisen epäonnistumisesta ilmoitetaan myös käyttäjälle.

## Uloskirjautuminen
Uloskirjautuminen tapahtuu painamalla oikeassa yläreunassa sijaitsevaa `Kirjaudu ulos`-nappia.

## Toiminnot
Kirjautunut käyttäjä näkee yläpalkissa neljä uutta linkkiä: `Havainnot`, `Eläimet`, `Käyttäjätili` ja `Tilastoja`. Näitä painamalla voi siirtyä kunkin ominaisuuden valikkoon, mistä voi siirtyä yksittäisiin näitä aihealueita koskeviin toimintoihin. `Tilastoja`-näkymässä ei ole alivalikkoa. Puhelimella, tai jos näyttö on liian pieni, toimintonapit piilotetaan valikkonapin taakse.

## Havainnot
Painamalla yläpalkin `Havainnot`, käyttäjä siirtyy havaintojen valikkoon, josta voi siirtyä edelleen havaintojen lisäämiseen painamalla `Lisää havainto`, omien havaintojen tarkastelemiseen painamalla `Tarkastele omia havaintoja`, tai tarkastelemaan kaikkia havaintoja painamalla `Tarkastele kaikkia havaintoja`.

### Lisää havainto
Havainnon lisäämisnäkymässä avautuu lomake, jonka yläreunassa on nappi `Eikö havaittua eläintä löydy? Siirry tästä lisäämään uusi eläin!`. Tästä napista voi siirtyä lisäämään uusia eläimiä. 

Havaintojen lisäämislomakkeessa valitaan eläin valikosta, joka avautuu valikkoa painamalla. Havainnon päivämäärä valitaan kalenterista, sekä aika ajanvalintakentistä. Kartalta voi valita koordinaatit, jossa havainto tapahtui. Koordinaatit voi syöttää myös käsin. Kunta valitaan kuntavalintaruudusta avautuvasta listasta. Paino syötetään kilogrammoina.
Muita annettavia tietoja ovat sukupuoli, havaintotapa, havaintoväline, sekä muita tietoja. Sukupuolen vaihtoehtoja on *uros*, *naaras*, *muu*, *ei tiedossa*. Havaintotapoja on neljä: *Saalis*, *Näköhavainto*, *Kiinnotto*, *Onnettomuus*. Välineitä on lukuisia. Muita tietoja kohtaan voi syöttää 500 merkin verran sanallista tietoa havainnosta.

### Tarkastele omia havaintoja
`Tarkastele omia havaintoja`-linkkiä painamalla avautuu näkymä, jossa näkyy sivutettuna listana käyttäjän kaikki omat havainnot. Listan yläpuolella on sivunavigaatio, sekä kaksi nappia: `Rajaa näytettäviä havaintoja` ja `Näytä kaikki`. `Rajaa näytettäviä havaintoja`-nappia painamalla käyttäjälle avautuu lomake, jonka avulla näytettäviä omia havaintoja voi rajata. Rajauksen voi kohdistaa kaikkiin havainnnon tietokohteisiin. Rajatun haun suorittaminen tapahtuu painamalla nappia `Hae`. Kaikki omat havainnot saa taas näkymään painamalla `Näytä kaikki`.

#### Muokkaus ja poistaminen
Jos käyttäjällä on oikeus muokata havaintoa tai poistaa se, näkyy listatun havainnon oikeassa reunassa napit: `Poista` ja `Muokkaa`. Muokkausnäkymässä käyttäjälle näytetään lähes samanlainen näkymä kuin havainnon lisäämisessä, mutta lomakkeen kentät on täytetty muokattavan havainnon tiedoilla. Muokkaus vahvistetaan napista `Suorita havainnon muokkaus`.

### Tarkastele kaikkia havaintoja
`Tarkastele omia havaintoja` avaa samanlaisen näkymän kuin omien havaintojen tarkastelu, mutta lisäksi havainnoista näytetään havaitsijan käyttäjänimi. Käyttäjänimeä painamalla voi siirtyä tarkastelemaan havaitsijan tietoja, sekä kaikkia hänen havaintojaan. Näytettävien havaintojen rajaus toimii jokaisessa havaintojen-tarkastelu-näkymässä samalla tavalla.

Leveys- tai pituusasteen numerosta painamalla voi avata uudelle välilehdelle Open Street Map:n havainnon koordinaateilla. Samaan tapaan, jos eläimelle on syötetty lisätietoja-linkki, niin eläimen nimen kohdalla on linkki, jota painamalla voi avata lisätietosivun uudelle välilehdelle.

## Eläimet
Eläimet-valikko sisältää linkin `Ehdota eläintä`, jota painamalla voi siirtyä ehdottamaan uusia eläimiä, `Tarkastele ehdotettuja eläimiä`, jota painamalla voi siirtyä tarkastelemaan ehdotettuja eläimiä, sekä äänestämään ehdotuksista, sekä linkin `Tarkastele eläimiä`, josta voi siirtyä tarkastelemaan järjestelmässä jo olevia eläimiä.

### Ehdota eläintä
Uuden eläimen ehdottaminen tapahtuu syöttämällä lomakkeeseen eläimen suomenkielinen nimi, latinankielinen nimi, sekä url-osoite, josta eläimestä voi saada lisätietoa.

### Tarkastele ehdotettuja eläimiä
Näkymässä näkyy sivutettuna kaikki ehdotetut eläimet. Jokaisen ehdotuksen kohdalla on vihreä nuoli ylös päin ja punainen nuoli alas päin. Vihreästä käyttäjä voi antaa ehdotukselle yhden äänen ehdotuksen lisäämiseksi, kun taas punaisesta äänen ehdotuksen poistamiseksi.

### Tarkastele eläimiä
Näkymässä näkyy kaikki järjestelmään hyväksytyt tai lisätyt eläimet sivutettuna listana.

###

## Käyttäjätili
Käyttäjätili-valikko sisältää linkit `Vaihda salasana`, `Vaihda käyttäjänimi`, `Tarkastele ja muokkaa omia käyttäjätietoja` sekä `Poista käyttäjätili`,.

### Vaihda salasana
`Vaihda salasana`-näkymässä on lomake, jossa käyttäjä voi vaihtaa tilinsä salasanan syöttämällä lomakkeeseen vanhan salasanansa, sekä uuden salasanan kaksi kertaa. Vaihto tapahtuu painamalla nappia `Vaihda salasana`. Järjestelmä ilmoittaa vaihdon lopputuloksesta.

### Vaihda käyttäjänimi
`Vaihda käyttäjänimi`-näkymä on hyvin samankaltainen kuin salasananvaihtonäkymä, mutta siinä on vain yksi syötekenttä: Uusi käyttäjänimi. Vaihtaminen tapahtuu painamalla `Vaihda käyttäjänimi`.

### Tarkastele omia käyttäjätietoja
Näkymä listaa käyttäjälle hänen käyttäjätietonsa. Näkymässä on myös nappi `Muokkaa käyttäjätietoja`, josta pääsee siirtymään käyttäjätietojenmuokkaus-lomakkeeseen. Muokkauslomake toimii samaan tapaan kuin esimerkiksi havainnonmuokkaus-lomake.

### Poista käyttäjätili
Käyttäjätilin poistaminen onnistuu painamalla nappia `Poista käyttäjäsi`, ja painamalla `OK` varmistus-dialogissa. Käyttäjätilin poistaminen poistaa sekä käyttäjätiedot, että käyttäjän luomat havainnot.

## Tilastoja
Tilastoja näkymässä käyttäjälle näytetään erilaisia tilastoja järjestelmästä. Tilastoja ovat:

- 10 eniten havaintoja tehnyttä käyttäjää järjestyksessä havaintomäärän mukaan.
- 10 eniten havaittua eläintä järjestyksessä havaintomäärän mukaan.
- 10 vähiten havaittua eläintä järjestyksessä havaintomäärän mukaan.
- 10 eniten metsästettyä eläintä havaintomäärän mukaan. Tämä tilastotaulu näyttää vain eläimet joilla on vähintään yksi saalis-tyypin havainto.
- 10 eniten käytettyä välinettä
- 10 vähiten käytettyä välinettä 

Lisäksi __pääkäyttäjä__ näkee tilastoissa ylimääräisen id rivin jokaisessa taulussa, sekä ylimääräisen tilaston kymmenestä vanhimmasta käyttäjästä, joilla ei ole lainkaan havaintoja. Näitä vanhimpia käyttäjiä tietenkin näkyy vain jos järjestelmässä on käyttäjiä ilman havaintoja. 

# Pääkäyttäjä
Pääkäyttäjällä on muutama käyttäjältä puuttuva ominaisuus. Näitä ovat: Välineiden luominen ja poistaminen, sekä kaikkien käyttäjien ja heidän tietojensa listaaminen. Linkkien: `Havainnot`, `Eläimet` ja `Käyttäjätili` lisäksi pääkäyttäjän yläpalkissa on linkit `Välineet` ja `Listaa käyttäjät`. Pääkäyttäjällä on mahdollisuus poistaa tai muokata jokaista havaintoa, poistaa käyttäjätilejä käyttäjätilien listausnäkymästä, sekä mahdollisuus lisätä suoraan, muokata ja poistaa eläimiä, sekä hyväksyä suoraan ja poistaa eläinehdotuksia. Pääkäyttäjä voi myös muokata kaikkien tilien käyttäjätietoja, mutta tällä hetkellä vain osoitekentän kautta.

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
