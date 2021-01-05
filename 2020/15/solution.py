input_str = "0,13,1,16,6,17"

numbers = [int(v) for v in input_str.strip().split(',')]

# Part 1 and 2: naive count
final_turns = [2020, 30000000]
for N in final_turns:
    game = {}
    for i in range(N):
        if i < len(numbers):
            # Start of game
            n = numbers[i]
            answer = n
            game[n] = i + 1
        else:
            if n not in game.keys():
                answer = 0
            else:
                answer = i - game[n]
            game[n] = i
        n = answer

    print(f"Turn {i + 1}: answer {answer}")
