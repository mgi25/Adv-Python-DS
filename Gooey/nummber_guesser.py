import random
from gooey import Gooey, GooeyParser

@Gooey(program_name="Number Guessing Game")
def main():
    parser = GooeyParser(description="Guess a number between 1 and 10")

    parser.add_argument("YourGuess", help="Enter your guess (1-10)", type=int)

    args = parser.parse_args()
    guess = args.YourGuess

    # Generate random number between 1 and 10
    secret = random.randint(1, 10)

    # Check guess
    if guess == secret:
        print(f"🎉 Correct! The number was {secret}.")
    else:
        print(f"❌ Try Again! The number was {secret}.")

if __name__ == "__main__":
    main()
