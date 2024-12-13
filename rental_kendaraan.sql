/*
SQLyog Professional v13.1.1 (64 bit)
MySQL - 8.0.30 : Database - rental_kendaraan
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`rental_kendaraan` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `rental_kendaraan`;

/*Table structure for table `jenis_kendaraan` */

DROP TABLE IF EXISTS `jenis_kendaraan`;

CREATE TABLE `jenis_kendaraan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(50) NOT NULL,
  `deskripsi` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `jenis_kendaraan` */

insert  into `jenis_kendaraan`(`id`,`nama`,`deskripsi`) values 
(1,'motor','2 roda'),
(2,'mobil','mobil'),
(3,'coba','coba'),
(5,'fsasa','sfafaf'),
(6,'elf','mobil 6 orang');

/*Table structure for table `kendaraan` */

DROP TABLE IF EXISTS `kendaraan`;

CREATE TABLE `kendaraan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jenis_id` int DEFAULT NULL,
  `nama` varchar(100) NOT NULL,
  `plat_nomor` varchar(20) NOT NULL,
  `harga_sewa` decimal(10,2) NOT NULL,
  `status` enum('tersedia','disewa') DEFAULT 'tersedia',
  PRIMARY KEY (`id`),
  UNIQUE KEY `plat_nomor` (`plat_nomor`),
  KEY `jenis_id` (`jenis_id`),
  CONSTRAINT `kendaraan_ibfk_1` FOREIGN KEY (`jenis_id`) REFERENCES `jenis_kendaraan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `kendaraan` */

insert  into `kendaraan`(`id`,`jenis_id`,`nama`,`plat_nomor`,`harga_sewa`,`status`) values 
(1,2,'Avanza','3112',500000.00,'tersedia'),
(2,1,'Beat','4112',250000.00,'tersedia'),
(4,1,'vario','7654',100000.00,'tersedia'),
(5,2,'Brio','9128',300000.00,'tersedia');

/*Table structure for table `pembayaran` */

DROP TABLE IF EXISTS `pembayaran`;

CREATE TABLE `pembayaran` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pemesanan_id` int DEFAULT NULL,
  `jumlah` decimal(10,2) NOT NULL,
  `tanggal_pembayaran` datetime NOT NULL,
  `metode_pembayaran` varchar(50) NOT NULL,
  `status` enum('menunggu','berhasil','gagal') DEFAULT 'menunggu',
  `denda` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `pemesanan_id` (`pemesanan_id`),
  CONSTRAINT `pembayaran_ibfk_1` FOREIGN KEY (`pemesanan_id`) REFERENCES `pemesanan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pembayaran` */

/*Table structure for table `pemesanan` */

DROP TABLE IF EXISTS `pemesanan`;

CREATE TABLE `pemesanan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pengguna_id` int DEFAULT NULL,
  `kendaraan_id` int DEFAULT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date NOT NULL,
  `total_biaya` decimal(10,2) NOT NULL,
  `status` enum('menunggu','disetujui','ditolak','selesai') DEFAULT 'menunggu',
  PRIMARY KEY (`id`),
  KEY `pengguna_id` (`pengguna_id`),
  KEY `kendaraan_id` (`kendaraan_id`),
  CONSTRAINT `pemesanan_ibfk_1` FOREIGN KEY (`pengguna_id`) REFERENCES `pengguna` (`id`),
  CONSTRAINT `pemesanan_ibfk_2` FOREIGN KEY (`kendaraan_id`) REFERENCES `kendaraan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pemesanan` */

insert  into `pemesanan`(`id`,`pengguna_id`,`kendaraan_id`,`tanggal_mulai`,`tanggal_selesai`,`total_biaya`,`status`) values 
(2,2,4,'2024-12-13','2024-12-14',200000.00,'menunggu');

/*Table structure for table `pengguna` */

DROP TABLE IF EXISTS `pengguna`;

CREATE TABLE `pengguna` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_telepon` varchar(20) DEFAULT NULL,
  `role` enum('admin','penyewa') NOT NULL,
  `status` enum('aktif','nonaktif') DEFAULT 'aktif',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pengguna` */

insert  into `pengguna`(`id`,`username`,`password`,`nama_lengkap`,`email`,`no_telepon`,`role`,`status`) values 
(1,'frank','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','Frankie Steinlie','frank@gmail.com','08883866931','admin','aktif'),
(2,'stein','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','stein','stein@gmail.com','08883866931','penyewa','aktif');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
