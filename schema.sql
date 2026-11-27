-- Database, user and table that python/sensor_processor.py and python/app.py expect.
-- Run once on the Raspberry Pi:   sudo mariadb < schema.sql
-- The user and password match the lab defaults in the code. On anything other
-- than a lab bench, pick your own and pass them in with DB_USER / DB_PASSWORD.

CREATE DATABASE IF NOT EXISTS Part2Data;
CREATE USER IF NOT EXISTS 'Nypuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON Part2Data.* TO 'Nypuser'@'localhost';
FLUSH PRIVILEGES;

USE Part2Data;

-- Column order matches the dashboard table (No., NYP ID, Name, Date, Window State,
-- Time Limit, Room Status, Alert), because app.py shows the rows column by column.
CREATE TABLE IF NOT EXISTS Part2Data (
  No           INT AUTO_INCREMENT PRIMARY KEY,
  NYP_ID       VARCHAR(16) DEFAULT NULL,
  Name         VARCHAR(64) DEFAULT NULL,
  Date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  IR_State     FLOAT NOT NULL,
  Rotary_Limit FLOAT NOT NULL,
  Room_Status  VARCHAR(32) NOT NULL,
  Alert_Msg    VARCHAR(64) NOT NULL
);
