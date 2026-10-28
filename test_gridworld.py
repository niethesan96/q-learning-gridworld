import unittest

from gridworld import GridWorld, rollout, train, update_q


class GridWorldTests(unittest.TestCase):
    def test_collision_and_goal(self):
        env = GridWorld(('S#', '.G'))
        self.assertEqual(env.step(env.start, 0), (env.start, -5.0, False))
        self.assertEqual(env.step(env.start, 1), (env.start, -5.0, False))
        self.assertEqual(env.step((1, 0), 1), (env.goal, 100.0, True))
        self.assertEqual(env.step(env.goal, 0), (env.goal, 0.0, True))

    def test_terminal_update_does_not_bootstrap(self):
        q = {(0, 0): [0.] * 4, (0, 1): [999.] * 4}
        update_q(q, (0, 0), 1, 100, (0, 1), True, 0.1, 0.95)
        self.assertEqual(q[(0, 0)][1], 10.0)

    def test_nonterminal_update(self):
        q = {(0, 0): [0.] * 4, (0, 1): [10.] * 4}
        update_q(q, (0, 0), 1, -1, (0, 1), False, 0.5, 0.9)
        self.assertEqual(q[(0, 0)][1], 4.0)

    def test_bad_maps(self):
        for rows in [(), ('S', '..G'), ('S#G',), ('SSG',), ('S?G',)]:
            with self.assertRaises(ValueError):
                GridWorld(rows)

    def test_learning_across_seeds(self):
        env = GridWorld()
        for seed in (0, 7, 42):
            with self.subTest(seed=seed):
                q, history = train(env, seed=seed)
                path, _, success = rollout(env, q)
                self.assertTrue(success)
                self.assertEqual(len(path) - 1, env.shortest_distance())
                self.assertTrue(all(state in env.walkable for state in path))
                self.assertTrue(all(abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1
                                    for a, b in zip(path, path[1:])))
                self.assertEqual(len(history), 3000)

    def test_reproducibility(self):
        env = GridWorld(('S.G',))
        self.assertEqual(train(env, episodes=20), train(env, episodes=20))


if __name__ == '__main__':
    unittest.main()
