import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="masterboda",
	passwd="p@ssword",
	port='3306',
)

# Create data base
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS telebot')
mycursor.execute('USE telebot')
mycursor.execute('CREATE TABLE IF NOT EXISTS message( id INT AUTO_INCREMENT PRIMARY KEY, msg_id INT, msg_chat_id INT,media TEXT NULL,file TEXT NULL, date VARCHAR(10) )')