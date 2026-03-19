# Awave_Metadata-Server

Der Awave-MetadataServer stellt den Datenbankbestandteil des Awave-Streamingsystems dar.

## Funktionsbereich

Dieser übernimmt konkret folgende Aufgaben:

- Content-Katalog
	
	Der Server liefert alles was der Nutzer sieht, bevor er auf "Play" drückt.
	
	- Strukturierung: Stellt dem Client konkrete Informationen zu unterschiedlichen Medien zur Verfügung
	- Discovery: Liefert Daten für die Suche, Filterung nach Genres, Tags oder anderen Indikatoren
	- Assets-Verwaltung: Speichert zwar keine Images selbst, liefert aber die URLs zu Postern und Thumbnails
	
- Personalisierung & User-State
	
	Der Server dokumentiert Personalisierungen und Nutzerverhalten mit
	
	- Fortschrittsbalken: Speichert für jeden Account sekundengenau, wo ein Video pausiert wurde.
	- Playlists: Verwaltet Playlists, die automatisch durch gewählte Tags entstehen und Favoriten der Nutzer
	- Profile & Settings: Server weiß, z.B. welche Sprache der Nutzer bevorzugt (Audio/Subtitle)

- Streaming-Logistik
	
	Der Server vermittelt zwischen dem Client und dem eigentlichen Video-File auf dem Streaming-Server
	
	- Pfad-Auflösung: Beim Streamstart eines Clients wird der Server dazu aufgerufen auf dem Streaming-Server die entsprechende URL weiterzugeben
	- Berechtigung: Überprüft, ob der Nutzer überhaupt angemeldet ist und diesen Inhalt sehen darf, bevor die URL weitergegeben wird
	
	
- Automatisierung
	
	Dies betrifft vor allem die Kommunikation zur Admin-Schnittstelle
	
	- Halbauto-Matching: Durch die Admin-Schnittstelle wird bei Festellung neuer Medien auf dem Streaming-Server neue Meta-Data durch diesen auf die DB gespeichert
	- Backend-Logik: Auf Befehl der Admin-Schnittstelle werden einträge nach CRUD bearbeitet und verwaltet
	
## ERM-Struktur der Datenbank

<img src= "erm.png" alt="ERM konnte nicht geladen werden" width="1000">

### Alle Entitäten mit ihren jeweiligen Attributen unterteilen sich in drei Kategorien:

- Account-Relevant (Lila)
	
	Entitäten, die pro Account personalisiert diesem zugeordnet und von dem jeweiligen Nutzer verwaltet werden
	
	- Account: Identifikation eines Nutzers
		- account_id
		- username
		- email
		- hashed_pw
		- profilpicture_url
		- date_of_birth
		- created_at
		- is_active
		
	- Settings: Account-speziefische Endgerät-übergreifende Einstellungen
		- settings_id
		- auto_select_language
		- audio_language
		- subtitle_language
		- seen_media_progress_value	(Beschreibt in % ab wann ein Video als "Gesehen" markiert wird)
		
	- Playlist: Vom Nutzer selbst erstellte Playlist, die manuell hinzugefügte Media oder durch verschiedene Tags autogeneriert ist
		- playlist_id
		- title
		- is_dynamic (Beschreibt, ob Nutzer manuell diese mit Medien füllt oder durch Tags autogeneriert wird)
		- filter_tag_id
		- filter_language_id
		- filter_actor_id
		- filter_publisher_id
	
- Grundstruktur der Medien (Gelb)

	Entitäten, die zueinander die Relation darstellen, in der Medien auf dem Streamingsystem abgebildet sind
	
	- Media: Ursprungs-Entität für sämtliche Äußerungen von Mediendateien
		- media_id
		- title
		- title_alternative
		- description
		- release_date
		- duration_in_sec
		- age_rating
		- upload_date
		- media_url
		- thumbnail_url
		- timestamp_intro_start
		- timestamp_intro_end
		- timestamp_outro_start
		- timestamp_outro_end
		
	- Movie: Erweiterte Media in Form eines Films
		- movie_id
		
	- Season: Staffel, die Folgen enthält
		- season_id
		- season_number
		- cover_url
		- release_date

	- Episode: Erweiterte Media in Form einer Folge einer Serie
		- episode_id
		- episode_number
	
	- Series: Serie, die Staffeln enthält
		- series_id
		- title
		- title_alternative
		- cover_url
		- release_date
		
	- Category: Übergreifende thematische Unterteilung von Medienwerken
		- category_id
		- title
		- icon_type
		
	- Collection: Gruppierung thematisch gleich passender Medienwerke unterhalb einer Kategorie
		- collection_id
		- title
		- cover_url
		
### Weitere Attribute die durch die jeweilige Relation der Entitäten entstehen

| Nr. | Entität 1 | Beziehungs-Typ | Entität 2 | Beschreibung |
| :---: | :---: | :---: | :---: | :--- |
| 1 | Media | (is a) | Episode | Eine Episode ist eine Media
| 2 | Media | (is a) | Movie | Ein Movie ist eine Media
| 3 | Publisher | 1/M:N | Movie | Ein Publisher kann mehrere Movie produzieren. Ein Movie hat mindestens einen Publisher
| 4 | Movie | M:N | Actor | Movie können viele Actor haben. Actor können an vielen Movie beteiligt sein
| 5 | Movie | M:N | Tag | Movie können viele Tag haben. Tag können mehreren Movie zugeordnet sein
| 6 | Category | 1:N | Movie | Eine Category kann mehrere Movie haben. Ein Movie ist explizit einer Category zugeordnet
| 7 | Collection | 1/0:1/N | Movie | Eine Collection hat mindestens ein Movie. Ein Movie ist eventuell Explizit einer Collection zugeordnet
| 8 | Season | 1:1/N | Episode | Eine Season hat mindestens eine Episode. Eine Episode ist explizit einer Season zugeordnet
| 9 | Series | 1:1/N | Season | Eine Series hat mindestens eine Season. Eine Season ist explizit einer Series zugeordnet
| 10 | Publisher | 1/M:N | Series | Ein Publisher kann mehrere Series produzieren. Eine Series hat mindestens einen Publisher
| 11 | Series | M:N | Actor | Series können viele Actor haben. Actor können an vielen Series beteiligt sein
| 12 | Series | M:N | Tag | Series können viele Tag haben. Tag können mehreren Series zugeordnet sein
| 13 | Series | M:N | Language | Series können viele Language haben. Language können mehreren Series zugeordnet sein
| 14 | Media | M:N | Language | Media können viele Language haben. Language können mehreren Media zugeordnet sein
| 15 | Category | 1:N | Series | Eine Category beinhalten mehrere Series. Eine Series ist explizit einer Category zugeordnet
| 16 | Category | 1:N | Collection | Eine Category beinhalten mehrere Collection. Eine Collection ist explizit einer Category zugeordnet
| 17 | Media | M:N | Playlist | Eine Media kann mehrere Playlist zugeordnet sein. Eine Playlist kann mehrere Medien haben
| 18 | Account | 1:N | Playlist | Jeder Account kann viele Playlist beinhalten. Eine Playlist ist explizit einem Account zugeordnet
| 19 | Account | 1:1 | Settings | Jeder Account hat exakt eine Settings und anders herum
| 20 | Account | M:N | Media | Ein Account kann mehrere Media gesehen haben. Ein Media kann von mehrere Account gesehen worden sein
| 21 | Account | M:N | Category | Ein Account hat Zugriff auf mehrere Category. Eine Category kann für mehrere Accounts freigeschaltet worden sein
