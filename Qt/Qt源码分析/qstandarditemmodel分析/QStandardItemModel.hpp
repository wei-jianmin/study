class Q_GUI_EXPORT QStandardItemModel : public QAbstractItemModel
{
    Q_OBJECT
    Q_PROPERTY(int sortRole READ sortRole WRITE setSortRole)

public:
    explicit QStandardItemModel(QObject *parent = 0);
    QStandardItemModel(int rows, int columns, QObject *parent = 0);
    ~QStandardItemModel();

    QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const;
    QModelIndex parent(const QModelIndex &child) const;

    int rowCount(const QModelIndex &parent = QModelIndex()) const;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;
    bool hasChildren(const QModelIndex &parent = QModelIndex()) const;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole);

    QVariant headerData(int section, Qt::Orientation orientation,
                        int role = Qt::DisplayRole) const;
    bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value,
                       int role = Qt::EditRole);

    bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex());
    bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex());
    bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex());
    bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex());

    Qt::ItemFlags flags(const QModelIndex &index) const;
    Qt::DropActions supportedDropActions() const;

    QMap<int, QVariant> itemData(const QModelIndex &index) const;
    bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles);

    void clear();

#ifdef Q_NO_USING_KEYWORD
    inline QObject *parent() const { return QObject::parent(); }
#else
    using QObject::parent;
#endif

    void sort(int column, Qt::SortOrder order = Qt::AscendingOrder);

    QStandardItem *itemFromIndex(const QModelIndex &index) const;
    QModelIndex indexFromItem(const QStandardItem *item) const;

    QStandardItem *item(int row, int column = 0) const;
    void setItem(int row, int column, QStandardItem *item);
    inline void setItem(int row, QStandardItem *item);
    QStandardItem *invisibleRootItem() const;

    QStandardItem *horizontalHeaderItem(int column) const;
    void setHorizontalHeaderItem(int column, QStandardItem *item);
    QStandardItem *verticalHeaderItem(int row) const;
    void setVerticalHeaderItem(int row, QStandardItem *item);

    void setHorizontalHeaderLabels(const QStringList &labels);
    void setVerticalHeaderLabels(const QStringList &labels);

    void setRowCount(int rows);
    void setColumnCount(int columns);

    void appendRow(const QList<QStandardItem*> &items);
    void appendColumn(const QList<QStandardItem*> &items);
    inline void appendRow(QStandardItem *item);

    void insertRow(int row, const QList<QStandardItem*> &items);
    void insertColumn(int column, const QList<QStandardItem*> &items);
    inline void insertRow(int row, QStandardItem *item);

    inline bool insertRow(int row, const QModelIndex &parent = QModelIndex());
    inline bool insertColumn(int column, const QModelIndex &parent = QModelIndex());

    QStandardItem *takeItem(int row, int column = 0);
    QList<QStandardItem*> takeRow(int row);
    QList<QStandardItem*> takeColumn(int column);

    QStandardItem *takeHorizontalHeaderItem(int column);
    QStandardItem *takeVerticalHeaderItem(int row);

    const QStandardItem *itemPrototype() const;
    void setItemPrototype(const QStandardItem *item);

    QList<QStandardItem*> findItems(const QString &text,
                                    Qt::MatchFlags flags = Qt::MatchExactly,
                                    int column = 0) const;

    int sortRole() const;
    void setSortRole(int role);

    QStringList mimeTypes() const;
    QMimeData *mimeData(const QModelIndexList &indexes) const;
    bool dropMimeData (const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent);

Q_SIGNALS:
    void itemChanged(QStandardItem *item);

protected:
    QStandardItemModel(QStandardItemModelPrivate &dd, QObject *parent = 0);

private:
    friend class QStandardItemPrivate;
    friend class QStandardItem;
    Q_DISABLE_COPY(QStandardItemModel)
    Q_DECLARE_PRIVATE(QStandardItemModel)

    Q_PRIVATE_SLOT(d_func(), void _q_emitItemChanged(const QModelIndex &topLeft,
                                                     const QModelIndex &bottomRight))
};

inline void QStandardItemModel::setItem(int arow, QStandardItem *aitem)
{ setItem(arow, 0, aitem); }

inline void QStandardItemModel::appendRow(QStandardItem *aitem)
{ appendRow(QList<QStandardItem*>() << aitem); }

inline void QStandardItemModel::insertRow(int arow, QStandardItem *aitem)
{ insertRow(arow, QList<QStandardItem*>() << aitem); }

