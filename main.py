def remove_not_having_yellow(word: str, yellow: list) -> bool:
    """
    Checks if the word should be removed because it is missing a yellow letter

    :param word: The word to check
    :param yellow: The list of yellow letters and the positions that they are not in
    :return: If the word should be removed
    """
    for l, _ in yellow:
        if l not in word:
            return True
    return False

def remove_yellow_in_bad_spot(word: str, yellow: list) -> bool:
    """
    Checks if the word should be removed because a yellow letter is in a spot that it is known to not be

    :param word: The word to check
    :param yellow: The list of yellow letters and the positions that they are not in
    :return: If the word should be removed
    """
    for l, i in yellow:
        if word[i] == l:
            return True
    return False

def remove_letter_not_in(word: str, not_in: set) -> bool:
    """
    Checks if the word should be removed because it contains a letter that is not in the target word

    :param word: The word to check
    :param not_in: The set of letters that are not in the target word
    :return: If the word should be removed
    """
    for l in not_in:
        if l in word:
            return True
    return False

def remove_no_green(word: str, green: list) -> bool:
    """
    Checks if the word should be removed because it is missing a letter that is known to be in the word, regardless of if it is in the right position or not

    :param word: The word to check
    :param green: The list of known letters in the correct position with underscores as blanks
    :return: If the word should be removed
    """
    for wl, gl in zip(word, green):
        if gl != "_" and wl != gl:
            return True
    return False

def cull_wordlist(wordlist: list, not_in: set, yellow: list, green: list) -> None:
    """
    Culls the wordlist of words that can't be the target word based on the infomation gathered so far

    :param wordlist: The wordlist
    :param not_in: The set of letters that are not in the target word
    :param yellow: The list of yellow letters and the positions that they are not in
    :param green: The list of known letters in the correct position with underscores as blanks
    :return None:
    """
    for word in wordlist.copy():
        if remove_not_having_yellow(word, yellow) or remove_yellow_in_bad_spot(word, yellow) or remove_letter_not_in(word, not_in) or remove_no_green(word, green):
            wordlist.remove(word)

def check_color_letters(s: str) -> bool:
    """
    Checks the string of color letters to make sure that they are all either y, g, or b

    :param s: The string of color letters
    :return: If they are valid color letters
    """
    for l in s:
        if l not in ["y", "g", "b"]:
            return False
    return True
  
def main():
    # import the wordlist
    wordlist = []
    with open("wordle_wordlist.txt", "r") as file:
        for line in file:
            line = line.strip()
            if len(line) == 5:
                wordlist.append(line)

    not_in = set() # letters that are not in the word anywhere
    yellow_letters_not_at = [] # letters that are in the word but not at the place listed (syntax: [letter, index])
    green_letters = list("_____") # the solved letters so far, will be updated with green letters as they are found

    # main loop
    for attempt in range(6):
        # get and check validity of guess
        guess = ""
        while True:
            guess = input("Enter your guess: ").lower()
            if len(guess) == 5:
                break
            else:
                print("Invalid entry. Try again...")
        
        # get and check validity of colors result
        colors = ""
        while True:
            colors = input("Enter the results from the attempt (y, b, g): ").lower()
            if len(colors) == 5 and check_color_letters(colors):
                break
            else:
                print("Invalid entry. Try again...")
        
        # end game if the user got the word
        if colors == "ggggg":
            print(f"\nCongratulations, you got the word \"{guess}\" in {attempt+1} tries")
            exit(0)
        
        # process the colors
        for i, l in enumerate(colors):
            if l == "g":
                green_letters[i] = guess[i]
            elif l == "y":
                yellow_letters_not_at.append([guess[i], i])
            elif l == "b":
                not_in.add(guess[i])
            else:
                print("Uhhhhh, something went wrong here.....")
                exit(1)
        
        # cull wordlist
        cull_wordlist(wordlist, not_in, yellow_letters_not_at, green_letters)
        print("Available words:")
        print(*list(wordlist), sep=", ")
        print("\n")
        
    # fail message    
    print("You failed to get the word...")

if __name__ == "__main__":
    main()