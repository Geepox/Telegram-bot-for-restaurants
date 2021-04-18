import mysql.connector


my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="restaurant_db"
)


def getInfo(table):
    global my_db
    cursor = my_db.cursor()
    sql = str(table)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def insertData(data, values):
    global my_db
    cursor = my_db.cursor()
    sql = str(data)
    val = tuple(values)
    cursor.execute(sql, val)
    my_db.commit()


def updateData(data, values):
    global my_db
    cursor = my_db.cursor()
    sql = str(data)
    val = tuple(values)
    cursor.execute(sql, val)
    my_db.commit()


def deleteData(data):
    global my_db
    cursor = my_db.cursor()
    sql = str(data)
    cursor.execute(sql)
    my_db.commit()


while True:
    print("PRESS 1 TO GET INFO FROM DB")
    print("PRESS 2 TO MODIFY DB")
    print("PRESS 0 TO EXIT")
    print('------------------------------------------------------------------')

    choice = input()

    if choice == "1":
        print("PRESS 1 TO GET INFO ABOUT RESTAURANTS")
        print("PRESS 2 TO GET INFO ABOUT FOODS")
        print("PRESS 3 TO GET INFO ABOUT FOOD_TYPES")
        print("PRESS 4 TO GET INFO ABOUT BASKET")
        print("PRESS 0 TO BACK TO THE MAIN MENU")
        print('------------------------------------------------------------------')

        choice_1 = input()

        if choice_1 == "1":
            restaurants = "select * from restaurants"
            result = getInfo(restaurants)
            for i in result:
                for j in i:
                    print(j, end='|')
                print()
            print('------------------------------------------------------------------')
            print()

        elif choice_1 == "2":
            foods = "select fd.id, fd.name, fd.price, fd.description, ft.name, rs. name from foods fd " \
                          "left join restaurants rs on fd.restaurant_id = rs.id " \
                          "left join food_types ft on ft.id = fd.food_type_id"
            result = getInfo(foods)
            for i in result:
                for j in i:
                    print(j, end='|')
                print()
            print('------------------------------------------------------------------')
            print()

        elif choice_1 == "3":
            food_types = "select * from food_types"
            result = getInfo(food_types)
            for i in result:
                for j in i:
                    print(j, end='|')
                print()
            print('------------------------------------------------------------------')
            print()

        elif choice_1 == "4":
            basket = "select * from basket"
            result = getInfo(basket)
            for i in result:
                for j in i:
                    print(j, end='|')
                print()
            print('------------------------------------------------------------------')
            print()

    elif choice == '2':
        print("PRESS 1 TO INSERT DATA")
        print("PRESS 2 TO UPDATE DATA")
        print("PRESS 3 TO DELETE DATA")
        print("PRESS 0 TO BACK TO THE MAIN MENU")
        print('------------------------------------------------------------------')

        choice_2 = input()

        if choice_2 == '1':
            print("PRESS 1 TO INSERT DATA ABOUT RESTAURANTS")
            print("PRESS 2 TO INSERT DATA ABOUT FOODS")
            print("PRESS 3 TO INSERT DATA ABOUT FOOD_TYPES")
            print("PRESS 0 TO BACK TO THE MAIN MENU")
            print('------------------------------------------------------------------')

            choice_3 = input()

            if choice_3 == "1":
                insert = "insert into restaurants(id, name, address) " \
                       "values(NULL, %s, %s)"
                value = []
                a = input("INSERT RESTAURANT NAME\n")
                value.append(a)
                a = input("INSERT RESTAURANT ADDRESS\n")
                value.append(a)
                insertData(insert, value)
                print("DATA INSERTED SUCCESSFUL\n----------------------------------------")
                print()

            elif choice_3 == "2":
                insert = "insert into foods(id, name, price, description, food_type_id, restaurant_id) " \
                       "values(NULL, %s, %s, %s, %s, %s)"
                value = []
                a = input("INSERT FOOD NAME\n")
                value.append(a)
                a = input("INSERT FOOD PRICE\n")
                value.append(a)
                a = input("INSERT FOOD DESCRIPTION\n")
                value.append(a)
                a = input("INSERT FOOD TYPE_ID\n")
                value.append(a)
                a = input("INSERT RESTAURANT_ID\n")
                value.append(a)
                insertData(insert, value)
                print("DATA INSERTED SUCCESSFUL\n----------------------------------------")
                print()

            elif choice_3 == "3":
                insert = "insert into food_types(id, name) " \
                       "values(NULL, %s)"
                value = []
                a = input("INSERT TYPE OF FOOD\n")
                value.append(a)
                insertData(insert, value)
                print("DATA INSERTED SUCCESSFUL\n----------------------------------------")
                print()

        elif choice_2 == '2':
            print("PRESS 1 TO UPDATE DATA ABOUT RESTAURANTS")
            print("PRESS 2 TO UPDATE DATA ABOUT FOODS")
            print("PRESS 0 TO BACK TO THE MAIN MENU")
            print('------------------------------------------------------------------')

            choice_4 = input()

            if choice_4 == '1':
                value = []
                a = input("INSERT ID OF RESTAURANT\n")
                b = input("INSERT NEW RESTAURANT NAME\n")
                value.append(b)
                b = input("INSERT NEW RESTAURANT ADDRESS\n")
                value.append(b)
                update = "update restaurants set name = %s, address = %s where id = " + str(a)
                updateData(update, value)
                print("DATA UPDATED SUCCESSFUL\n----------------------------------------")
                print()

            elif choice_4 == '2':
                value = []
                a = input("INSERT ID OF FOOD\n")
                b = input("INSERT NEW PRICE OF FOOD\n")
                value.append(b)
                b = input("INSERT NEW DESCRIPTION OF FOOD\n")
                value.append(b)
                update = "update foods set price = %s, description = %s where id = " + str(a)
                updateData(update, value)
                print("DATA UPDATED SUCCESSFUL\n----------------------------------------")
                print()

        elif choice_2 == '3':
            print("PRESS 1 TO DELETE DATA FROM RESTAURANTS")
            print("PRESS 2 TO DELETE DATA FROM FOODS")
            print("PRESS 3 TO DELETE DATA FROM FOOD TYPES")
            print("PRESS 0 TO BACK TO THE MAIN MENU")
            print('------------------------------------------------------------------')

            choice_5 = input()

            if choice_5 == '1':
                a = int(input("INSERT ID OF RESTAURANT\n"))
                delete = "delete from restaurants where id = " + str(a)
                deleteData(delete)
                print("DATA WAS DELETED\n----------------------------------------")
                print()

            elif choice_5 == '2':
                a = int(input("INSERT ID OF FOOD\n"))
                delete = "delete from foods where id = " + str(a)
                deleteData(delete)
                print("DATA WAS DELETED\n----------------------------------------")
                print()

            elif choice_5 == '3':
                a = int(input("INSERT ID OF FOOD TYPE\n"))
                delete = "delete from food_types where id = " + str(a)
                deleteData(delete)
                print("DATA WAS DELETED\n----------------------------------------")
                print()

    elif choice == "0":
        break
