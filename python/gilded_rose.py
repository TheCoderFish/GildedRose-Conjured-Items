# -*- coding: utf-8 -*-

class GildedRose(object):
    MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS = 50
    MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS = 0

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            item_name = item.name

            match item_name:
                case "Aged Brie":
                    item.quality = min(item.quality + 1, self.MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    item.sell_in = item.sell_in - 1

                case "Sulfuras, Hand of Ragnaros":
                    pass

                case "Backstage passes to a TAFKAL80ETC concert":
                    sell_in = item.sell_in
                    if sell_in > 10:
                        item.quality = min(item.quality + 1, self.MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    elif sell_in > 5:
                        item.quality = min(item.quality + 2, self.MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    elif sell_in > 0:
                        item.quality = min(item.quality + 3, self.MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    else:
                        item.quality = 0

                    item.sell_in = item.sell_in - 1

                case "Conjured Mana Cake":
                    item.quality = max(item.quality - 2, self.MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    item.sell_in = item.sell_in - 1

                case _:
                    item.quality = max(item.quality - 1, self.MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    item.sell_in = item.sell_in - 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


if __name__ == "__main__":
    items = [Item('Aged Brie', 0, 50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    print(gilded_rose.items[0])
