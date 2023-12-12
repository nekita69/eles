import psycopg2

HOST_DB = 'localhost'
PORT_DB = '5432'
DB_NAME = 'elest_db' #Имя БД
USER = 'postgres' #Пользователь который работает с БД (в СУБД)
DB_PASS = '123451515' #Пароль от пользователя


class Manager:
    def __init__(self):
        self.connect = psycopg2.connect(host=HOST_DB, port=PORT_DB, dbname = DB_NAME , user= USER, password= DB_PASS)
        self.cursor = self.connect.cursor()
        #Таблица пользователей (Имя, Фамилия, Отчество)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INT PRIMARY KEY,
            login varchar(100),
            password varchar(100),
            f_name varchar(100), 
            s_name varchar(100), 
            t_name varchar(100),      
            is_admin boolean        
        );
                            

        CREATE OR REPLACE FUNCTION create_user(lgn varchar, pass varchar, f_nme varchar, s_nme varchar, t_nme varchar, adm boolean)
        RETURNS boolean
        AS $$
        DECLARE
            cnt_usn INT = 0; next_id INT;
        BEGIN
            SELECT COUNT(*) INTO cnt_usn FROM users WHERE lower(login) = lower(lgn);
            IF cnt_usn > 0 THEN
                RETURN false;
            END IF;
            SELECT MAX(user_id) INTO next_id FROM users;
            IF next_id IS null THEN next_id = 0;
            ELSE next_id = next_id + 1;
            END IF;
            INSERT INTO users VALUES(next_id, lgn, pass, f_nme, s_nme, t_nme, adm);
            RETURN true;
        END;
        $$ LANGUAGE plpgsql;
        """)
        self.connect.commit()


    def __del__(self): #Деструктор
        self.connect.commit()
        self.connect.close()


    def get_name(self, login, password):
        self.cursor.execute("SELECT * FROM users WHERE LOWER(login) = %s AND password = %s;", (login, password))
        res = self.cursor.fetchone()
        if(res != None):
            return {'s_name':res[4], 'f_name':res[3],'t_name':res[5], 'is_admin':res[6]}
        return None
    

    def create_teacher(self, data):
        self.cursor.execute("SELECT create_user(%s, %s, %s, %s, %s, %s)", (data['login'], data['password'], data['f_name'], data['s_name'], data['t_name'], data['is_admin']))
        #Проверяет на несовпадение login;
        res = self.cursor.fetchone()[0]
        if res:
            self.connect.commit()
        return res
    

    def delete_teacher(self, login):
        self.cursor.execute(f"DELETE FROM users WHERE login = '{login}';")
        self.connect.commit()
        return True