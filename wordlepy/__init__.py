import requests
import re
import json
from collections import Counter


class Wordle:
    def __init__(self, dont=False):
        self.getWordsList()
        self.letters_possibilities = {i: list({chr(97+j) for j in range(26)}) for i in range(5)}
        self.constraint_letters = []
        self.guesses = 0
        self.dont = dont
        word = self.nextWord()
        print("Picking a word out of the {} possibilities…".format(len(self.words)))
        print("> {}".format(word))
        while True:
            response = input("Response from wordle (* for missed letter, lower case for correct letter, wrong location, capital for correct letter and location:\n# ")
            if len(response) != 5:
                print("Incorrect response length, 5 characters expected.\n")
                continue
            if response.upper() == response and '*' not in response:
                print("Congrats, you found the solution '{}' in {} guesses!".format(word.upper(), self.guesses))
                break
            word = self.nextWord(word, response)
            print("Picking a word out of the {} possibilities…".format(len(self.words)))
            print("> {}".format(word))
            if len(self.words) <= 1:
                print("Congrats, you found the solution '{}' in {} guesses!".format(word.upper(), self.guesses))
                break

    def getLetterFreqs(self):
        return [
            dict(Counter([word[i] for word in self.words]).most_common())
        for i in range(5)]

    def getWordsList(self):
        mainpage = requests.get("https://www.nytimes.com/games/wordle/index.html")
        m = re.search(re.compile('src="https://www\.nytimes\.com/games-assets/v2/wordle\.([^"]+).js"'), mainpage.content.decode())
        data = requests.get("https://www.nytimes.com/games-assets/v2/wordle.{}.js".format(m.group(1)))
        m = re.search(re.compile("var [A-Za-z]=(\\[[^\\]]+\\])"), data.content.decode())
        self.words = json.loads(m.group(1))

    # We clean up the list of words we currently have, to remove the latest try and clean up based on feedback
    # eg filterOut(words, "slate", "*latE") means we got the E right, lat wonr location and s wrong
    def updateLetterSets(self, tried, response):
        for i in range(5):
            letter = response[i]
            if letter == '*':
                if tried[i] in self.constraint_letters:
                    self.letters_possibilities[i].remove(tried[i])
                else:
                    for j in self.letters_possibilities:
                        if tried[i] in self.letters_possibilities[j]:
                            self.letters_possibilities[j].remove(tried[i])
            elif letter >= 'A' and letter <= 'Z': # Proper position
                self.letters_possibilities[i] = {letter.lower()}
                if letter not in self.constraint_letters:
                    self.constraint_letters.append(letter.lower())
            else: # Wrong position
                if letter in self.letters_possibilities[i]:
                    self.letters_possibilities[i].remove(letter)
                if letter not in self.constraint_letters:
                    self.constraint_letters.append(letter)
    
    def letterSetsToRegex(self):
        return re.compile("^[{}][{}][{}][{}][{}]".format(
                ''.join(self.letters_possibilities[0]),
                ''.join(self.letters_possibilities[1]),
                ''.join(self.letters_possibilities[2]),
                ''.join(self.letters_possibilities[3]),
                ''.join(self.letters_possibilities[4]),
            ))
    
    def filterWords(self):
        pattern = self.letterSetsToRegex()
        newwords = []
        for word in self.words:
            if sum([l in word for l in self.constraint_letters]) == len(self.constraint_letters) and re.match(pattern, word):
                newwords.append(word)
        self.words = newwords
        
    def rankWords(self, freqs):
        wordscores = {}
        for word in self.words:
            wordscores[word] = 0
            for i in range(5):
                wordscores[word] += freqs[i][word[i]]
        return wordscores
    
    def nextWord(self, tried=None, response=None):
        if tried != None and response != None:
            self.updateLetterSets(tried, response)
        self.filterWords()
        freqs = self.getLetterFreqs()
        wordscores = self.rankWords(freqs)
        nextword = sorted(wordscores, key=lambda x: wordscores[x], reverse=(not self.dont))[0]
        self.guesses += 1
        return nextword
        
