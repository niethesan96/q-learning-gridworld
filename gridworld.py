"""Dependency-free tabular Q-learning for a deterministic grid world."""
from __future__ import annotations

import argparse
import csv
import json
import random
from collections import deque
from pathlib import Path

ACTION_NAMES = ('up', 'right', 'down', 'left')
DELTAS = ((-1, 0), (0, 1), (1, 0), (0, -1))
DEFAULT_MAP = ('S.....', '.###..', '...#..', '.#....', '.#.##.', '.....G')


class GridWorld:
    """# is an impassable obstacle, S is start, and G is terminal."""

    def __init__(self, rows=DEFAULT_MAP):
        self.rows = tuple(rows)
        if not self.rows or not self.rows[0] or len({len(r) for r in self.rows}) != 1:
            raise ValueError('Map must be a nonempty rectangle.')
        if any(c not in '.#SG' for row in self.rows for c in row):
            raise ValueError('Map supports only ., #, S, G.')
        self.height, self.width = len(self.rows), len(self.rows[0])
        self.states = [(r, c) for r in range(self.height) for c in range(self.width)
                       if self.rows[r][c] != '#']
        starts = [s for s in self.states if self.rows[s[0]][s[1]] == 'S']
        goals = [s for s in self.states if self.rows[s[0]][s[1]] == 'G']
        if len(starts) != 1 or len(goals) != 1:
            raise ValueError('Map must contain exactly one S and one G.')
        self.start, self.goal = starts[0], goals[0]
        self.walkable = set(self.states)
        if self.shortest_distance() is None:
            raise ValueError('Goal is unreachable from start.')

    def step(self, state, action):
        if state not in self.walkable or action not in range(4):
            raise ValueError('Invalid state or action.')
        if state == self.goal:
            return state, 0.0, True
        dr, dc = DELTAS[action]
        target = (state[0] + dr, state[1] + dc)
        if target not in self.walkable:
            return state, -5.0, False
        done = target == self.goal
        return target, 100.0 if done else -1.0, done

    def shortest_distance(self):
        queue = deque([(self.start, 0)])
        seen = {self.start}
        while queue:
            state, distance = queue.popleft()
            if state == self.goal:
                return distance
            for dr, dc in DELTAS:
                nxt = (state[0] + dr, state[1] + dc)
                if nxt in self.walkable and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, distance + 1))
        return None


def greedy_action(values, rng=None):
    best = [a for a, value in enumerate(values) if value == max(values)]
    return rng.choice(best) if rng else best[0]


def update_q(q, state, action, reward, nxt, done, alpha, gamma):
    target = reward if done else reward + gamma * max(q[nxt])
    q[state][action] += alpha * (target - q[state][action])


def train(env, episodes=3000, alpha=0.1, gamma=0.95, epsilon_start=1.0,
          epsilon_min=0.05, epsilon_decay=0.997, max_steps=200, seed=42):
    if episodes < 1 or max_steps < 1:
        raise ValueError('Episodes and max_steps must be positive.')
    if not 0 < alpha <= 1 or not 0 <= gamma <= 1:
        raise ValueError('Require 0 < alpha <= 1 and 0 <= gamma <= 1.')
    if not 0 <= epsilon_min <= epsilon_start <= 1 or not 0 < epsilon_decay <= 1:
        raise ValueError('Invalid exploration settings.')
    rng = random.Random(seed)
    q = {state: [0.0] * 4 for state in env.states}
    history = []
    for episode in range(episodes):
        epsilon = max(epsilon_min, epsilon_start * epsilon_decay ** episode)
        state, total, done = env.start, 0.0, False
        for steps in range(1, max_steps + 1):
            action = rng.randrange(4) if rng.random() < epsilon else greedy_action(q[state], rng)
            nxt, reward, done = env.step(state, action)
            # Time limits truncate a trajectory; only the goal is terminal.
            update_q(q, state, action, reward, nxt, done, alpha, gamma)
            state, total = nxt, total + reward
            if done:
                break
        history.append(dict(episode=episode + 1, reward=total, steps=steps,
                            success=done, epsilon=epsilon))
    return q, history


def rollout(env, q, max_steps=200):
    path, state, total = [env.start], env.start, 0.0
    for _ in range(max_steps):
        state, reward, done = env.step(state, greedy_action(q[state]))
        path.append(state)
        total += reward
        if done:
            return path, total, True
        if state in path[:-1]:
            break  # A deterministic greedy policy will repeat this cycle forever.
    return path, total, False


def render_svg(env, path):
    cell, margin = 64, 24
    width, height = env.width * cell + margin * 2, env.height * cell + 80
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#f8fafc"/>',
             '<text x="24" y="28" font-family="sans-serif" font-size="20" fill="#0f172a">Q-learning: learned greedy route</text>']
    for r in range(env.height):
        for c in range(env.width):
            char = env.rows[r][c]
            color = {'#': '#334155', 'S': '#bfdbfe', 'G': '#bbf7d0'}.get(char, '#ffffff')
            x, y = margin + c * cell, 48 + r * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color}" stroke="#cbd5e1"/>')
            if char in 'SG':
                parts.append(f'<text x="{x + 32}" y="{y + 39}" text-anchor="middle" font-family="sans-serif" font-size="22">{char}</text>')
    points = ' '.join(f'{margin + c * cell + 32},{48 + r * cell + 32}' for r, c in path)
    parts.append(f'<polyline points="{points}" fill="none" stroke="#2563eb" stroke-width="5" stroke-linejoin="round" opacity="0.7"/>')
    parts.append('</svg>')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=int, default=3000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--max-steps', type=int, default=200)
    parser.add_argument('--map', type=Path, help='Text map using S, G, #, and .')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).parent / 'results')
    args = parser.parse_args()
    try:
        env = GridWorld(args.map.read_text().splitlines() if args.map else DEFAULT_MAP)
        q, history = train(env, episodes=args.episodes, seed=args.seed, max_steps=args.max_steps)
    except ValueError as exc:
        parser.error(str(exc))
    path, reward, success = rollout(env, q, args.max_steps)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / 'training.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(history[0]))
        writer.writeheader()
        writer.writerows(history)
    summary = dict(seed=args.seed, episodes=args.episodes, reached_goal=success,
                   greedy_steps=len(path) - 1, greedy_reward=reward,
                   shortest_possible_steps=env.shortest_distance(), path=path,
                   last_100_training_success_rate=sum(h['success'] for h in history[-100:]) / len(history[-100:]))
    (args.output_dir / 'summary.json').write_text(json.dumps(summary, indent=2))
    (args.output_dir / 'q_table.json').write_text(json.dumps({f'{r},{c}': dict(zip(ACTION_NAMES, values)) for (r, c), values in q.items()}, indent=2))
    (args.output_dir / 'learned_path.svg').write_text(render_svg(env, path))
    display = [list(row) for row in env.rows]
    for r, c in path[1:-1]:
        if display[r][c] == '.':
            display[r][c] = '*'
    print('\n'.join(' '.join(row) for row in display))
    print(json.dumps(summary, indent=2))
    print(f'Results saved to {args.output_dir.resolve()}')
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
