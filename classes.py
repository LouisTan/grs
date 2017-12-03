#!/usr/bin/env python
debug = True

class Receipt:
    def __init__(self, merchant, client, date, time, cashNo, cashier, items, value, payment):
        self.merchant = merchant
        self.client = client
        self.date = date
        self.time = time
        self.cashNo = cashNo
        self.cashier = cashier
        self.items = []
        self.value = value
        self.payment = payment

    def printReceipt(self):
        desc_str = "Merchant:\t" + self.merchant + "\nClient:\t\t" #+ self.client + "\nDate:\t\t" + self.date + "\nTime:\t\t" + self.time + "\nCash no:\t" + self.cashNo + "\nCashier:\t" + self.cashier + "\nValue:\t\t" + self.value + "\nPayment:\t" + self.payment + "\n"
        print(desc_str)


class Item:
    def __init__(self, name, price):  # quantity, mesureUnit, category
        self.name = name
        self.price = price
        # self.quantity = quantity
        # self.mesureUnit = mesureUnit
        # self.category = category

    def printItem(self):
        desc_str = "Name:\t\t" + self.name + "\nPrice:\t\t" + self.price + '\n'
        print(desc_str)