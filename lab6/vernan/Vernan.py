from secrets import choice
from string import printable

def generate_pad(length: int) -> str:

    pad = ""
    for index in range(length):
        pad_letter = choice(printable)
        pad += (pad_letter)

    save(pad, "pad.txt")
    return pad


def encrypt(text: str, pad: str) -> str:

    ciphertext = ""

    for text_character, pad_character in zip(text, pad):
        print(text_character, pad_character)
        if text_character not in printable:
            raise ValueError(f"Text value: {text_character} provided is not printable ascii")

        xored_value = ord(text_character) ^ ord(pad_character)

        ciphertext_character = chr(xored_value)

        ciphertext += (ciphertext_character)

    save(ciphertext, "ciphertext.txt")

    return ciphertext


def decrypt(pad: str, ciphertext: str) -> str:

    plaintext = ""

    for pad_character, ciphertext_number in zip(pad, ciphertext):
        xored_value = ord(pad_character) ^ ord(ciphertext_number)
        plaintext += chr(xored_value)

    save(plaintext, "plaintext.txt")

    return plaintext


def save(text: str, path: str):

    try:
        with open(path, "w+") as output_file:
            output_file.write(text)
    except:
        print(f"Unable to save file {path}")


if __name__ == "__main__":

    text = '''Falling too fast to prepare for this
Tripping in the world could be dangerous
Everybody circling is vulturous
Negative, nepotist
Everybody waiting for the fall of man
Everybody praying for the end of times
Everybody hoping they could be the one
I was born to run, I was born for this
Whip, whip
Run me like a race horse
Hold me like a rip cord
Break me down and build me up
I wanna be the slip, slip
Word upon your lip, lip
Letter that you rip, rip
Break me down and build me up
Whatever it takes
Cause I love the adrenaline in my veins
I do whatever it takes,
Cause I love how it feels when I break the chains
Whatever it takes
You take me to the top
I'm ready for whatever it takes
Cause I love the adrenaline in my veins
I do what it takes.'''

    pad = generate_pad(len(text))
    print(f"The pad is: {pad}")

    ciphertext = encrypt(text, pad)
    print(f"\nThe ciphertext is: {ciphertext}")

    plaintext = decrypt(pad, ciphertext)
    print(f"\nThe decrypted plaintext is: {plaintext}")