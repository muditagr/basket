
import json

class Basket:

    def __init__(self) -> None:
        with open("data/products.json", mode="r") as products:
            self.products = json.load(products)
        
        with open("data/deliveryRules.json", mode="r") as d:
            self.delivery_rules = json.load(d)
        
        self.items = []
        self.delivery_fee = None
        self.basket_sum = None


    def add(self, sku) -> None:
        sku = str.upper(sku)
        if sku not in [widget["id"] for widget in self.products]:
            print("wrong product code! Try again.")
            return
        self.items.append(sku)


    def getWidget(self, sku) -> "dict":
        for widget in self.products:
            if widget["id"] == sku:
                return widget

    
    def applyOffer(self) -> None:
        # can be improved by creating a standard json based rules
        red_widget_sku = "R01"
        sku_count = self.items.count(red_widget_sku)
        if sku_count//2 > 0:
            price_factor = self.getWidget(red_widget_sku)["price"]*.5
            self.basket_sum -= (sku_count//2)*price_factor #


    def applyDeliveryfee(self) -> None:
        for rule in self.delivery_rules:
            if rule["minAmount"] <= self.basket_sum < rule["maxAmount"]:
                self.delivery_fee = rule["fee"]
                self.basket_sum += self.delivery_fee


    def total(self) -> "float":
        basket_sum = 0
        for sku in self.items:
            basket_sum += self.getWidget(sku)["price"]
        self.basket_sum = basket_sum
        self.applyOffer()
        self.applyDeliveryfee()

        return round(self.basket_sum, 2)

        
if __name__ == "__main__":
    baskets = [
        ["B01", "G01"],
        ["R01", "R01"],
        ["R01", "G01"],
        ["B01", "B01", "R01", "R01", "R01"],
    ]
    for bskt in baskets:
        basket = Basket()
        for sku in bskt:
            basket.add(sku)
        bskt_total = basket.total()
        print(f"For products {bskt}, basket total inlcuding delivery fee (${basket.delivery_fee}) is ${bskt_total}")

  
