# Faculty presentation script

**Project:** Q-learning in a Grid World  
**Suggested duration:** 8–10 minutes, plus questions  
**Presentation:** `presentation/Q_Learning_Grid_World.pptx`

Read the quoted paragraphs aloud. Instructions in square brackets are actions for you, not words to read. Replace `[your name]` before presenting. Rehearse once with a timer and speak at a comfortable pace.

## Before you begin

- Open the PowerPoint and use Presenter View if available.
- Open PowerShell in the project folder containing `gridworld.py`.
- Keep `results/learned_path.svg` open in a browser as a demo backup.
- Check that `py gridworld.py` and `py -m unittest -v` run successfully.
- Keep the report available if the faculty asks about implementation details.

## Slide 1 — Q-learning in a grid world

**About 30 seconds**

> Good morning, respected faculty members. My name is [your name]. Today I will present the project “Q-learning in a Grid World.”
>
> The project demonstrates how an agent can learn a route from a starting point to a goal while avoiding obstacles. I will explain the environment, the learning algorithm, the implementation, and the results, followed by a short demonstration.

[Pause briefly and move to slide 2. Use “Good afternoon” if appropriate.]

## Slide 2 — Problem and project objective

**About 40 seconds**

> The problem is to navigate a grid containing open cells and blocked cells. The agent begins at a fixed start cell and must reach a fixed goal.
>
> We do not provide the agent with a route during training. Instead, it tries actions and receives rewards. Over repeated episodes, it learns which actions lead to better outcomes.
>
> The objective is to implement this learning process, obtain a valid route, and compare its length with an independently computed shortest-path baseline.

## Slide 3 — Environment and rewards

**About 50 seconds**

> The default environment is a six-by-six grid. It contains eight obstacle cells and twenty-eight traversable cells, including the start and goal.
>
> The start is at row zero, column zero. The goal is at row five, column five. The agent can move up, right, down, or left. Diagonal movement is not allowed.
>
> A normal move gives a reward of minus one. Attempting to move into an obstacle or outside the grid gives minus five, and the agent remains in its current cell. Reaching the goal gives plus one hundred and ends the episode.
>
> These rewards encourage the agent to reach the goal, reduce unnecessary movement, and avoid repeated collisions. Each training episode has a maximum of two hundred actions.

## Slide 4 — How Q-learning updates action values

**About 65 seconds**

> Q-learning stores a value for each state and action pair. Here, a state is the agent’s current grid position. A Q-value estimates the discounted future reward from taking an action in that state.
>
> Initially, all Q-values are zero. After taking an action, the agent observes the reward and next state, then adjusts the selected Q-value toward a target.
>
> For an ordinary transition, the target is the immediate reward plus gamma times the highest Q-value in the next state. At the goal, the target is simply the immediate reward because the episode has ended.
>
> Alpha is the learning rate. It controls how much the current estimate changes. Gamma is the discount factor. It controls the influence of future rewards.
>
> For a simple example, if the current Q-value is zero, the terminal reward is one hundred, and alpha is zero point one, the new Q-value becomes ten.

[Point to the formula without reading every symbol aloud.]

## Slide 5 — Exploration and training settings

**About 45 seconds**

> The agent uses an epsilon-greedy strategy to balance exploration and exploitation. Exploration means trying a random action. Exploitation means choosing an action with the highest current Q-value.
>
> Epsilon starts at one, so the agent initially explores frequently. It decreases over training, with a minimum value of zero point zero five. This allows some exploration to continue.
>
> The default run uses three thousand episodes, a learning rate of zero point one, and a discount factor of zero point nine five. The random seed is forty-two, which makes the experiment reproducible under the same settings.

## Slide 6 — Training workflow

**About 40 seconds**

> The Q-table is initialized once before training. At the beginning of each episode, the agent returns to the start cell.
>
> It selects an action, receives the next state and reward, and updates one Q-value. It repeats this process until it reaches the goal or the action limit.
>
> The table carries what it has learned into the next episode. The program also records total reward, action count, success, and epsilon for every episode, so we can inspect how training progresses.

## Slide 7 — Project structure and live demonstration

**About 75 seconds, including the demo**

