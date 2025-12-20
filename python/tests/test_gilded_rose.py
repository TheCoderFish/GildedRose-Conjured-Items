# -*- coding: utf-8 -*-
import unittest

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

# 2.
# make sure quality >=0

# 3.
# aged brie +1 quality from number of days

# 4.
# q <= 50
# except
# sulfuras q=80

# 5.
# preserve state of sulfuras no matter what, no quality change no sell in change needed
# sulfuras quality=80
# sulfuras quality dont change ever

# 6.
# Backstage passes -> if one day passed then
#   -- q+=1 sellIn > 10
#   -- q+=2 -> 5 > sellIn<=10
#   -- q+=3 -> 0 > sellIn<=5
#   -- q = 0 selling <= 0

# 7.
# conjured q-=2 for each day

# 8.
# anything other than sulfuras,backstage passes,conjured items with each day passed q-=1

# 9.
# anything other than sulfuras with each day passed sellIn-=1

if __name__ == '__main__':
    unittest.main()
