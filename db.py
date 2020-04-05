import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="telebot",
	passwd="password",
	port='3306',
)

# Create data base
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS telebot')
mycursor.execute('USE telebot')
mycursor.execute('CREATE TABLE IF NOT EXISTS message( id INT AUTO_INCREMENT PRIMARY KEY, msg_id INT, msg_chat_id INT,media TEXT NULL, date VARCHAR(10))')
mycursor.execute('CREATE TABLE IF NOT EXISTS media( id INT AUTO_INCREMENT PRIMARY KEY, msg_chat_id INT,media_group_id TEXT NULL,file_id TEXT, caption TEXT NULL)')