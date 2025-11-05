import random
import time

def intro():
    print("🎯 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100...")
    time.sleep(1)
    print("Try to guess it in as few attempts as possible.\n")

def get_guess():
    while True:
        try:
            guess = int(input("Enter your guess: "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("⚠️ Please guess a number between 1 and 100.")
        except ValueError:
            print("❌ That's not a valid number, try again!")

def play_game():
    number = random.randint(1, 100)
    attempts = 0
    start_time = time.time()

    while True:
        guess = get_guess()
        attempts += 1

        if guess < number:
            print("Too low! 📉")
        elif guess > number:
            print("Too high! 📈")
        else:
            end_time = time.time()
            print(f"🎉 Correct! The number was {number}.")
            print(f"You took {attempts} attempts and {end_time - start_time:.2f} seconds.")
            break

if __name__ == "__main__": 
    intro()
    play_game()
