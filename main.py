def remove_not_having_yellow(word: str, yellow: list) -> bool:
    for l, _ in yellow:
        if l not in word:
            return True
    return False

def remove_yellow_in_bad_spot(word, yellow) -> bool:
    for l, i in yellow:
        if word[i] == l:
            return True
    return False

def remove_letter_not_in(word, not_in) -> bool:
    for l in not_in:
        if l in word:
            return True
    return False

def remove_no_green(word, green) -> bool:
    for wl, gl in zip(word, green):
        if gl != "_" and wl != gl:
            return True
    return False

def cull_wordlist(wordlist: set, not_in: list, yellow: list, green: list) -> None:
    for word in wordlist.copy():
        if remove_not_having_yellow(word, yellow) or remove_yellow_in_bad_spot(word, yellow) or remove_letter_not_in(word, not_in) or remove_no_green(word, green):
            wordlist.remove(word)
       
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
            def check_letters(s: str) -> bool:
                for l in s:
                    if l not in ["y", "g", "b"]:
                        return False
                return True
            if len(colors) == 5 and check_letters(colors):
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