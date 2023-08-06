from .rules_dictionary import RulesDictionary
from .alphabet import Alphabet

class SemiThueSystem():
    def __init__(self, axiom: str, rules_dictionary: RulesDictionary):
        self._alphabet = Alphabet(rules_dictionary.alphabet)
        self._dictionary = rules_dictionary.dictionary
        self._interactions = [ axiom ]

        if not self.valid_axiom(self._interactions[0]):
            raise Exception(f"This axiom { self._interactions[0] } is not valid")

    @property
    def alphabet(self):
        return self._alphabet.symbols

    @property
    def dictionary(self):
        return self._dictionary

    @property
    def interactions(self):
        return self._interactions

    def valid_axiom(self, axiom: str):
        return False not in map(lambda symbol: self._alphabet.has(symbol), axiom)

    def replace(self, string: str):
        if not self.valid_axiom(string):
            raise Exception(f"This axiom { string } is not valid")
        
        return "".join(map(lambda symbol: self._dictionary[symbol], string))
    
    def interact(self):
        current_axiom = self._interactions[len(self._interactions) - 1]
        interaction = self.replace(current_axiom)
        self._interactions.append(interaction)

        return interaction

if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B", "C" })
    rules_dictionary = RulesDictionary(alphabet)
    rules_dictionary.register({
        "of": "A",
        "to": "AB"
    })
    semiThueSystem = SemiThueSystem("ABC", rules_dictionary)
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())
    print(semiThueSystem.interact())

