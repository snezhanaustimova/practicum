from ceasar.Ceasar import decrypt_text_caesar


def break_text_caesar(text: str) -> str:
    res = []

    for i in range(32):
        res.append(decrypt_text_caesar(text, i))

    return (res)

variants = break_text_caesar('Жт исм хтрсйсмн, жт исм цгзтхцсящ фдличрмн т хчиаедщ ртйн фтимся, – ця тимс рсй утиийфкод м тутфд, т жйпмомн, ртзчымн, уфджимжян м хжтетисян фчххомн гляо! Сй ечиа цйег – одо сй жудхца ж тцыдгсмй уфм жмий жхйзт, ыцт хтжйфьдйцхг итрд? Ст сйпалг жйфмца, ыцтея цдотн гляо сй еяп идс жйпмотрч сдфтич!')

frequency = []

with open('dictionary.txt', 'r', encoding='utf-8') as file:
    dictList = file.readlines()
    for i in variants:
        k = 0
        i = i.split()
        for j in i:
            if (j+'\n') in dictList:
                k += 1
        frequency.append(k)
print(variants[(frequency.index(max(frequency)))])