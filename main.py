#ctrl+c to exit

import cbpro
import colorama
import termcolor
import os

colorama.init()


def print_precise_float(num):
    num_str = "%0.*f" % (8, num)
    return num_str[:10]


class coinbase_pro_websocket(cbpro.WebsocketClient):

    def __init__(self, url="wss://ws-feed.pro.coinbase.com", message_type="subscribe"):
        super().__init__(url, message_type)
        self.message_count = 0
        self.buy_vol = 0
        self.sell_vol = 0
        self.total_volume = 0

    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["ETH-USD"]
        self.channels = ["ticker"]

    def on_message(self, msg):
        self.message_count += 1
        # clear on screen buffer to prevent possible performance problems with longer sessions
        # this only works on windows, so change it if you're running linux
        if self.message_count % 1000 == 0:
            os.system('cls')

        if 'price' in msg and 'type' in msg:
            color = "green" if msg["side"] == "buy" else "red"
            side_volume = self.buy_vol if msg["side"] == "buy" else self.sell_vol
            self.total_volume += float(msg["last_size"])

            if msg["side"] == "buy":
                self.buy_vol += float(msg["last_size"])
            else:
                self.sell_vol += float(msg["last_size"])

            last_size = print_precise_float(float(msg["last_size"]))
            price = "\t ${:.2f}".format(float(msg["price"]))
            vol = "\t({}) ".format(print_precise_float(float(side_volume)))
            percentage = "{:.2f}%".format((side_volume / self.total_volume) * 100)

            print(termcolor.colored(" {} {} {} {}".format(last_size, price, vol, percentage), color))


wsClient = coinbase_pro_websocket()
wsClient.start()
print(wsClient.url, wsClient.products)

# ugly but it works
while True:
    try:
        None
    except KeyboardInterrupt:
        wsClient.close()


