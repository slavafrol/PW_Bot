create table users (
	DiscordID BIGINT,
    SteamID varchar(255),
    FirstName varchar(20),
    LastName varchar(20),
    PRIMARY KEY (DiscordID)
);

SELECT * FROM users;