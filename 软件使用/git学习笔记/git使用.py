Git的工作方式
    git存储/管理文件的方式：
        大部分其它工具（包括svn）以“文件变更列表”的方式存储信息，
        这类系统将他们存储的信息看做一组基本文件and每个文件随时间逐步累积的差异。
        因此，通常称他们为“基于差异”的版本控制。
        而在git中，更像是把数据看做是对“小型文件系统”的一系列快照，
        每当你提交一次更新，git基本上就会对当时的全部文件创建一个快照
        （所以这造成了git管理大文件，如pdb、pdf、exe时，很容易使仓库变得很大），
        并保存这个快照的索引，如果文件没有修改，git不会重新存储该文件，
        而只是保存一个链接指向之前存储的文件。
        git中所有数据在存储前都计算校验和，然后通过校验和（哈希值）来引用。
    文件快照
        https://blog.csdn.net/m0_37075681/article/details/83218592
        快照应该理解为整个系统或者应用在某个时刻的状态记录
        例如，假定在A时刻，你的git工作空间分别有file1和file2，
        到B时刻的时候，你对file1进行了修改。
        随后，在你准备进行一次commit之前，git就已经准备好快照了，
        这个快照记录了当前工作空间中指向未修改文件file2的指针
        和已经修改的file2数据（即当前时刻工作空间的文件数据状态）
        因此，commit的时候，就等同于保存了一次快照。
        快照怎么进行
            git会读取当前工作空间的所有数据，进行数据预存，再重新调整。
            它会和上一次的快照版本的内容进行比较，
            对于没有改变的文件数据，
            git会把当前预存中冗余文件的数据去除掉，
            改为保留指向上一个版本中该文件数据的指针，
            对于有差异的文件数据就会保留下来，
            最终再把数据完整保存下来，这才算是执行了一次快照。
        git和CVS,、Subversion等的区别
            前者是记录和组装一系列快照流的微型系统，
            关心文件数据的整体是否发生变化。
            每次commit的时候保存一次快照，
            而每个快照都包含了完整的数据；
            后者则关心文件内容的具体差异，
            第一次保存了完整的数据，往后每次保存的都不是完整的数据，
            只会记录基于之前的版本和现在两者的变化信息，
            对于此外没有变化的都不会去记录。
            例如一个文本文件发生了变化，
            git会把当前已经变化的文件重新保存一份，
            而svn则是基于之前的文件，记录当前文件的变化信息
    文件快照
        https://blog.csdn.net/weixin_40085040/article/details/109061495
        文件快照是基于文件是在磁盘上分块存储的事实来工作的
        文件描述结构一个文件所占用的1个或多个磁盘块的地址
        而对文件的修改，通常只是对文件的部分磁盘块的修改，而非全部磁盘块的修改
        所以创建快照时，那些没有修改的磁盘块是可以复用的：
        快照只保存新的文件描述结构和变化了的磁盘块
        所以它不同于简单的文件复制
        基于这种思想，所以一次git提交，
        就是记录一系列的文件描述符和变化了/新增的磁盘块
        所以本次提交的数据是基于上次提交的数据的，
        而上次提交的数据又基于上上次提交的数据，
        所以历史提交的各版本会形成个依赖链
        如果这个链的某个环丢失，就会可能导致数据恢复到历史版本时出现问题
        例如即使丢失的第-n次提交，但可能导致恢复到第-1版本时出错
        但这种情况通常不会发生，因为git暴露这样的可以删除第-n次提交的手段
        而.svn仓库通常也不会被用户修改
    文件对于git来说有两种状态：
        已跟踪文件   被纳入了版本控制的文件，就是 Git 已经知道的文件
        未跟踪文件
    git文件的三种状态
        已修改（modified） ： 如果自上次检出后，作了修改但还没有放到暂存区域，就是 已修改 状态
        已暂存（staged）   ： 如果文件已修改并放入暂存区，就属于 已暂存 状态
        已提交（committed）： 如果 Git 目录中保存着特定版本的文件，就属于 已提交 状态
    git设备
        工作区：对项目的某个版本独立提取出来的内容（就是你在电脑里能看到的目录）
        暂存区：是一个文件，保存了将要提交的文件列表信息，
                一般存放在 .git 目录下的 index 文件（.git/index）中
                按照git的术语，叫做“索引”，但一般还是叫做暂存区
        git仓库目录：保存项目元数据和对象数据库的地方（.git目录下）
    HEAD（.git/HEAD文件）
        HEAD 是当前分支引用的指针，它总是指向某次commit，默认是上一次的commit
        通常，可以把 HEAD 看做你的上一次提交的快照。
        当然HEAD的指向是可以改变的，比如你提交了commit，切换了仓库，分支，或者回滚了版本，切换了tag等
        HEAD的内容（通常情况下）：ref: refs/heads/master
        refs/heads/master文件的内容：存放了最近一次提交的commit id