inline bool QStandardItemModel::insertRow(int arow, const QModelIndex &aparent)
{ return QAbstractItemModel::insertRow(arow, aparent); }
inline bool QStandardItemModel::insertColumn(int acolumn, const QModelIndex &aparent)
{ return QAbstractItemModel::insertColumn(acolumn, aparent); }

#ifndef QT_NO_DATASTREAM
Q_GUI_EXPORT QDataStream &operator>>(QDataStream &in, QStandardItem &item);
Q_GUI_EXPORT QDataStream &operator<<(QDataStream &out, const QStandardItem &item);
#endif

#endif // QT_NO_STANDARDITEMMODEL

QT_END_NAMESPACE

QT_END_HEADER

#endif //QSTANDARDITEMMODEL_H


QStandardItemModel *QStandardItem::model() const
{
    Q_D(const QStandardItem);
    return d->model;
}


QStandardItemModel::QStandardItemModel(QObject *parent)
    : QAbstractItemModel(*new QStandardItemModelPrivate, parent)
{
    Q_D(QStandardItemModel);
    d->init();
    d->root->d_func()->setModel(this);
}


QStandardItemModel::QStandardItemModel(int rows, int columns, QObject *parent)
    : QAbstractItemModel(*new QStandardItemModelPrivate, parent)
{
    Q_D(QStandardItemModel);
    d->init();
    d->root->insertColumns(0, columns);
    d->columnHeaderItems.insert(0, columns, 0);
    d->root->insertRows(0, rows);
    d->rowHeaderItems.insert(0, rows, 0);
    d->root->d_func()->setModel(this);
}


QStandardItemModel::QStandardItemModel(QStandardItemModelPrivate &dd, QObject *parent)
    : QAbstractItemModel(dd, parent)
{
    Q_D(QStandardItemModel);
    d->init();
}


QStandardItemModel::~QStandardItemModel()
{
}


void QStandardItemModel::clear()
{
    Q_D(QStandardItemModel);
    d->root.reset(new QStandardItem);
    d->root->d_func()->setModel(this);
    qDeleteAll(d->columnHeaderItems);
    d->columnHeaderItems.clear();
    qDeleteAll(d->rowHeaderItems);
    d->rowHeaderItems.clear();
    reset();
}


QStandardItem *QStandardItemModel::itemFromIndex(const QModelIndex &index) const
{
    Q_D(const QStandardItemModel);
    if ((index.row() < 0) || (index.column() < 0) || (index.model() != this))
        return 0;
    QStandardItem *parent = static_cast<QStandardItem*>(index.internalPointer());
    if (parent == 0)
        return 0;
    QStandardItem *item = parent->child(index.row(), index.column());
    // lazy part
    if (item == 0) {
        item = d->createItem();
        parent->d_func()->setChild(index.row(), index.column(), item);
    }
    return item;
}


QModelIndex QStandardItemModel::indexFromItem(const QStandardItem *item) const
{
    if (item && item->d_func()->parent) {
        QPair<int, int> pos = item->d_func()->position();
        return createIndex(pos.first, pos.second, item->d_func()->parent);
    }
    return QModelIndex();
}


void QStandardItemModel::setRowCount(int rows)
{
    Q_D(QStandardItemModel);
    d->root->setRowCount(rows);
}


void QStandardItemModel::setColumnCount(int columns)
{
    Q_D(QStandardItemModel);
    d->root->setColumnCount(columns);
}


void QStandardItemModel::setItem(int row, int column, QStandardItem *item)
{
    Q_D(QStandardItemModel);
    d->root->d_func()->setChild(row, column, item, true);
}




QStandardItem *QStandardItemModel::item(int row, int column) const
{
    Q_D(const QStandardItemModel);
    return d->root->child(row, column);
}


QStandardItem *QStandardItemModel::invisibleRootItem() const
{
    Q_D(const QStandardItemModel);
    return d->root.data();
}


void QStandardItemModel::setHorizontalHeaderItem(int column, QStandardItem *item)
{
    Q_D(QStandardItemModel);
    if (column < 0)
        return;
    if (columnCount() <= column)
        setColumnCount(column + 1);

    QStandardItem *oldItem = d->columnHeaderItems.at(column);
    if (item == oldItem)
        return;

    if (item) {
        if (item->model() == 0) {
            item->d_func()->setModel(this);
        } else {
            qWarning("QStandardItem::setHorizontalHeaderItem: Ignoring duplicate insertion of item %p",
                     item);
            return;
        }
    }

    if (oldItem)
        oldItem->d_func()->setModel(0);
    delete oldItem;

    d->columnHeaderItems.replace(column, item);
    emit headerDataChanged(Qt::Horizontal, column, column);
}


