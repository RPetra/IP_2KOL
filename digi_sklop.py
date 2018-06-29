#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:40:40 2018

@author: sarapuz
"""

from pj import *

# ------------------ TOKENI ------------------  #

class DIGI(enum.Enum):
    OR = '+'
    NOT = "'"
    OOTV, OZAT, ONAND, ZNAND = '()[]' 
    
    class VAR(Token):
        def vrijednost(self, **interpretacija):
            try: return interpretacija[self.sadržaj]
            except KeyError: self.nedeklaracija()

# ------------------ LEXER ------------------  #

def DIGI_lex(source):
    lex = Tokenizer(source)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak.isalpha() : yield lex.token(DIGI.VAR)
        else :yield lex.token(operator(DIGI, znak) or lex.greška()  )  
  
# ------------------ GRAMATIKA ------------------  #
"""

sklop       -> sklop OR disjunkt | disjunkt
disjunkt    -> disjunkt faktor | faktor
faktor      -> VAR | faktor NOT | OOTV faktor OZAT | ONANS faktor ZNAND

"""
    
# ------------------ AST ------------------  #
"""

And(ulazi)
Or(ulazi)
Not(ulaz)

"""

# ------------------ PARSER ------------------  #

class DIGIParser(Parser): 
    
    def sklop(self):
        disjunkti = [ self.disjunkt() ]
        while self >> DIGI.OR:
            disjunkti.append( self.disjunkt() )
        return disjunkti[0] if len(disjunkti) == 1 else Or(disjunkti)

        
        
    def disjunkt(self):
        faktori = [ self.faktor() ]
        while self >= { DIGI.VAR, DIGI.ONAND, DIGI.OOTV }:
            faktori.append( self.faktor() )
        return faktori[0] if len(faktori) == 1 else And(faktori)

     
        
    def faktor(self):
        if self >> DIGI.VAR:
            trenutni = self.zadnji
        elif self >> DIGI.OOTV:
            trenutni = self.sklop()
            self.pročitaj(DIGI.OZAT)
        elif self >> DIGI.ONAND:
            trenutni = Not( self.sklop() )
            self.pročitaj(DIGI.ZNAND)            
        else: self.greška()
        while self >> DIGI.NOT:
            trenutni = Not(trenutni)
        return trenutni               
   
    start = sklop
     
    
class Or(AST('ulazi')):pass
class And(AST('ulazi')):pass
class Not(AST('ulaz')):pass
    
    

ulaz = """[a+bc]"""
        
print("********LEXER********")

tokeni = list(DIGI_lex(ulaz))
print(*tokeni)        

digi = DIGIParser.parsiraj(DIGI_lex(ulaz) )
print(digi)

      