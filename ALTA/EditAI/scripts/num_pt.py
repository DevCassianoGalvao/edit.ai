"""Número em algarismo -> palavras em PORTUGUÊS, no mesmo formato que o roteiro escreve.

O roteiro escreve por extenso ("quatrocentos e cinquenta e oito", "mil novecentos e oitenta e oito") e o Whisper
escreve em algarismo ("458", "1988"): sem soletrar, o casamento caía para 66–84% nos parágrafos cheios de número
(filme do navio, 16/09). Os tokens "e" também são emitidos, porque o roteiro os escreve.
"""
UNITS = ("zero um dois três quatro cinco seis sete oito nove dez onze doze treze quatorze quinze dezesseis "
         "dezessete dezoito dezenove").split()
TENS = {2: "vinte", 3: "trinta", 4: "quarenta", 5: "cinquenta", 6: "sessenta", 7: "setenta", 8: "oitenta", 9: "noventa"}
HUND = {1: "cento", 2: "duzentos", 3: "trezentos", 4: "quatrocentos", 5: "quinhentos", 6: "seiscentos",
        7: "setecentos", 8: "oitocentos", 9: "novecentos"}


def num_words_pt(n):
    if n < 20:
        return [UNITS[n]]
    if n < 100:
        t, r = divmod(n, 10)
        return [TENS[t]] + (["e"] + num_words_pt(r) if r else [])
    if n < 1000:
        h, r = divmod(n, 100)
        if h == 1 and r == 0:
            return ["cem"]
        return [HUND[h]] + (["e"] + num_words_pt(r) if r else [])
    if n < 10 ** 6:
        m, r = divmod(n, 1000)
        cabeca = ["mil"] if m == 1 else num_words_pt(m) + ["mil"]
        if not r:
            return cabeca
        # o português liga com "e" quando o resto é menor que 100 ou é centena redonda
        liga = ["e"] if (r < 100 or r % 100 == 0) else []
        return cabeca + liga + num_words_pt(r)
    for div, sing, plur in ((10 ** 9, "bilhão", "bilhões"), (10 ** 6, "milhão", "milhões")):
        if n >= div:
            q, r = divmod(n, div)
            cabeca = num_words_pt(q) + [sing if q == 1 else plur]
            return cabeca + (["e"] + num_words_pt(r) if r else [])
    return [str(n)]
