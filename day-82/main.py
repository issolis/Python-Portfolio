morse_dict = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 
    'D': '-..',   'E': '.',     'F': '..-.',
    'G': '--.',   'H': '....',  'I': '..',
    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',
    'S': '...',   'T': '-',     'U': '..-',
    'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}





def strToMorse(string:str): 
    string = string.upper()
    morse = ''
    for char in string: 
        if char == ' ': 
            morse = morse + "/" + " "
            continue
        try:
            morse = morse + morse_dict[char] + ' '
        except:
            morse = morse + "?" + ' '
    return morse




if __name__ == '__main__': 
    print(strToMorse("hello@ isaac" ))