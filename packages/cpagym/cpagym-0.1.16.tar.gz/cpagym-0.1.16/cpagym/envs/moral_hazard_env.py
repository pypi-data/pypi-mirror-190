import gym
from gym import spaces
import numpy as np
import random

class MoralHazardEnv(gym.Env):
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
            reward = 0.05
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
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.state = np.array([0.8])
        self.steps = 0
        info = {}
        return self.state, info
    
    def render(self, mode="human"):
        pass
    
    def close(self):
        pass

if __name__ == '__main__':
    print("~"*120)
    env = MoralHazardEnv()

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