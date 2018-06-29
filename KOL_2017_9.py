from pj import *
class LOGO(enum.Enum):
    UOTV, UZAT = '[]'
    FORWARD_token = "FORWARD"
    LEFT_token = "LEFT"
    REPEAT = "REPEAT"
    GRESKA = ""
    KRAJ = ""
    class BROJ(Token):
        def vrijednost(self): return int(self.sadržaj)


def logo_lex(kôd):
    lex = Tokenizer(kôd)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        #FORWARD
        elif znak == 'F':
            sljed = lex.čitaj()
            if sljed == 'O':
                #pročitao FO .. citaj dalje rijec
                lex.pročitaj('R')
                lex.pročitaj('W')
                lex.pročitaj('A')
                lex.pročitaj('R')
                lex.pročitaj('D')
                yield lex.token(LOGO.FORWARD_token)
            elif znak == 'D':
                #pročitao skračenicu
                yield lex.token(LOGO.FORWARD_token)
        #LEFT
        elif znak == 'L':
            sljed = lex.čitaj()
            if sljed == 'E':
                #počitao LE citaj cijelu rijec onda
                lex.pročitaj('F')
                lex.pročitaj('T')
                yield lex.token(LOGO.LEFT_token)
            elif sljed == 'T':
                yield lex.token(LOGO.LEFT_token)
        #REPEAT
        elif znak == 'R':
            lex.pročitaj('E')
            lex.pročitaj('P')
            lex.pročitaj('E')
            lex.pročitaj('A')
            lex.pročitaj('T')
            yield lex.token(LOGO.REPEAT)
        elif znak.isdigit():
            lex.zvijezda(str.isdigit)
            yield lex.token(LOGO.BROJ)
        elif znak == '[':
            yield lex.token(LOGO.UOTV)
        elif znak == ']':
            yield lex.token(LOGO.UZAT)
        else:
            while znak!= ' ':
                znak = lex.čitaj()
            lex.vrati();
            yield lex.token(LOGO.GRESKA)
    lex.token(LOGO.KRAJ)

if __name__ == '__main__':
    ulaz = "[ LEFT 58 LT AA ]"
    print('ulaz = ', ulaz)

    tokeni = list(logo_lex(ulaz))
    print(*tokeni)
