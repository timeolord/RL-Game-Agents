from gym.envs.registration import register

register(
    id='brawlhalla-v0',
    entry_point='brawlhalla.envs:brawlhalla_env',
)
