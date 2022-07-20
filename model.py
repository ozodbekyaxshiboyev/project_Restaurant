import os
import sqlite3
from settings import db_name


class Basemodel:
    table = ""
    def __init__(self):
        self.id = None

    def save(self):
        pass

    def delete(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table} Where id='{self.id}'")
        conn.commit()
        conn.close()

    def update(self):
        pass

    def objects(table):
        pass

    def get_by_id(table):
        pass




class Manager(Basemodel):
    table = 'manager'
    def __init__(self, cooker_salary_prot = 200000,waiter_salary_prot = 5,cooker_salary = 0,waiter_salary = 0,cook_raise = 40,\
                 drink_raise = 20,money = 0,expense = 0,profit = 0,realprofit = 0,id = None):
        super().__init__()
        self.cooker_salary_prot = cooker_salary_prot
        self.waiter_salary_prot = waiter_salary_prot
        self.cooker_salary = cooker_salary
        self.waiter_salary = waiter_salary
        self.cook_raise = cook_raise
        self.drink_raise = drink_raise
        self.money = money
        self.expense = expense
        self.profit = profit
        self.realprofit = realprofit
        self.id = id

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO {self.table} (cooker_salary_prot,waiter_salary_prot,cooker_salary,waiter_salary,cook_raise,drink_raise,money,expense,profit ,realprofit ) \
                    VALUES ('{self.cooker_salary_prot}','{self.waiter_salary_prot}','{self.cooker_salary}','{self.waiter_salary}', '{self.cook_raise}', '{self.drink_raise}','{self.money}','{self.expense}', '{self.profit}','{self.realprofit}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(f"UPDATE {self.table} set   cooker_salary_prot='{self.cooker_salary_prot}',waiter_salary_prot='{self.waiter_salary_prot}', \
            cooker_salary='{self.cooker_salary}',waiter_salary='{self.waiter_salary}', cook_raise='{self.cook_raise}', drink_raise='{self.drink_raise}',money='{self.money}',expense='{self.expense}', profit='{self.profit}',realprofit='{self.realprofit}' where id = {self.id}")
        conn.commit()
        conn.close()

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Manager.table} Where id={1}")
        row = list(cursor)[0]
        sel_manager = Manager(row[1],row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],row[10],  row[0])
        conn.close()
        return sel_manager


    def createtable(self,number):
        if not number in Table.tablenumbers():
            table = Table(number)
            table.save()
        else:
            print("Bunday stol mavjud!")


    def addproduct(self,id,count,price):          # mahsulot qo`shiladi
        product = Basemodel.get_by_id(Product.table,id)
        product.price = (product.price * product.count + count * price) / (product.count + count)
        product.count += count
        product.save()
        self.expense += count*price




