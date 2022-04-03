import unittest

from flower import Flower, Tulip, Rose, Chamomile, FlowerSet, Bucket


class TestFlower(unittest.TestCase):
    def testFlower(self):
        flower = Flower('red', 2, 10)
        self.assertEqual(flower.color, 'red')
        self.assertEqual(flower.petals, 2)
        self.assertEqual(flower.price, 10)

        self.assertRaises(ValueError, Flower, 1, 1, 1)
        self.assertRaises(ValueError, Flower, "red", 1., 1)
        self.assertRaises(ValueError, Flower, "red", -1, 1)
        self.assertRaises(ValueError, Flower, "red", 5, 1.)
        self.assertRaises(ValueError, Flower, "red", 5, -1)
        self.assertRaises(ValueError, Flower, 0, -5, -1)

    def testTulip(self):
        tulip = Tulip(4, 20)
        self.assertIsInstance(tulip, Flower)
        self.assertEqual(tulip.color, 'pink')

    def testRose(self):
        rose = Rose(4, 30)
        self.assertIsInstance(rose, Flower)
        self.assertEqual(rose.color, 'red')

    def testChamomile(self):
        chamomile = Chamomile(4, 25)
        self.assertIsInstance(chamomile, Flower)
        self.assertEqual(chamomile.color, 'white')

    def testFlowerSet(self):
        tulip = Tulip(4, 20)
        rose = Rose(4, 30)
        flower_set = FlowerSet()
        flower_set.add_flower(tulip)
        flower_set.add_flower(rose)

    def testBucket(self):
        tulip = Tulip(4, 20)
        rose = Rose(4, 30)
        flower_set1 = FlowerSet()
        flower_set1.add_flower(tulip)
        flower_set1.add_flower(rose)
        flower = Flower('re', 5, 10)
        chamomile = Chamomile(4, 25)
        flower_set2 = FlowerSet()
        flower_set2.add_flower(flower)
        flower_set2.add_flower(chamomile)

        bucket = Bucket()
        bucket.add_set(flower_set1)
        bucket.add_set(flower_set2)
        self.assertEqual(bucket.total_price(), 85)

        flower_set1.add_flower(tulip)
        flower_set1.add_flower(rose)
        bucket = Bucket()
        bucket.add_set(flower_set1)
        bucket.add_set(flower_set2)
        self.assertEqual(bucket.total_price(), 85)
