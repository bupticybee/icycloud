# icycloud

一个基于docker的IAAS平台
示例站点： cloud.icybee.cn

思路基于： http://icybee.cn/article/57.html

# 部署方式(大概):

## 第一步 准备各种docker

0. `apt install docker.io`

1. 进入 `images\icy_baseimage-docker\image` 运行 `build.sh`

2. 进入 `images\jump-docker` 运行 `build.sh`

## 第二步 运行

1. 安装各种东西

先是apt

``` bash
apt install python python-pip uwsgi maria mariadb-common mariadb-client mariadb-server libmariadbd-dev rabbitmq-server
```

然后是pip

``` bash
pip install django
pip install celery
pip install django-celery
pip install docker
pip install mysql-connector-python --allow-external mysql-connector-python
pip install wusgi
pip install flask
```

然后是我因为菜不得不使用的

```bash
apt install screen
```

2. 把`web`文件夹放在一个合适的位置

3. 开始进行修改

大致位置如下

- `web\icycloud\icycloud_uwsgi.ini` 相关路径进行修改
- `web\icycloud\webui\tasks.py` \#42 域名
- `web\icycloud\icycloud\settings.py` \#29 很重要的key \#35 加上你的域名以确保访问 \#93 数据库相关
- `nginx_conf\sites-available\default` \#25 \#45 的域名进行修改 \#35 的路径 和下面的提示看一眼
- `router\router.py` \# 10 数据库相关

当然还有一些落下的,自己看着改吧,网站模板什么的就不改了,又不是不能用

4. 初始化

在`web\icycloud\manage.py` 文件所在目录下

``` bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. 运行

在有`icycloud_uwsgi.ini`的目录下面 运行 `uwsgi icycloud_uwsgi.ini`

准备一个在docker组里的低权限用户(虽然可以操作docker权限已经很高了),我用的是icycloud,来运行worker,不能用root,除非你强制这么做.

开一个screen,运行`sudo -u icycloud python manage.py celery worker -c 4 --loglevel=info`

进入 `router` 路径 再开一个screen(原谅我太菜了) 运行 `python router.py`

把nginx的配置文件放到他可以生效的位置,重启nginx

## 第三步 使用

访问自己配置的域名就可以得到和预览栈一样的效果,进入后台`/admin`然后使用创建的超级管理员创建一个邀请码,然后自己使用这个邀请码创建一个账号,就可以正常使用了.