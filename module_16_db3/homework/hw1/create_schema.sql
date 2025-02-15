CREATE TABLE IF NOT EXISTS director (
    dir_id INTEGER PRIMARY KEY,
    dir_first_name VARCHAR(50),
    dir_last_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS movie (
    mov_id INTEGER PRIMARY KEY,
    mov_title VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS actor (
    act_id INTEGER PRIMARY KEY,
    act_first_name VARCHAR(50),
    act_last_name VARCHAR(50),
    act_gender VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS movie_direction (
    dir_id INTEGER,
    mov_id INTEGER,
    FOREIGN KEY (dir_id) REFERENCES director(dir_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS oscar_awarded (
    award_id INTEGER PRIMARY KEY,
    mov_id INTEGER,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS movie_cast (
    act_id INTEGER,
    mov_id INTEGER,
    role VARCHAR(50),
    FOREIGN KEY (act_id) REFERENCES actor(act_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);
