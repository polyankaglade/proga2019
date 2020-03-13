import json
import random

class FlashCards():
    def __init__(self, path_to_file: str):
        '''
        Прочитает пары слов из указанного файла в формате json.
        Создаст все требующиеся атрибуты.
        '''

        with open(path_to_file, 'r', encoding='utf-8') as f:
            self.__translations = json.load(f)

        pass

    @property
    def words(self):
        return sorted(list(self.__translations.keys()))

    def play(self) -> str:
        '''
        Выдает русские слова из словаря в рандомном порядке,
        сверяет введенный пользователем перевод с правильным
        (регистр введенного слова при этом не важен),
        пока слова в словаре не закончатся.
        Возвращает строку с количеством правильных ответов/общим количеством
        слов в словаре (см пример работы).
        '''
        if len(self.__translations.keys()) < 1:
            print("Dictionary is empty!")

        else:
            score = 0
            print("Начало игры.")
            game = self.words
            random.shuffle(game)
            for word in game:
                print(word)
                answer = str(input('')).lower()
                if answer == self.__translations[word]:
                    score += 1
            return "Done! %s out of %s words correct" % (str(score), str(len(self.words)))

    def add_word(self, russian: str, english: str) -> str:
        '''
        Добавляет в словарь новую пару слов,
        если русского слова еще нет в словаре.
        Возвращает строку в зависимоти от результата (см пример работы).
        '''
        if type(russian) != str or type(english) != str:
            return "That's not a word"
        else:
            if russian not in self.__translations.keys():
                self.__translations[russian] = english
                return "Succesfully added word " + "'" + russian + "'"
            else:
                return "'" + russian + "'" + " already in dictionary."

    def delete_word(self, russian: str) -> str:
        '''
        Удаляет из словаря введенное русское слово
        и соответсвующее ему английское.
        Возвращает строку в зависимоти от результата (см пример работы).
        '''
        if type(russian) != str:
            return "That's not a word"
        else:
            if russian not in self.__translations.keys():
                return "'%s' is not in dictionary" % (russian)
            else:
                del self.__translations[russian]
                return "Succesfully deleted word '%s'" % (russian)
