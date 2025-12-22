# -*- coding: utf-8 -*-
import unittest

import pytest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)


# tests to write

# 1.
# sell in date < 0 , quality will degrade 2x
# except
# sulfuras -> never changes from 80
# aged brie -> quality increases
# backstage passes -> will be 0 when sellIn <=0
@pytest.mark.parametrize("item_name,starting_quality, expected_quality", [
    ("foo", 2, 0),  # base case for all items
    ("Sulfuras, Hand of Ragnaros", 80, 80),  # Sulfuras, Hand of Ragnaros case, dont change quality
    ("Aged Brie", 1, 2),  # # Increment by one
    ("Backstage passes to a TAFKAL80ETC concert", 100, 0),  # backstage will become 0
])
def test_degrade_quality_twice_faster(item_name, starting_quality, expected_quality):
    items = [Item(item_name, 0, starting_quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].quality == expected_quality


# code issues found after this
# aged brie fails this case as we double increment for it after sellin is <=0

# more cases around boundary conditions needed
# check around behavior change or normal edge
# check when sellIn becomes 0 from 1,-1 from 0
# check when quality goes from 49->50,50 -> 51 (not allowed)m 49-> 51
# check basic clamp cases as increment +2 or +3 will make it go above 50


# 2.
# make sure quality >=0
@pytest.mark.parametrize("item_name, sell_in, starting_quality", [
    ("foo", 0, 0),  # if quality stays 0 when sell in will move negative
    ("foo", -1, 0),  # if quality continues to stay the same when sell in is already past before
    ("Sulfuras, Hand of Ragnaros", 0, 80),  # Sulfuras, Hand of Ragnaros case, dont change quality
    ("Aged Brie", 0, 1),  # should not go negative
    ("Backstage passes to a TAFKAL80ETC concert", 0, 0),  # backstage should remain 0
])
def test_quality_is_never_negative(item_name, sell_in, starting_quality):
    items = [Item(item_name, sell_in, starting_quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].quality >= 0


@pytest.mark.parametrize("item_name, sell_in, starting_quality, days", [
    ("foo", 0, 5, 100),  # check quality stays clamped to zero after 100 days
    ("Sulfuras, Hand of Ragnaros", 0, 80, 1),  # Sulfuras, Hand of Ragnaros case, dont change quality
    ("Aged Brie", 0, 10, 100),  # should not go negative
    ("Backstage passes to a TAFKAL80ETC concert", 0, 100, 100),  # backstage should remain 0
])
def test_quality_is_never_negative_after_x_days(item_name, sell_in, starting_quality, days):
    items = [Item(item_name, sell_in, starting_quality)]
    gilded_rose = GildedRose(items)
    for _ in range(days):
        gilded_rose.update_quality()
    assert gilded_rose.items[0].quality >= 0


# 3.
# aged brie +1 quality from number of days
def test_aged_brie_increment_by_one():
    items = [Item('Aged Brie', 10, 0)]
    gilded_rose = GildedRose(items)
    for _ in range(10):
        gilded_rose.update_quality()
    assert gilded_rose.items[0].quality == 10


@pytest.mark.parametrize("sell_in, starting_quality, expected_quality", [
    (10, 5, 15),  # base case
    (10, 49, 50),  # clamp 50 case
    (1, 50, 50),  # already 50
])
def test_aged_brie_increment_by_one_multiple(sell_in, starting_quality, expected_quality):
    items = [Item('Aged Brie', sell_in, starting_quality)]
    gilded_rose = GildedRose(items)
    for _ in range(sell_in):
        gilded_rose.update_quality()
    assert gilded_rose.items[0].quality == expected_quality


# 4.
# q <= 50
# except
# sulfuras q=80
# brie is already covered
@pytest.mark.skip(reason="can be ignored as repeat testing of same scenario")
@pytest.mark.parametrize("item_name, sell_in, starting_quality,expected_quality", [
    ("foo", 10, 5, 0),  # if quality stays 0 when sell in will move negative
    ("Sulfuras, Hand of Ragnaros", 1, 80, 80),  # Sulfuras, Hand of Ragnaros case, dont change quality
])
def test_quality_is_never_negative(item_name, sell_in, starting_quality, expected_quality):
    items = [Item(item_name, sell_in, starting_quality)]
    gilded_rose = GildedRose(items)

    for _ in range(sell_in):
        gilded_rose.update_quality()

    item_quality = gilded_rose.items[0].quality
    assert 0 <= item_quality <= expected_quality


# 5.
# preserve state of sulfuras no matter what, no quality change no sell in change needed
# sulfuras quality=80
# sulfuras quality dont change ever
@pytest.mark.parametrize("sell_in,days_passed", [
    (1, 1),  # maintain state
    (1, 0)  # check init logic and state
])
def test_sulfuras_state_maintained(sell_in, days_passed):
    items = [Item('Sulfuras, Hand of Ragnaros', sell_in, 80)]
    gilded_rose = GildedRose(items)

    for _ in range(days_passed):
        gilded_rose.update_quality()

    item_quality = gilded_rose.items[0].quality
    item_sell_in = gilded_rose.items[0].sell_in
    assert item_quality == 80 and item_sell_in == sell_in


# 6.
# Backstage passes -> if one day passed then
#   -- q+=1 sellIn > 10
#   -- q+=2 -> 5 > sellIn<=10
#   -- q+=3 -> 0 > sellIn<=5
#   -- q = 0 selling <= 0

@pytest.mark.parametrize("sell_in,days_passed,starting_quality,expected_quality", [
    (20, 5, 40, 45),  # check increment
    (20, 10, 40, 50),  # check edge case around boundary when 10 days are remaining
    (20, 11, 10, 22),  # check +2 increments
    (10, 1, 49, 50),  # quality clamp on rollover
    (6, 1, 40, 42),  # check edge case around boundary when 5 days are remaining
    (6, 2, 40, 45),  # check crossover to +3
    (5, 1, 48, 50),  # quality clamp on rollover
    (2, 2, 20, 26),  # check inc to +3
    (2, 3, 20, 0),  # check reset to zero
    (0, 1, 50, 0),  # check reset to zero
])
def test_backstage_passes(sell_in, days_passed, starting_quality, expected_quality):
    items = [Item('Backstage passes to a TAFKAL80ETC concert', sell_in, starting_quality)]
    gilded_rose = GildedRose(items)

    for _ in range(days_passed):
        gilded_rose.update_quality()

    item_quality = gilded_rose.items[0].quality
    assert item_quality == expected_quality


# 7.
# conjured q-=2 for each day
def test_conjured_items_degrade_twice():
    items = [Item("Conjured Mana Cake", 1, 2)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].quality == 0


# 8.
# anything other than sulfuras,backstage passes,conjured items with each day passed q-=1

# 9.
# anything other than sulfuras with each day passed sellIn-=1
@pytest.mark.parametrize("item_name,sell_in, days_passed, expected_sell_in", [
    ("foo", 2, 2, 0),  # base case for all items
    ("Sulfuras, Hand of Ragnaros", 2, 2, 2),  # edge case
    ("foo", 0, 2, -2)
])
def test_decrement_sell_in(item_name, sell_in, days_passed, expected_sell_in):
    items = [Item(item_name, sell_in, 20)]
    gilded_rose = GildedRose(items)
    for _ in range(days_passed):
        gilded_rose.update_quality()
    assert gilded_rose.items[0].sell_in == expected_sell_in


if __name__ == '__main__':
    unittest.main()
