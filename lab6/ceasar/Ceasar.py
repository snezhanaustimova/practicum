# coding: utf-8

def text_caesar(text: str, shift: int) -> str:
    alphabet_lower = 'йцукенгшщзхъфывапролджэячсмитьбю'
    alphabet_upper = alphabet_lower.upper()

    ord_first_letter_lower = ord('а')
    ord_first_letter_upper = ord('А')

    new_text = ''

    for i in text:
        if i in alphabet_lower:
            new_text += chr(((ord(i) - ord_first_letter_lower + shift) % 32) + ord_first_letter_lower)
        elif i in alphabet_upper:
            new_text += chr(((ord(i) - ord_first_letter_upper + shift) % 32) + ord_first_letter_upper)
        else:
            new_text += i

    return new_text


def decrypt_text_caesar(text: str, shift: int) -> str:
    return text_caesar(text, -shift)

if __name__ == '__main__':
    print(text_caesar('Во дни сомнений, во дни тягостных раздумий о судьбах моей родины, – ты один мне поддержка и опора, о великий, могучий, правдивый и свободный русский язык! Не будь тебя – как не впасть в отчаяние при виде всего, что совершается дома? Но нельзя верить, чтобы такой язык не был дан великому народу!', 4))