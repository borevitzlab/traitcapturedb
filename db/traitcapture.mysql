SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`accession`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`accession` (
  `id_accession` BIGINT UNSIGNED NOT NULL ,
  `external_stocknum` VARCHAR(45) NULL COMMENT 'e.g. ABRC ID' ,
  `source` TEXT NULL COMMENT 'ie who sent us the seeds (e.g. ABRC)' ,
  `accession_name` VARCHAR(45) NOT NULL ,
  `ecotype` VARCHAR(45) NULL ,
  `background` VARCHAR(45) NULL ,
  `generation` VARCHAR(45) NULL ,
  `country_origin` VARCHAR(45) NULL ,
  `gps_lat` DECIMAL(20,16) NULL ,
  `gps_long` DECIMAL(20,16) NULL ,
  `altitude` DECIMAL(10,6) NULL ,
  `collection_date` DATETIME NULL ,
  `collector_name` TINYTEXT NULL ,
  `parental_id` BIGINT UNSIGNED NULL COMMENT 'ID of parental  accession (if available)' ,
  `ploidy` VARCHAR(45) NULL ,
  `bulk_or_matern` VARCHAR(45) NULL COMMENT 'Source is: bulk or maternal line?' ,
  `habitat` VARCHAR(45) NULL ,
  `qr_code` VARCHAR(45) NULL ,
  `notes` TEXT NULL ,
  `species_id` BIGINT UNSIGNED NULL ,
  UNIQUE INDEX `accession_name_UNIQUE` (`accession_name` ASC) ,
  PRIMARY KEY (`id_accession`) ,
  UNIQUE INDEX `id_UNIQUE` (`id_accession` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tray`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`tray` (
  `id_tray` BIGINT UNSIGNED NOT NULL ,
  `experiment_tray_number` TINYINT UNSIGNED NULL ,
  `qr_code` BLOB NULL ,
  PRIMARY KEY (`id_tray`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`plant`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`plant` (
  `id_plant` BIGINT UNSIGNED NOT NULL COMMENT 'A unique 5 digit alphnumeric for each plant' ,
  `tray_id_tray` BIGINT UNSIGNED NOT NULL ,
  `experiment_id` BIGINT UNSIGNED NOT NULL ,
  `anuid` VARCHAR(45) NOT NULL COMMENT 'This is the ANU ID that is generated from the plant\'s unique number, spp type' ,
  `tray_coord` VARCHAR(2) NOT NULL ,
  `qr_code` BLOB NULL ,
  `accession_id` BIGINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`id_plant`, `accession_id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id_plant` ASC) ,
  INDEX `fk_plant_accession` (`accession_id` ASC) ,
  INDEX `fk_plant_tray1` (`tray_id_tray` ASC) ,
  CONSTRAINT `fk_plant_accession`
    FOREIGN KEY (`accession_id` )
    REFERENCES `mydb`.`accession` (`id_accession` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_plant_tray1`
    FOREIGN KEY (`tray_id_tray` )
    REFERENCES `mydb`.`tray` (`id_tray` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`experiment`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`experiment` (
  `id_experiment` BIGINT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NOT NULL ,
  `protocol_pre_treatments` TEXT NULL ,
  `protocol_in_chamber` TEXT NULL ,
  `protocol_trayscan_experiment` TEXT NULL ,
  `protocol_trayscan_fluorescence` TEXT NULL ,
  `notes` TEXT NULL ,
  PRIMARY KEY (`id_experiment`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`species`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`species` (
  `id_species` BIGINT UNSIGNED NOT NULL ,
  `species_genus` VARCHAR(127) NOT NULL ,
  `species_species` VARCHAR(127) NOT NULL ,
  `species_abrv` VARCHAR(3) NOT NULL ,
  PRIMARY KEY (`id_species`) ,
  UNIQUE INDEX `id_UNIQUE` (`id_species` ASC) ,
  UNIQUE INDEX `species_abrv_UNIQUE` (`species_abrv` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`raw_data`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`raw_data` (
  `id_raw_data` BIGINT UNSIGNED NOT NULL ,
  `file_structure_id` INT UNSIGNED NOT NULL ,
  `plant_id` BIGINT UNSIGNED NOT NULL ,
  `file_source_id` INT UNSIGNED NOT NULL ,
  `md5sum` BINARY(16) NOT NULL ,
  PRIMARY KEY (`id_raw_data`) ,
  UNIQUE INDEX `idraw_data_UNIQUE` (`id_raw_data` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`file_sources`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`file_sources` (
  `id_file_sources` INT UNSIGNED NOT NULL ,
  `owner` VARCHAR(45) NULL ,
  `uri` VARCHAR(255) NULL ,
  PRIMARY KEY (`id_file_sources`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`file_structure`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`file_structure` (
  `id_file_structure` INT UNSIGNED NOT NULL ,
  `file_type` VARCHAR(45) NULL ,
  PRIMARY KEY (`id_file_structure`) ,
  UNIQUE INDEX `idfile_structure_UNIQUE` (`id_file_structure` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`users` (
  `id_users` INT UNSIGNED NOT NULL ,
  `user_name` VARCHAR(45) NOT NULL ,
  `lab` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id_users`) ,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
