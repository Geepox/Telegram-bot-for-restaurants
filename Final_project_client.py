import telebot
import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="restaurant_db"
)


token = '1693242280:AAGZUc4AzNdzRkdWAR_FSla4H0Ca4BMHbM8'

bot = telebot.TeleBot(token)


def getAllFoodTypes():
    global my_db
    cursor = my_db.cursor()

    sql = "SELECT * FROM food_types"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getAllRestaurants():
    global my_db
    cursor = my_db.cursor()

    sql = "SELECT * FROM restaurants"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getFoodsByRestaurantId(rest_id):
    global my_db
    cursor = my_db.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.food_type_id, ft.name as foodType, " \
          "r.name as restaurantName " \
        "FROM foods f " \
        "LEFT OUTER JOIN food_types ft ON ft.id = f.food_type_id " \
        "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
        "WHERE f.restaurant_id = "+str(rest_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getFoodByFoodType(ft_id):
    global my_db
    cursor = my_db.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.food_type_id, " \
          "ft.name as foodType, r.name as restaurantName " \
        "FROM foods f " \
        "LEFT OUTER JOIN food_types ft ON ft.id = f.food_type_id " \
        "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
        "WHERE f.food_type_id = "+str(ft_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getFood(food_id):
    global my_db
    cursor = my_db.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.food_type_id, ft.name as foodType, " \
          "r.name as restaurantName " \
        "FROM foods f " \
        "LEFT OUTER JOIN food_types ft ON ft.id = f.food_type_id " \
        "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
        "WHERE f.id = "+str(food_id)

    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def insert_to_basket(data, value):
    global my_db
    cursor = my_db.cursor()

    sql = data
    val = tuple(value)
    cursor.execute(sql, val)
    my_db.commit()


def get_all(user_id):
    global my_db
    cursor = my_db.cursor()

    sql = user_id
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def total_price(user_id):
    global my_db
    cursor = my_db.cursor()

    sql = user_id
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def update_flag(data):
    global my_db
    cursor = my_db.cursor()

    sql = data
    cursor.execute(sql)
    my_db.commit()


menu = "main"


@bot.message_handler(content_types=["text"])
def handle_text(message):

    global menu

    if message.text.lower() == "/start":
        text = ""
        text = text + "#########################\n"
        text = text + "Добро пожаловать в сервис заказа еды\n"
        text = text + "#########################\n"
        text = text + "Выберите опцию поиска: \n"
        text = text + "1 - Поиск по типу еды\n"
        text = text + "2 - Поиск по ресторану\n"

        bot.send_message(message.chat.id, text)
        menu = "main"

    else:

        if menu == "main":
            if message.text.lower() == "1":
                allFoodTypes = getAllFoodTypes()
                text = "#####################\n"
                for food in allFoodTypes:
                    text = text+str(food[0]) + ") " + food[1] + "\n"
                menu = "choose_by_food_type"
                bot.send_message(message.chat.id, text)

            elif message.text.lower() == "2":
                allRestaurants = getAllRestaurants()
                text = "#####################\n"
                for rest in allRestaurants:
                    text = text + str(rest[0]) + ") " + rest[1] + "\n"
                menu = "choose_by_restaurant"
                bot.send_message(message.chat.id, text)

        elif menu == "choose_by_food_type":
            menu = "another_one"
            id = message.text.lower()
            foods = getFoodByFoodType(id)
            text = "#####################\n"
            for food in foods:
                text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[7] + "\n"

            bot.send_message(message.chat.id, text)

        elif menu == "choose_by_restaurant":
            menu = "another_one"
            food_id = message.text.lower()
            foods = getFoodsByRestaurantId(food_id)
            text = "#####################\n"
            for food in foods:
                text = text+str(food[0]) + ") " + food[1] + " " + str(food[2])+" KZT - " + food[6] + "\n"

            bot.send_message(message.chat.id, text)

        elif menu == "another_one":
            menu = "choose_food"
            values = []
            id = message.text.lower()
            food = getFood(id)
            insert = "insert into basket(id, user_id, count_food, food_id, total) " \
                     "values(NULL, %s, %s, %s, %s)"
            values.append(message.chat.id)
            values.append(1)
            values.append(food[0])
            values.append(food[2])
            insert_to_basket(insert, values)
            text = "#####################\n"
            text = text + "Ваш заказ добавлен в корзину\n"
            text = text + "Нажмите start для продолжения\n"
            text = text + "Нажмите stop для оплаты\n"
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("/start", "stop")
            bot.send_message(message.from_user.id, text, reply_markup=user_markup)

        elif menu == "choose_food":
            list_of_orders = ""
            user_id = "SELECT f.name, total * sum(count_food), f.description, sum(b.count_food) " \
                      "FROM basket b left JOIN foods f on b.food_id = f.id " \
                      "WHERE Flag = '' and user_id = " + str(message.chat.id) + " GROUP by f.name"
            food = total_price(user_id)
            all = "SELECT sum(b.total * b.count_food) " \
                "FROM basket b " \
                "where b.Flag = '' and b.user_id = " + str(message.chat.id)
            total = get_all(all)
            for i in food:
                text = i[0] + " " + str(i[3]) + " шт " + " за " + str(i[1])+" KZT\n"
                text = text+"Состав: ["+i[2] + "] \n"
                list_of_orders += text
            bot.send_message(message.chat.id, "Вы заказали: ")
            bot.send_message(message.chat.id, list_of_orders)
            text_1 = "К оплате: " + str(total[0]) + " KZT\n"
            text_1 = text_1 + "Спасибо за покупку\n"
            update = "update basket set flag = 1 where user_id = " + str(message.chat.id)
            update_flag(update)
            hide_markup = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, text_1, reply_markup=hide_markup)


bot.polling(none_stop=True, interval=0)