git配置：
    git自带一个git config工具来帮助设置 "控制git外观和行为的" 配置变量,
    这些变量存储在三个不同的位置
        /etc/gitconfig : 
            通用配置，如果在执行git config时，
            带上--system选项，则读写的就是该文件中的变量
        ~/.gitconfig或~/.config/git/config文件 ： 
            针对当前用户，如果使用--global选项，就是读写此文件，
        git目录下的config文件，即.git/config： 
            针对本仓库。可以传递——-local选项让git读写该文件（默认值）
    编辑配置文件：
        git config -e --system
        git config -e --global
        git config -e --local
    优先级: 
        local > global > system
    查看配置项
        如果想要检查你的配置，可以使用 git config --list 命令来列出所有 Git 当时能找到的配置
        你可能会看到重复的变量名，因为 Git 会从不同的文件中读取同一个配置）。 
        这种情况下，Git 会使用它找到的每一个变量的最后一个配置。
        你可以使用git config --show-origin 配置变量名，他会告诉你哪一个配置文件最后设置了该值
 
获取帮助
    git help 命令     对该命令的详细描述
    git 命令 -h       对该命令的简要描述
 
设置用户名&邮箱
    $ git config --global user.name "Your Name"
    $ git config --global user.email "email@example.com"
    --global参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，
    当然也可以对某个仓库指定不同的用户名和Email地址
    如果不进行上面的设置，则git只能add，不能commit

创建git仓库
    从本地目录创建 ： git init
    从服务器克隆：    git clone url
    克隆举例：
        git clone https://github.com/libgit2/libgit2
        这会在当前目录下创建一个名为 “libgit2” 的目录，
        在这个目录下初始化一个 .git 文件夹， 
        从远程仓库拉取下所有数据放入 .git 文件夹，
        然后从中读取最新版本的文件的拷贝。
        git clone https://github.com/libgit2/libgit2 mylibgit
        在克隆远程仓库的时候，自定义本地仓库的名字
        git clone git://github.com/libgit2/libgit2
        使用git协议克隆
        git clone ser@server:path/to/repo.git
        使用ssh协议克隆
    克隆的将是git仓库服务器上的几乎所有数据（如每个commit，可能丢失的是某些服务器端的钩子），
    而不仅仅复制当前版本的文件。

把文件添加到版本库：
    git add 文件名
    git commit

把更新提交到版本库
    git add 文件名
    git commit -m "注释"
    或
    git commit 文件名 -m "注释"  //虽然可行，但是不正规用法
    
add命令
    该命令‘使用在工作树中找到的当前内容’更新索引（index），以准备下一次提交的内容。
    它通常会整体添加现有路径的当前内容，但是通过某些选项，它也可以用于添加仅对工作树文件进行部分更改的内容
    该index持有一个对当前工作树的内容的快照，而且下次的commit，就是提交的该快照。
    因此在commit之前，如果对工作树做了任何改动,你必须用add添加任何新的或更改的文件到index。
    该函数可以在commit之前执行多次，但最终只会添加最后一次执行add命令————实测多次add的效果是叠加汇总。
    根据实测，直接调用"git add"，不会把所有更新的文件自动添加到索引中，相似的命令应该是 "git add ."
    add命令后面跟文件名或路径作为参数，如果是路径，则命令会递归的跟踪目录下的所有文件
    add命令有三个功能：
        开始跟踪文件
        把已跟踪文件放到缓存区
        合并时，把有冲突的文件标记为已解决状态
    经测试，添加一个新文件后，执行"add 新文件名"命令，
    不光.git/index文件会变化，而且.git/object目录下的内容会变化
    可见（猜测）add命令会为下一步的commit做好准备工作：
    检查文件的变化，缓存下变化文件的快照（描述信息和变化的磁盘块）
    
status命令
    用git status 可以查看当前分支的名称，如 master分支（git的默认分支）
    git status -s 或  git status --short     紧凑形式输出
    紧凑输出格式：
        标记符  文件名
            ??  未跟踪
            A   已add到暂存区
            M   已修改
            MM  对修改的暂存后，又做了修改
            
