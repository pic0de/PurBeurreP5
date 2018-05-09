-- MySQL Script generated by MySQL Workbench
-- Sat Apr 21 14:26:00 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema DBOpenFoodFacts
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DBOpenFoodFacts
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DBOpenFoodFacts` DEFAULT CHARACTER SET utf8 ;
USE `DBOpenFoodFacts` ;

-- -----------------------------------------------------
-- Table `DBOpenFoodFacts`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOpenFoodFacts`.`Categories` (
  `cat_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cat_name` VARCHAR(75) NOT NULL,
  `cat_url` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`cat_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DBOpenFoodFacts`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOpenFoodFacts`.`User` (
  `User_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `User_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`User_id`),
  UNIQUE INDEX `User_name_UNIQUE` (`User_name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DBOpenFoodFacts`.`Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOpenFoodFacts`.`Product` (
  `pro_id` INT NOT NULL AUTO_INCREMENT,
  `pro_name` VARCHAR(75) NOT NULL,
  `pro_shop` VARCHAR(75) NULL,
  `pro_url` VARCHAR(150) NOT NULL,
  `pro_nutriscore` INT NOT NULL,
  `pro_cat_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`pro_id`),
  INDEX `fk_Product_Categories1_idx` (`pro_cat_id` ASC),
  UNIQUE INDEX `pro_name_UNIQUE` (`pro_name` ASC),
  CONSTRAINT `fk_Product_Categories1`
    FOREIGN KEY (`pro_cat_id`)
    REFERENCES `DBOpenFoodFacts`.`Categories` (`cat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DBOpenFoodFacts`.`Saved`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOpenFoodFacts`.`Saved` (
  `sav_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `sav_pro_id` INT NOT NULL,
  `sav_User_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`sav_id`),
  INDEX `fk_Saved_Product1_idx` (`sav_pro_id` ASC),
  INDEX `fk_Saved_User1_idx` (`sav_User_id` ASC),
  CONSTRAINT `fk_Saved_Product1`
    FOREIGN KEY (`sav_pro_id`)
    REFERENCES `DBOpenFoodFacts`.`Product` (`pro_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Saved_User1`
    FOREIGN KEY (`sav_User_id`)
    REFERENCES `DBOpenFoodFacts`.`User` (`User_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
