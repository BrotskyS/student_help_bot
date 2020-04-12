import mysql.connector

connection = mysql.connector.connect(
	host="localhost",
	user="telebot-user",
	passwd="telebot-p@ssword",
	port='3306',
	auth_plugin='mysql_native_password'
)

# Create data base
mycursor = connection.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS telebot')
mycursor.execute('USE telebot')

mycursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS homework( 
	id INT AUTO_INCREMENT PRIMARY KEY,
	message_id INT NULL,
	user_id INT,
	from_chat_id INT,
	media_group_id TEXT NULL,
	date VARCHAR(10))
	"""
)

mycursor.execute(
	"""
	CREATE TABLE IF NOT EXISTS media( 
	id INT AUTO_INCREMENT PRIMARY KEY,
	media_group_id TEXT,
	files TEXT)
	"""
)