QStandardItem *QStandardItemModel::horizontalHeaderItem(int column) const
{
    Q_D(const QStandardItemModel);
    if ((column < 0) || (column >= columnCount()))
        return 0;
    return d->columnHeaderItems.at(column);
}


void QStandardItemModel::setVerticalHeaderItem(int row, QStandardItem *item)
{
    Q_D(QStandardItemModel);
    if (row < 0)
        return;
    if (rowCount() <= row)
        setRowCount(row + 1);

    QStandardItem *oldItem = d->rowHeaderItems.at(row);
    if (item == oldItem)
        return;

    if (item) {
        if (item->model() == 0) {
            item->d_func()->setModel(this);
        } else {
            qWarning("QStandardItem::setVerticalHeaderItem: Ignoring duplicate insertion of item %p",
                     item);
            return;
        }
    }

    if (oldItem)
        oldItem->d_func()->setModel(0);
    delete oldItem;

    d->rowHeaderItems.replace(row, item);
    emit headerDataChanged(Qt::Vertical, row, row);
}


QStandardItem *QStandardItemModel::verticalHeaderItem(int row) const
{
    Q_D(const QStandardItemModel);
    if ((row < 0) || (row >= rowCount()))
        return 0;
    return d->rowHeaderItems.at(row);
}


void QStandardItemModel::setHorizontalHeaderLabels(const QStringList &labels)
{
    Q_D(QStandardItemModel);
    if (columnCount() < labels.count())
        setColumnCount(labels.count());
    for (int i = 0; i < labels.count(); ++i) {
        QStandardItem *item = horizontalHeaderItem(i);
        if (!item) {
            item = d->createItem();
            setHorizontalHeaderItem(i, item);
        }
        item->setText(labels.at(i));
    }
}


void QStandardItemModel::setVerticalHeaderLabels(const QStringList &labels)
{
    Q_D(QStandardItemModel);
    if (rowCount() < labels.count())
        setRowCount(labels.count());
    for (int i = 0; i < labels.count(); ++i) {
        QStandardItem *item = verticalHeaderItem(i);
        if (!item) {
            item = d->createItem();
            setVerticalHeaderItem(i, item);
        }
        item->setText(labels.at(i));
    }
}


void QStandardItemModel::setItemPrototype(const QStandardItem *item)
{
    Q_D(QStandardItemModel);
    if (d->itemPrototype != item) {
        delete d->itemPrototype;
        d->itemPrototype = item;
    }
}


const QStandardItem *QStandardItemModel::itemPrototype() const
{
    Q_D(const QStandardItemModel);
    return d->itemPrototype;
}


QList<QStandardItem*> QStandardItemModel::findItems(const QString &text,
                                                    Qt::MatchFlags flags, int column) const
{
    QModelIndexList indexes = match(index(0, column, QModelIndex()),
                                    Qt::DisplayRole, text, -1, flags);
    QList<QStandardItem*> items;
    for (int i = 0; i < indexes.size(); ++i)
        items.append(itemFromIndex(indexes.at(i)));
    return items;
}


void QStandardItemModel::appendRow(const QList<QStandardItem*> &items)
{
    invisibleRootItem()->appendRow(items);
}


void QStandardItemModel::appendColumn(const QList<QStandardItem*> &items)
{
    invisibleRootItem()->appendColumn(items);
}




void QStandardItemModel::insertRow(int row, const QList<QStandardItem*> &items)
{
    invisibleRootItem()->insertRow(row, items);
}




void QStandardItemModel::insertColumn(int column, const QList<QStandardItem*> &items)
{
    invisibleRootItem()->insertColumn(column, items);
}


QStandardItem *QStandardItemModel::takeItem(int row, int column)
{
    Q_D(QStandardItemModel);
    return d->root->takeChild(row, column);
}


QList<QStandardItem*> QStandardItemModel::takeRow(int row)
{
    Q_D(QStandardItemModel);
    return d->root->takeRow(row);
}


QList<QStandardItem*> QStandardItemModel::takeColumn(int column)
{
    Q_D(QStandardItemModel);
    return d->root->takeColumn(column);
}


