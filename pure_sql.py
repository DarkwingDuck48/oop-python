import sqlite3


def create_database():
    """Создание базы данных и таблиц"""

    # Подключаемся к базе (создается автоматически если не существует)
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()

    # Создаем таблицу Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Создаем таблицу Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
    )
    """)

    # Создаем индекс для ускорения поиска по user_id
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_messages_user_id 
    ON Messages (user_id)
    """)

    conn.commit()
    print('✅ База данных и таблицы созданы успешно!')
    return conn, cursor


def add_users(cursor):
    """Добавляем пользователей в базу"""

    users = [('alice123', 'alice@example.com'), ('bob456', 'bob@example.com')]

    try:
        cursor.executemany(
            """
        INSERT INTO Users (username, email) 
        VALUES (?, ?)
        """,
            users,
        )
        print('✅ Пользователи добавлены успешно!')
    except sqlite3.IntegrityError as e:
        print(f'⚠️ Ошибка при добавлении пользователей: {e}')


def add_messages(cursor):
    """Добавляем сообщения от пользователей"""

    # Сначала получим ID пользователей
    cursor.execute('SELECT id, username FROM Users')
    users = cursor.fetchall()

    if not users:
        print('❌ Нет пользователей в базе!')
        return

    user_ids = {username: user_id for user_id, username in users}
    print(f'📋 Найдены пользователи: {user_ids}')

    messages = [
        (user_ids['alice123'], 'Привет всем! Как дела?'),
        (user_ids['alice123'], 'Кто хочет пиццы? 🍕'),
        (user_ids['bob456'], 'Привет, Элис! У меня все отлично!'),
        (user_ids['bob456'], 'Я за пиццу! 🍕'),
        (user_ids['alice123'], 'Отлично! Заказываем!'),
    ]

    cursor.executemany(
        """
    INSERT INTO Messages (user_id, message_text) 
    VALUES (?, ?)
    """,
        messages,
    )

    print('✅ Сообщения добавлены успешно!')


def display_data(cursor):
    """Показываем все данные из базы"""

    print('\n' + '=' * 50)
    print('📊 ДАННЫЕ ИЗ БАЗЫ:')
    print('=' * 50)

    # Показываем пользователей
    print('\n👥 ПОЛЬЗОВАТЕЛИ:')
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    for user in users:
        print(f'ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}')

    # Показываем сообщения с именами пользователей
    print('\n💬 СООБЩЕНИЯ:')
    cursor.execute("""
    SELECT m.id, u.username, m.message_text, m.created_at 
    FROM Messages m
    JOIN Users u ON m.user_id = u.id
    ORDER BY m.created_at
    """)
    messages = cursor.fetchall()

    for msg in messages:
        print(f'ID: {msg[0]}, User: {msg[1]}, Message: {msg[2]}, Time: {msg[3]}')


def demonstrate_relationships(cursor):
    """Демонстрируем связи между таблицами"""

    print('\n' + '=' * 50)
    print('🔗 ДЕМОНСТРАЦИЯ СВЯЗЕЙ:')
    print('=' * 50)

    # Сколько сообщений у каждого пользователя
    print('\n📈 СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ:')
    cursor.execute("""
    SELECT u.username, COUNT(m.id) as message_count
    FROM Users u
    LEFT JOIN Messages m ON u.id = m.user_id
    GROUP BY u.id
    ORDER BY message_count DESC
    """)

    stats = cursor.fetchall()
    for username, count in stats:
        print(f'👤 {username}: {count} сообщений')

    # Все сообщения конкретного пользователя
    print('\n📨 СООБЩЕНИЯ АЛИС:')
    cursor.execute("""
    SELECT m.message_text, m.created_at
    FROM Messages m
    JOIN Users u ON m.user_id = u.id
    WHERE u.username = 'alice123'
    ORDER BY m.created_at
    """)

    alice_messages = cursor.fetchall()
    for i, (text, time) in enumerate(alice_messages, 1):
        print(f'{i}. {text} ({time})')


def advanced_queries(cursor):
    """Продвинутые запросы для демонстрации возможностей"""

    print('\n' + '=' * 50)
    print('🎯 ПРОДВИНУТЫЕ ЗАПРОСЫ:')
    print('=' * 50)

    # Последнее сообщение каждого пользователя
    print('\n🕒 ПОСЛЕДНИЕ СООБЩЕНИЯ:')
    cursor.execute("""
    SELECT u.username, m.message_text, m.created_at
    FROM Messages m
    JOIN Users u ON m.user_id = u.id
    WHERE m.created_at = (
        SELECT MAX(created_at) 
        FROM Messages 
        WHERE user_id = u.id
    )
    """)

    last_messages = cursor.fetchall()
    for username, text, time in last_messages:
        print(f"👤 {username}: '{text}' ({time})")


def main():
    """Основная функция"""

    try:
        # Создаем базу и таблицы
        conn, cursor = create_database()

        # Добавляем данные
        add_users(cursor)
        add_messages(cursor)

        # Показываем результаты
        display_data(cursor)
        demonstrate_relationships(cursor)
        advanced_queries(cursor)

        # Сохраняем изменения
        conn.commit()

    except sqlite3.Error as e:
        print(f'❌ Ошибка SQLite: {e}')
    finally:
        # Всегда закрываем соединение
        if 'conn' in locals():
            conn.close()
            print('\n🔒 Соединение с базой закрыто')


# Дополнительные утилиты
def test_database():
    """Тестируем базу данных отдельно"""
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()

    # Проверяем что таблицы существуют
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('\n📋 ТАБЛИЦЫ В БАЗЕ:')
    for table in tables:
        print(f' - {table[0]}')

    conn.close()


if __name__ == '__main__':
    main()

    # Дополнительная проверка
    print('\n' + '=' * 50)
    test_database()
