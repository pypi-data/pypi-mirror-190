from .alphabet import Alphabet
from typing import TypedDict
from typing import Dict

Rule = TypedDict("Rule", { "of": str, "to": str })

class RulesDictionary():
    def __init__(self, alphabet: Alphabet):
        self._alphabet = alphabet
        self._dictionary: Dict[str, str] = dict()

        self._initialize_dictionary()

    def _initialize_dictionary(self):
        for symbol in self._alphabet.symbols:
            self._dictionary[symbol] = symbol

    def register(self, rule: Rule):
        if not self._alphabet.has(rule["of"]):
            raise Exception("The symbol {} is not in the alphabet".format(rule["of"]))
        
        if False in map(lambda symbol: self._alphabet.has(symbol), rule["to"]):
            raise Exception("There is a symbol that does not belong to the alphabet in {}".format(rule["to"]))


        self._dictionary[rule["of"]] = rule["to"]

        return self

    @property
    def dictionary(self):
        return self._dictionary

    @property
    def alphabet(self):
        return self._alphabet.symbols

if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B", "C" })

    rules_dictionary = RulesDictionary(alphabet)

    rules_dictionary.register({
        "of": "A",
        "to": "C"
    })

    print(rules_dictionary.dictionary)
    
    rules_dictionary.register({
        "of": "F",
        "to": "C"
    })