QStandardItem *QStandardItemModel::takeHorizontalHeaderItem(int column)
{
    Q_D(QStandardItemModel);
    if ((column < 0) || (column >= columnCount()))
        return 0;
    QStandardItem *headerItem = d->columnHeaderItems.at(column);
    if (headerItem) {
        headerItem->d_func()->setParentAndModel(0, 0);
        d->columnHeaderItems.replace(column, 0);
    }
    return headerItem;
}


QStandardItem *QStandardItemModel::takeVerticalHeaderItem(int row)
{
    Q_D(QStandardItemModel);
    if ((row < 0) || (row >= rowCount()))
        return 0;
    QStandardItem *headerItem = d->rowHeaderItems.at(row);
    if (headerItem) {
        headerItem->d_func()->setParentAndModel(0, 0);
        d->rowHeaderItems.replace(row, 0);
    }
    return headerItem;
}


int QStandardItemModel::sortRole() const
{
    Q_D(const QStandardItemModel);
    return d->sortRole;
}

void QStandardItemModel::setSortRole(int role)
{
    Q_D(QStandardItemModel);
    d->sortRole = role;
}


int QStandardItemModel::columnCount(const QModelIndex &parent) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(parent);
    return item ? item->columnCount() : 0;
}


QVariant QStandardItemModel::data(const QModelIndex &index, int role) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(index);
    return item ? item->data(role) : QVariant();
}


Qt::ItemFlags QStandardItemModel::flags(const QModelIndex &index) const
{
    Q_D(const QStandardItemModel);
    if (!d->indexValid(index))
        return d->root->flags();
    QStandardItem *item = d->itemFromIndex(index);
    if (item)
        return item->flags();
    return Qt::ItemIsSelectable
        |Qt::ItemIsEnabled
        |Qt::ItemIsEditable
        |Qt::ItemIsDragEnabled
        |Qt::ItemIsDropEnabled;
}


bool QStandardItemModel::hasChildren(const QModelIndex &parent) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(parent);
    return item ? item->hasChildren() : false;
}


QVariant QStandardItemModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    Q_D(const QStandardItemModel);
    if ((section < 0)
        || ((orientation == Qt::Horizontal) && (section >= columnCount()))
        || ((orientation == Qt::Vertical) && (section >= rowCount()))) {
        return QVariant();
    }
    QStandardItem *headerItem = 0;
    if (orientation == Qt::Horizontal)
        headerItem = d->columnHeaderItems.at(section);
    else if (orientation == Qt::Vertical)
        headerItem = d->rowHeaderItems.at(section);
    return headerItem ? headerItem->data(role)
        : QAbstractItemModel::headerData(section, orientation, role);
}


Qt::DropActions QStandardItemModel::supportedDropActions () const
{
    return Qt::CopyAction | Qt::MoveAction;
}


QModelIndex QStandardItemModel::index(int row, int column, const QModelIndex &parent) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *parentItem = d->itemFromIndex(parent);
    if ((parentItem == 0)
        || (row < 0)
        || (column < 0)
        || (row >= parentItem->rowCount())
        || (column >= parentItem->columnCount())) {
        return QModelIndex();
    }
    return createIndex(row, column, parentItem);
}


bool QStandardItemModel::insertColumns(int column, int count, const QModelIndex &parent)
{
    Q_D(QStandardItemModel);
    QStandardItem *item = parent.isValid() ? itemFromIndex(parent) : d->root.data();
    if (item == 0)
        return false;
    return item->d_func()->insertColumns(column, count, QList<QStandardItem*>());
}


bool QStandardItemModel::insertRows(int row, int count, const QModelIndex &parent)
{
    Q_D(QStandardItemModel);
    QStandardItem *item = parent.isValid() ? itemFromIndex(parent) : d->root.data();
    if (item == 0)
        return false;
    return item->d_func()->insertRows(row, count, QList<QStandardItem*>());
}


QMap<int, QVariant> QStandardItemModel::itemData(const QModelIndex &index) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(index);
    return item ? item->d_func()->itemData() : QMap<int, QVariant>();
}


QModelIndex QStandardItemModel::parent(const QModelIndex &child) const
{
    Q_D(const QStandardItemModel);
    if (!d->indexValid(child))
        return QModelIndex();
    QStandardItem *parentItem = static_cast<QStandardItem*>(child.internalPointer());
    return indexFromItem(parentItem);
}


