# -*- coding: utf-8 -*-

class GildedRose(object):
    MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS = 50
    MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS = 0

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            item_name = item.name

            # we are only calculating is_expired here and not decrementing sell in here
            # moving sulfuras out of case can simplify code and remove duplicate deduction
            # we have kept it along with other items for future logic updates which will be simple to modify
            is_expired = item.sell_in - 1 < 0

            match item_name:

                case "Sulfuras, Hand of Ragnaros":
                    continue

                case "Aged Brie":
                    increase_by = 2 if is_expired else 1
                    item.quality = min(item.quality + increase_by, self.MAX_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    item.sell_in = item.sell_in - 1

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
                    decrease_by = 4 if is_expired else 2
                    item.quality = max(item.quality - decrease_by, self.MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
                    item.sell_in = item.sell_in - 1

                case _:
                    decrease_by = 2 if is_expired else 1
                    item.quality = max(item.quality - decrease_by, self.MIN_QUALITY_ALL_ITEMS_EXCEPT_SULFURAS)
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
