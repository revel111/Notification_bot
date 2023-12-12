def read_dictionary() -> set:
    dictionary = set()

    with open('dictionary.txt', encoding='utf-8') as dictionary_file:
        for word in dictionary_file:
            dictionary.add(word[0:len(word) - 1])

    return dictionary
