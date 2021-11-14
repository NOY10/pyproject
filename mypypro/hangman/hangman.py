import random
from wordforhangman import words
import string

def get_valid_word(words):
    word=random.choice(words)
    while '-' in word and ' ' in word:
        word=random.choice(words)
    return word.upper()

def hangman():
    word=get_valid_word(words)
    word_letters=set(word)
    alphabet=set(string.ascii_uppercase)
    used_letters=set()
    lives=6

    while(len(word_letters)>0 and lives>0):
        print("you have", lives, "you have used these letters"," ".join(used_letters))
        word_list=[letter if letter in used_letters else "_" for letter in word ]
        print("current word",' '.join(word_list))
        
        user_letter=input().upper()
        if user_letter in alphabet-used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives-=1
                print("letter is not in the word")
        elif user_letter in used_letters:
            print("you have use it already")
        else:
          print("error")
    if lives==0:
        print("you died the word was", word)
    else:
        print('You guessed the word ', word, "!!")

hangman()
    