bool QStandardItemModel::removeColumns(int column, int count, const QModelIndex &parent)
{
    Q_D(QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(parent);
    if ((item == 0) || (count < 1) || (column < 0) || ((column + count) > item->columnCount()))
        return false;
    item->removeColumns(column, count);
    return true;
}


bool QStandardItemModel::removeRows(int row, int count, const QModelIndex &parent)
{
    Q_D(QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(parent);
    if ((item == 0) || (count < 1) || (row < 0) || ((row + count) > item->rowCount()))
        return false;
    item->removeRows(row, count);
    return true;
}


int QStandardItemModel::rowCount(const QModelIndex &parent) const
{
    Q_D(const QStandardItemModel);
    QStandardItem *item = d->itemFromIndex(parent);
    return item ? item->rowCount() : 0;
}


bool QStandardItemModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!index.isValid())
        return false;
    QStandardItem *item = itemFromIndex(index);
    if (item == 0)
        return false;
    item->setData(value, role);
    return true;
}


bool QStandardItemModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role)
{
    Q_D(QStandardItemModel);
    if ((section < 0)
        || ((orientation == Qt::Horizontal) && (section >= columnCount()))
        || ((orientation == Qt::Vertical) && (section >= rowCount()))) {
        return false;
    }
    QStandardItem *headerItem = 0;
    if (orientation == Qt::Horizontal) {
        headerItem = d->columnHeaderItems.at(section);
        if (headerItem == 0) {
            headerItem = d->createItem();
            headerItem->d_func()->setModel(this);
            d->columnHeaderItems.replace(section, headerItem);
        }
    } else if (orientation == Qt::Vertical) {
        headerItem = d->rowHeaderItems.at(section);
        if (headerItem == 0) {
            headerItem = d->createItem();
            headerItem->d_func()->setModel(this);
            d->rowHeaderItems.replace(section, headerItem);
        }
    }
    if (headerItem) {
        headerItem->setData(value, role);
        return true;
    }
    return false;
}


bool QStandardItemModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)
{
    QStandardItem *item = itemFromIndex(index);
    if (item == 0)
        return false;
    item->d_func()->setItemData(roles);
    return true;
}


void QStandardItemModel::sort(int column, Qt::SortOrder order)
{
    Q_D(QStandardItemModel);
    d->root->sortChildren(column, order);
}





QStringList QStandardItemModel::mimeTypes() const
{
    return QAbstractItemModel::mimeTypes() <<  QLatin1String("application/x-qstandarditemmodeldatalist");
}


QMimeData *QStandardItemModel::mimeData(const QModelIndexList &indexes) const
{
    QMimeData *data = QAbstractItemModel::mimeData(indexes);
    if(!data)
        return 0;

    QString format = QLatin1String("application/x-qstandarditemmodeldatalist");
    if (!mimeTypes().contains(format))
        return data;
    QByteArray encoded;
    QDataStream stream(&encoded, QIODevice::WriteOnly);
    
    QSet<QStandardItem*> itemsSet;
    QStack<QStandardItem*> stack;
    itemsSet.reserve(indexes.count());
    stack.reserve(indexes.count());
    for (int i = 0; i < indexes.count(); ++i) {
        QStandardItem *item = itemFromIndex(indexes.at(i));
        itemsSet << item;
        stack.push(item);
    }
    
    //remove duplicates childrens
    {
        QSet<QStandardItem *> seen;
        while (!stack.isEmpty()) {
            QStandardItem *itm = stack.pop();
            if (seen.contains(itm))
                continue;
            seen.insert(itm);
            
            const QVector<QStandardItem*> &childList = itm->d_func()->children;
            for (int i = 0; i < childList.count(); ++i) {
                QStandardItem *chi = childList.at(i);
                if (chi) {
                    QSet<QStandardItem *>::iterator it = itemsSet.find(chi);
                    if (it != itemsSet.end()) {
                        itemsSet.erase(it);
                    }
                    stack.push(chi);
                }
            }
        }
    }
    
    stack.reserve(itemsSet.count());
    foreach (QStandardItem *item, itemsSet) {
        stack.push(item);
    }
    
    //stream everything recursively
    while (!stack.isEmpty()) {
        QStandardItem *item = stack.pop();
        if(itemsSet.contains(item)) { //if the item is selection 'top-level', strem its position
            stream << item->row() << item->column(); 
        }
        if(item) {
            stream << *item << item->columnCount() << item->d_ptr->children.count();
            stack += item->d_ptr->children;
        } else {
            QStandardItem dummy;
            stream << dummy << 0 << 0;
        }
    }

    data->setData(format, encoded);
    return data;
}