commit命令
    创建一个新提交（包含当前index的内容和修改描述）
    提交的方式：
        1.  使用git add，再commit
        2.  使用git rm，在commit
        3.  后跟文件列表作为commit的参数，
            此时commit将忽略index中的内容（前提是该文件需要被git知道）
        4.  使用git commit -a，可直接把git已知文件的修改进行提交（无需add,跳过使用暂存区）
            该命令会自动缓存已修改或已删除的文件，但没有告知给git的新文件不会受影响
        5.  commit时，使用--interactive或--patch开关，以交互模式提交
    选项：
        -a或--all    自动缓存文件（包括修改的或删除的，但不包括未添加的）
        -F <file> 或 --file=<file>  从给定文件中获取提交信息，
                                    特殊的，可使用 - 标识从 standard input 获取
        -m <msg> 或 --message=<msg> 使用给定的<msg>作为提交信息
        --amend   将本次的提交归并到上次的提交，这两次提交算作一次提交
                  如果你提交后，发现有几个文件忘了提交，可以用这个命令
        --  选项结束标记，告诉git不要再把后面的内容当做选项参数了
    经测试，在add之后执行commit，
        .git/index会变化、
        .git/object目录下会变化
        .git/logs目录下会变化
        .git/commit_editmsg会变化

rm命令
    git rm <file> : 将文件从工作区删除，且git不再跟踪
    git rm -f <file> : 将文件从工作区和缓存区删除，且git不再跟踪
                       适用于文件被修改，且提交到缓存区了（git add）的情形
    git rm --cached <file> : 使git将不再跟踪该文件，但不会从工作区删除
    
mv命令
    将库中的一个文件改名
    git mv a.txt b.txt
    相当于执行了下面三条操作：
    mv a.txt b.txt
    git rm a.txt
    git add a.txt
    可以看到，mv之后，需要跟commit操作
 
diff命令
    git diff [file] : 显示缓存区和工作区的差异，后面的file参数为可选（下同）
    git diff --cached/--staged [file] : 显示缓存区和仓储(上次提交的)的差异
    git diff [版本1]...[版本2] : 显示仓库中两次提交的差异
    使用可视化比较工具
        可以使用git difftool --tool-help ，看当前都支持哪些可视化比较工具
        使用TortoiseGit，可提供图形化比较工具
        https://blog.csdn.net/gdutxiaoxu/article/details/80455810
        git config --global diff.tool bc3 
        git config --global difftool.bc3.path "beyondcompare.exe的路径"
        之后，使用git difftool命令，即可打开可视化工具BCompare
        同样的也可使用bcomp作为mergetool，配置方式为：
        git config --global merge.tool bc3 
        git config --global mergetool.bc3.path "bcomp.exe的路径"
    
reset命令
    git reset [--soft/--mixed/-hard ] [版本]
    选项：
        --soft: 不改变工作区和缓存区，只移动HEAD到指定的commit
        --mixed: 只改变缓存区，不改变工作区[默认]，通常用于撤销 git add
        --hard: 改变工作区和缓存区到指定的commit
    版本：
        git reset       //如果不指定，默认为 HEAD
        git reset HEAD  //恢复到HEAD指向的版本，也就是最新一次提交的版本
        git reset HEAD^
        git reset HEAD^^
        git reset HEAD~100
        git reset 历史版本的哈希值
    使用--soft选项回退到第-n次提交后
        .git下的变化
            多了个ORIG_HEAD文件，记录了在reset前，最后一次的commit id
            refs/heads/master文件内容发生变化，变为恢复到的那次版本的commit id
            logs下面的内容发生了变化
        用status查看，发现自-n次提交之后的修改与提交都变得无效，
        例如自第-n次之后添加并提交的文件，将被git认定为未追踪的新文件
        结语：
            可以近似的认为 --soft 就是简单的把HEAD指向指向-n历史版本
            注：每次的提交，都是以 HEAD（及之前的版本--依赖链）为参考
            但这样有个问题，就是这种方法不会删除仓库中第-n次提交以来保存的快照
            而这些快照也没用了，所以将造成磁盘空间的浪费
    使用--mixed恢复
        一般是add或rm之后，导致了暂存区的变化，但又想撤销之前的add或rm操作
        此时可用该方法恢复暂存区

