# Generates a list of apple locations for a predetermined game of snake
from random import randint

def main():
    with open("sequence.txt", "w") as file:
        for _ in range(400):
            file.write(str(randint(0, 18)) + "," + str(randint(0, 24)) + "\n")


if __name__ == "__main__":
    main()
