CREATE DATABASE twitter;
-- use database
USE [twitter];
GO 
-- check to see if table exist in sys.tables ignore DROP TABLE if it does not 
IF EXISTS (SELECT *
	FROM sys.tables
    WHERE SCHEMA_NAME(schema_id) like 'dbo'
    AND name like 'MyTable0')
DROP TABLE [dbo].[MyTable0];
GO