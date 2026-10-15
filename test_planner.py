import unittest
from src.planner import astar

class AStarTests(unittest.TestCase):
    def test_straight_path(self):
        self.assertEqual(astar(4, 3, set(), (0, 0), (3, 0)), [(0,0),(1,0),(2,0),(3,0)])
    def test_avoids_obstacle(self):
        path = astar(3, 3, {(1, 0)}, (0, 0), (2, 0))
        self.assertTrue(path)
        self.assertNotIn((1, 0), path)
        self.assertEqual(path[0], (0, 0)); self.assertEqual(path[-1], (2, 0))
    def test_no_path(self):
        self.assertEqual(astar(3, 3, {(1,0),(1,1),(1,2)}, (0,1), (2,1)), [])
    def test_blocked_endpoint(self):
        self.assertEqual(astar(3, 3, {(0,0)}, (0,0), (2,2)), [])

if __name__ == "__main__": unittest.main()
