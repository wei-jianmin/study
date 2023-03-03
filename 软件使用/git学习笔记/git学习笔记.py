log命令
    -p/--patch   显示每次提交所引入的差异 （按补丁的格式输出）
    -n    n为数字，表限制日志输出的条目数量
    --stat   显示每次提交时的简略统计信息
            （列出所有被修改的文件，哪些行是新加的，哪些行被删除了）
    --pretty    这个选项有一些内建的子选项供你使用
        oneline  将每个提交放在一行显示,在浏览大量的提交时非常有用
        short/full/fuller  它们展示信息的格式基本一致，但是详尽程度不一
        format   可以定制记录的显示格式
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
            例： git log --pretty=format:"%h %cn %s"
    --graph   这个选项添加了一些 ASCII 字符串来形象地展示你的分支、合并历史
              一般配合 --pretty oneline 或 --pretty format 使用
    --since/--before/--until  按照时间限制展示的日志
            例：--since=2.weeks 展示最近两的提交
            --since="2008-10-01"  --before="2008-11-01"
            该命令可用的格式十分丰富————
            可以是类似 "2008-01-15" 的具体的某一天，
            也可以是类似 "2 years 1 day 3 minutes ago" 的相对日期
    --author   选项显示指定作者的提交
               可以指定多个--author搜索条件，多个条件相或
               如果配合--all-match 选项，则多个条件相与
    --grep     选项搜索提交说明中的关键字
               可以指定多个--grep 搜索条件，多个条件相或
               如果配合--all-match 选项，则多个条件相与
    -S   它接受一个字符串参数，并且只会显示那些添加或删除了该字符串的提交
         例如想看某个函数是啥时候添加的，可以 git log -S function_name
    各选项汇总
        选项	        说明
        -p              按补丁格式显示每个提交引入的差异。
        --stat          显示每次提交的文件修改统计信息。
        --shortstat     只显示 --stat 中最后的行数修改添加移除统计。
        --name-only     仅在提交信息后显示已修改的文件清单。
        --name-status   显示新增、修改、删除的文件清单。
        --abbrev-commit 仅显示 SHA-1 校验和所有 40 个字符中的前几个字符。
        --relative-date 使用较短的相对时间而不是完整格式显示日期（比如“2 weeks ago”）。
        --graph         在日志旁以 ASCII 图形显示分支与合并历史。
        --pretty        使用其他格式显示历史提交信息。
                        可用的选项包括 oneline、short、full、fuller 和 format（用来定义自己的格式）。
        --oneline       --pretty=oneline --abbrev-commit 合用的简写。
        -<n>            仅显示最近的 n 条提交。
        --since, --after    仅显示指定时间之后的提交。
        --until, --before   仅显示指定时间之前的提交。
        --author        仅显示作者匹配指定字符串的提交。
        --committer     仅显示提交者匹配指定字符串的提交。
        --grep          仅显示提交说明中包含指定字符串的提交。
        -S              仅显示添加或删除内容匹配指定字符串的提交。