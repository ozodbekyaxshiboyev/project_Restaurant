import sqlite3

# conn = sqlite3.connect('db/test.db')
# print("Opened database successfully")
#
# conn.execute('''CREATE TABLE COMPANY
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           TEXT    NOT NULL,
#          AGE            INT     NOT NULL,
#          ADDRESS        CHAR(50),
#          SALARY         REAL);''')
# print("Table created successfully")
#
# conn.close()


# conn = sqlite3.connect('db/test.db')
# print("Opened database successfully")
#
# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")
#
# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
#
# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
#
# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
#
# conn.commit()
# print("Records created successfully")
# conn.close()


# reg_name = input('Enter region name')
#
# conn = sqlite3.connect('db/test.db')
# print("Opened database successfully")
#
# conn.execute(f"INSERT INTO Region (Name) \
#       VALUES ('{reg_name}')")
#
#
# conn.commit()
# print("Records created successfully")
# conn.close()

#
# conn = sqlite3.connect('db/test.db')
# print("Opened database successfully")
#
# conn.execute("DELETE from COMPANY where ID = 2;")
# conn.commit()
# print("Total number of rows deleted :", conn.total_changes)
#
#
# cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
# for row in cursor:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])
#    print("ADDRESS = ", row[2])
#    print("SALARY = ", row[3], "\n")
#
# print("Operation done successfully")
# conn.close()

class Car:
   def __init__(self,name,adress):
      self.id = None
      self.name = name
      self.adress = adress

   def save(self):
      conn = sqlite3.connect('db/test1.db')
      cursor = conn.cursor()
      cursor.execute('''CREATE TABLE IF NOT EXISTS CAR
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               ADDRESS        CHAR(50));
               ''')
      cursor.execute("INSERT INTO CAR (ID,NAME,ADDRESS) \
            VALUES ( 1, f'{self.name}',  f'{self.adress}')")
      conn.commit()
      conn.close()


   def __str__(self):
      return self.name

car = Car("BMW","Uzbekistan")
car.save()




