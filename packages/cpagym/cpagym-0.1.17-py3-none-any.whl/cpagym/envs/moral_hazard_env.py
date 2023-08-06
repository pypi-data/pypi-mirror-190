import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
#Alignment with problem definition: The environment appears to model a simple moral hazard problem, but it may not be sufficient to accurately capture the complexity of real-world moral hazard problems.

#Relevant rewards: The rewards provided by the environment are aligned with the problem definition and encourage the agent to not take action. However, the reward signal may not be complex enough to reflect the nuances of the problem and guide the agent towards an optimal solution.

#Difficulty: The environment may not be challenging enough, as the state always starts at a value of 0.8 and the agent is only rewarded for not taking action. This may not provide a sufficient range of learning opportunities for the agent.

#Data availability: The code does not specify the maximum number of steps per episode, so it is unclear whether the environment generates enough data to support training of a reinforcement learning agent.

#Scalability: The code does not specify how the environment would scale to larger problems, so it is unclear whether it would remain effective as the problem size increases.

class Moral_HazardEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    def __init__(self, max_steps=1000, max_state=1.0, min_state=0.0, termination_state=0.5):
        self.observation_space = spaces.Box(low=min_state, high=max_state, shape=(1,))
        self.action_space = spaces.Discrete(2)
        self.additional_info = None
        self.state = np.array([0.8])
        self.max_steps = max_steps
        self.steps = 0
        self.termination_state = termination_state
        self.min_state = min_state
        self.max_state = max_state
    def transition(self,action):
        if action:
            self.state[0] = min(self.state[0] + 0.05, 1)
        else:
            self.state[0] = max(self.state[0] - 0.05, 0)
        return self.state 
    def reward(self, action, terminated):
        if action:
            reward =  0
        else:
            reward=0.05
        if terminated:
            reward = -1
        return reward
    def step(self, action):
        self.steps += 1
        info = {}
        new_state = self.transition(action)
        truncated = self.steps >= self.max_steps
        terminated = bool(self.state[0] < self.termination_state)
        reward = self.reward(action, terminated)
        self.state = new_state
        return new_state, reward, terminated, truncated, info
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation= np.array([0.8])
        info = {}
        #print(observation)
        return observation,info  # reward, done, info can't be included
    def render(self, mode="human"):
        pass
    def close(self):
        pass
if __name__ == '__main__':
    print("~"*120)
    env = Moral_HazardEnv()

# Reset the environment to get the initial state
    obs,_= env.reset()

# Take 10 steps in the environment
    for i in range(10):
        action = env.action_space.sample() # select a random action
        obs, reward, done,_,info = env.step(action) # take a step in the environment
        print("Observation at step {}: {}".format(i, obs))
        print("Reward at step {}: {}".format(i, reward))
        
        if done:
            print("Episode finished after {} steps".format(i+1))
            break