checkout命令
    git [选项] checkout [分支名]  
        -b 分支名  ： 创建并检出一个新分支
    将某次commit的状态检出到工作区
    它的过程是先将HEAD指向某个分支的最近一次commit，
    然后从commit恢复index（缓存），最后从index恢复工作区。
    放弃工作区中全部的修改:  git checkout .
    放弃工作区中某个文件的修改：  git checkout -- filename
    强制放弃 index 和 工作区 的改动： git checkout -f
        
log命令
    -n    n为数字，表限制日志输出的条目数量
    --pretty=oneline    将每个提交放在一行显示,在浏览大量的提交时非常有用
    --format="format"   可以定制记录的显示格式
        %H  提交的完整哈希值
        %h  提交的简写哈希值
        %T  树的完整哈希值
        %t  树的简写哈希值
        %P  父提交的完整哈希值
        %p  父提交的简写哈希值
        %an 作者名字
        %ae 作者的电子邮件地址
        %ad 作者修订日期（可以用 --date=选项 来定制格式）
        %ar 作者修订日期，按多久以前的方式显示
        %cn 提交者的名字
        %ce 提交者的电子邮件地址
        %cd 提交日期
        %cr 提交日期（距今多长时间）
        %s  提交说明
        例： git log --format="%h %cd %s"
    --since/--before/--until  按照时间限制展示的日志
            例：--since=2.weeks 展示最近两的提交
            --since="2008-10-01"  --before="2008-11-01"
            该命令可用的格式十分丰富————
            可以是类似 "2008-01-15" 的具体的某一天，
            也可以是类似 "2 years 1 day 3 minutes ago" 的相对日期
    --grep     选项搜索"提交说明"中的关键字
               可以指定多个--grep 搜索条件，多个条件相或
               如果配合--all-match 选项，则多个条件相与
    -S   查找，它接受一个字符串参数，并且只会显示那些添加或删除了该字符串的提交
         例如想看某个函数是啥时候添加的，可以 git log -S function_name
        
忽略文件
    有一些文件，虽然是未跟踪的，但我们不希望它总出现在“未跟踪列表”中，
    我们可以创建一个.gitignore的文件，也可以利用在现有.gitignore模板修改得到，
    https://github.com/github/gitignore下面有各种语言的忽略文件模板，可以直接拿来使用
    .gitignore文件一般只在根目录下有一个，但其实在子目录下也可有这样的文件，它只作用于当前文件夹
    .gitignore的文件格式规范：
        #开头的行表注释行
        可以使用标准的 glob 模式匹配，它会递归地应用在整个工作区中
            所谓的 glob 模式是指 shell 所使用的简化了的正则表达式
                问号（?）只匹配一个任意字符
                星号（*）匹配零个或多个任意字符
                [abc] 匹配任何一个列在方括号中的字符：匹配一个a或一个b或一个c
                如果在方括号中使用短划线分隔两个字符，表示匹配一个范围
                    比如 [0-9] 表示匹配所有 0 到 9 的数字
                使用两个星号（**）表示匹配任意级的中间目录
                    比如 a/**/z 可以匹配 a/z 、 a/b/z 或 a/b/c/z 等。
                匹配模式可以以（/）开头防止递归
                匹配模式可以以（/）结尾指定目录
                要忽略指定模式以外的文件或目录，可以在模式前加上叹号（!）取反
                    比如 !a 表a文件外的其它所有文件都将被忽略
    .gitignore文件举例：
        *.[oa]      //忽略所有以.o或.a结尾的文件
        *~          //忽略所有以~结尾的文件
        *.a         //忽略所有的 .a 文件
        !lib.a      //在前一条的基础上，不忽略lib.a
        build/      //忽略任何目录下名为 build 的文件夹
        doc/*.txt   //忽略doc直接目录下txt文件，但如果doc子目录下有txt文件，则不会忽略
        doc/**/*.pdf    //忽略doc及其子目录下的pdf文件
    
取消操作
    取消某个/某些文件的暂存
        git reset HEAD <file>...
        注：在2.23.0版本中，变为："git restore --staged <file>..."
    撤销对文件的修改
        git checkout -- <file>...
        注：在2.23.0版本中，变为："git restore <file>..."
        注：缓存中有该文件时，从缓存中复制文件（缓存中文件不变），缓存中没有时，从仓库中复制

