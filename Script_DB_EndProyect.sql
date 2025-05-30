-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.5.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for db_grafogt
CREATE DATABASE IF NOT EXISTS `db_grafogt` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `db_grafogt`;

-- Dumping structure for table db_grafogt.tbl_aristadistancia
CREATE TABLE IF NOT EXISTS `tbl_aristadistancia` (
  `idDistancia` int(11) NOT NULL AUTO_INCREMENT,
  `idOrigen` int(11) NOT NULL,
  `idDestino` int(11) NOT NULL,
  `kmDistancia` decimal(5,3) NOT NULL,
  PRIMARY KEY (`idDistancia`),
  KEY `FK_tbl_aristadistancia_tbl_verticesmunicipios` (`idOrigen`),
  KEY `FK_tbl_aristadistancia_tbl_verticesmunicipios_2` (`idDestino`),
  CONSTRAINT `FK_tbl_aristadistancia_tbl_verticesmunicipios` FOREIGN KEY (`idOrigen`) REFERENCES `tbl_verticesmunicipios` (`idMunicipio`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_tbl_aristadistancia_tbl_verticesmunicipios_2` FOREIGN KEY (`idDestino`) REFERENCES `tbl_verticesmunicipios` (`idMunicipio`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci COMMENT='La distancia son las aristas del grafo';

-- Data exporting was unselected.

-- Dumping structure for table db_grafogt.tbl_verticesmunicipios
CREATE TABLE IF NOT EXISTS `tbl_verticesmunicipios` (
  `idMunicipio` int(4) NOT NULL AUTO_INCREMENT,
  `nombreMunicipio` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idMunicipio`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci COMMENT='Los municipios serán los vertices de los grafos';

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
