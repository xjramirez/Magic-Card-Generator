import lib.card as card

def main():
    card1 = card.Card(colors=['U'])

    for i in range(0,5):
        card1.generateCard()
        card1.printCard()

if __name__ == "__main__":
    main()