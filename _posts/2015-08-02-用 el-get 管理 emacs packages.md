---
last-updated: 2015-08-02
title: 用 el-get 管理 emacs packages
categories: emacs casual note
---
好久不更新博客了，先扯点乱七八糟的吧。从复旦毕业是人生中的一件大事，见多了离别时候的各种场面，到如今也抒不出什么浓烈的情感了，只是祝大家能够得到自己想要的前程，但是不要迷失在了别人的目光里。

我觉得自己是个有点奇怪的人，既是人来疯，又很喜欢独处，琢磨一些别人看起来无关紧要的东西，我却觉得不必跟他们争什么意义。大部分时候很少有人理解自己不 是一件很快乐的事情，然而从这种痛苦中也能让自己更加具有思辨和质疑的能力。最近学emacs也是这种感觉，虽然从数学系过来读CS，但是这不妨碍我想象出来，上个世纪的hackers用elisp写出一个奇怪的小玩意儿时候开心的表情，就像小时候对着搓了一下午奇形怪状的泥巴傻笑一样。话不多说，写下今天研究`el-get`的经验，算作是笔记，也是对之后能坚持更新博客的一次鼓励吧。

写代码的人大概都知道geek中vi[m]?和emacs两派的圣战，这是一个挺有意思的话题，有兴趣可以搜索
**vi emacs holy war**去看各种以前的谈(si)论(bi)。不过目前大家的争论范围通常跑到了IDE和emacs/vim加plugin/extention的话题上，这我觉得就不是很有意思了，想看撕逼可以知乎。我之所以觉得前一个holy war有趣，是因为当时的条件所限，其实这两个东西满足了两部分人的哲学。vi做出来的时候，原作者想优化它，使得在300bit的带宽下也能远程编辑，emacs做出来后，lisp赋予其无穷的扩展性让人着迷，甚至有人说它是一个附带了编辑器的操作系统。我之前也用过一段时间vim，并不是大神，并没有滚键盘如飞，但是我还是想玩一玩emacs，所以现在尝试把最基础的包管理功能做到当前最好，方便以后的使用和玩耍:)

话说回来，[`el-get`][el-get]是dimitri开发的一个emacs包管理器 ，代码托管在Github上，是个开源项目。emacs包管理器的历史其实已经很长了，其中elpa，melpa，marmalade，emacswiki等都是比较常见的repo。因为emacs是GNU开源软件基金会host的一个东西，所以想要往官方host的GNU ELPA贡献扩展是件很麻烦的事情，你得签署GPL，得保持一些格式，这使得elpa上的东西很少，但是至少能保证安全。第三方的repo就包含了很多包了，但是谁都能够往上传代码，安全性不能保证。其实最主要的缺点还是不太容易迁移，一旦换了电脑或者重装了操作系统，或者想在几个emacs客户端上保持配置的一致性，手动维护包的安装和配置情况绝对能让人弃疗。

el-get的出现解决了这些问题，其中的基础思想是，通过写被称作recipe的描述性文件来管理包，至于其余的事情，让el-get帮你完成。这件事意义重大，因为这既能使用已有的所有elpa项目host的包，也能使用github上个人维护的包，甚至其他一些奇怪的网站，只要你能用网络工具(git,svn,hg等)获取到，就能写进recipe让el-get帮你装好。这样，你只需要在不同emacs上保持一份配置就好了，其余的交给el-get就行，真是方便。

el-get的recipe也能算是一份文档，读起来非常的清楚。我这里举例子说明我是怎么安装一个最简单的包`better-defaults`。

在melpa之类的repo上很容易找到`better-defaults`，其实都来自Github上作者的repo。这个包核心只有一个小文件，修改了一些大家都觉得应该改进的emacs默认配置，比如打开ido-mode之类的。在el-get之前，我是用`package.el`的办法，具体是在`~/.emacs.d/init.el`中写入

{% highlight lisp %}
(require 'package)
(add-to-list 'package-archives
             '("melpa" . "http://melpa.org/packages/"))
{% endhighlight %}

然后使用`M-x package-install`的方式来安装。

现在我只需要安装el-get，官方有的我只需要写一行配置，没有的我只需要把recipe写在`~/.emacs.d/el-get-user/recipes/`下面，然后同样在`init.el`里面写一行配置就行了。当然，如果对于有额外设置的包，需要把额外的配置写上，不过这并不影响文件的可读性。

由于melpa里面有`better-defaults`这个包，所以我可以简单这么写(刚刚写到这里的时候，按错快捷键把iTerm的tab关掉了，然后重新打开发现写的东西基本都没了= =!，差点直接报警。还好有#filename#文件，用`M-x recover-file`命令恢复了，感谢emacs的自动保存功能！)

{% highlight lisp %}
;; install el-get
(add-to-list 'load-path "~/.emacs.d/el-get/el-get")

(unless (require 'el-get nil 'noerror)
  (with-current-buffer
      (url-retrieve-synchronously
       "https://raw.githubusercontent.com/dimitri/el-get/master/el-get-install.el")
    (goto-char (point-max))
    (eval-print-last-sexp)))
    
;; add self crafted recipe into path, so that el-get can see them when using el-get-install
(add-to-list 'el-get-recipe-path "~/.emacs.d/el-get-user/recipes")

;; el-get shortcut for installing a package in elpa
(el-get-bundle elpa:better-defaults)
{% endhighlight %}

可以看到我并没有写recipe，先是安装了el-get，然后就直接说"用elpa安装better-defaults"，一行搞定。
其实最后一行是个syntax sugar，应该写作`(el-get-bundle better-defaults :type elpa)`。

我在安装el-get后面有一行配置，是告诉el-get我自己的recipe在哪里找，所以我还可以在`~/.emacs.d/el-get-user/recipes/`目录下新建一个文件`better-defaults.rcp`，在里面写

{% highlight lisp %}
(:name better-defaults
       :type git
       :description "A small number of better defaults for Emacs"
       :url "https://github.com/technomancy/better-defaults")
{% endhighlight %}

然后在`init.el`里面就可以把`elpa:`去掉了。

我觉得写成分开的文件会让init.el可读性强一点，不过这样就不能做到一个文件同步所有配置了，所以也是有办法把recipe直接写到启动文件里面的。

{% highlight lisp %}
(setq el-get-sources
      '(
        (:name better-defaults
               :type git
               :description "..."
               :url "..."
               )))
(el-get 'sync el-get-sources)
{% endhighlight %}

`'sync`是为了让安装的所有包不要并发地下载，如果没有依赖关系的话，不用`'sync`也是可以的。

大概就是这么多了，希望能够跟emacs玩得愉快~(说着就打算去装ipython模式看看了)

[el-get]: https://github.com/dimitri/el-get
