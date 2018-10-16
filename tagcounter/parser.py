from html.parser import HTMLParser


class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.tagdict = {}

    def handle_starttag(self, tag, attrs):
        self.total_amount = self.tagdict.get(tag)
        if self.total_amount is not None:
            self.total_amount[0] += 1
            self.tagdict[tag] = self.total_amount
        else:
            self.total_amount = [0,0]
            self.total_amount[0] = 1
            self.tagdict[tag] = self.total_amount


    def handle_endtag(self, tag):
        self.total_amount = self.tagdict.get(tag)
        if self.total_amount is not None:
            self.total_amount[1] += 1
            self.tagdict[tag] = self.total_amount
        else:
            self.total_amount = [0, 0]
            self.total_amount[1] = 1
            self.tagdict[tag] = self.total_amount