void QStandardItemModelPrivate::decodeDataRecursive(QDataStream &stream, QStandardItem *item)
{
    int colCount, childCount;
    stream >> *item;
    stream >> colCount >> childCount;
    item->setColumnCount(colCount);
    
    int childPos = childCount;
    
    while(childPos > 0) {
        childPos--;
        QStandardItem *child = createItem();
        decodeDataRecursive(stream, child);
        item->setChild( childPos / colCount, childPos % colCount, child);
    }
}



bool QStandardItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action,
                                      int row, int column, const QModelIndex &parent)
{
    Q_D(QStandardItemModel);
    // check if the action is supported
    if (!data || !(action == Qt::CopyAction || action == Qt::MoveAction))
        return false;
    // check if the format is supported
    QString format = QLatin1String("application/x-qstandarditemmodeldatalist");
    if (!data->hasFormat(format))
        return QAbstractItemModel::dropMimeData(data, action, row, column, parent);

    if (row > rowCount(parent))
        row = rowCount(parent);
    if (row == -1)
        row = rowCount(parent);
    if (column == -1)
        column = 0;

    // decode and insert
    QByteArray encoded = data->data(format);
    QDataStream stream(&encoded, QIODevice::ReadOnly);


    //code based on QAbstractItemModel::decodeData
    // adapted to work with QStandardItem
    int top = INT_MAX;
    int left = INT_MAX;
    int bottom = 0;
    int right = 0;
    QVector<int> rows, columns;
    QVector<QStandardItem *> items;

    while (!stream.atEnd()) {
        int r, c;
        QStandardItem *item = d->createItem();
        stream >> r >> c;
        d->decodeDataRecursive(stream, item);

        rows.append(r);
        columns.append(c);
        items.append(item);
        top = qMin(r, top);
        left = qMin(c, left);
        bottom = qMax(r, bottom);
        right = qMax(c, right);
    }

    // insert the dragged items into the table, use a bit array to avoid overwriting items,
    // since items from different tables can have the same row and column
    int dragRowCount = 0;
    int dragColumnCount = right - left + 1;

    // Compute the number of continuous rows upon insertion and modify the rows to match
    QVector<int> rowsToInsert(bottom + 1);
    for (int i = 0; i < rows.count(); ++i)
        rowsToInsert[rows.at(i)] = 1;
    for (int i = 0; i < rowsToInsert.count(); ++i) {
        if (rowsToInsert[i] == 1){
            rowsToInsert[i] = dragRowCount;
            ++dragRowCount;
        }
    }
    for (int i = 0; i < rows.count(); ++i)
        rows[i] = top + rowsToInsert[rows[i]];

    QBitArray isWrittenTo(dragRowCount * dragColumnCount);

    // make space in the table for the dropped data
    int colCount = columnCount(parent);
    if (colCount < dragColumnCount + column) {
        insertColumns(colCount, dragColumnCount + column - colCount, parent);
        colCount = columnCount(parent);
    }
    insertRows(row, dragRowCount, parent);

    row = qMax(0, row);
    column = qMax(0, column);

    QStandardItem *parentItem = itemFromIndex (parent);
    if (!parentItem)
        parentItem = invisibleRootItem();

    QVector<QPersistentModelIndex> newIndexes(items.size());
    // set the data in the table
    for (int j = 0; j < items.size(); ++j) {
        int relativeRow = rows.at(j) - top;
        int relativeColumn = columns.at(j) - left;
        int destinationRow = relativeRow + row;
        int destinationColumn = relativeColumn + column;
        int flat = (relativeRow * dragColumnCount) + relativeColumn;
        // if the item was already written to, or we just can't fit it in the table, create a new row
        if (destinationColumn >= colCount || isWrittenTo.testBit(flat)) {
            destinationColumn = qBound(column, destinationColumn, colCount - 1);
            destinationRow = row + dragRowCount;
            insertRows(row + dragRowCount, 1, parent);
            flat = (dragRowCount * dragColumnCount) + relativeColumn;
            isWrittenTo.resize(++dragRowCount * dragColumnCount);
        }
        if (!isWrittenTo.testBit(flat)) {
            newIndexes[j] = index(destinationRow, destinationColumn, parentItem->index());
            isWrittenTo.setBit(flat);
        }
    }

    for(int k = 0; k < newIndexes.size(); k++) {
        if (newIndexes.at(k).isValid()) {
            parentItem->setChild(newIndexes.at(k).row(), newIndexes.at(k).column(), items.at(k));
        } else {
            delete items.at(k);
        }
    }

    return true;
}
