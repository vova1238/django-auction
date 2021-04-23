def slugify(sequence):
    translit_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia',
        'ь': '', '\'': ''
    }
    forbidden_symbols = ('!', '?', '+', '*', '/', '=', '%', '^', '&', '$', '@', '(', ')', '[', ']', '{', '}', ',', '.')

    def translit(w):
        result = []
        if 'зг' in w:
            w = w.replace('зг', 'zgh')
        for i in w:
            if i in translit_table.keys():
                result.append(translit_table[i])
            elif i not in forbidden_symbols:
                result.append(i)
        return ''.join(result)

    words = sequence.strip().split(' ')
    if '' in words:
        words.remove('')
    return '-'.join(translit(word.lower()) for word in words)