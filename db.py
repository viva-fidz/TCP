import sqlite3


def create_db():
    with sqlite3.connect('company.db3') as conn:
        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        cursor = conn.cursor()

        cursor.execute("""DROP table if exists Terminal""")
        cursor.execute("""DROP table if exists Partner""")
        cursor.execute("""DROP table if exists Payment""")

        cursor.execute("""
                         CREATE TABLE if not exists Terminal (
                                id  INTEGER PRIMARY KEY,
                                title TEXT, 
                                configuration TEXT,
                                comment TEXT,
                                pub_key TEXT   
                                );
                         """)

        cursor.execute("""               
                         CREATE TABLE if not exists Payment (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                datetime TEXT, 
                                terminal_id  INTEGER, 
                                transaction_id  INTEGER,
                                partner_id  INTEGER,
                                summ INTEGER,
                                FOREIGN KEY (terminal_id) REFERENCES Terminal(id) ON DELETE CASCADE,
                                FOREIGN KEY (partner_id) REFERENCES Partner(id) ON DELETE CASCADE
                                );
                         """)

        cursor.execute("""
                         CREATE TABLE if not exists Partner (
                                id INTEGER PRIMARY KEY, 
                                title TEXT, 
                                comment TEXT  
                                );
                         """)


class Terminal:
    def insert(self, terminal_id, title, configuration):
        """ Добавляет данные в БД
        """

        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                 insert into Terminal (id, title, configuration)
                 VALUES (?, ?, ?);""",
                           (terminal_id, title, configuration))

    def delete(self, terminal_id):
        """ Удаляет данные терминала из БД
        """

        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                delete from Terminal where id = ?;""",
                           (terminal_id,))

    def get_total_sum(self, terminal_id):
        """ Считает суммму прошедших через указанный терминал средств
        """

        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select sum(summ) from Payment where terminal_id = ?; """,
                           (terminal_id,))
        print('terminal_id =', terminal_id, 'sum:', cursor.fetchone())


class Payment:
    def insert(self, datetime, terminal_id, transaction_id, partner_id, summ):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                 insert into Payment (
                 datetime, terminal_id, transaction_id, partner_id, summ)
                 VALUES (?, ?, ?, ?, ?);""",
                           (datetime, terminal_id, transaction_id, partner_id, summ))

    def delete(self, transaction_id):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                delete from Payment where transaction_id = ?;""",
                           (transaction_id,))
            # print('payment transaction_id = {} delete ok'.format(transaction_id))

    def get_all_data(self):
        """ Выводит все данные обо всех платежах
        """

        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                select * from Payment"""),
            output = cursor.fetchall()

            while output:
                print(output)
                output = cursor.fetchall()


class Partner:
    def insert(self, partner_id, title, comment):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Partner (id, title, comment)
                VALUES (?, ?, ?);""",
                           (partner_id, title, comment))

    def delete(self, partner_id):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                delete from Partner where id = ?;""",
                           (partner_id,))
            # print('partner id = {} delete ok'.format(partner_id))

    def get_partners_total_sum(self):
        """ формирует выборку с итоговой задолжностью
        перед каждым из партнёров
        """

        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        select title, sum(summ) from Payment
                        inner join Partner on Payment.partner_id = Partner.id
                        group by title"""),
            output = cursor.fetchone()

            while output:
                print(output)
                output = cursor.fetchone()


if __name__ == "__main__":
    create_db()
