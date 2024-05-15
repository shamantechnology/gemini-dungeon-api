CREATE TABLE `player_account` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `email` varchar(255),
  `name` varchar(255),
  `signon_method` varchar(255),
  `credits` integer DEFAULT 0,
  `active` bool DEFAULT false,
  `suspended` bool DEFAULT false,
  `login_at` timestamp DEFAULT (now()),
  `created_at` timestamp
);

CREATE TABLE `player_sessions` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `session_id` text,
  `created_at` timestamp
);

CREATE TABLE `player` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `stats_id` integer,
  `first_name` varchar(512),
  `last_name` varchar(512),
  `char_class` varchar(100),
  `race` varchar(40),
  `gender` varchar(8) DEFAULT 'Female',
  `alignment` varchar(2),
  `level` integer DEFAULT 1,
  `hit_points` integer DEFAULT 5,
  `strength` integer DEFAULT 5,
  `dexterity` integer DEFAULT 5,
  `constitution` integer DEFAULT 5,
  `intelligence` integer DEFAULT 5,
  `wisdom` integer DEFAULT 5,
  `charisma` integer DEFAULT 5,
  `age` integer DEFAULT 18,
  `background` text,
  `description` text,
  `created_at` timestamp,
  `updated_at` timestamp DEFAULT (now())
);

CREATE TABLE `player_stats` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `proficiency_mod` integer DEFAULT 2,
  `exp` integer DEFAULT 0,
  `str_mod` integer,
  `str_score` integer,
  `dex_mod` integer,
  `dex_score` integer,
  `con_mod` integer,
  `con_score` integer,
  `int_mod` integer,
  `int_score` integer,
  `wis_mod` integer,
  `wis_score` integer,
  `cha_mod` integer,
  `cha_score` integer,
  `armor_class` integer,
  `initiative` integer,
  `death_saves_success` integer DEFAULT 0,
  `death_saves_failed` integer DEFAULT 0,
  `hit_dice` varchar(255),
  `speed` varchar(255),
  `personality_traits` text,
  `ideals` text,
  `bonds` text,
  `flaws` text,
  `languages` text
);

CREATE TABLE `player_features_traits` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `name` varchar(255),
  `description` text
);

CREATE TABLE `player_items` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `item_id` integer,
  `amount` integer
);

CREATE TABLE `player_weapons` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `item_id` integer,
  `proficient` bool DEFAULT false,
  `attack_bonus` integer DEFAULT 0
);

CREATE TABLE `player_bank` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `player_id` integer,
  `cp` integer DEFAULT 0,
  `sp` integer DEFAULT 0,
  `ep` integer DEFAULT 0,
  `gp` integer DEFAULT 0,
  `pp` integer DEFAULT 0
);

CREATE TABLE `npc` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `world_id` integer,
  `name` varchar(255),
  `location` text,
  `created_at` timestamp DEFAULT (now())
);

CREATE TABLE `npc_stats` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `npc_id` integer,
  `proficiency_mod` integer DEFAULT 2,
  `level` integer DEFAULT 0,
  `hp` integer,
  `exp` integer DEFAULT 0,
  `str_mod` integer,
  `str_score` integer,
  `dex_mod` integer,
  `dex_score` integer,
  `con_mod` integer,
  `con_score` integer,
  `int_mod` integer,
  `int_score` integer,
  `wis_mod` integer,
  `wis_score` integer,
  `cha_mod` integer,
  `cha_score` integer,
  `armor_class` integer,
  `initiative` integer,
  `death_saves_success` integer DEFAULT 0,
  `death_saves_failed` integer DEFAULT 0,
  `hit_dice` varchar(255),
  `speed` varchar(255),
  `class` varchar(255),
  `sex` varchar(255),
  `race` varchar(255),
  `alignment` varchar(255),
  `languages` text
);

CREATE TABLE `npc_features_traits` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `npc_id` integer,
  `name` varchar(255),
  `description` text
);

CREATE TABLE `npc_items` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `npc_id` integer,
  `item_id` integer,
  `proficient` bool,
  `amount` integer
);

CREATE TABLE `npc_bank` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `npc_id` integer,
  `cp` integer DEFAULT 0,
  `sp` integer DEFAULT 0,
  `ep` integer DEFAULT 0,
  `gp` integer DEFAULT 0,
  `pp` integer DEFAULT 0
);

CREATE TABLE `npc_weapons` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `npc_id` integer,
  `item_id` integer,
  `proficient` bool DEFAULT false,
  `attack_bonus` integer DEFAULT 0
);

ALTER TABLE `player_account` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_sessions` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_features_traits` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_stats` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_items` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_bank` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `player_weapons` ADD FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

ALTER TABLE `npc_features_traits` ADD FOREIGN KEY (`npc_id`) REFERENCES `npc` (`id`);

ALTER TABLE `npc_stats` ADD FOREIGN KEY (`npc_id`) REFERENCES `npc` (`id`);

ALTER TABLE `npc_items` ADD FOREIGN KEY (`npc_id`) REFERENCES `npc` (`id`);

ALTER TABLE `npc_bank` ADD FOREIGN KEY (`npc_id`) REFERENCES `npc` (`id`);

ALTER TABLE `npc_weapons` ADD FOREIGN KEY (`npc_id`) REFERENCES `npc` (`id`);

