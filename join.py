import psycopg2
import sqlalchemy
from pprint import pprint

database = sqlalchemy.create_engine('postgresql://postgres:dnweapons1513@localhost:5432/homework_db')
connection = database.connect()


if __name__ == '__main__':
    
    #количество исполнителей в каждом жанре;
    
    connection.execute("""SELECT name, COUNT(name)
                        FROM genre g
                        JOIN executor_genre ex ON g.id = ex.genre_id
                        GROUP BY g.id;""").fetchall()

    #количество треков, вошедших в альбомы 2019-2020 годов;
    
    connection.execute("""SELECT COUNT(t.id) album_date 
                        FROM album a
                        JOIN track t ON a.id = t.id
                        WHERE a.album_date >= 2019 and a.album_date < 2020;""").fetchall()
    
    #средняя продолжительность треков по каждому альбому;
    
    connection.execute("""SELECT round(AVG(duratation)), a.name 
                        FROM track t
                        JOIN album a ON t.id = a.id
                        GROUP BY a.name;""").fetchall()
    
    #все исполнители, которые не выпустили альбомы в 2020 году;
    
    connection.execute("""SELECT e.name, a.album_date FROM executor e
                        JOIN executor_album ea ON e.id = ea.executor_id
                        JOIN album a ON ea.album_id = a.id
                        WHERE a.album_date != 2020;""").fetchall()
    
    #названия сборников, в которых присутствует конкретный исполнитель Chester;
    

    connection.execute("""SELECT c.name FROM collection c
                        JOIN track_collection tk ON c.id = tk.track_id
                        JOIN track t ON tk.track_id = t.id
                        JOIN album a ON t.album_id = a.id
                        JOIN executor_album ea ON a.id = ea.album_id
                        JOIN executor e ON ea.executor_id = e.id
                        WHERE e.name LIKE 'Chester';""").fetchall()

    #название альбомов, в которых присутствуют исполнители более 1 жанра;
    
    connection.execute("""SELECT a.name FROM album a
                       JOIN executor_album ea ON a.id = ea.album_id
                       JOIN executor e ON ea.executor_id = e.id
                       JOIN executor_genre eg ON e.id = eg.executor_id
                       JOIN genre g ON eg.genre_id = g.id
                       GROUP BY e.name, a.name
                       HAVING count(eg.genre_id) != 1;""").fetchall()
    
    #наименование треков, которые не входят в сборники;
    
    connection.execute("""SELECT t.name FROM track t
                        LEFT JOIN track_collection tc ON t.id = tc.track_id
                        WHERE tc.track_id IS NULL;""").fetchall()
    


    #исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
    
    connection.execute("""SELECT e.name, t.duratation from executor e
                        JOIN executor_album ea ON e.id = ea.executor_id
                        JOIN album a ON ea.album_id = a.id
                        JOIN track t ON a.id = t.album_id
                        WHERE t.duratation = (
                        SELECT MIN(duratation) FROM track);""").fetchall()
    
    #название альбомов, содержащих наименьшее количество треков.
    
    connection.execute("""SELECT a.name, COUNT(t.name) from album a
                        JOIN track t ON a.id = t.album_id
                        GROUP BY a.name
                        HAVING COUNT(t.name) = (
                        SELECT MIN(COUNT) FROM (
                        SELECT a.name, COUNT(t.name) from album a
                        JOIN track t ON a.id = t.album_id
                        GROUP BY a.name) AS test)""").fetchall() 
   