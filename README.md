使用Django和Vue开发一个生鲜电商平台，采用前后端分离技术实现。

#### 安装环境依赖
在克隆或下载项目后，在项目目录下执行`pip install -r requirements.txt`命令安装项目所需库。

#### V1.0
搭建项目整体框架，先进行项目初始化、进行数据库和app配置，并进行用户、商品、交易和用户操作数据模型的设计，并配置xadmin后台管理系统，最后实现数据映射和测试数据导入。

#### V1.1
在V1.0的基础上使用搭建前端项目框架，根据项目需求构建所需要的组件。

#### V1.2
主要实现DRF（Django Restful Framework），先通过普通方式实现商品详情页，再通过DRF的各种View实现，最后实现过滤（包括字段过滤、搜索和筛选）。

#### V1.3
先通过嵌套方式实现商品类别数据接口，再通过Vue展示商品分类，最后实现展示商品列表页数据和搜索功能。