> The project uses Python and requires no additional packages to run. The main file, gridworld.py, contains the environment, trainer, evaluator, and command-line interface. The test file contains six automated tests.
>
> I will now run the default experiment.

[Switch to PowerShell in the project folder and run:]

```powershell
py gridworld.py
```

> The program trains the agent and then evaluates its greedy policy without random exploration. The printed map uses stars to mark the route. The summary reports whether the goal was reached, the number of moves, and the reward.
>
> It also saves the training history, learned Q-table, JSON summary, and a route visualization.

[Run the tests:]

```powershell
py -m unittest -v
```

> All six tests pass. These check movement rules, Q-value updates, map validation, reproducibility, and successful learning across multiple seeds.

[Return to the presentation. If the live demo fails, show the saved SVG and summary. Say: “I will use the saved output from the completed experiment to explain the result.” Do not describe a failed live run as successful.]

## Slide 8 — Training rewards improve as exploration falls

**About 40 seconds**

> This graph uses the rewards recorded during the actual training run. Each point is the average total reward over a consecutive block of one hundred episodes.
>
> Early rewards are lower because the agent explores, takes longer routes, and attempts blocked moves. As it learns and exploration decreases, average reward rises.
>
> These are training rewards, so they include exploratory actions. The final greedy evaluation is a separate measurement with exploration disabled.

## Slide 9 — The learned route reaches the goal in 10 moves

**About 50 seconds**

> This is the route produced by the learned greedy policy. The blue line connects the agent’s successive positions from S to G while avoiding the blocked cells.
>
> The route takes ten moves. An independent breadth-first search also finds that the shortest possible route has ten moves, so the learned route is optimal for this tested grid.
>
> The total evaluation reward is ninety-one. There are nine normal moves, each worth minus one, followed by the goal move worth one hundred.
>
> Breadth-first search only validates reachability and provides the baseline distance. It does not choose the training actions or supply the learned route.

## Slide 10 — Validation and test evidence

**About 40 seconds**

> The tests verify that the agent cannot enter obstacles or leave the grid. They also check that terminal updates exclude future rewards and ordinary updates include the discounted next-state value.
>
> The learning test runs three seeds: zero, seven, and forty-two. Each learns a valid ten-move route on the default map.
>
> In the saved default experiment, all of the final one hundred training episodes reach the goal. That result applies to this part of the experiment and does not establish success on every map.

## Slide 11 — GitHub publication workflow

**About 25 seconds**

> The project includes a step-by-step guide for publishing it to GitHub. The workflow is to create an empty online repository, initialize the local project with Git, commit the files, connect the repository URL, and push the main branch.
>
> The repository can then contain the code, tests, documentation, presentation, and example results together.

[If you have uploaded it before presenting, you may show your real repository. Do not claim it is already published unless you have completed the upload.]

## Slide 12 — Conclusions and future improvements

**About 40 seconds**

> The project demonstrates tabular Q-learning in a small navigation problem. Through repeated interaction and rewards, the agent learns a valid route that matches the shortest possible length on the tested grid.
>
> The current environment is static and deterministic. A different map requires retraining, and the results do not guarantee success for every configuration.
>
> Future improvements could include larger maps, uncertain movement, and a comparison with another reinforcement learning algorithm such as SARSA.
>
> Thank you for your time. I am ready to answer your questions.

## Likely faculty questions and suggested answers

### 1. What is reinforcement learning?

> Reinforcement learning is a method where an agent learns from interacting with an environment and receiving rewards. Its objective is to learn a policy that produces high expected cumulative reward.

### 2. What are the agent, state, action, and policy in your project?

> The agent is the learner moving through the grid. The state is its row and column. An action is one of the four movement directions. The policy is the rule for selecting an action from a state. Training uses an epsilon-greedy policy, and evaluation selects the highest-Q action.

### 3. Why did you use Q-learning?

> It is suitable for a small environment with discrete states and actions. A table is sufficient, which makes the learning process easy to inspect without a neural network. It also demonstrates how rewards can guide navigation through repeated experience.

### 4. Is Q-learning model-free?

> Yes. Its updates use experienced transitions and rewards without requiring a transition-probability model. The simulator implements the movement rules, but the Q-learning trainer learns its action values from interaction.

