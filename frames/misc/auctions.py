import tkinter.ttk as ttk
from enum import Enum

class EventType(Enum):
    SOLD = 1
    NEWBID = 2
    BIDWAR = 3
    BIN = 4
    BIDWON = 5
    LOST = 6
    OUTBID = 7
    UPDATE = 8

class Auctions():
    cards = {}

    def __init__(self, frame):
        t = ttk.Treeview(frame, columns=('timestamp', 'initial', 'current', 'bin', 'expires'), selectmode='browse')
        t.column("#0", width=75)
        t.column("timestamp", width=100)
        t.column("initial", width=50)
        t.column("current", width=50)
        t.column("bin", width=50)
        t.column("expires", width=50)

        t.heading("#0", text="Name", anchor="w")
        t.heading("timestamp", text="Time")
        t.heading("initial", text="Initial Bid")
        t.heading("current", text="Current Bid")
        t.heading("bin", text="BIN")
        t.heading("expires", text="Expires")

        t.tag_configure('won', foreground='#006400', background='grey')
        t.tag_configure('bid', foreground='#006400')
        t.tag_configure('war', foreground='#B77600')
        t.tag_configure('sold', foreground='#1C7CA9', background='grey')
        t.tag_configure('lost', foreground='#B70000', background='grey')

        self.view = t

    def get_view(self):
        return self.view

    def add_auction(self, card, timestamp, currbid, index='end', tag=''):
        if not card.cardid in self.cards:
            self.cards[card.cardid] = card
            return self.view.insert("", index, card.cardid, text=card.cardname, values=(timestamp, card.startingBid,
                                                                                        currbid, card.buyNowPrice,
                                                                                        card.expires), tags=(tag,))

    def update_status(self, card, timestamp, currbid, tag=''):
        if not card.cardid in self.cards:
            self.add_auction(card, timestamp, currbid, 'end', tag)
        else:
            options = self.view.item(card.cardid)
            options['values'] = (timestamp, card.startingBid,
                                 currbid, card.buyNowPrice,
                                 card.expires)
            if tag:
                options['tags'] = (tag,)
            self.view.item(card.cardid, text=options['text'], values=options['values'], tags=options['tags'])
        self.view.see(card.cardid)
        self.view.selection_set([card.cardid])

class Card():

    def __init__(self, item):
        self.cardid = item['id']
        self.resourceId = item['resourceId']
        self.tradeId = item['tradeId']
        self.cardType = item['itemType']
        self.buyNowPrice = item['buyNowPrice'] if item['buyNowPrice'] is not None else item['lastSalePrice']
        self.startingBid = item['startingBid'] if item['startingBid'] is not None else "BIN"
        self.currentBid = item['currentBid'] if item['currentBid'] is not None else item['lastSalePrice']
        self.contract = item['contract']
        self.expires = item['expires'] if item['expires'] is not None else -1

class PlayerCard(Card):

    def __init__(self, item, name):
        Card.__init__(self, item)
        self.cardname = name