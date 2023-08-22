-- Create the  database 
CREATE DATABASE loginapp;


-- Switch to 'loginapp' 
USE loginapp; 


-- Create 'account' table 
CREATE TABLE accounts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
); 



