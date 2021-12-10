create_schema = ('''

    CREATE SCHEMA IF NOT EXISTS petl2
    '''
)

create_tables = ('''

    DROP TABLE IF EXISTS petl2.movie_list;

    CREATE TABLE IF NOT EXISTS petl2.movie_list (
        title TEXT NOT NULL,
        rated TEXT ,
        released date,
        runtime int,
        genre TEXT[],
        director TEXT,
        writer text[],
        actors text[],
        plot TEXT,
        awards TEXT,
        poster TEXT
    );
''')


insert_movie = ('''  
  INSERT INTO petl2.movie_list (Title, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Awards, Poster)
  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
''')

