# Asennus Paikallisesti (Terminaalissa, python3 asennettuna)
1. Siirry kansioon johon haluat asentaa sovelluksen ja kloonaa repositorio komennolla:

    `git clone https://github.com/LauriTahvanainen/GameTracker.git`

2. Kloonamisen jälkeen, siirry sovelluksen kansioon komennolla:
    
    `cd GameTracker`
    
3. Luo kansioon pythonin virtuaaliympäristö komennolla:

    `python3 -m venv venv`
    
4. Aktivoi luotu ympäristö komennolla:

    `source venv/bin/activate`
    
5. Asenna ympäristön vaatimat riippuvuudet pip:llä, komennolla:

    `pip install -r requirements.txt`
    
## Ensimmäinen käynnistys
Asennettuna tulee olla python3 ja sqlite3.

0. Aina käynnistettäessä sovellus paikallisesti, tulee juurikansiossa ensin ottaa virtuaaliympäristö käyttöön komennolla:

   `source venv/bin/activate`
   
   
1. Käynnistä sovellus komennolla:

    `python3 run.py`
    
    * Ensimmäisen käynnistyksen yhteydessä luodaan tietokantataulut. 
  
2. Sammuta sovellus painamalla näppäinyhdistelmää:
  
     `CTRL+C`
     
3. Avaa tietokanta sqlite:llä komennolla: 

    `sqlite3 application/observations.db`
    
  * Lisää ylläpitäjän tunnus tietokantaan syöttämällä sqlite:lle komento:
  
  `INSERT INTO Account (account_id, username, name, password, city, age, urole) VALUES ('1', 'admin', 'admin', 'pbkdf2:sha256:150000$HjvHR88r$1932e4bbb0eb9ada9dfce1d627d085a35b2a416e97bd5265c8fa07919ac83fe1', 'admin', '2000', 'ADMIN');`

   * Admin-tunnuksen käyttäjänimi on: _admin_ ja salasana on: _admin123_      MUISTA VAIHTAA ADMIN-SALASANA!

   * Lisäämisen jälkeen poistu sqlite:stä komennolla: `.exit`
 
 4. Käynnistä sovellus uudelleen komennolla: 
    
    `python3 run.py`
    
 5. Avaa selaimella osoite:
 
    [127.0.0.1:5000](http://127.0.0.1:5000/)
    
__Jatkossa käynnistäminen tapahtuu toistamalla juurikansiossa kohdat 0 ja 1.__
 
# Asennus Herokuun
__Asentaminen tapahtuu paikallisen asennuksen tapaan terminaalissa, sovelluksen juurikansiossa. Vaatimuksena on: Heroku CLI ja python3 asennettuna, sekä Heroku-käyttäjä, jolle on kirjauduttu laitteella.__

0. Suorita paikallinen asennus yllä olevien ohjeiden mukaan.

1. Luo Herokuun uusi sovellus komennolla:
    
    `heroku create SOVELLUKSEN_NIMI`
    
    * _Huom! Nimen pitää olla uniikki herokussa, joten luomista saattaa joutua yrittämään muutaman kerran._

2. Lisää versionhallintaan tieto Herokusta komennolla:

    `git remote add heroku https://git.heroku.com/SOVELLUKSEN_NIMI.git`
    
3. Lähetä projekti Herokuun komennoilla:

    `git add .`
    `git commit -m "COMMIT_VIESTI"`
    `git push heroku master`
    
4. Määritetään sovellus käyttämään PostgreSql-tietokannanhallintajärjestelmää ja lisätään tietokanta komennoilla:

    `heroku config:set HEROKU=1`
    `heroku addons:add heroku-postgresql:hobby-dev`
    
5. Lisätään lopuksi Herokun tietokantaan pääkäyttäjän tunnukset:
    * Avataan yhteys tietokantaan komennolla:
    
    `heroku pg:psql`
    
    * Lisätään pääkäyttäjän tunnuksen komennolla:
    
    `INSERT INTO Account (account_id, username, name, password, city, age, urole) VALUES ('1', 'admin', 'admin', 'pbkdf2:sha256:150000$HjvHR88r$1932e4bbb0eb9ada9dfce1d627d085a35b2a416e97bd5265c8fa07919ac83fe1', 'admin', '2000', 'ADMIN');`
    
    * Suljetaan yhteys komennolla:
    
    `\q`

## Käynnistäminen

Heroku-sovelluksen voi avata siirtymällä selaimella osoitteeseen:

[GameTracker](https://gmtrackr.herokuapp.com/)

tai, jos olet luonut oman sovelluksen Herokuun, on osoite muotoa:

`https://SOVELLUKSEN_NIMI.herokuapp.com/`
