CREATE USER 'admin'@'localhost' IDENTIFIED BY 'toor';

CREATE DATABASE IF NOT EXISTS shopping_basket_db;
GRANT ALL PRIVILEGES ON  *.* to 'admin'@'localhost' WITH GRANT OPTION;