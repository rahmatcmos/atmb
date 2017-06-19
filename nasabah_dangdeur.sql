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
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nasabah`
--

LOCK TABLES `nasabah` WRITE;
/*!40000 ALTER TABLE `nasabah` DISABLE KEYS */;
INSERT INTO `nasabah` VALUES (1,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','e€c“ö÷\'kš•Ìp»©·','L',NULL,NULL,'2017-05-31 18:08:06',NULL,1),(2,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','LS6@¬Å€tÂf÷qc','L',NULL,NULL,'2017-05-31 18:08:09',NULL,1),(3,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','j§Ûº&Çï/?‘1íìÜ','L',NULL,NULL,'2017-05-31 18:08:42',NULL,1),(4,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‡XØDy 3Ç\'G\0ß»´i','L',NULL,NULL,'2017-05-31 18:08:45',NULL,1),(5,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ',']¬æƒ9Ë‘³”~­˜','L',NULL,NULL,'2017-05-31 18:08:48',NULL,1),(6,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ál¶¥vM×\nššxÜ`Çþ','L',NULL,NULL,'2017-05-31 18:08:51',NULL,1),(7,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','V p€Yáö¾“–¥KFà','L',NULL,NULL,'2017-05-31 18:08:54',NULL,1),(8,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','8¼µ5w¾éÈ¦b§ó£','L',NULL,NULL,'2017-05-31 18:08:57',NULL,1),(9,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‡Ø_O—ÎAÆ ½2#5','L',NULL,NULL,'2017-05-31 18:09:00',NULL,1),(10,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','#ø5œH\r¡Õ¦°ë^¸','L',NULL,NULL,'2017-05-31 18:09:03',NULL,1),(11,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','4Œ2Y—Ò?ê~@¬ç¸¤Z','L',NULL,NULL,'2017-05-31 18:09:11',NULL,1),(12,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','åŽ‰¦È3Œƒ<¤¹¾jÚ','L',NULL,NULL,'2017-05-31 18:09:14',NULL,1),(13,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ìjÉQ‚z#Ñ}´–\'Ù%','L',NULL,NULL,'2017-05-31 18:09:17',NULL,1),(14,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','a[Ó÷xHn\r¿ði[\r›','L',NULL,NULL,'2017-05-31 18:09:20',NULL,1),(15,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','T&€AM…=Ì¼ÞãNö','L',NULL,NULL,'2017-05-31 18:09:23',NULL,1),(16,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\0Þ@2~î!\'ŸÛ¡K5‰GS','L',NULL,NULL,'2017-05-31 18:09:26',NULL,1),(17,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ckæàøÕû¹ï„Æ&','L',NULL,NULL,'2017-05-31 18:09:28',NULL,1),(18,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ë¡¿ha­àY	>+Á„','L',NULL,NULL,'2017-05-31 18:09:31',NULL,1),(19,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','’L“ªãÞF‰üD£q(n','L',NULL,NULL,'2017-05-31 18:09:33',NULL,1),(20,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Æpu¤&±ýþ”Æ™Ÿ<Ü$','L',NULL,NULL,'2017-05-31 18:09:36',NULL,1),(21,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ãô÷W«`R®›$ƒ¢%','L',NULL,NULL,'2017-05-31 18:09:39',NULL,1),(22,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','³ÏdŸØ^¬;3/\"Û\"7…','L',NULL,NULL,'2017-05-31 18:09:41',NULL,1),(23,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Ì¸d ¯öµ÷Å5•…u7','L',NULL,NULL,'2017-05-31 18:09:44',NULL,1),(24,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','îîèŒÍõ‡G‚.Ü','L',NULL,NULL,'2017-05-31 18:09:47',NULL,1),(25,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Û‹¥ÌX5ÔÍ•Ñ ¾\n™','L',NULL,NULL,'2017-05-31 18:09:50',NULL,1),(26,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ê#ýøGÜ­¤0€´Þ;Ç','L',NULL,NULL,'2017-05-31 18:09:52',NULL,1),(27,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','&Þþ	Œ…+Û·k(','L',NULL,NULL,'2017-05-31 18:09:55',NULL,1),(28,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','†í9ÈÚ™ÛiÆ(G…»›–9','L',NULL,NULL,'2017-05-31 18:09:57',NULL,1),(29,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','/”d\ZYq¯qæ(2©{§¬','L',NULL,NULL,'2017-05-31 18:10:00',NULL,1),(30,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','%•ú#*Àæ ¼0','L',NULL,NULL,'2017-05-31 18:10:02',NULL,1),(31,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ŸŽ/<Û˜Ñ+á÷¿ÁÙ','L',NULL,NULL,'2017-05-31 18:10:05',NULL,1),(32,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','œàŸ@ÎJ5£)tD','L',NULL,NULL,'2017-05-31 18:10:07',NULL,1),(33,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ÐÔ[_•ªÌ¿òðy`pG×','L',NULL,NULL,'2017-05-31 18:10:10',NULL,1),(34,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','HÿPSA.ÙÓ	X|	¨\r•','L',NULL,NULL,'2017-05-31 18:10:12',NULL,1),(35,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Öú4ÅiÄNÀ%n¬²\0¡','L',NULL,NULL,'2017-05-31 18:10:15',NULL,1),(36,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','â|F]	ËÕ‡T²´¸û','L',NULL,NULL,'2017-05-31 18:10:18',NULL,1),(37,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','!­x€‘lQFzEOæ\'µ','L',NULL,NULL,'2017-05-31 18:10:21',NULL,1),(38,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','»\"tÝF#Ö{Q$É/Ž\\g','L',NULL,NULL,'2017-05-31 18:10:23',NULL,1),(39,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','­UÛãÎúø9tÂŠoÇ','L',NULL,NULL,'2017-05-31 18:10:26',NULL,1),(40,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','p¢\0—¾È6õx¶Þ~tÿ)','L',NULL,NULL,'2017-05-31 18:10:28',NULL,1),(41,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','·À^©uÒxUY™-#','L',NULL,NULL,'2017-05-31 18:10:35',NULL,1),(42,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ',' ­£óü†bñS$uKù›¥','L',NULL,NULL,'2017-05-31 18:10:38',NULL,1),(43,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ð¶ñÈ¼ó5(w€–ÓÆ½êt','L',NULL,NULL,'2017-05-31 18:10:41',NULL,1),(44,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Ž×Ü.o%µØé­Tg]¿I]','L',NULL,NULL,'2017-05-31 18:10:44',NULL,1),(45,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\Z‚‡nÆšÄÔ¸¦*¼è','L',NULL,NULL,'2017-05-31 18:10:46',NULL,1),(46,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','’F?ˆuRÉëƒ!ö{}b#','L',NULL,NULL,'2017-05-31 18:10:49',NULL,1),(47,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‘qWóZÓ}ä4Öð','L',NULL,NULL,'2017-05-31 18:10:51',NULL,1),(48,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¨ÓM/”)Ìµ­eúâ·‡è','L',NULL,NULL,'2017-05-31 18:10:54',NULL,1),(49,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\rÁÅ%ÅDÕC§Ðƒ4*','L',NULL,NULL,'2017-05-31 18:10:56',NULL,1),(50,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\rÁÅ%ÅDÕC§Ðƒ4*','L',NULL,NULL,'2017-05-31 18:10:58',NULL,1),(51,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','IAˆi¸–“&½k€','L',NULL,NULL,'2017-05-31 18:11:04',NULL,1),(52,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','‰Ö7A%=¹¾6Û¿aú','L',NULL,NULL,'2017-05-31 18:11:07',NULL,1),(53,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¡\r‹;\n`¥«D³í!¤T','L',NULL,NULL,'2017-05-31 18:11:14',NULL,1),(54,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ÌÁ¼®Ôl‹¹ŽÈÐÕ','L',NULL,NULL,'2017-05-31 18:11:17',NULL,1),(55,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ',']ùÓ®*…È’WÁ%-‹€©','L',NULL,NULL,'2017-05-31 18:11:20',NULL,1),(56,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','í/úªÅ¦k˜Ûü»é¶>l','L',NULL,NULL,'2017-05-31 18:11:23',NULL,1),(57,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','´Ÿà²’{NN¬Zî?¶\"','L',NULL,NULL,'2017-05-31 18:11:26',NULL,1),(58,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','\\#¤%¾÷¹Î=+f\\—Ý','L',NULL,NULL,'2017-05-31 18:11:29',NULL,1),(59,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Á);=—Ý+ÊV(x[S','L',NULL,NULL,'2017-05-31 18:11:36',NULL,1),(60,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ò+÷ïÎœÜ¨ˆªò¨x¯Ë¦','L',NULL,NULL,'2017-05-31 18:11:40',NULL,1),(61,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ',')Y9úL#3dû\"[5^','L',NULL,NULL,'2017-05-31 18:11:43',NULL,1),(62,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','œ#\'ýÔvÝF]Ä˜¨{Ki','L',NULL,NULL,'2017-05-31 18:11:57',NULL,1),(63,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','H¶Û¼ÑùO\n¤bÔ+\'/˜','L',NULL,NULL,'2017-05-31 18:12:00',NULL,1),(64,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','®LýU®ÄcS”Kq[x«Ý=','L',NULL,NULL,'2017-05-31 18:12:03',NULL,1),(65,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ILlêr˜\"é…g}¯çã0','L',NULL,NULL,'2017-05-31 18:12:06',NULL,1),(66,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¬ï«` Ad)gK²\"þ','L',NULL,NULL,'2017-05-31 18:12:12',NULL,1),(67,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','áÑÚhVÉw²ûÙ—Úªi','L',NULL,NULL,'2017-05-31 18:12:15',NULL,1),(68,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¾}æt:ô»ÃµRwõÆ¡ò','L',NULL,NULL,'2017-05-31 18:12:18',NULL,1),(69,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','c”ò…q—8šÎ´12R','L',NULL,NULL,'2017-05-31 18:12:22',NULL,1),(70,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','÷êbl–EH2Ês:oŸ\r','L',NULL,NULL,'2017-05-31 18:12:25',NULL,1),(71,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','Ìùfb€6Æ8^³üŠ §H','L',NULL,NULL,'2017-05-31 18:12:28',NULL,1),(72,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','¶ùã³\"ŽP›¶nWi«^ù','L',NULL,NULL,'2017-05-31 18:12:30',NULL,1),(73,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','<}ëá¯\nº¼lìLs)ú','L',NULL,NULL,'2017-05-31 18:12:33',NULL,1),(74,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','zßóÒ@ÊSi9µj','L',NULL,NULL,'2017-05-31 18:12:38',NULL,1),(75,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','º9;­uõ{×gbnf$c','L',NULL,NULL,'2017-05-31 18:12:40',NULL,1),(76,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','ùwY1RØ«ŽÈ­€P¥\'','L',NULL,NULL,'2017-05-31 18:12:44',NULL,1),(77,'PENERIMA',15,'ü¬¯Þ±´˜Üõn¿ˆ‡ñ','T¡ÝirÖŸ¡Ñk;SÅ½A—','L',NULL,NULL,'2017-05-31 18:12:46',NULL,1);
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

-- Dump completed on 2017-06-01  1:46:16
