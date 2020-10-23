# 狼人杀发牌器
[网页地址](https://weiyinfu.cn/Wolf/index.html)

## 功能说明
* 创建房间 
* 进入房间（房主视图/玩家视图）

# 涉及到的技术
## 定时器
房间的存活时间是5小时，如果5小时内房间内无人活动，则房间自动解散。

## 并发
如果多进程且没有同步机制，会出现两个用户同时领到女巫、预言家的情况，导致场上有两个预言家、两个女巫。  
如果部署多实例，那么必定需要并发控制。  
* 如果部署到多个实例，那么需要并发控制
* 也可以设置一个单实例路由器，把房间路由到特定实例
* 更简单的方式是始终是单实例部署，本repo就是如此。

## 业务设计
* 如何设计业务才能够防止被攻击，才能防止用户作弊。
* 房间如何防止被无关人员发现并进入
* 同一个用户多次刷新领到同一个身份
