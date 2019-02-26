-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema codenames_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema codenames_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `codenames_db` DEFAULT CHARACTER SET utf8 ;
USE `codenames_db` ;

-- -----------------------------------------------------
-- Table `codenames_db`.`colors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `codenames_db`.`colors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `color` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `codenames_db`.`words`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `codenames_db`.`words` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `word` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `codenames_db`.`cards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `codenames_db`.`cards` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `color_id` INT NOT NULL,
  `word_id` INT NOT NULL,
  `game_id` DATETIME NULL,
  INDEX `fk_cards_colors_idx` (`color_id` ASC) VISIBLE,
  INDEX `fk_cards_words1_idx` (`word_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_cards_colors`
    FOREIGN KEY (`color_id`)
    REFERENCES `codenames_db`.`colors` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cards_words1`
    FOREIGN KEY (`word_id`)
    REFERENCES `codenames_db`.`words` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
