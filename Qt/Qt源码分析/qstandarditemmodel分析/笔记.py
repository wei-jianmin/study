看QStandardItemModelPrivate.hpp，可以发现其主要数据成员有
    QVector<QStandardItem*> columnHeaderItems;
    QVector<QStandardItem*> rowHeaderItems;
    QScopedPointer<QStandardItem> root;

看QStandardItemPrivate.hpp，可以发现其主要数据成员有   
    QStandardItemModel *model;          //记录存在于那个模型中    
    QStandardItem *parent;              //记录父QStandardItem*
    QVector<QWidgetItemData> values;    //存放各种角色信息，如图标、文本、字体、前景色等等
    QVector<QStandardItem*> children;   //按行依次存放各个子元素（意味着一个QStandardItem中可以存放一个子QStandardItem表）
    int rows;                           //记录子表有多少行
    int columns;                        //记录子表有多少列
    QStandardItem *q_ptr;               //指向QStandardItem
    int lastIndexOf;                    //记录上次查找的子QStandardItem*的位置

也就是说 QStandardItem 里面可以通过QVector，维护一个子 QStandardItem* 表格

所以 QStandardItemModel 中的数据成员 root ，内部维护一个子 QStandardItem* 表格
而各个QStandardItem*子元素的parent指向root，子元素的model指向QStandardItemModel