class Table(Basemodel):
    table = 'for_tables'
    def __init__(self, number,isbusy=0,balance=0,table_id=0,id=None):
        super().__init__()
        self.id = id
        self.number = number
        self.isbusy = isbusy
        self.balance = balance
        self.table_id = table_id
        self.waiter_pay = 0



    def save(self):
        base = Baseorder.base_object()
        if self.id is None:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table} (number,isbusy,balance,table_id,waiter_pay) VALUES ('{self.number}', '{self.isbusy}','{self.balance}','{self.table_id}','{self.waiter_pay}')")
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            #taom uchun masalliq table yaratish
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            name = "order_num_"+str(base.order_number)
            base.order_number+=1
            base.save()

            cursor.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY, cook_id  INTEGER,drink_id INTEGER, name MESSAGE_TEXT ,count REAL, price REAL,sale_price REAL,table_id  INTEGER,type1 MESSAGE_TEXT,waiter_prot REAL )")
            conn.close()
            #masalliq tableni nomini taom atributiga saqlash
            self.table_id = name
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table} set  number = '{self.number}', isbusy = '{self.isbusy}',balance = '{self.balance}',table_id = '{self.table_id}', waiter_pay = '{self.waiter_pay}' where id = {self.id}")
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table} set  number = '{self.number}', isbusy = '{self.isbusy}',balance = '{self.balance}',table_id = '{self.table_id}', waiter_pay = '{self.waiter_pay}'  where id = {self.id}")
            conn.commit()
            conn.close()

    def create_table(self):
        base = Baseorder.base_object()
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        name = "order_num_" + str(base.order_number)
        base.order_number += 1
        base.save()

        cursor.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY, cook_id  INTEGER,drink_id INTEGER, name MESSAGE_TEXT ,count REAL, price REAL,sale_price REAL, table_id  INTEGER,type1 MESSAGE_TEXT,waiter_prot REAL )")
        conn.close()

        self.table_id = name
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {self.table} set  number = '{self.number}', isbusy = '{self.isbusy}',balance = '{self.balance}',table_id = '{self.table_id}', waiter_pay = '{self.waiter_pay}' where id = {self.id}")
        conn.commit()
        conn.close()



    def delete(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table} Where id='{self.id}'")
        conn.commit()
        conn.close()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Drop Table {self.table_id}")
        conn.commit()
        conn.close()


    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Table.table}")
        list1 = list()
        for row in cursor:
            list1.append(Table(row[1],row[2],row[3],row[4],row[0]))
        conn.close()
        return list1

    def objects_to_check():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT number from {Table.table}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {Table.table} Where id={id}")
        sql_row = list(cursor)[0]
        sel_table = Table(sql_row[1],sql_row[2],sql_row[3],sql_row[4], sql_row[0])
        conn.commit()
        conn.close()
        return sel_table


    def check_isorderyes(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {self.table_id}")
        list1 = list()
        sql_row = list(cursor)
        conn.close()
        return sql_row



    def set_order_table(self,order):
        if order.id is None:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table_id} (cook_id, drink_id,name,count,price,sale_price,table_id,type1,waiter_prot) VALUES ('{order.cook_id}','{order.drink_id}','{order.name}','{order.count}','{order.price}','{order.sale_price}','{order.table_id}','{order.type1}','{order.waiter_prot}')")
            order.id = cursor.lastrowid
            conn.commit()
            conn.close()

        else:
            print("id none emas ekan")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table_id} set  cook_id='{order.cook_id}',drink_id='{order.drink_id}',name='{order.name}',count='{order.count}',price='{order.price}',sale_price='{order.sale_price}',table_id='{order.table_id}',type1='{order.type1}',waiter_prot='{order.waiter_prot}' where id = {order.id}")
            conn.commit()
            conn.close()

    def order_delete(self,order):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table_id} Where id='{order.id}'")
        conn.commit()
        conn.close()


    def order_cook_id_to_check(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT cook_id from {self.table_id}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def order_drink_id_to_check(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT drink_id from {self.table_id}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    ####SINF UCHUN
    def order_object():
        list1 = list()
        for table in Table.objects():
            conn = sqlite3.connect(db_name)
            cursor = conn.execute(f"SELECT * from {table.table_id}")
            for row in cursor:
                list1.append(row[1])
            conn.close()
        return list1


    def order_objects(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {self.table_id}")
        list1 = list()
        for row in cursor:
            list1.append(Order(row[1], row[2], row[3],row[4], row[5], row[6],row[7],row[8],row[9], row[0]))
        conn.close()
        return list1

    def order_get_by_id(self,id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {self.table_id} Where id={id}")
        row = list(cursor)[0]
        sel_order = Order(row[1], row[2], row[3],row[4], row[5], row[6],row[7],row[8],row[9], row[0])
        conn.commit()
        conn.close()
        return sel_order



    def order_get_by_cook_id(self,id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {self.table_id} Where cook_id={id}")
        row = list(cursor)[0]
        sel_order = Order(row[1], row[2], row[3],row[4], row[5], row[6],row[7],row[8],row[9], row[0])
        conn.commit()
        conn.close()
        return sel_order

    def order_get_by_drink_id(self,id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {self.table_id} Where drink_id={id}")
        row = list(cursor)[0]
        sel_order = Order(row[1], row[2], row[3],row[4], row[5], row[6],row[7],row[8],row[9], row[0])
        conn.commit()
        conn.close()
        return sel_order




    def __str__(self):
        x = f"{self.number}-stol"
        if self.isbusy == 0:
            return f"{x}"
        else:
            return f"{x} busy"



class Cook(Basemodel):
    table = 'cook'
    def __init__(self,name,count=0,price=0,sale_price=0,sale_count=0,product_id=None,id = None):
        super().__init__()
        self.name = name
        self.count = count
        self.price = price
        self.sale_price = sale_price
        self.sale_count = sale_count
        self.product_id= product_id
        self.id = id# kerakli mahsulat id si va miqdori turadi

    def save(self):

        if self.id is None:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table} (name,count,price,sale_price,sale_count) VALUES ('{self.name}', '{self.count}','{self.price}','{self.sale_price}', '{self.sale_count}')")
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            #taom uchun masalliq table yaratish
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            name = "product_num_" + str(self.id)
            cursor.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY, product_id  INTEGER, counts  REAL )")
            conn.close()
            #masalliq tableni nomini taom atributiga saqlash
            self.product_id = name
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table} set  name = '{self.name}', count='{self.count}',price='{self.price}',sale_price='{self.sale_price}', sale_count='{self.sale_count}', product_id = '{self.product_id}' where id = {self.id}")
            conn.commit()
            conn.close()


        else:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table} set  name = '{self.name}', count='{self.count}',price='{self.price}',sale_price='{self.sale_price}', sale_count='{self.sale_count}', product_id = '{self.product_id}' where id = {self.id}")
            conn.commit()
            conn.close()

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Cook.table}")
        list1 = list()
        for row in cursor:
            list1.append(Cook(row[1], row[2], row[3], row[4], row[5],row[6], row[0]))
        conn.close()
        return list1

    def objects_to_check():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT name from {Cook.table}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {Cook.table} Where id={id}")
        sql_row = list(cursor)[0]
        sel_drink = Cook(sql_row[1], sql_row[2], sql_row[3], sql_row[4], sql_row[5],sql_row[6], sql_row[0])
        conn.commit()
        conn.close()
        return sel_drink

    def delete(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table} Where id='{self.id}'")
        conn.commit()
        conn.close()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Drop Table {self.product_id} ")
        conn.commit()
        conn.close()

    def check_isorderyes(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {self.product_id}")
        list1 = list()
        sql_row = list(cursor)
        conn.close()
        return sql_row

    #@@@@@@@@@@@@@@@@@@@@  pro uchun

    def get_product_table(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {self.product_id}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def set_product_table(self,pro):
        if pro.id is None:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.product_id} (product_id,counts) VALUES ('{pro.product_id}', '{pro.counts}')")
            pro.id = cursor.lastrowid
            conn.commit()
            conn.close()

        else:
            print("id none emas ekan")
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.product_id} set  counts = '{pro.counts}' where id = {pro.id}")
            conn.commit()
            conn.close()

    def pro_objects_to_check(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT product_id from {self.product_id}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    ####SINF UCHUN
    def pro_object():
        list1 = list()
        for cook in Cook.objects():
            conn = sqlite3.connect(db_name)
            cursor = conn.execute(f"SELECT * from {cook.product_id}")
            for row in cursor:
                list1.append(row[1])
            conn.close()
        return list1


    def pro_objects(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {self.product_id}")
        list1 = list()
        for row in cursor:
            list1.append(Pro(row[1], row[2], row[0]))
        conn.close()
        return list1

    def pro_get_by_id(self,id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {self.product_id} Where id={id}")
        sql_row = list(cursor)[0]
        sel_drink = Pro(sql_row[1], sql_row[2], sql_row[0])
        conn.commit()
        conn.close()
        return sel_drink

    def pro_delete(self,id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.product_id} Where id='{id}'")
        conn.commit()
        conn.close()



    def __str__(self):
        return f"{self.name} {self.count} {self.price} {self.sale_price}"



class Drink(Basemodel):
    table = 'drink'
    def __init__(self,name,count=0,price=0,sale_price=0,sale_count=0,id = None):
        super().__init__()
        self.name = name
        self.count = count
        self.price = price
        self.sale_price = sale_price
        self.sale_count=sale_count
        self.id = id

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                f"INSERT INTO {self.table} (name,count,price,sale_price,sale_count) VALUES ('{self.name}', '{self.count}','{self.price}','{self.sale_price}', '{self.sale_count}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(f"UPDATE {self.table} set  name = '{self.name}', count='{self.count}',price='{self.price}',sale_price='{self.sale_price}', sale_count='{self.sale_count}' where id = {self.id}")
        conn.commit()
        conn.close()

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Drink.table}")
        list1 = list()
        for row in cursor:
            list1.append(Drink(row[1], row[2], row[3], row[4],row[5], row[0]))
        conn.close()
        return list1

    def objects_to_check():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT name from {Drink.table}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {Drink.table} Where id={id}")
        sql_row = list(cursor)[0]
        sel_drink = Drink(sql_row[1], sql_row[2], sql_row[3], sql_row[4],sql_row[5], sql_row[0])
        conn.commit()
        conn.close()
        return sel_drink


    def __str__(self):
        return f"{self.name} {self.count}  {self.price} {self.sale_price}"


class Product(Basemodel):
    table = 'product'
    def __init__(self,name,count = 0,price = 0,id = None):
        super().__init__()
        self.id = id
        self.name = name
        self.count = count
        self.price = price

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO {self.table} (name,count,price) VALUES ('{self.name}', '{self.count}','{self.price}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(f"UPDATE {self.table} set  name = '{self.name}', count = '{self.count}',price = '{self.price}' where id = {self.id}")
        conn.commit()
        conn.close()

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Product.table}")
        list1 = list()
        for row in cursor:
            list1.append(Product(row[1], row[2], row[3], row[0]))
        conn.close()
        return list1

    def objects_to_check():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT name from {Product.table}")
        list1 = list()
        for row in cursor:
            list1.append(row[0])
        conn.close()
        return list1

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from {Product.table} Where id={id}")
        sql_row = list(cursor)[0]
        sel_product = Product(sql_row[1],sql_row[2],sql_row[3], sql_row[0])
        conn.commit()
        conn.close()
        return sel_product


    def __str__(self):
        return f"{self.name} {self.count} {self.price}"


class Pro(Basemodel):
    def __init__(self,product_id,counts = 0,id = None):
        super().__init__()
        self.id = id
        self.product_id = product_id
        self.counts = counts

    @property
    def product_name(self):
        product = Product.get_by_id(self.product_id)
        return product.name

    def __str__(self):
        return f"{self.product_name} {self.counts}"


class Order(Basemodel):
    def __init__(self, cook_id=0, drink_id=0,name='',count=0,price=0,sale_price=0,table_id=0,type1=0,waiter_prot=0, id=None):
        super().__init__()
        self.id = id
        self.cook_id = cook_id
        self.drink_id = drink_id
        self.name = name
        self.count = count
        self.price = price
        self.sale_price = sale_price
        self.table_id = table_id
        self.type1 = type1
        self.waiter_prot = waiter_prot

    def get_by_order_name(name):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {name}")
        list1 = list()
        for row in cursor:
            list1.append(Order(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[0]))
        conn.close()
        return list1



    def __str__(self):
        all = self.sale_price * self.count
        return f"{self.name} {self.count} {self.sale_price}  {all}"



class Baseorder(Basemodel):
    table = 'baseorder'
    def __init__(self, order_number, order_table_name, id=None):
        super().__init__()
        self.id = id
        self.order_number = order_number
        self.order_table_name = order_table_name

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO {self.table} (order_number,order_table_name) VALUES ('{self.order_number}','{self.order_table_name}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"UPDATE {self.table} set   order_number='{self.order_number}',order_table_name='{self.order_table_name}' where id = {self.id}")
        conn.commit()
        conn.close()

    def base_object():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Baseorder.table} Where id={1}")
        row = list(cursor)[0]
        base_order = Baseorder(row[1], row[2], row[0])
        conn.close()
        return base_order



class Orderedtables(Basemodel):
    table = "orderedtables"
    def __init__(self, name,id=None):
        super().__init__()
        self.id = id
        self.name = name
        self.table_id = 0

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO {self.table} (name) VALUES ('{self.name}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"UPDATE {self.table} set   name='{self.name}' where id = {self.id}")
        conn.commit()
        conn.close()

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Orderedtables.table}")
        list1 = list()
        for row in cursor:
            list1.append(Orderedtables(row[1], row[0]))
        conn.close()
        return list1

    def get_by_id(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Orderedtables.table} Where id={id}")
        row = list(cursor)[0]
        order = Orderedtables(row[1], row[0])
        conn.close()
        return order

    def delete(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Delete From {self.table} Where id='{self.id}'")
        conn.commit()
        conn.close()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"Drop Table {self.name}")
        conn.commit()
        conn.close()



    def __str__(self):
        buyurtma = f"{self.id}-buyurtma"
        return  buyurtma


class Maosh(Basemodel):
    table = "maosh"
    def __init__(self, cooker=0,waiter=0, id=None):
        super().__init__()
        self.id = id
        self.cooker = cooker
        self.waiter = waiter

    def objects():
        conn = sqlite3.connect(db_name)
        cursor = conn.execute(f"SELECT * from {Maosh.table} Where id={1}")
        row = list(cursor)[0]
        sel_manager = Maosh(row[1],row[2], row[0])
        conn.close()
        return sel_manager

    def save(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(f"INSERT INTO {self.table} (cooker,waiter )  VALUES ('{self.cooker}','{self.waiter}')")
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"UPDATE {self.table} set  cooker='{self.cooker}',waiter='{self.waiter}' where id = {self.id}")
        conn.commit()
        conn.close()

# maosh = Maosh()
# maosh.save()

# base = Baseorder(1,"orderedtables")
# base.save()

#########################################################################################

# table = Table(6,1,400000,5)
# table.save()
# manager = Manager()
# manager.save()
#

# conn = sqlite3.connect(db_name)
# cursor = conn.execute(f"SELECT cook_id from order_num_1")
# list1 = list()
# for row in cursor:
#     list1.append(row[0])
# conn.close()
# print(list1)
# if 1 in list1:
#     print("yes")
# else:
#     print("no")


# list1 = Table.check_isorderyes()
# print(list1)
