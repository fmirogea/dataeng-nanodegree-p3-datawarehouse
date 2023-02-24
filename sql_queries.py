import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events(
    artist VARCHAR(256),
    auth VARCHAR(25),
    firstName VARCHAR(256),
    gender VARCHAR(25),
    itemInSession INTEGER,
    lastName VARCHAR(256),
    length NUMERIC(9,4),
    level VARCHAR(10),
    location VARCHAR(256),
    method VARCHAR(10),
    page VARCHAR(16),
    registration NUMERIC(14,1),
    sessionId INTEGER,
    song VARCHAR(256),
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR(256),
    userId int
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    num_songs INTEGER primary key,
    artist_id VARCHAR(25),
    artist_latitude NUMERIC(9,6),
    artist_longitude NUMERIC(9,6),
    artist_location VARCHAR(256),
    artist_name VARCHAR(256),
    song_id VARCHAR(25),
    title VARCHAR(256),
    duration NUMERIC(10,6),
    year INT
);

""")

songplay_table_create = ("""
CREATE TABLE songplays(
    sp_songlay_id INT IDENTITY(0,1) PRIMARY KEY,
    sp_start_time TIMESTAMP not null, 
    sp_user_id INTEGER not null, 
    sp_level VARCHAR(10) not null, 
    sp_song_id VARCHAR(256) not null, 
    sp_artist_id VARCHAR(256) not null, 
    sp_session_id INTEGER not null, 
    sp_location VARCHAR(256) not null, 
    sp_user_agent VARCHAR(256) not null
)
DISTSTYLE KEY
DISTKEY ( sp_start_time )
SORTKEY ( sp_start_time );

""")

user_table_create = ("""
CREATE TABLE users(
    u_user_id INTEGER PRIMARY KEY,
    u_first_name VARCHAR(25) not null,
    u_last_name VARCHAR(25) not null,
    u_gender VARCHAR(1) not null,
    u_level VARCHAR(10) not null
)
DISTSTYLE ALL
SORTKEY ( u_user_id );

""")

song_table_create = ("""
CREATE TABLE songs(
    s_song_id VARCHAR(25) primary key,
    s_title VARCHAR(256) not null,
    s_artist_id VARCHAR(25) not null,
    s_year INTEGER,
    s_duration NUMERIC(10,6) not null
)
DISTSTYLE ALL
SORTKEY ( s_song_id );
""")

artist_table_create = ("""
CREATE TABLE artists(
    a_artist_id VARCHAR(25) primary key,
    a_name VARCHAR(256) not null,
    a_location VARCHAR(256),
    a_latitude NUMERIC(9,6),
    a_longitude NUMERIC(9,6)
)
DISTSTYLE ALL
SORTKEY ( a_artist_id );
""")

time_table_create = ("""
CREATE TABLE times(
    t_start_time TIMESTAMP primary key,
    t_hour INTEGER not null,
    t_day INTEGER not null,
    t_week INTEGER not null,
    t_month INTEGER not null,
    t_year INTEGER not null,
    t_weekday varchar(25) not null
)
DISTSTYLE KEY
DISTKEY ( t_start_time )
SORTKEY ( t_start_time );
""")



# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from 's3://udacity-dend/log_data' 
    credentials {}
    format as json {}
    region 'us-west-2';
""").format(config["IAM_ROLE"]["ARN"], config["S3"]["log_jsonpath"])

staging_songs_copy = ("""
    copy staging_songs from 's3://udacity-dend/song_data' 
    credentials {} 
    format as json 'auto'
    region 'us-west-2';
""").format(config["IAM_ROLE"]["ARN"])


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (sp_start_time, sp_user_id, sp_level, sp_song_id, sp_artist_id, sp_session_id, sp_location, sp_user_agent)
SELECT
    TIMESTAMP 'epoch' + (e.ts/1000) * interval '1 second' AS sp_start_time, 
    e.userId AS sp_user_id, 
    e.level AS sp_level, 
    s.song_id AS sp_song_id, 
    s.artist_id AS sp_artist_id, 
    e.sessionId AS sp_session_id, 
    e.location AS sp_location, 
    e.userAgent AS sp_user_agent
FROM staging_songs AS s
INNER JOIN staging_events AS e
ON s.artist_name = e.artist
AND s.title = e.song
WHERE page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (u_user_id, u_first_name, u_last_name, u_gender, u_level)
SELECT DISTINCT
    userId AS u_user_id,
    firstName AS u_first_name,
    lastName AS u_last_name,
    gender AS u_gender,
    level AS u_level
FROM staging_events
WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (s_song_id, s_title, s_artist_id, s_year, s_duration)
SELECT DISTINCT
    song_id AS s_song_id,
    title AS s_title,
    artist_id AS s_artist_id,
    year AS s_year,
    duration AS s_duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists (a_artist_id, a_name, a_location, a_latitude, a_longitude)
SELECT DISTINCT
    artist_id AS a_artist_id,
    artist_name AS a_name,
    artist_location AS a_location,
    artist_latitude AS a_latitude,
    artist_longitude AS a_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO times (t_start_time, t_hour, t_day, t_week, t_month, t_year, t_weekday)
SELECT DISTINCT
    TIMESTAMP 'epoch' + (ts/1000) * interval '1 second' AS t_start_time,
    EXTRACT(HOUR FROM t_start_time) AS t_hour,
    EXTRACT(DAY FROM t_start_time) AS t_day,
    EXTRACT(WEEK FROM t_start_time) AS t_week,
    EXTRACT(MONTH FROM t_start_time) AS t_month,
    EXTRACT(YEAR FROM t_start_time) AS t_year,
    EXTRACT(WEEKDAY FROM t_start_time) AS t_weekday
FROM staging_events
WHERE ts IS NOT NULL
    
""")

# QUERY LISTS

# Original
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

# Testing
#drop_table_queries = [songplay_table_drop]
#create_table_queries = [songplay_table_create]
#insert_table_queries = [songplay_table_insert]
