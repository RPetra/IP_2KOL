from pj import *
class DG(enum.Enum):
    OR, ONAND, ZNAND, NOT, OZAG, ZZAG = "+[]'()"
    class VAR(Token):
        def vrijednost(self, **interpretacija):
            try: return interpretacija[self.sadržaj]
            except KeyError: self.nedeklaracija()

def dg_lex(kôd):
    lex = Tokenizer(kôd)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak.isalpha(): yield lex.token(DG.VAR)
        else: yield lex.token(operator(DG, znak) or lex.greška())

#gramatika
#PLUS -> PUTA + PLUS | PUTA
#PUTA -> ELEM PUTA | ELEM
#ELEM -> VAR | ELEM ' | ( ELEM ) | [ ELEM ]

#*************************************************
#na ispitu u tokenima!!
#*************************************************

#stabla
# and = (ulazi) --> lijevo & desno
# or = (ulazi)
# not = (ulaz)

class DGParser(Parser):

    def sklop(self):
        disjunktiLIST = [self.disjunkt()]
        #prvi = self.disjunkt()
        while self >> DG.OR:
            disjunktiLIST.append( self.disjunkt() )
        # return disjunktiLIST[0] if len(disjunktiLIST) == 1 else Or(disjunktiLIST)
        if len(disjunktiLIST) == 1:
            return disjunktiLIST[0] #AKO JE JEDAN ELEMENT ODVOJI SLUČAJ!
            # zato jer ako ga posajemo u OR()
            # onda on primi jedan element a to je string pa sece po stringu
            # i onda hoce dohvatiti vrijednost svakog slova a to ne postoji
        else: return Or(disjunktiLIST)

    def disjunkt(self):
        faktoriLISTA = [ self.faktor() ]
        while self >= {DG.VAR, DG.ONAND, DG.OZAG}:
            faktoriLISTA.append( self.faktor() )
        #return faktoriLISTA[0] if len(faktoriLISTA) == 1 else And(faktoriLISTA)
        if len( faktoriLISTA ) == 1:
            return faktoriLISTA[0]
        else: return And(faktoriLISTA)

    def faktor(self):
        if self >> DG.VAR:
            unutra = self.zadnji #jer sam ga procitala i spremila u tu varijablu
        elif self >> DG.OZAG:
            unutra = self.sklop()
            self.pročitaj(DG.ZZAG)
        elif self >> DG.ONAND:
            unutra = Not(self.sklop())
            self.pročitaj(DG.ZNAND)
        while self >> DG.NOT:
            unutra = Not(unutra)
        return unutra

    start = sklop

class Or(AST('ulazi')):
    pass

class And(AST('ulazi')):
    pass

class Not(AST('ulaz')):
    pass


if __name__ == '__main__':
    ulaz = "[a+bc]"
    print(ulaz)

    tokeni = list(dg_lex(ulaz))
    print(*tokeni)

    stablo = DGParser.parsiraj(dg_lex(ulaz))
    print (stablo)
