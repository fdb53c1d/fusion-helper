DROP TABLE IF EXISTS `equips`;
DROP TABLE IF EXISTS `rituals`;
DROP TABLE IF EXISTS `fusions`;
DROP TABLE IF EXISTS `cards`;
DROP TABLE IF EXISTS `types`;
DROP TABLE IF EXISTS `stars`;

CREATE TABLE `cards` (
	`Id` SMALLINT(6) NOT NULL,
	`Name` VARCHAR(40) NOT NULL,
	`Description` VARCHAR(200) NOT NULL,
	`GuardianStarA` TINYINT(4) NOT NULL,
	`GuardianStarB` TINYINT(4) NOT NULL,
	`Level` TINYINT(4) NOT NULL,
	`Type` TINYINT(4) NOT NULL,
	`Attack` SMALLINT(6) NOT NULL,
	`Defense` SMALLINT(6) NOT NULL,
	`Stars` MEDIUMINT(9) NOT NULL,
	`CardCode` INT(11) NOT NULL,
	`Attribute` TINYINT(4) NOT NULL,
	PRIMARY KEY (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `equips` (
	`Id` MEDIUMINT(9) NOT NULL AUTO_INCREMENT,
	`Equip_id` SMALLINT(6) NOT NULL,
	`Equipped_id` SMALLINT(6) NOT NULL,
	PRIMARY KEY (`Id`),
	INDEX `Equip_id` (`Equip_id`),
	INDEX `Equipped_id` (`Equipped_id`),
	CONSTRAINT `Equip_id` FOREIGN KEY (`Equip_id`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Equipped_id` FOREIGN KEY (`Equipped_id`) REFERENCES `cards` (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `rituals` (
	`Id` TINYINT(4) NOT NULL AUTO_INCREMENT,
	`Ritual_id` SMALLINT(6) NOT NULL,
	`Card1` SMALLINT(6) NOT NULL,
	`Card2` SMALLINT(6) NOT NULL,
	`Card3` SMALLINT(6) NOT NULL,
	`Result` SMALLINT(6) NOT NULL,
	PRIMARY KEY (`Id`),
	INDEX `Ritual_id` (`Ritual_id`),
	INDEX `Card1` (`Card1`),
	INDEX `Card2` (`Card2`),
	INDEX `Card3` (`Card3`),
	INDEX `Result_id` (`Result`),
	CONSTRAINT `Ritual_Card1` FOREIGN KEY (`Card1`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Ritual_Card2` FOREIGN KEY (`Card2`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Ritual_Card3` FOREIGN KEY (`Card3`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Ritual_Result` FOREIGN KEY (`Result`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Ritual_id` FOREIGN KEY (`Ritual_id`) REFERENCES `cards` (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `fusions` (
	`Id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`Card1` SMALLINT NOT NULL,
	`Card2` SMALLINT NOT NULL,
	`Result` SMALLINT NOT NULL,
	PRIMARY KEY (`Id`),
	CONSTRAINT `Fusion_Card1` FOREIGN KEY (`Card1`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Fusion_Card2` FOREIGN KEY (`Card2`) REFERENCES `cards` (`Id`),
	CONSTRAINT `Fusion_Result` FOREIGN KEY (`Result`) REFERENCES `cards` (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `types` (
	`Id` TINYINT NOT NULL,
	`Type` VARCHAR(15) NOT NULL,
	PRIMARY KEY (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `stars` (
	`Id` TINYINT NOT NULL,
	`Star` VARCHAR(15) NOT NULL,
	PRIMARY KEY (`Id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
