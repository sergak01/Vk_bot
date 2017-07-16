# Vk_bot
Бот для сообщества Вк с тематикой на тему кино.
Гарантирована робота на ОС семейства Windows с предустановленым 'Python' версии 3.5.

# Установка
Выполнить в консоли команду 'pip install vk_api'

# Скилы
1. Пересылка сообщений пользователей администратору сообщества (еще не полностью реализовано)
2. Бот имеет функцию быстрого ответа пользователю по его id
> Пример текста сообщения: id1 Привет, Павел Дуров!
> Пользователь получит только фразу которая стоит после id1.
> Важно: если пользователь не писал сообщесту или запретил отправлять себе сообщения - сообщение не будет отправлено!
3. Ответ на сообщение _привет_ с разьяснением возможных команд
4. Поиск по стене сообщества. Имееться 2 варианта команд
 * Команда 'найди (название фильма)' - выполняет поиск фильма по сообществу убирая с запроса слово _найди_
 * Команда '#жанр' - выполнит поиск фильмов по хештэгу указаному в команде
5. Присутствует алгоритм назначения админом для бота - еще не используеться
