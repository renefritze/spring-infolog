<?
require ("logical/common.php");

DB_Query ("CREATE TABLE `dbSpringInfolog`.`cache` (
`Field` VARCHAR( 128 ) NOT NULL ,
`Data` MEDIUMTEXT NULL ,
`Updated` INT UNSIGNED NULL ,
PRIMARY KEY ( `Field` ) 
) ENGINE = MYISAM");
?>