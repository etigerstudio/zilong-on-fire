# 十面埋伏 Zilong on Fire

## 蓝图

- [x] 基本游戏控制器类
- [x] DeepQ网络
  - [x] 全连接
  - [x] CNN
  - [ ] 尝试优化方法
    - [x] 经验回放随机算法改进
    - [x] 独热编码状态 （改进效果暂不清楚）
    - [ ] batch_size和buffer_size超参数调优
    - [x] eps贪心概率线性退火1到0.1
    - [ ] 算法优化
        - [ ] DDQN
        - [ ] Dueling DQN
        - [ ] Prioritized Experience Replay
        - [ ] Rainbow
        - [ ] HER - Hindsight Experience Replay
  - [ ] Loss可视化
    - [ ] 累计reward
    - [ ] 单次loss
    - [ ] 单次存活时长
- [x] 简单的渲染器
- [x] 完善基本环境
  - [ ] Slash环境中惩罚连续挥击（已过时不再开发）
- [x] 2D渲染器
  - [ ] 角色一步操作里转两次bug？
  - [ ] 箭塔、箭位置微调对齐
  - [ ] 按照命名规范修改类名、文件名
  - [ ] 组织资源文件位置
- [x] 输出二维地图的环境
  - [x] Basic环境
  - [ ] Slash环境（已过时不再开发）
- [ ] RPG环境
  - [x] 世界
  - [ ] 游戏控制器
  - [ ] 所有实体
- [ ] 3D渲染器
  - [x] 游戏规则确定
  - [ ] Unity场景构建
  - [ ] Python-Unity通讯
- [ ] 补充注释
  - [ ] 类
    - [x] 1期
  - [ ] 函数
    - [x] 1期
  - [ ] 重点具体语句
    - [] 1期

## 项目组织结构

### env

环境类，管理状态保存、动作执行、回报计算。

- basic.py 基本环境，子龙静止。

### game

游戏控制器类，管理游戏生命周期，控制游戏的开始与结束、处理游戏对象（暗箭、子龙）之间的交互。

- game.py 基本游戏控制器。

### net

神经网络类，实现具体的神经网络（例如DeepQ)，定义网络结构，实现前向预测、反向传播逻辑。

- deep_q.py DeepQ网络实现。

### renderer

渲染器类，即各类游戏的图形化展示前端（例如命令行终端、tkinter、pyglet、pygame、panda3d等），实现渲染器的初始化、更新。

- base.py 空渲染器子类，待被继承实现。

## 强化学习元素

- 状态: 暗箭角度的分区编号，盾牌朝向的分区编号
- 动作: 盾牌左转、盾牌右转或盾牌不动
- 奖励: 盾牌朝向与暗箭角度的夹角（分区编号差值）

