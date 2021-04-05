import gym
import numpy as np
from gym.vector.tests.utils import make_env
from stable_baselines.common import make_vec_env
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.policies import MlpPolicy, MlpLnLstmPolicy, MlpLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines import PPO2, ACKTR, A2C
import os
import win32gui
from brawlhalla.envs.brawlhalla_env import brawlhalla_env
from hotlinemiami import hotlinemiami_env


def train():
    env = hotlinemiami_env()

    env = make_vec_env(lambda: env, n_envs=1)

    # model = A2C(MlpPolicy, env, verbose=1)

    model = A2C.load("Hotlinemiami.zip")

    model.set_env(env)

    model.learn(total_timesteps=1000)

    print("Saving model")

    model.save("Hotlinemiami")

    env.reset()

    # env.close()


def test():
    env = hotlinemiami_env()

    env = make_vec_env(lambda: env, n_envs=1)

    # model = PPO2.load("Brawlhalla")

    model = A2C(MlpPolicy, env, verbose=1)

    for episode in range(10):
        observation = env.reset()
        done = False
        while not done:
            action, _states = model.predict(observation)
            observation, rewards, done, info = env.step(action)
            # print(rewards)
            # env.render()
    # env.close()


while True:
    train()
# test()
