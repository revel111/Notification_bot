import sqlite3


def sql_start() -> None:
    global base, cur
    base = sqlite3.connect('notification.db')
    cur = base.cursor()

    if base:
        print('Database was connected')

    base.execute('CREATE TABLE IF NOT EXISTS User_preferences(ID INTEGER, WORD TEXT, PRIMARY KEY(ID, WORD))')
    base.commit()


async def sql_add_words(words, id) -> None:
    for word in words:
        cur.execute('INSERT OR IGNORE INTO User_preferences VALUES(?, ?)', (id, word,))
        base.commit()


async def sql_print_words(id) -> str:
    cur.execute('SELECT WORD FROM User_preferences WHERE ID = ?', (id,))
    found = cur.fetchall()

    if not found:
        return 'You do not have any tracked words. Use command /add_words to add words to be tracked.\n'

    answer = 'Your key-words: '

    for fo in found:
        answer += fo[0] + ' '

    return answer


async def sql_delete_words(id) -> None:
    cur.execute('DELETE FROM User_preferences WHERE ID = ?', (id,))
    base.commit()


async def sql_find_user(words) -> list:
    user_id_list = []

    for word in words:
        cur.execute('SELECT ID FROM User_preferences WHERE WORD = ?', (word,))
        results = cur.fetchall()

        for result in results:
            user_id_list.append(result[0])

    return user_id_list
