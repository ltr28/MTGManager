from nzmagic.downloads import CardKingdom


class Card:
    """A singular Magic: The Gathering card (including all printings)."""

    def __init__(self, card_name):
        self.card_name = card_name

    def get_image(self):
        """"""


if __name__ == "__main__":
    CARD_NAME = "Boseiju, Who Endures"

    ck = CardKingdom()
    ck.get_price_data()
    # card = Card("name")
