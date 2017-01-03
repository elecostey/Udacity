-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS scores;
DROP VIEW IF EXISTS player_wins;
DROP VIEW IF EXISTS player_matches;


CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name text
);


CREATE TABLE scores (
    match_id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players(player_id),
    loser INTEGER REFERENCES players(player_id)
);


CREATE VIEW player_wins AS
    SELECT players.player_id AS player, count(scores.winner) as wins
    FROM players LEFT JOIN scores
    ON players.player_id = scores.winner
    GROUP BY players.player_id, scores.winner
    ORDER BY players.player_id;


CREATE VIEW player_matches AS
    SELECT players.player_id AS player, count(scores.match_id) as matches
    FROM players LEFT JOIN scores
    ON players.player_id = scores.winner
    OR players.player_id = scores.loser
    GROUP BY players.player_id
    ORDER BY players.player_id ASC;


CREATE VIEW standings AS
    SELECT players.player_id, players.name, player_wins.wins as wins, player_matches.matches as matches
    FROM players, player_wins, player_matches
    WHERE players.player_id = player_wins.player and player_wins.player = player_matches.player;