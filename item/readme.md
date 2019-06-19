
1.需求分析
(1)并发方案：　Process多进程
(2)套接字:运用tcp防止数据丢失
2.数据库：
    (1)用户表：
        create table user(
        id int primary key auto_increment,
        username varchar(32) not null,
        password varchar(128) not null,
        tel int(24) unsigned,
        createtime datetime default now());
    (2)历史记录表：
        create table hist(
        id int primary key auto_increment, 
        username varchar(32) not null, 
        word varchar(32) not null, 
        time datetime default now());
3.结构设计, 如何封装,客户端服务端工作流程

　　 * 客户端 (发请求,展示结果)
	* 服务端 (逻辑操作,解决请求)
	* 数据库操作端 (操作数据库)
		界面处理    
		while True:
			界面1 
			while  True:
				界面2
4.功能划分：
    网络搭建
    注册
    登录
    查单词
    历史记录
   
注册: 客户端　R name passwd
登录: 客户端　L name passwd
退出: 客户端　E 
查单词: 客户端　Q name word
历史记录: 客户端　H name


