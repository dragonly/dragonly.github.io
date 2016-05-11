---
title: Spark+Intellij 舒服的源码开发环境配置
last_updated: 2016-05-10
category: note
---

# **TL;DR**
---

```
放弃 spark 💩
```


## 废话
---

记录一下关于 spark 开发的相关环境配置, 以及与 intellij 的集成.

> 本文针对的是需要了解 **spark 源码** 的情况下的开发环境配置. 如果只是需要写 spark job, 而并不想 trace 到源码里面去看运行上下文, 那么有很多资料讲这个的了: 无非是下载 spark 的 jar, 新建一个 scala/python/R 项目, 花式把这个 jar 设置成依赖就可以开始写了. 具体怎么运行 spark job, 在官方文档中已经写得很清楚了. 本文记录的 **不是** 后一种情况

由于实验室工作需要于是开始学习 spark 的源码. 之前都是东一坨西一块地配置, 好了也不知道为什么, 没好也只会到处找相关 blog, 然后关闭项目再从头 import 试试. 大部分能找到的中文资料还是比较没用, 或者只能干掉一两件事, 于是坐下来好好看了看 maven 的入门文档 (因为 spark 开发组偏向于 maven 做项目管理, 感觉钦定的比较🐵), 从头到尾地把大部分入门 spark 开发的 intellij 配置给手动操作了一遍, 目前算是一篇`milestone`文档.


### *<del>可能的</del>前置要求*

1. *能够翻墙*
2. *Windows 没有充分测试, 建议 **POSIX** 环境*
3. <del>脑补能力</del>


## 配置代码阅读环境 `符号跳转`
---

### 获取 spark 源码

从[这里](spark-download)选择一个镜像, 下载源码 (我用的是`spark-1.6.1.tgz`).

### 编译

`build/mvn -Pyarn -Phadoop-2.4 -Dhadoop.version=2.4.0 -DskipTests clean package`
执行一次干净的从头编译, 包括所有 spark submodules, 不运行测试

在[官方文档](spark-build)里面有更详细的介绍

### 导入 Intellij 项目

在 Intellij 什么项目也没有打开的小页面, 选择

```
Import Project
    -> /path/to/spark-1.6.1/
    -> 单选 Import project from external model[Maven]
    -> 勾选 Search for projects recursively
    -> Next -> Next -> Next -> Next -> Finish
```

### 配置依赖

#### Maven

等待 Intellij 下方状态条显示 Index 和 Resolve Dependencies 等工作结束, 查看左边`Project`视图最下方的`External Libraries`, 展开后应该只有`JDK`

在`Project`视图中, 右键点击根目录 (spark-1.6.1) 下的`pom.xml`文件, 选择 `Maven -> Reimport`, 完成后在`External Libraries`内会找到大量 spark 项目的 maven 依赖

> 如果没有执行之前的编译操作, 这一步大概并不能找到 maven 依赖

#### Scala

随便打开一个 scala 文件, 比如`examples/src/main/scala/org/apache/spark/examples/SparkPi`, 编辑器右上角会提示设置 scala sdk, 建议设置为`2.10.5`版本

> 如果下拉框里面没有 scala sdk, 那么创建一个, 如果创建窗口里面仍然没有, 点击`Download`下载一个, 注意版本别太高, 行为未知

到这个地方, Intellij 已经解析了需要的依赖的symbol, 跳转功能正常, 已经可以**阅读**代码了. 接下来的配置是为了更好地<del>编写</del>**调试**代码


## 配置代码开发环境 `编译->打包->运行`
---

### 改动后快速编译

如果每次都使用之前的编译整个项目的`mvn`命令进行编译的话, 每天工作10小时大概能改20多次代码💩. 我想帮老板多干点活, 于是搬砖之前先去考察下有没有解决方案. 这里有一个能用的方案, 有更好的再更新.

Intellij 提供了比较好的 maven GUI 集成, 所以我们可以通过鼠标和快捷键来运行`maven lifecycle/goal`. 在 Intellij 里面打开`View -> Tool Buttons`, 此时右侧会有`Maven Projects`按钮, 点击可以打开能够执行的 `maven lifecycle/goal`. 比如我更改了 `examples/.../SparkPi.scala`文件, 然后想重新编译打包运行, 那么我找到`Maven Projects -> Spark Project Examples -> Plugins`, 先双击运行`scala -> scala:compile`, 完成之后再双击运行`jar -> jar:jar`, 可以看到编译出来了对应的 jar (在console里面注意`SUCCESS`之前的信息, 这个 jar 是需要在运行`spark-submit`的时候指定的).

