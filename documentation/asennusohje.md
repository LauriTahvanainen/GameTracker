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

Aina käynnistettäessä sovellus paikallisesti, tulee juurikansiossa ensin ottaa virtuaaliympäristö käyttöön komennolla:

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
 
# Asennus Herokussa
