import sqlite3

db = sqlite3.connect("database")

cursor = db.cursor()
# cursor.execute("""DROP TABLE users""")
if db:
	# Create a table
	cursor.execute("""CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT unique, password TEXT)""")
	db.commit()

name1 = 'Andres'
phone1 = '3366858'
email1 = 'user@example.com'
password1 = '12345'

name2 = 'John'
phone2 = '5557241'
email2 = 'johndoe@example.com'
password2 = 'abcdef'

# Inserting new entries
cursor.execute("""INSERT INTO users(name, phone, email, password) VALUES (?,?,?,?)""", (name1, phone1, email1, password1))
id = cursor.lastrowid
print("First user inserted")
print("last row id: %d" % id)

cursor.execute("""INSERT INTO users(name, phone, email, password) VALUES (?,?,?,?)""", (name2, phone2, email2, password2))
id = cursor.lastrowid
print("Second user inserted")
print("last row id: %d" % id)
db.commit()

# Reading entries
cursor.execute("""SELECT name, email, phone FROM users""")

# Get one user
# user1 = cursor.fetchone()
# print("Name: " + user1[0])

# Get all users
for row in cursor:
	print('{0} : {1} , {2}'.format(row[0], row[1], row[2]))


# Selecting one predefined user
# user_id = 3
# cursor.execute("""SELECT name, email, phone FROM users WHERE id=?""", (user_id,))
# user = cursor.fetchone()

# Updating users
newphone = '3113093164'
userid = 1
cursor.execute("""UPDATE users SET phone = ? WHERE id = ?""", (newphone, userid))

# Delete users
userid = 2
cursor.execute(""" DELETE FROM users WHERE id = ?""", (userid,))

db.commit()


# Drop a table
cursor.execute("""DROP TABLE users""")
db.commit()

db.close()
