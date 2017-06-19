-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: atm_beras
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `nasabah`
--

DROP TABLE IF EXISTS `nasabah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nasabah` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(50) NOT NULL,
  `saldo` int(11) NOT NULL DEFAULT '0',
  `pin` varchar(64) DEFAULT NULL,
  `card_id` varchar(64) DEFAULT NULL,
  `jenis_kelamin` varchar(1) NOT NULL DEFAULT 'L',
  `tanggal_lahir` date DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `no_ktp` varchar(50) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nasabah`
--

LOCK TABLES `nasabah` WRITE;
/*!40000 ALTER TABLE `nasabah` DISABLE KEYS */;
INSERT INTO `nasabah` VALUES (1,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','##ÃLðbãÀ‡}×Xy','L',NULL,NULL,'2017-06-14 19:55:04',NULL,1),(2,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Ø-Z#±[R„L×ñÃ¸','L',NULL,NULL,'2017-06-14 19:55:11',NULL,1),(3,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ƒÿŸÊè\"\"óf{¤š)Šo','L',NULL,NULL,'2017-06-14 19:55:15',NULL,1),(4,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','£›un#\0z˜–f·C','L',NULL,NULL,'2017-06-14 19:55:18',NULL,1),(5,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ÿÜt\Z$KÃÂ-gø€','L',NULL,NULL,'2017-06-14 19:55:22',NULL,1),(6,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','™R&`|éÎ¸è6œxIè','L',NULL,NULL,'2017-06-14 19:55:25',NULL,1),(7,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ëwœ<¹]<Iþ±O—¿â','L',NULL,NULL,'2017-06-14 19:55:34',NULL,1),(8,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‘,F—@üÛŠ‰DU“…íé','L',NULL,NULL,'2017-06-14 19:55:37',NULL,1),(9,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','á‹“è \0ü*4D@ÅâÙ','L',NULL,NULL,'2017-06-14 19:55:40',NULL,1),(10,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\\ã‡õE˜ \'å\\»ð:','L',NULL,NULL,'2017-06-14 19:55:44',NULL,1),(11,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','=àHQ \Zm±x,¶)ª-´','L',NULL,NULL,'2017-06-14 19:55:47',NULL,1),(12,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ªÓ~~Ò·Ä¯pE£‚ ','L',NULL,NULL,'2017-06-14 19:55:50',NULL,1),(13,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','äì|\r£œLì\r¢dœöQes','L',NULL,NULL,'2017-06-14 19:55:53',NULL,1),(14,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ë3®òµ§ÄVo_¯\nFs','L',NULL,NULL,'2017-06-14 19:55:56',NULL,1),(15,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¹²Q\n)ªY¥L6“\Z8(§','L',NULL,NULL,'2017-06-14 19:55:59',NULL,1),(16,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','_:Î‚dáý5Èm>C§','L',NULL,NULL,'2017-06-14 19:56:02',NULL,1),(17,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','vzƒˆÑajci©KS8Ã¶','L',NULL,NULL,'2017-06-14 19:56:06',NULL,1),(18,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‘í WnJ«=à¸_Ú','L',NULL,NULL,'2017-06-14 19:56:09',NULL,1),(19,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ï\nz .@ÿuÇnÛÆFÍ<','L',NULL,NULL,'2017-06-14 19:56:12',NULL,1),(20,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','³\'\næ¡G5#ç;¼K†U','L',NULL,NULL,'2017-06-14 19:56:15',NULL,1),(21,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','?Á<À£AZgšK©=¤åì','L',NULL,NULL,'2017-06-14 19:56:18',NULL,1),(22,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','oÝUŠ›Ü÷kL“ÿ:‚Í|','L',NULL,NULL,'2017-06-14 19:56:21',NULL,1),(23,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','1—×Ó0¼{‰Á-l¤xl','L',NULL,NULL,'2017-06-14 19:56:23',NULL,1),(24,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','T¡ÝirÖŸ¡Ñk;SÅ½A—','L',NULL,NULL,'2017-06-14 19:56:35',NULL,1);
/*!40000 ALTER TABLE `nasabah` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-15  2:57:27
