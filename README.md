# SCF CLI

SCF CLI 是腾讯云无服务器云函数（Serverless Cloud Function, SCF）产品的命令行工具。通过 SCF 命令行工具，您可以方便地实现函数打包、部署、本地调试，也可以方便的生成云函数的项目并基于 demo 项目进一步的开发。

SCF CLI 通过一个函数模板配置文件，完成函数及相关周边资源的描述，并基于配置文件实现本地代码及配置部署到云端的过程。

目前 SCF CLI 以开源形式发布，您可以在本项目中查看命令行源代码及更多帮助文档，并可以通过项目 issue 反馈问题。

### 功能特性

通过 SCF 命令行工具，你可以：

* 快速初始化云函数项目
* 在本地开发及测试你的云函数代码
* 使用模拟的 COS、CMQ、Ckafka、API 网关等触发器事件来触发函数运行
* 验证 TCSAM 模板配置文件
* 打包、上传函数代码，创建函数及更新函数配置
* 获取函数列表，删除指定函数

### 快速入门

您可以前往腾讯云官网查看 [SCF 快速入门](https://cloud.tencent.com/document/product/583/33446)


### 详细使用指导


* [安装与配置](https://cloud.tencent.com/document/product/583/33449)
* [初始化示例项目](https://cloud.tencent.com/document/product/583/33450)
* [打包部署](https://cloud.tencent.com/document/product/583/33451)
* [日志查看](https://cloud.tencent.com/document/product/583/36352)
* [本地调试(native invoke)](https://cloud.tencent.com/document/product/583/35402)
* [本地调试(local invoke)](https://cloud.tencent.com/document/product/583/35401)
* [测试模板](https://cloud.tencent.com/document/product/583/33453)
* [模板文件](https://cloud.tencent.com/document/product/583/33454)
* [TCSAM 说明](https://cloud.tencent.com/document/product/583/36198)
* [更新日志](https://cloud.tencent.com/document/product/583/36908)
* [常见问题 FAQ](https://cloud.tencent.com/document/product/583/33456)
