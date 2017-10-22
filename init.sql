--crm_role
insert crm_role values(1,'Dashborad',1,'/dashboard','fa-dashboard');
insert crm_role values(2,'MySQL集群状态',1,'#','fa-cubes');
insert crm_role values(3,'慢查询管理',1,'/slowlog/slowlogindex','fa-bolt');
insert crm_role values(4,'Inception',1,'#','fa-book');
insert crm_role values(5,'SQLAdvisor',1,'#','fa-gavel');

--crm_role_node
insert crm_role_node values(1,'状态监控','/dbcluster/monitor',2,1);
insert crm_role_node values(2,'任务管理','/dbcluster/crontab',2,2);
insert crm_role_node values(3,'Topology','/dbcluster/topology',2,3);
insert crm_role_node values(5,'工单管理','/inception/orderlist',4,1);
insert crm_role_node values(6,'上线SQL申请','/inception/submitsql',4,2);