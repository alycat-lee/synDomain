# synDomain
自动更新阿里云域名解析工具
###  **_注意_** 
该脚本有2个前置条件
- 脚本所在网络的ip是公网ip
- 需要预装阿里云SDK

##  **设置** 
主要的配置是放在ali.json文件中
配置项在注释里有说明

##  **使用** 
python synDomain.py即可
返回ok即更新成功 
返回no need则不需要更新