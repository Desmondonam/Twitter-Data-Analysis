USE schema

-- Create table on the database
CREATE TABLE `schema`.`rawdata` (
  `idrawdata` INT NOT NULL,
  PRIMARY KEY (`idrawdata`));

-- Drop table
DROP TABLE `schema`.`tobedeletedtable`;


-- Insert a value in a database
INSERT INTO `schema`.`rawdata` (`idrawdata`) VALUES ('11');


-- Update a value in a database
UPDATE `schema`.`rawdata` SET `idrawdata` = '5' WHERE (`idrawdata` = '10');