### 5. Why use Q-learning when BFS can find the path directly?

> For a known, fixed, unweighted grid, BFS is a simpler direct shortest-path solver. This project’s purpose is to demonstrate reinforcement learning. BFS supplies an independent baseline so we can evaluate the route that Q-learning learned.

### 6. Does the agent always avoid obstacles?

> The environment always prevents it from entering obstacles. During training, it can attempt blocked moves and receive a penalty. The evaluated learned route contains no such collisions on the default grid.

### 7. Why does the goal give 100 while an ordinary move gives minus 1?

> The positive goal reward encourages completion, while the step penalty discourages unnecessary movement. The collision penalty discourages repeated blocked actions. These are design choices that can be changed and tested.

### 8. What happens if epsilon is zero from the start?

> The agent acts greedily using its initial estimates and tie-breaking behavior. It may explore insufficiently and learn a poor policy. Starting with a high epsilon encourages it to try different actions before relying on its estimates.

### 9. How large is the Q-table?

> There are twenty-eight traversable states and four actions, so the table contains one hundred and twelve values. This includes four goal-state entries, which remain zero during training because no actions are taken after the terminal transition.

### 10. What is an episode?

> An episode is one attempt beginning at the start. It ends when the agent reaches the goal or when the two-hundred-action limit truncates the attempt.

### 11. Why treat the goal differently from the action limit?

> The goal is a terminal state, so no future reward follows it. The action limit is an artificial training cutoff. The underlying state can still have future value, so its final update retains the next-state term.

### 12. Does your experiment prove convergence?

> No. It shows successful learning for the tested maps, seeds, and settings. General convergence has additional assumptions, and a finite experiment with a fixed learning rate does not establish it for every environment.

### 13. Why is Q-learning called off-policy?

> It learns using the value of the best next action, even when the exploration policy actually chooses a different action. The policy producing the experience can therefore differ from the greedy policy represented by the update target.

### 14. How is Q-learning different from SARSA?

> Q-learning uses the maximum next-state action value in its target. SARSA uses the value of the next action actually selected by its policy. SARSA is on-policy, whereas Q-learning is off-policy.

### 15. What happens when the map changes?

> The learned table is specific to the original map. I would create the new environment and retrain. The program checks whether the goal is reachable before training and rejects an unreachable map.

### 16. What is the difference between return and discounting here?

> The Q update uses gamma to discount future rewards. The reward printed for an episode or greedy rollout is the ordinary sum of rewards without discounting. That is why the reported ten-move route earns ninety-one.

### 17. What are the main limitations?

> The map is small, fully observed, and deterministic. The project does not evaluate generalization to new maps, moving obstacles, or uncertain movement. Table storage also grows as the state space grows.

### 18. Did you develop the project entirely without assistance?

> I used AI assistance to help build and document the project. I have reviewed the implementation, run the tests, and prepared to explain the learning process and results.

[Use this answer only after you have personally reviewed and run the project. Be accurate about your own contribution and follow your institution’s rules on assistance.]

## Short version if the faculty gives you only two minutes

> Good morning. My project implements Q-learning to solve a grid navigation problem.
>
> The environment is a six-by-six grid containing a start, a goal, and eight obstacles. The agent chooses up, right, down, or left. A normal move gives minus one, a blocked move gives minus five, and reaching the goal gives plus one hundred.
>
> Q-learning stores a value for every state and action pair. After each move, the program updates that value using the reward and the best estimated future value. An epsilon-greedy policy initially explores frequently, then gradually uses what it has learned.
>
> The default experiment trains for three thousand episodes with seed forty-two. Evaluation then disables exploration. The learned route reaches the goal in ten moves with a total reward of ninety-one.
>
> An independent BFS baseline also gives ten moves, confirming that the route is shortest on this grid. BFS is used for validation, while the agent’s actions come from its learned Q-table.
>
> Six automated tests pass, including successful shortest-route learning across three random seeds. The project saves its Q-table, episode history, summary, and route visualization.
>
> The main limitation is that the environment is small and fixed. Future work could explore larger maps and uncertain movement. Thank you.