当然为了能够把这两件事一起做, 更重要的是跟下一步*远程调试*一起做掉, 最好的方式还是写进脚本在 CLI 运行. 我们在`spark-1.6.1`根目录下运行`mvn -pl examples scala:compile jar:jar`, 告诉 maven 只在 examples 这个 submodule 下运行`scala:compile`和`jar:jar`两个 `maven goals`, 能够看到类似输出

```
➜  ~/work/spark-1.6.1  mvn -pl examples scala:compile jar:jar
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building Spark Project Examples 1.6.1
[INFO] ------------------------------------------------------------------------
[INFO]
[INFO] --- scala-maven-plugin:3.2.2:compile (default-cli) @ spark-examples_2.10 ---
[INFO] Using zinc server for incremental compilation
[info] Compile success at May 11, 2016 11:42:13 PM [0.390s]
[INFO]
[INFO] --- maven-jar-plugin:2.6:jar (default-cli) @ spark-examples_2.10 ---
[INFO] Building jar: /Users/dragonly/work/spark-1.6.1/examples/target/spark-examples_2.10-1.6.1.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 10.931 s
[INFO] Finished at: 2016-05-11T23:42:15+08:00
[INFO] Final Memory: 54M/762M
[INFO] ------------------------------------------------------------------------
```

可以看到我们的改动后的 examples 的代码被编译打包到了`spark-1.6.1/examples/target/spark-examples_2.10-1.6.1.jar`.


### 远程调试

#### 废话

由于 spark job 的运行需要 spark 环境, 不同于以往的单机程序, 需要借助`bin/spark-submit`脚本提交给 spark 去运行 (查看脚本源码可以知道, 启动前要先做一些环境检查和初始化, 然后调用 launcher 和 deploy 相关 class 去加载和运行提交的 jar). 因此断点调试起来会比较麻烦, 因为这个 server 端跟我们写的代码是两个 process (广义), 所以需要类似 gdb 的远程调试一样的功能. 原理上讲是给出一堆运行参数, 让 jvm 运行 spark 的时候, 开一个调试端口, 然后在 Intellij 这边用 debugger 远程连过去进行调试. 虽然说是"远程", 但是在这种情况下其实就是 localhost 上开的端口而已.

#### Intellij 创建远程调试的 Debug Configuration

进入`Run -> Edit Configurations`, 单击左上角`+`, 新建一个 Remote Configuration, 名字随便改一下, 其余留作默认. 点击`OK`之前, 复制`Configuration`tab下的`Command line arguments for running remote JVM`里面的内容, 之后会用到这个参数, 并做如下更改

```
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
改成
-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005
```

 然后点`OK`创建这个 Configuration.

#### 命令行

先运行`mvn -pl examples scala:compile jar:jar`进行编译和打包, 然后运行

```
bin/spark-submit \
--driver-java-options "-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005" \
--class org.apache.spark.examples.SparkPi \
examples/target/spark-examples_2.10-1.6.1.jar
```

注意到第二行的参数是告诉 spark 运行的时候设置额外的 java 参数, 就是上面复制出来的参数, 改成`suspend=y`是告诉 spark 启动之后暂停运行, 等待 debugger 连接之后才开始运行, 方便我们加断点.

然后 CLI 会显示`Listening for transport dt_socket at address: 5005`, 表示 spark 正在等待 debugger 连接.

此时只需要在 Intellij 上打开`SparkPi.scala`文件, 加上断点, 再点`Run -> Debug 'Remote'`, 就能开始单步追踪调试了.


### PS

目前正在一边看源码, 一边看 [www.artima.com/pins1ed](www.artima.com/pins1ed) 学 scala, 这是官方推荐的 spark book 的第一版, 免费阅读, 虽然是 2008 年出版的, 但是感觉大部分内容还是覆盖了 scala 的关键用法, 值得当做遇到不太明白的 scala 语法的时候的查阅资料.


[spark-download]: http://spark.apache.org/downloads.html
[spark-build]: https://spark.apache.org/docs/latest/building-spark.html