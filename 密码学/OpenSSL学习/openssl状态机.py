Openssl为什么需要状态机
    Openssl是通过“握手“建立加密信道
    Openssl握手通过客户端和服务端互相交换信息计算出secret
    计算出密钥的方式有很多种。这中间可能需要几个RTT来回
    状态机需要针对约定好的加密算法按照一定的步骤执行
状态机是什么
    状态机保存Ssl握手需要一些消息处理函数，和算法函数，来解析消息，执行加解密操作。
    要么是发送处理好的消息流，要么是接收对方的消息流
    所以一个状态机是在读写函数不断切换。
    消息状态机如果不按正常的流程走，就形成了状态机的异常或者遭受到了安全攻击。
    
    消息流状态机
        消息流状态机由MSG_FLOW_UNINITED到读写多次来回切换到MSG_FLOW_FINISHED状态
        MSG_FLOW_UNINITED（1）   MSG_FLOW_FINISHED（4）
               │                          │
               ├──────────────────────────┘
               ↓   
            MSG_FLOW_WRITING（写状态机）（2） ←→ MSG_FLOW_READING（读状态机）（3）
               │                    ┌─┬─┐
               ↓                    │↓│←│    
            MSG_FLOW_FINISHED（4）  ├─┼─┤
               │                    │→│↑│
               ↓                    └─┴─┘    
            [SUCCESS]（5）
            
    写状态机
        写的状态机是由消息流状态机调用，写状态机调用结束后有两种返回状态：
        SUB_STATE_FINISHED或者SUB_STATE_END_HANDSHAKE
        SUB_STATE_FINISHED表明此次写状态机调用结束，
        写状态机完成必要的状态迁移或者发送操作，
        控制权转交给消息流状态机，由消息流状态机决定下个操作。
        SUB_STATE_END_HANDSHAKE则向消息流状态机表示握手已经完满成功。
        
        写状态机的控制条件：
        WRITE_STATE_TRANSITION决定ssl握手的下一步状态。
        WRITE_STATE_PRE_WORK和WRITE_STATE_POST_WORK
        则会根据ssl握手的当前状态，进行相对应的操作。
        也就是一个switch-case操作。
        也可能对BIO进行必要的操作（比如清空buffer）。
        这里的BIO是什么？BIO和EVP是openssl两个重要系列的函数。
        BIO或者EVP只不过是一些底层的支撑接口，没有任何的现实意义，
        正是SSL使用了BIO和EVP 的机制提供了一个已经成型的安全套接字的实现策略。
        其实想象一下，安全套接字有两层含义，
        一层就是安全，这个由EVP接口实现了，
        另外一层含义就是套接字，也就是说它必须是一个套接字，
        必须在操作的网络协议栈上进行IO，这一层含义是在BIO接口体现的，
        这个意义上，SSL正是通过组合BIO和EVP来实现安全套接字的。
        
        ┌─> WRITE_STATE_TRANSITION ─────> [SUB_STATE_FINISHED]
        │            │
        │            ↓
        │     WRITE_STATE_PRE_WORK ─────> [SUB_STATE_END_HANDSHAKE]
        │            │
        │            ↓
        │     WRITE_STATE_SEND
        │            │
        │            ↓
        │     WRITE_STATE_POST_WORK
        │            │
        └────────────┘
        WRITE_STATE_PRE_WORK ： 完成数据发送前的握手功能
        WRITE_STATE_SEND ： 完成数据的发送功能
        WRITE_STATE_POST_WORK ： 删除数据发送后的工作
        
    2.3、读状态机
        READ_STATE_HEADER ←──┐←─────────────┐
          │                  │              │
          ↓                  │              │
        READ_STATE_BODY──────┴───>READ_STATE_POST_PROCESS
          │                                 │
          ├─────────────────────────────────┘
          ↓
        [SUB_STATE_FINISHED]
        
        READ_STATE_HEADER：
            根据读到的消息头（type）去决定ssl握手的状态。并且决定之后怎么处理该消息。
        READ_STATE_BODY：
            读取消息的剩余部分，接着处理
        READ_STATE_POST_PROCESS：
            由于阻塞block的消息，有可能需要在当前SSL握手状态继续重试读取消息。
            
Openssl握手状态
    这些消息流状态机、写状态机、读状态机共同完成了TLS握手过程
    file://imgs/openssl状态.png
    