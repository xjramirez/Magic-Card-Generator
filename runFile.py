import card

def main():
    card1 = card.Card(colors=['G'])

    for i in range(0,1):
        card1.generateCard()
        card1.printCard()

if __name__ == "__main__":
    main()