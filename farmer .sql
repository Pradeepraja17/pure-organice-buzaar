-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 04, 2024 at 10:48 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `farmer`
--

-- --------------------------------------------------------

--
-- Table structure for table `add_product`
--

CREATE TABLE `add_product` (
  `id` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `price` varchar(20) NOT NULL,
  `quality` varchar(20) NOT NULL,
  `image` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `type` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `add_product`
--

INSERT INTO `add_product` (`id`, `name`, `price`, `quality`, `image`, `description`, `type`) VALUES
(1, 'tomato', '28', 'medium', 'tomta.jpg', 'apple ..', 'vegetable'),
(2, 'coconut ', '200', 'high', 'Coconut.jpg', 'pure oil ', 'oil'),
(3, 'banana', '5', 'medium', 'banana.jpg', 'green banana ', 'fruits');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(100) NOT NULL,
  `password` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', ''),
('123', ''),
('admin', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cartid` int(11) NOT NULL,
  `pid` varchar(10) NOT NULL,
  `nos` varchar(10) NOT NULL,
  `cid` varchar(10) NOT NULL,
  `status` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartid`, `pid`, `nos`, `cid`, `status`) VALUES
(6, '1', '4', '2', ''),
(7, '0', '2', '2', ''),
(8, '1', '2', '2', ''),
(9, '0', '1', '2', ''),
(10, '1', '1', '4', ''),
(11, '1', '2', '4', ''),
(13, '0', '', '4', ''),
(15, '0', '1', '4', ''),
(18, '0', '1', '4', ''),
(22, '1', '1', '4', ''),
(23, '2', '', '4', ''),
(26, '1', '1', '10', '1'),
(27, '2', '1', '10', '1'),
(33, '2', '1', '2', ''),
(34, '2', '2', '4', ''),
(42, '2', '2', '9', '1'),
(43, '1', '1', '9', '1'),
(44, '2', '1', '9', '1'),
(45, '2', '12', '9', '1'),
(46, '1', '21', '9', '1'),
(47, '1', '1', '9', '1'),
(48, '2', '1', '9', '1'),
(49, '2', '1', '9', '1'),
(50, '3', '1', '9', '1'),
(51, '1', '1', '9', '1');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `phone` int(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `email`, `phone`, `password`, `address`) VALUES
(2, 'nithish', '9751172802@gmail.com', 9698999, '1', '48'),
(4, 'pradeep', 'pradeepomr2001@gmail', 84545833, '1234', '4/36 middle'),
(5, 'raja', 'raja@gmali.com', 2147483647, '123', '4/36 middle'),
(8, 'velan', 'velan@gmail.com', 2147483647, '123', '4/36 middle'),
(9, 'arun', 'arun@gmail.com', 2147483647, '123', '2b chennai'),
(10, 'yuvaraj', 'yuva@gmail.com', 1234567890, '123456', '4/36 middle'),
(11, 'ragu', 'ragu@gmail.com', 2147483647, '123', '4b main road'),
(12, 'tamil', 'tamil@gmail.com', 2147483647, '123', '3b  main road chennai'),
(13, 'siva', 'siva@gmail.com', 2147483647, '123', '2b trichy'),
(14, 'VELAN M', 'mbala9645@gmail.com', 2147483647, '1234', '48,NANGA MANGALA SATHIRAM');

-- --------------------------------------------------------

--
-- Table structure for table `view_product`
--

CREATE TABLE `view_product` (
  `id` int(10) NOT NULL,
  `name` char(20) NOT NULL,
  `phone` text NOT NULL,
  `total of booking` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `add_product`
--
ALTER TABLE `add_product`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cartid`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `add_product`
--
ALTER TABLE `add_product`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cartid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
