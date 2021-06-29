USE schemas

-- This is to create a table on the database
CREATE TABLE `schemas`.`rawdata` (
  `idrawdata` INT NOT NULL,
  PRIMARY KEY (`idrawdata`));

-- This is to drop a table from the database 
DROP TABLE `schemas`.`tobedeletedtable`;


-- THis is to Insert a value in a database
INSERT INTO `schemas`.`rawdata` (`idrawdata`) VALUES ('11');


-- This is to Update a value in a database
UPDATE `schemas`.`rawdata` SET `idrawdata` = '5' WHERE (`idrawdata` = '10');