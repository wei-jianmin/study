QAbstractItemModel
  纯虚函数
    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) = 0；
    QModelIndex parent(const QModelIndex &child) = 0;
    int rowCount(const QModelIndex &parent = QModelIndex()) = 0;
    int columnCount(const QModelIndex &parent = QModelIndex()) = 0;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const = 0;
  虚函数
   无实现的函数
    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole);
    bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex());
    bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex());
    bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex());
    bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex());
    bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value,int role = Qt::EditRole);
    void fetchMore(const QModelIndex &parent);
    bool canFetchMore(const QModelIndex &parent)
    void sort(int column, Qt::SortOrder order = Qt::AscendingOrder)
    QModelIndex buddy(const QModelIndex &index) 
    QSize span(const QModelIndex &index)
    bool submit();  //这是个槽函数
    void revert();  //这是个槽函数
   有实现的函数
    '根据传入的行、列，与函数rowCount、columnCount比较
    bool hasIndex(int row, int column, const QModelIndex &parent)
    'return index(row, column, parent(idx))
    QModelIndex sibling(int row, int column, const QModelIndex &idx)
    '只要rowCount或columnCount都大于0，即返回真
    bool hasChildren(const QModelIndex &parent = QModelIndex())；    
    'role==Qt::DisplayRole返回section+1，否则返回空QVariant()
    QVariant headerData(int section, Qt::Orientation orientation,int role = Qt::DisplayRole)
    '遍历ItemDataRole，只要data(index,角色)有效，就将(角色，值)放到map中，最后返回map
    QMap<int, QVariant> itemData(const QModelIndex &index)；
    '遍历map中的各个角色值，调用setData，设置给index指向的item，只要有一条设置失败，就返回失败
    bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles);
    '返回固定值application/x-qabstractitemmodeldatalist
    QStringList mimeTypes() const;
    '返回new QMimeData()->setData(mimeTypes().at(0),encodeData(indexes))
    QMimeData *mimeData(const QModelIndexList &indexes) const;
    '如果action是拷贝或移动，decodeData(row,column,data->data(mimeTypes().at(0)))
    bool dropMimeData(const QMimeData *data, Qt::DropAction action,
                      int row, int column, const QModelIndex &parent);
    '返回固定值Qt::CopyAction
    Qt::DropActions supportedDropActions() const;
    '内部调用insertRows
    bool insertRow(int row, const QModelIndex &parent = QModelIndex());
    '内部调用insertColumns
    bool insertColumn(int column, const QModelIndex &parent = QModelIndex());
    '内部调用removeRows
    bool removeRow(int row, const QModelIndex &parent = QModelIndex());
    '内部调用removeColumns
    bool removeColumn(int column, const QModelIndex &parent = QModelIndex());
    'QAbstractItemModelPrivate->indexValid(index)返回无效，则返回0，否则返回Qt::ItemIsSelectable+Qt::ItemIsEnabled
    Qt::ItemFlags flags(const QModelIndex &index)
    '返回QAbstractItemModelPrivate->roleNames
    QHash<int,QByteArray> &roleNames()
    '
    QModelIndexList match(const QModelIndex &start, int role,const QVariant &value, int hits = 1,
                          Qt::MatchFlags flags =Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) 
  信号函数
    void dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight);
    void headerDataChanged(Qt::Orientation orientation, int first, int last);
    void layoutChanged();
    void layoutAboutToBeChanged();
   只有没有定义Q_MOC_RUN和qdoc宏时才有效的信号 (只会被QAbstractItemModel发送)
    void rowsAboutToBeInserted(const QModelIndex &parent, int first, int last);
    void rowsInserted(const QModelIndex &parent, int first, int last);
    void rowsAboutToBeRemoved(const QModelIndex &parent, int first, int last);
    void rowsRemoved(const QModelIndex &parent, int first, int last);
    void columnsAboutToBeInserted(const QModelIndex &parent, int first, int last);
    void columnsInserted(const QModelIndex &parent, int first, int last);
    void columnsAboutToBeRemoved(const QModelIndex &parent, int first, int last);
    void columnsRemoved(const QModelIndex &parent, int first, int last);
    void modelAboutToBeReset();
    void modelReset();
    void rowsAboutToBeMoved( const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow );
    void rowsMoved( const QModelIndex &parent, int start, int end, const QModelIndex &destination, int row );
    void columnsAboutToBeMoved( const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn );
    void columnsMoved( const QModelIndex &parent, int start, int end, const QModelIndex &destination, int column );
  实函数
   保护函数
    '遍历indexes，将行数列数itemData(index)依次写到stream中
    void encodeData(const QModelIndexList &indexes, QDataStream &stream) const;
    '取出stream中的内容(行值列值数据)，放到各自相应的栈中
    '???后面没看明白，猜测是把stream中的数据放到row、column、parent所指示的items中
    bool decodeData(int row, int column, const QModelIndex &parent, QDataStream &stream);
    void beginInsertRows(const QModelIndex &parent, int first, int last);
    void endInsertRows();
    void beginRemoveRows(const QModelIndex &parent, int first, int last);
    void endRemoveRows();
    bool beginMoveRows(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationRow);
    void endMoveRows();
    void beginInsertColumns(const QModelIndex &parent, int first, int last);
    void endInsertColumns();
    void beginRemoveColumns(const QModelIndex &parent, int first, int last);
    void endRemoveColumns();
    bool beginMoveColumns(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationColumn);
    void endMoveColumns();
    void reset();
    void beginResetModel();
    void endResetModel();
    void changePersistentIndex(const QModelIndex &from, const QModelIndex &to);
    void changePersistentIndexList(const QModelIndexList &from, const QModelIndexList &to);
    QModelIndexList persistentIndexList() const;
    void setRoleNames(const QHash<int,QByteArray> &roleNames);

QAbstractItemModel更多意义上像是定义个接口/规范