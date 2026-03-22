def get_possible_divisions(num):
    return [n for n in [3, 4, 5] if num % n == 0]


def gamerules(starting_num):
    current_num = starting_num
    total_score = 0
    bank = 0
    current_player = 1

    while True: #for testing
        possible = get_possible_divisions(current_num)

        if not possible:
            break
        
        while True:
            try:
                move = int(input(f"Player {current_player}, choose divisor {possible}: "))
                if move not in possible:
                    print(f"Invalid choice. Please pick from {possible}.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer.")
        #all upper "while" have to be rewroten to implement AI and interface


        result = current_num // move

        if result % 2 == 0:
            total_score += 1
        else:
            total_score -= 1


        if result % 10 in (0, 5):
            bank += 1

        current_num = result
        current_player = 2 if current_player == 1 else 1

    if total_score % 2 == 0:
        final_score = total_score - bank
    else:
        final_score = total_score + bank

    if final_score % 2 == 0:
        winner = 1
    else:
        winner = 2
