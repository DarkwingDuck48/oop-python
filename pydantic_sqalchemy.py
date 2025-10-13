from pydantic_sqlalchemy import (
    DatabaseService,
    MessageCreate,
    MessageService,
    UserCreate,
    UserService,
)


def main():
    # Инициализация сервисов
    db_service = DatabaseService()
    user_service = UserService(db_service)
    message_service = MessageService(db_service)

    # Создаем таблицы
    db_service.create_tables()

    print('\n' + '=' * 50)
    print('👥 СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ')
    print('=' * 50)

    try:
        # Создаем пользователей
        alice = user_service.create_user(UserCreate(username='alice123', email='alice@example.com'))

        bob = user_service.create_user(UserCreate(username='bob456', email='bob@example.com'))

        # Пытаемся создать дубликат (должна быть ошибка)
        try:
            user_service.create_user(UserCreate(username='alice123', email='another@example.com'))
        except ValueError as e:
            print(f'❌ Ожидаемая ошибка: {e}')

    except Exception as e:
        print(f'❌ Ошибка при создании пользователей: {e}')
        return

    print('\n' + '=' * 50)
    print('💬 СОЗДАЕМ СООБЩЕНИЯ')
    print('=' * 50)

    try:
        # Создаем сообщения
        messages_data = [
            MessageCreate(user_id=alice.id, message_text='Привет всем! Как дела?'),
            MessageCreate(user_id=alice.id, message_text='Кто хочет пиццы? 🍕'),
            MessageCreate(user_id=bob.id, message_text='Привет, Алис! У меня все отлично!'),
            MessageCreate(user_id=bob.id, message_text='Я за пиццу! 🍕'),
            MessageCreate(user_id=alice.id, message_text='Отлично! Заказываем!'),
        ]

        for msg_data in messages_data:
            message_service.create_message(msg_data)

    except Exception as e:
        print(f'❌ Ошибка при создании сообщений: {e}')
        return

    print('\n' + '=' * 50)
    print('📊 ВЫВОДИМ РЕЗУЛЬТАТЫ')
    print('=' * 50)

    # Показываем всех пользователей
    print('\n👥 ВСЕ ПОЛЬЗОВАТЕЛИ:')
    users = user_service.get_all_users()
    for user in users:
        print(f'  {user.id}. {user.username} ({user.email}) - создан {user.created_at}')

    # Показываем все сообщения
    print('\n💬 ВСЕ СООБЩЕНИЯ:')
    messages = message_service.get_all_messages()
    for msg in messages:
        print(f'  {msg.user.username}: {msg.message_text} ({msg.created_at})')

    # Показываем сообщения Алисы
    print('\n📨 СООБЩЕНИЯ АЛИСЫ:')
    alice_messages = message_service.get_user_messages(alice.id)
    for msg in alice_messages:
        print(f'  {msg.created_at}: {msg.message_text}')

    # Статистика
    print('\n📈 СТАТИСТИКА:')
    stats = message_service.get_conversation_stats()
    for username, count, last_msg in stats:
        print(f'  {username}: {count} сообщений, последнее: {last_msg}')


# --- FastAPI-подобное использование ---
def demonstrate_fastapi_style():
    """Показывает как это будет выглядеть в FastAPI"""

    db_service = DatabaseService()
    user_service = UserService(db_service)

    # Эмуляция FastAPI endpoint
    def create_user_endpoint(user_data: UserCreate):
        try:
            user = user_service.create_user(user_data)
            return {
                'status': 'success',
                'data': user.model_dump(),
                'message': 'Пользователь создан успешно',
            }
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}

    # Тестируем
    print('\n' + '=' * 50)
    print('🚀 ДЕМОНСТРАЦИЯ FASTAPI СТИЛЯ')
    print('=' * 50)

    result = create_user_endpoint(UserCreate(username='charlie789', email='charlie@example.com'))
    print(f'Результат создания пользователя: {result}')


if __name__ == '__main__':
    main()
    demonstrate_fastapi_style()
