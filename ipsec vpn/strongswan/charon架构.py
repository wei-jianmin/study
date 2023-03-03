  https://docs.strongswan.org/docs/5.9/daemons/charon.html
简述
    charon守护程序用于为 strongSwan 项目实现 IKEv2 协议
    大多数代码都位于libcharon中，从而使得 IKE 守护程序可以被
    charon-systemd, charon-svc, charon-cmd 或 Android app 使用
    
架构：
      +---------------------------------+       +----------------------------+
      |          Credentials            |       |          Backends          |
      +---------------------------------+       +----------------------------+
       +------------+    +-----------+          +------+            +----------+
       |  receiver  |    |           |          |      |  +------+  | CHILD_SA |
       +----+-------+    | Scheduler |          | IKE- |  | IKE- |--+----------+
            |            |           |          | SA   |--| SA   |  | CHILD_SA |
       +-------+--+      +-----------+          |      |  +------+  +----------+
    <->|  socket  |            |                | Man- |
       +-------+--+      +-----------+          | ager |  +------+  +----------+
            |            |           |          |      |  | IKE- |--| CHILD_SA |
       +----+-------+    | Processor |----------|      |--| SA   |  +----------+
       |   sender   |    |           |          |      |  +------+
       +------------+    +-----------+          +------+
      +---------------------------------+       +----------------------------+
      |               Bus               |       |      Kernel Interface      |
      +---------------------------------+       +----------------------------+
             |                    |                           |
      +-------------+     +-------------+                     V
      | File-Logger |     |  Sys-Logger |                  //////
      +-------------+     +-------------+      
    
    对上图中各组件的介绍：
        Processor
            线程实现为线程池，守护进程中的所有线程都源自 processor，
            将一个任务分配给线程，一个 job 会被放到 processor 中的队列中（异步执行）
        Scheduler
            执行定时事件（timed events），
            jobs 可能被排队到 scheduler 中并且在特定时间执行（如 rekeying）， 
            scheduler自己不执行这些 jobs，而是交给 processor 处理
        IKE_SA Manager
            IKE_SA manager 管理所有的 IKE_SAs，它还进一步处理了同步：
            每个 IKE_SA 必须被严格的检出(check out)，并且用完后再检入(check in)。
            管理器确保只有一个线程可以检出一个 IKE_SA。
            这允许我们将（复杂的）IKE_SAs 例程编写为非线程保存的
        IKE_SA
            保存 IKE_SA 的状态和逻辑，并处理消息
        CHILD_SA
            保存 IPSEC_SA 的状态并管理他们，一个 IKE_SA 可能有多个 CHILD_SA，
            在这里完成与内核的通信（借助 kerel interface）
        Kernel Interface
            添加创建(install) IPSEC_SA、policies、路由和虚拟地址。
            它还进一步提供了枚举接口的方法，并且当底层发生了状态改变时，可以通知(notify）daemon
        Bus
            从不同的线程中接收信号，然后发布给注册的监听者。
            调试信号以及重要的状态转换或错误信息在bus上被发送
        Controller
            提供了一个简单的api，以方便plugins控制daemon，如初始化IKE_SA、关闭IKE_SA等等
        Backends
            backends是提供了配置功能的"可插拔"模块，
            他们必须提供（特定的）API，以供 daemon core 用来获取（该插件的）配置信息
        Credentials
            使用注册的插件，提供信任链验证和认证服务
            
插件（注：应该就是上面的backends）
    守护程序在开始时加载插件，这些插件实现了 plugin_t 接口
    每个插件都会向守护程序注册自己，以将自己的功能 hook in 到守护程序上