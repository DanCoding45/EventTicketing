
import sqlite3


class Ticket():

    def __init__(self, event_id, price, quantity):
        self.event_id = event_id
        self.price = price
        self.quantity = quantity
