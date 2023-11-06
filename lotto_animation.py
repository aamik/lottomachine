import time
import os

NUM_LOTTERY_NUMBERS = 7


def clear_console():
    # Clear console based on operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def braille_animation():
    braille_frames = [
        "⠟⠛⠋",
        "⠏⠋⠙",
        "⠹⠸⠼",
        "⢿⣷⣿"
    ]
    return braille_frames

def drum_frame():
    return " _________\n|         |\n|         |\n|_________|"

def rolling_drum_animation():
    drum_frames = [
        " _________\n|         |\n|    {}   |\n|_________|",
        " _________\n|         |\n|   {}    |\n|_________|",
        " _________\n|         |\n|    {}   |\n|_________|",
        " _________\n|         |\n|   {}    |\n|_________|"
    ]

    braille_frames = braille_animation()

    for _ in range(12):
        for i in range(len(drum_frames)):
            clear_console()  # Clear console before printing the next frame
            print(drum_frames[i].format(braille_frames[i % len(braille_frames)]))
            time.sleep(0.1)


def ending_animation():
    braille_ball1 = "        ⠈"
    braille_ball2 = "        ⠐"
    braille_ball3 = "        ⠠"
    braille_pile = "           "

    for _ in range(NUM_LOTTERY_NUMBERS):
        clear_console()  # Clear console before printing the next frame
        print(drum_frame())
        time.sleep(0.1)
        print(braille_ball1)
        time.sleep(0.1)
        print(braille_ball2)
        time.sleep(0.1)
        print(braille_ball3)
        time.sleep(0.1)
        braille_pile += braille_ball2.strip()  # Add braille ball to the pile
        print(braille_pile)  # Display the braille pile
        time.sleep(0.3)


    print("\nAnd we have the correct numbers!")



