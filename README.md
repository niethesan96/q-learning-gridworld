# Q-learning Grid World

A complete, dependency-free Python project that learns to navigate from a start to a goal while avoiding walls. Requires Python 3.9 or newer.

## Run

Open a terminal in this folder:

```sh
python gridworld.py
python -m unittest -v
```

On Windows, use `py` in place of `python` if needed.

The program trains for 3,000 episodes, evaluates its greedy policy, prints the route, and saves results in `results/`. Open `results/learned_path.svg` in a browser to see the route. The exit code is 0 when evaluation reaches the goal and 1 when it fails.

## Environment

The default world is a 6 × 6 grid:

```text
S.....
.###..
...#..
.#....
.#.##.
.....G
```

- `S`: start; `G`: goal; `#`: obstacle; `.`: open cell.
- Actions: up, right, down, left. No diagonal moves.
- Legal move: reward −1. Wall or obstacle collision: reward −5 and the agent stays in place. Reaching the goal: reward +100 and the episode ends.
- Episodes stop after 200 actions if the goal is not reached.

## Learning algorithm

Each traversable cell has four Q-values, initialized to zero. An epsilon-greedy policy chooses a random action with probability epsilon and a maximum-Q action otherwise. Training breaks maximum-Q ties randomly using a seeded generator.

```text
target = reward                         if the next state is terminal
target = reward + gamma * max(Q[next])   otherwise
Q[state, action] += alpha * (target - Q[state, action])
```

Defaults: learning rate `alpha = 0.1`, discount `gamma = 0.95`, epsilon starts at `1.0` and decays by `0.997` each episode to a floor of `0.05`. A time limit truncates an episode without making the state terminal, so updates still bootstrap at that boundary.

Evaluation disables exploration and resolves ties in up/right/down/left order. It stops on the goal, a repeated state, or the action limit. The default seed is 42. Q-learning is a learning method, so short training runs or different maps may need more episodes; success is checked explicitly.

## Customize

```sh
python gridworld.py --episodes 5000 --seed 7 --max-steps 300
python gridworld.py --map example_map.txt --output-dir custom_results
```

Custom maps must be rectangular and use only `.`, `#`, `S`, and `G`, with exactly one start and one reachable goal. The `train()` API also accepts learning and exploration parameters.

## Saved results

| File | Contents |
| --- | --- |
| `training.csv` | Per-episode reward, actions, success, and epsilon |
| `q_table.json` | Learned action values keyed by row,column (zero-based) |
| `summary.json` | Greedy route, reward, success, and training statistics |
| `learned_path.svg` | Grid and learned route |

The summary includes a breadth-first-search shortest-path length as an independent evaluation baseline. Breadth-first search validates reachability and measures the result; it does not select training actions or construct the learned route. Multiple shortest routes may exist.

## Project files

`gridworld.py` contains the environment, Q update, trainer, evaluator, visualization, and CLI. `test_gridworld.py` checks collisions, terminal and nonterminal updates, invalid maps, reproducibility, and successful shortest-route learning across three seeds.

## Documentation and presentation

- [Full project documentation (PDF)](docs/Project_Documentation.pdf)
- [Editable project documentation (Word)](docs/Project_Documentation.docx)
- [Step-by-step GitHub upload guide](docs/GITHUB_GUIDE.md)
- [PowerPoint presentation with speaker notes](presentation/Q_Learning_Grid_World.pptx)
- [Faculty presentation speaking script and questions](script.md)

The presentation covers the objective, environment, Q update, training settings, workflow, reward chart, learned route, tests, GitHub publication, and limitations. The saved experiment learns an optimal 10-move route with a greedy reward of 91.
