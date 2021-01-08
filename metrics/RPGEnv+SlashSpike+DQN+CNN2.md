# Baseline

参考训练参数

eps_initial=1,
eps_minimum=0.15,
eps_decay_steps=15000,
train_freq=4,
target_update_freq=100,
buffer_size=2000,
learning_rate=0.001,
batch_size=64

DESTROY_REWARD = 0.125
VAIN_SLASH_REWARD = -0.125

self.c1 = Conv2D(filters=16, kernel_size=(4, 4), strides=2, activation='relu')  # 卷积层
self.c2 = Conv2D(filters=32, kernel_size=(2, 2), strides=1, activation='relu')  # 卷积层
self.flatten = Flatten()
self.d1 = Dense(64, activation='relu')
self.d3 = Dense(output_dim)

DQN is frozen! round:14800 timestep:64971 network_train_times:15744
DQN is frozen! round:11000 timestep:38347 network_train_times:9088
DQN is frozen! round:15200 timestep:65183 network_train_times:15797

# Exploration steps

epsilon探索概率线性退火到多少步（每次训练衰减一次），默认15000

## 50000

r:29200 t:95734 epoch 23400 Won't converge

## 7500

epoch 22200 won't

# Buffer size

经验回放缓存总数，默认2000

## 4000

loss: 0.06982903480529785 epoch: 17800
DQN is frozen! round:16400 timestep:75737 epoch:17935

# Reward

回报设计，主要是指砍掉仙人掌给多少（给不给）正向回报、攻击落空给多少（给不给）负向回报

默认值0.125、-0.125

## No Vain Slash

DESTROY_REWARD = 0.25
VAIN_SLASH_REWARD = 0

# Batch size

一个epoch（训练一次）的batch大小，默认64

## 32

Won't converge loss: 0.027185585498809815 epoch: 70600

# train_freq

每玩几步训练一次，默认4

## 8 7500

epoch: 19200
DQN is frozen! round:23600 timestep:155786

## 1 15000

epoch: 111092

# CNN2

CNN结构和参数

## 16, (3,3), stride=0, fc=64 单层CNN

loss: 0.044364948272705075 epoch: 19800
loss: 0.04180571556091309 epoch: 20000
DQN is frozen! round:17200 timestep:82167

# TCNN

CNN出除了矩阵，还会将回合当前计时TimeStep传入全连接

# RandomReset

是否随机重设玩家位置和宝藏位置，默认随机生成