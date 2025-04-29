


def format_correct(string1):
    numbers_letters = {
        '0': ['O',],
        '1': ['I',],
        '2': ['Z'],
        '3': ['E'],
        '4': ['A'],
        '5': ['S'],
        '6': ['G'],
        '7': ['T',],
        '8': ['B'],
        '9': ['G']
    }

    letters_numbers = {
        'A': ['4'],
        'B': ['8'],
        'C': ['0'],
        'D': ['0'],
        'E': ['3',],
        'F': ['9'],
        'G': ['9'],
        'H': ['8',],
        'I': ['1',],
        'J': ['1'],
        'K': ['7'],
        'L': ['7'],
        'M': ['0'],
        'N': ['0'],
        'O': ['0',],
        'P': ['9',],
        'Q': ['0',],
        'R': ['7'],
        'S': ['5'],
        'T': ['7',],
        'U': ['0',],
        'V': ['0',],
        'W': ['3',],
        'X': ['8',],
        'Y': ['7',],
        'Z': ['2',]
    }

    
 
    # Check if the length of string1 is greater than 7
    if len(string1) > 7:
        # If so, truncate string1 to the first 7 characters
        string1 = string1[0:6]

    # Replace '?' with '9' in string1
    if '?' in string1:
        string1 = string1.replace('?', '9')

    # Replace '}' with '9' in string1
    if '}' in string1:
        string1 = string1.replace('}', '9')

    # Check if the length of string1 is 7
    if len(string1) == 7:
        # Convert string1 to a list of characters
        string_list = list(string1)

        # If the first character is a digit, replace it with its corresponding letter
        if string_list[0].isdigit():
            string_list[0] = numbers_letters[string_list[0]][0]

        # If the second character is a digit, replace it with its corresponding letter
        if string_list[1].isdigit():
            string_list[1] = numbers_letters[string_list[1]][0]

        # If the third character is a letter, replace it with its corresponding number
        if string_list[2].isalpha():
            string_list[2] = letters_numbers[string_list[2]][0]

        # If the fourth character is a letter, replace it with its corresponding number
        if string_list[3].isalpha():
            string_list[3] = letters_numbers[string_list[3]][0]

        # If the fifth character is a digit, replace it with its corresponding letter
        if string_list[4].isdigit():
            
            string_list[4] = letters_numbers[string_list[4]][0]

        # If the sixth character is a digit, replace it with its corresponding letter
        if string_list[5].isdigit():
            string_list[5] = numbers_letters[string_list[5]][0]

        # If the seventh character is a digit, replace it with its corresponding letter
        if string_list[6].isdigit():
            string_list[6] = numbers_letters[string_list[6]][0]

        # Join the characters back into a string
        string1 = ''.join(string_list)
        print(string1)
        return string1
        

def retry(string1, i):
    letter_letter = {
        'A': ['R'],
        'B': ['D'],
        'C': ['G'],
        'D': ['B'],
        'E': ['F'],
        'F': ['T'],
        'G': ['C',],
        'H': ['I'],
        'I': ['L',],
        'J': ['I'],
        'K': ['J'],
        'L': ['I'],
        'M': ['N'],
        'N': ['M'],
        'O': ['D'],
        'P': ['T'],
        'Q': ['O'],
        'R': ['A'],
        'S': ['Z'],
        'T': ['F'],
        'U': ['V'],
        'V': ['U'],
        'W': ['M',],
        'X': ['K'],
        'Y': ['T'],
        'Z': ['S']
    }

    numbers_numbers = {
    
        '3': ['8'],
        '6': ['9'],
        '8': ['3'],
        '9': ['6'],
        '7': ['2'],
        '2': ['7']
    }
    if len(string1) ==7:
        string_list = list(string1)
        #replaces the corrspning numbers with another value.
        if string_list[i-1].isnumeric():
            if string_list[i-1] == '6':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
            elif string_list[i-1] == '9':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
            elif string_list[i-1] == '3':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
            elif string_list[i-1] == '8':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
            elif string_list[i-1] == '7':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
            elif string_list[i-1] == '2':
                string_list[i-1] =numbers_numbers[string_list[i-1]][0]
        if string_list[i-1].isalpha():
            string_list[i-1] =letter_letter[string_list[i-1]][0]
        string1 = ''.join(string_list)
        print(string1)
        return string1
    else:
        print(string1)
        return 'break'

            


retry('27YTJLO',2 )

#print(string_list)



    