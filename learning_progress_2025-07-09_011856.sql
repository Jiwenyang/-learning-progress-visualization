-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: learning_progress
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text,
  `file_path` varchar(200) DEFAULT NULL,
  `total_units` int NOT NULL,
  `current_unit` int DEFAULT NULL,
  `time_spent` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
INSERT INTO `progress` VALUES (1,'Python Programming from Beginner to Expert','Learn Python basics and practical projects','static/uploads/test.docx',20,10,15.5,'2025-07-09 01:17:55','2025-07-09 01:17:55',1),(2,'Data Structures and Algorithms','Learn common data structures and algorithms','static/uploads/test.docx',15,5,8,'2025-07-09 01:17:55','2025-07-09 01:17:55',1),(3,'Machine Learning Fundamentals','Learn basic concepts and algorithms of machine learning','static/uploads/test.docx',12,12,20,'2025-07-09 01:17:55','2025-07-09 01:17:55',1),(4,'Web Development Introduction','Learn HTML, CSS and JavaScript','static/uploads/test.docx',10,8,12.5,'2025-07-09 01:17:55','2025-07-09 01:17:55',1),(5,'Database Design','Learn relational database design and SQL','static/uploads/test.docx',8,0,0,'2025-07-09 01:17:56','2025-07-09 01:17:56',1),(6,'Java Programming Basics','Learn Java language basics and object-oriented programming','static/uploads/test.docx',18,9,14,'2025-07-09 01:17:56','2025-07-09 01:17:56',2),(7,'Frontend Framework Vue','Learn Vue.js framework for single page applications','static/uploads/test.docx',10,10,16.5,'2025-07-09 01:17:56','2025-07-09 01:17:56',2),(8,'Linux System Management','Learn Linux system basic operations and management','static/uploads/test.docx',12,3,5,'2025-07-09 01:17:56','2025-07-09 01:17:56',2),(9,'Deep Learning','Learn neural networks and deep learning models','static/uploads/test.docx',15,7,18.5,'2025-07-09 01:17:56','2025-07-09 01:17:56',3),(10,'Cloud Computing Basics','Learn cloud services and application deployment','static/uploads/test.docx',10,10,12,'2025-07-09 01:17:56','2025-07-09 01:17:56',3);
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(200) NOT NULL,
  `email` varchar(120) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'111111','111111','111111@example.com','2025-07-09 01:17:55'),(2,'222222','222222','222222@example.com','2025-07-09 01:17:55'),(3,'333333','333333','333333@example.com','2025-07-09 01:17:55');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

--
-- Dumping routines for database 'learning_progress'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-09  1:19:04