远程仓库的使用        
    国内远程仓库地址：https://gitee.com/
    用户名：常用邮箱，密码：常用密码
    1. 用ssh测试能否连接到 gitee : ssh git@gitee.com
       如果不能，先用 ssh-keygen -t rsa 命令生成密钥对（一路回车）
       完成后，在屏幕上会输出类似如下的信息：
       。。。
       Your identification has been saved in /c/Users/Administrator/.ssh/id_rsa
       Your public key has been saved in /c/Users/Administrator/.ssh/id_rsa.pub
       。。。
       查看 /c/Users/Administrator/.ssh/id_rsa.pub 文件中存的公钥信息
       然后 gitee.com/设置/账号设置/SSH公钥， 在这个页面中添加上刚才的公钥
       然后再次用 ssh git@gitee.com 测试看是否能连通了
   2.  git config --global user.name "weijianmin"
       git config --global user.email "wei-jianmin@163.com"
   3.  关联远程版本库
       git remote add [shortname] [url]
       git remote add origin https://gitee.com/weijianmin/study.git
       这里的shortname ，是为远程仓库设置一个简单的名字，以便将来引用
       使用git remote -v ，可看到别名所对应的实际链接的地址
       git remote add 只是修改了local配置文件，为git远程仓库的url地址起了个短名而已
       可使用 git remote rename <oldshortname> <newshortname> 重命名该短名
    4. 推送到远程仓库
       git push <remote> <branch>  推送到远程仓库
           remote 可为短名，也可为git远程仓库的url地址
    5. 获取远程仓库的更新
       git fetch + git merge
           git fetch <remote> <branch>
               会在.git下多出个FETCH_HEAD的文件（如果有，则改文件会变化）
               .git/refs/remotes/短名/master文件会新增或变化
               .git/objects目录下会变化（新增）
               .git/logs目录下会变化
           git merge FETCH_HEAD
               会将仓库中的FETCH_HEAD分支（远程仓库更新下来的）
               和HEAD分支（本地仓库原有的）进行merge操作
               merge的结果会更新在本地目录中
       git pull
           直接将远程仓库中的最新版本与当前仓库的最新版本进行merge
           不推荐使用这种方法
    6. 从远程仓库克隆
       git clone url  [本地文件夹名]  : 从远程仓库克隆（克隆前无需git init）   
       克隆举例：
            git clone https://gitee.com/weijianmin/study [学习笔记]
            这会在当前目录下创建一个名为 “libgit2” 的目录，
            在这个目录下初始化一个 .git 文件夹， 
            从远程仓库拉取下所有数据放入 .git 文件夹，
            然后从中读取最新版本的文件的拷贝。
            git clone https://github.com/libgit2/libgit2 mylibgit
            在克隆远程仓库的时候，自定义本地仓库的名字
            git clone git://github.com/libgit2/libgit2
            使用git协议克隆
            git clone ser@server:path/to/repo.git 
            使用ssh协议克隆  例： git git@gitee.com:xingyuxinhen/gittest.git
        克隆的将是git仓库服务器上的几乎所有数据（如每个commit，可能丢失的是某些服务器端的钩子），
        而不仅仅复制当前版本的文件。 
        中间过程中会要求输入用户名和密码（在push的时候也要求输入用户名密码）
        克隆时，会自动将这个服务器地址"存到默认的名为origin的变量中"
        克隆时，会自动设置(创建)本地 master 分支跟踪克隆的远程仓库的 master 分支    
    gitee的限制
        总仓库容量不超过3G
        单个仓库容量不超过500M/1G
        单个文件大小不超过50M/100M
        
大文件
    1. 安装lfs：下载地址 https://github.com/git-lfs/git-lfs/releases
    2. 进到git库目录，开启lfs  ： git lfs install
    3. 设置lfs要管理的文件 ： git lfs track 要跟踪的目录或文件
    4. 像普通文件一样add、commit、push即可
    注：gitee虽然支持lfs，但只针对付费企业用户开放
    
    git lfs 介绍
        大文件存储功能，Git Large File Storage (LFS)
        可用于处理项目中的大文件，在git中只会记录对此大文件的引用，
        不会将其加入.git文件夹中，使得项目体积不会猛增
        在git lfs install之后，使用以下格式的命令git lfs track "*.iso"来追踪大文件，
        此命令会将相关信息存入.gitattributes文件中。
        之后所有放入的iso都会正常放入LFS中。
        git add时不用手工做特殊处理。上传时会显式提示使用了LFS功能。
        可使用git lfs help 获取命令帮助信息
        
可视管理工具        
    tortoise git ： 和tortoise svn类似，通过右键菜单管理文件的提交