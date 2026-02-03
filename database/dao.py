from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod

    def read_all_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, sum(t.milliseconds)/60000 as durata 
                from album a , track t 
                where a.id=t.album_id 
                group by a.id, a.title
                having sum(t.milliseconds)/60000>%s """

        cursor.execute(query,(durata,))

        for row in cursor:
            result.append(Album(row['id'], row['title'], row['durata']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_connessioni(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ with AlbumFiltrati as (
                    select a.id, a.title, sum(t.milliseconds)/60000 as durata 
                    from album a, track t
                    where a.id = t.album_id
                    group by a.id, a.title
                    having sum(t.milliseconds)/60000 > %s)
                    select distinct t1.album_id as album1, t2.album_id as album2
                    from track t1, track t2,  playlist_track pt1, playlist_track pt2
                    where  t1.id = pt1.track_id
                    and t2.id = pt2.track_id      
  and t1.album_id < t2.album_id 
  and pt1.playlist_id = pt2.playlist_id   
  and t1.album_id in (select id from AlbumFiltrati)
  and t2.album_id in (select id from AlbumFiltrati) """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append((row['album1'], row['album2']))
        cursor.close()
        conn.close()
        return result



    # --> devo verificare:
    #---> le due traccie sino presenti nella tabella playlist_track, abbiano la stessa playlist, ma due album differenti
    # i due album devono appartenere alla tabella ALBULM FILTRATI


"""
select  a1.album_id, a2.album_id 
from (select distinct t.id, t.album_id, pt.playlist_id  
			from track t, playlist_track pt 
			where t.id= pt.track_id and t.album_id in (select a.id  
            from album a, track t
            where a.id = t.album_id
            group by a.id 
            having sum(t.milliseconds)/60000 > 120)) a1, 
       (select distinct t.id, t.album_id, pt.playlist_id 
			from track t, playlist_track pt 
			where t.id= pt.track_id and t.album_id in (select a.id  
            from album a, track t
            where a.id = t.album_id
            group by a.id 
            having sum(t.milliseconds)/60000 > 120)) a2 
where a1.playlist_id = a2.playlist_id and a1.album_id< a2.album_id
group by a1.album_id, a2.album_id 
    	 
       




"""





