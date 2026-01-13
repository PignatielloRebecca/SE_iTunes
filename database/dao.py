from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def read_all_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.title,a.id, sum(t.milliseconds)/60000.0 as durata_album_minuti 
                    from album a, track t
                    where a.id=t.album_id 
                    group by a.id, a.title 
                    having sum(t.milliseconds)/60000.0>%s """

        cursor.execute(query,(durata,))

        for row in cursor:
            result.append(Album(row["id"], row["title"], row["durata_album_minuti"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_connessioni(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ WITH AlbumFiltrati AS (SELECT a.id 
                                            FROM album a, track t
                                            WHERE a.id = t.album_id
                                            GROUP BY a.id
                                            HAVING SUM(t.milliseconds)/60000.0 > %s)
                SELECT DISTINCT t1.album_id as album_a, t2.album_id as album_b
                from track t1, track t2, playlist_track pt1, playlist_track pt2 

                where t1.id=pt1.track_id and t2.id=pt2.track_id and pt1.playlist_id= pt2.playlist_id and 
		        t1.album_id< t2.album_id and t1.album_id in(select id from AlbumFiltrati) and t2.album_id in (select id from AlbumFiltrati)"""

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append([row["album_a"],row["album_b"]]) # cero una lista di liste

        cursor.close()
        conn.close()
        return result

    # --> devo verificare:
    #---> le due traccie sino presenti nella tabella playlist_track, abbiano la stessa playlist, ma due album differenti
    # i due album devono appartenere alla tabella ALBULM FILTRATI



