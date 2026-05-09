import sqlite3
import random

db = sqlite3.connect("test.db")
defaultRights= "books"
admRigts = "redactOther"
curs=db.cursor()
#Метод редактирования для суперюзера
def redactOtherUser(mailAdm, mail):
    curs.execute(f"SELECT * FROM users WHERE email = '{mailAdm}'")
    us=curs.fetchone()
    if(us[6]=="redactOther"):
        red= int(input("Что вы хотите обновить в пользователе: 1 2 3 4 5 6"))
        match red:
            case 1:
                curs.execute(f"UPDATE users SET {input("Введите новое имя")} WHERE email = '{mail}'")
            case 2:
                curs.execute(f"UPDATE users SET {input("Введите новую фамилию")} WHERE email = '{mail}'")
    else:
        print("Недостаточно прав")
    return
#Метод редактирования себя для пользователя, вместо кейсов будут входные данные с интерфейса
def redactItself(mail):
    red= int(input("Что вы хотите обновить в пользователе: 1 2 3 4 5 6"))
    match red:
            case 1:
                curs.execute(f"UPDATE users SET {input("Введите новое имя")} WHERE email = '{mail}'")
            case 2:
                curs.execute(f"UPDATE users SET {input("Введите новую фамилию")} WHERE email = '{mail}'")

    return

#Авторизация пользователя + изменения параметров для автологина все выводы должны идти на фронтэнд
def login(mail, pword):
    state = False
    curs.execute(f"SELECT * FROM users WHERE email = '{mail}'")
    tempuser=curs.fetchone()
    if((not(tempuser == None))and(tempuser[4]==1)):
        if((tempuser[3]==pword) and (tempuser[4]==1)):

            loginIdGen = random.randint(0, 2000)

            while((curs.execute(f"SELECT * FROM users WHERE auth_id = '{loginIdGen}'")==None)):
                loginIdGen = random.randint(0, 2000)

            with open("cookie.txt","w+") as f:
                f.write(str(loginIdGen))
            curs.execute(f"UPDATE users SET auth_id = {loginIdGen} WHERE email = '{mail}'")    

            return tempuser
    else:
        print("неверный логин или пароль")

# Автоматическая авторизация с запросом в БД
def autolog():
    with open("cookie.txt","r+") as f:
        authtoken = f.read()
    if(not(curs.execute(f"SELECT * FROM users WHERE auth_id = '{authtoken}'")==None)):
        curs.execute(f"SELECT * FROM users WHERE auth_id = '{authtoken}'")
        return curs.fetchone()
    else:
        return None
    
# Выход из сессии, + должен быть выход на фронтэнде
def logout(mail):
    curs.execute(f"UPDATE users SET auth_id = 'NotAuthorized' WHERE email = '{mail}'")
    return None

# Мягкое удаление
def softdelete(mail):
    curs.execute(f"UPDATE users SET is_active = 0 WHERE email = '{mail}'")
    return

# Регистрация обычного пользователя
def register():
    mail = input("Введите почту: ")
    name = input("Введите имя:")
    surname = input("Введите фамилию: ")
    firstPasswordInput = input("Введите пароль: ")
    secondPasswordInput = ""
    while(not(firstPasswordInput==secondPasswordInput)):
        secondPasswordInput = input("Введите пароль повторно: ")
    curs.execute(f"INSERT INTO users VALUES ('{name}', '{surname}', '{mail}', '{firstPasswordInput}', True, 'none', '{defaultRights}', 'none')")

# Тестовая БД
# curs.execute("DROP TABLE users")
# curs.execute("""CREATE TABLE users (
#              name text,
#              surname text,
#              email text,
#              password text,
#              is_active boolean,
#              rigts text,
#              resourses text,
#              auth_id text
#              )
            
# """)
# Тестовый юзер
#curs.execute("INSERT INTO users VALUES ('Олег', 'Олегов', 'ogeg@mail.ru', '12345', True, 'none', 'books', 'none')")

# Тест для входа в аккаунт
# autorised_user = login(input("Введите логин: "), input("Введите пароль: "))
# Тест для автолога
print(autolog())
db.commit()
db.close()