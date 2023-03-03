class QStandardItemPrivate
{
    Q_DECLARE_PUBLIC(QStandardItem)
public:
    inline QStandardItemPrivate()
        : model(0),
          parent(0),
          rows(0),
          columns(0),
          q_ptr(0),
          lastIndexOf(2)
        { }
    virtual ~QStandardItemPrivate();

    inline int childIndex(int row, int column) const {
        if ((row < 0) || (column < 0)
            || (row >= rowCount()) || (column >= columnCount())) {
            return -1;
        }
        return (row * columnCount()) + column;
    }
    inline int childIndex(const QStandardItem *child) {
        int start = qMax(0, lastIndexOf -2);    //从上次查找到的位置，继续往下查找
        lastIndexOf = children.indexOf(const_cast<QStandardItem*>(child), start);
        if (lastIndexOf == -1 && start != 0)
            lastIndexOf = children.lastIndexOf(const_cast<QStandardItem*>(child), start);
        return lastIndexOf;
    }
    QPair<int, int> position() const;
    void setChild(int row, int column, QStandardItem *item,
                  bool emitChanged = false);
    inline int rowCount() const {
        return rows;
    }
    inline int columnCount() const {
        return columns;
    }
    void childDeleted(QStandardItem *child);

    void setModel(QStandardItemModel *mod);

    inline void setParentAndModel(
        QStandardItem *par,
        QStandardItemModel *mod) {
        setModel(mod);
        parent = par;
    }

    void changeFlags(bool enable, Qt::ItemFlags f);
    void setItemData(const QMap<int, QVariant> &roles);
    const QMap<int, QVariant> itemData() const;

    bool insertRows(int row, int count, const QList<QStandardItem*> &items);
    bool insertRows(int row, const QList<QStandardItem*> &items);
    bool insertColumns(int column, int count, const QList<QStandardItem*> &items);

    void sortChildren(int column, Qt::SortOrder order);

    QStandardItemModel *model;
    QStandardItem *parent;
    QVector<QWidgetItemData> values;    //存放各种角色信息，如图标、文本、字体、前景色等等
    QVector<QStandardItem*> children;   //按行依次存放各个子元素（意味着一个QStandardItem中可以存放一个子QStandardItem表）
    int rows;
    int columns;

    QStandardItem *q_ptr;

    int lastIndexOf;
};

QStandardItemPrivate::~QStandardItemPrivate()
{
    QVector<QStandardItem*>::const_iterator it;
    for (it = children.constBegin(); it != children.constEnd(); ++it) {
        QStandardItem *child = *it;
        if (child)
            child->d_func()->setModel(0);
        delete child;
    }
    children.clear();
    if (parent && model)
        parent->d_func()->childDeleted(q_func());
}


QPair<int, int> QStandardItemPrivate::position() const
{
    if (QStandardItem *par = parent) {
        int idx = par->d_func()->childIndex(q_func());
        if (idx == -1)
            return QPair<int, int>(-1, -1);
        return QPair<int, int>(idx / par->columnCount(), idx % par->columnCount());
    }
    // ### support header items?
    return QPair<int, int>(-1, -1);
}


void QStandardItemPrivate::setChild(int row, int column, QStandardItem *item,
                                    bool emitChanged)
{
    Q_Q(QStandardItem);
    if (item == q) {
        qWarning("QStandardItem::setChild: Can't make an item a child of itself %p",
                 item);
        return;
    }
    if ((row < 0) || (column < 0))
        return;
    if (rows <= row)
        q->setRowCount(row + 1);
    if (columns <= column)
        q->setColumnCount(column + 1);
    int index = childIndex(row, column);
    Q_ASSERT(index != -1);                  //说明只能对已存在的元素设置新值
    QStandardItem *oldItem = children.at(index);
    if (item == oldItem)
        return;
    if (item) {
        if (item->d_func()->parent == 0) {
            item->d_func()->setParentAndModel(q, model);
        } else {
            qWarning("QStandardItem::setChild: Ignoring duplicate insertion of item %p",
                     item);
            return;
        }
    }
    if (oldItem)
        oldItem->d_func()->setModel(0);
    delete oldItem;                 //释放旧元素，替换上新元素
    children.replace(index, item);
    if (emitChanged && model)
        model->d_func()->itemChanged(item);
}



void QStandardItemPrivate::changeFlags(bool enable, Qt::ItemFlags f)
{
    Q_Q(QStandardItem);
    Qt::ItemFlags flags = q->flags();
    if (enable)
        flags |= f;
    else
        flags &= ~f;
    q->setFlags(flags);
}


void QStandardItemPrivate::childDeleted(QStandardItem *child)
{
    int index = childIndex(child);
    Q_ASSERT(index != -1);
    children.replace(index, 0);
}


void QStandardItemPrivate::setItemData(const QMap<int, QVariant> &roles)
{
    Q_Q(QStandardItem);

    //let's build the vector of new values
    QVector<QWidgetItemData> newValues;
    QMap<int, QVariant>::const_iterator it;
    for (it = roles.begin(); it != roles.end(); ++it) {
        QVariant value = it.value();
        if (value.isValid()) {
            int role = it.key();
            role = (role == Qt::EditRole) ? Qt::DisplayRole : role;
            QWidgetItemData wid(role,it.value());
            newValues.append(wid);
        }
    }

    if (values!=newValues) {
        values=newValues;
        if (model)
            model->d_func()->itemChanged(q);
    }
}


const QMap<int, QVariant> QStandardItemPrivate::itemData() const
{
    QMap<int, QVariant> result;
    QVector<QWidgetItemData>::const_iterator it;
    for (it = values.begin(); it != values.end(); ++it)
        result.insert((*it).role, (*it).value);
    return result;
}


void QStandardItemPrivate::sortChildren(int column, Qt::SortOrder order)
{
    Q_Q(QStandardItem);
    if (column >= columnCount())
        return;

    QVector<QPair<QStandardItem*, int> > sortable;
    QVector<int> unsortable;

    sortable.reserve(rowCount());
    unsortable.reserve(rowCount());

    for (int row = 0; row < rowCount(); ++row) {
        QStandardItem *itm = q->child(row, column);
        if (itm)
            sortable.append(QPair<QStandardItem*,int>(itm, row));
        else
            unsortable.append(row);
    }

    if (order == Qt::AscendingOrder) {
        QStandardItemModelLessThan lt;
        qStableSort(sortable.begin(), sortable.end(), lt);
    } else {
        QStandardItemModelGreaterThan gt;
        qStableSort(sortable.begin(), sortable.end(), gt);
    }

    QModelIndexList changedPersistentIndexesFrom, changedPersistentIndexesTo;
    QVector<QStandardItem*> sorted_children(children.count());
    for (int i = 0; i < rowCount(); ++i) {
        int r = (i < sortable.count()
                 ? sortable.at(i).second
                 : unsortable.at(i - sortable.count()));
        for (int c = 0; c < columnCount(); ++c) {
            QStandardItem *itm = q->child(r, c);
            sorted_children[childIndex(i, c)] = itm;
            if (model) {
                QModelIndex from = model->createIndex(r, c, q);
                if (model->d_func()->persistent.indexes.contains(from)) {
                    QModelIndex to = model->createIndex(i, c, q);
                    changedPersistentIndexesFrom.append(from);
                    changedPersistentIndexesTo.append(to);
                }
            }
        }
    }

    children = sorted_children;

    if (model) {
        model->changePersistentIndexList(changedPersistentIndexesFrom, changedPersistentIndexesTo);
    }

    QVector<QStandardItem*>::iterator it;
    for (it = children.begin(); it != children.end(); ++it) {
        if (*it)
            (*it)->d_func()->sortChildren(column, order);
    }
}


void QStandardItemPrivate::setModel(QStandardItemModel *mod)
{
    if (children.isEmpty()) {
        if (model)
            model->d_func()->invalidatePersistentIndex(model->indexFromItem(q_ptr));
        model = mod;
    } else {
        QStack<QStandardItem*> stack;
        stack.push(q_ptr);
        while (!stack.isEmpty()) {
            QStandardItem *itm = stack.pop();
            if (itm->d_func()->model) {
                itm->d_func()->model->d_func()->invalidatePersistentIndex(itm->d_func()->model->indexFromItem(itm));
            }
            itm->d_func()->model = mod;
            const QVector<QStandardItem*> &childList = itm->d_func()->children;
            for (int i = 0; i < childList.count(); ++i) {
                QStandardItem *chi = childList.at(i);
                if (chi)
                    stack.push(chi);
            }
        }
    }
}


bool QStandardItemPrivate::insertRows(int row, const QList<QStandardItem*> &items)
{
    Q_Q(QStandardItem);
    if ((row < 0) || (row > rowCount()))
        return false;
    int count = items.count();
    if (model)
        model->d_func()->rowsAboutToBeInserted(q, row, row + count - 1);
    if (rowCount() == 0) {
        if (columnCount() == 0)
            q->setColumnCount(1);
        children.resize(columnCount() * count);
        rows = count;
    } else {
        rows += count;
        int index = childIndex(row, 0);
        if (index != -1)
            children.insert(index, columnCount() * count, 0);
    }
    for (int i = 0; i < items.count(); ++i) {
        QStandardItem *item = items.at(i);
        item->d_func()->model = model;
        item->d_func()->parent = q;
        int index = childIndex(i + row, 0);
        children.replace(index, item);
    }
    if (model)
        model->d_func()->rowsInserted(q, row, count);
    return true;
}

bool QStandardItemPrivate::insertRows(int row, int count, const QList<QStandardItem*> &items)
{
    Q_Q(QStandardItem);
    if ((count < 1) || (row < 0) || (row > rowCount()))
        return false;
    if (model)
        model->d_func()->rowsAboutToBeInserted(q, row, row + count - 1);
    if (rowCount() == 0) {
        children.resize(columnCount() * count);
        rows = count;
    } else {
        rows += count;
        int index = childIndex(row, 0);
        if (index != -1)
            children.insert(index, columnCount() * count, 0);
    }
    if (!items.isEmpty()) {
        int index = childIndex(row, 0);
        int limit = qMin(items.count(), columnCount() * count);
        for (int i = 0; i < limit; ++i) {
            QStandardItem *item = items.at(i);
            if (item) {
                if (item->d_func()->parent == 0) {
                    item->d_func()->setParentAndModel(q, model);
                } else {
                    qWarning("QStandardItem::insertRows: Ignoring duplicate insertion of item %p",
                             item);
                    item = 0;
                }
            }
            children.replace(index, item);
            ++index;
        }
    }
    if (model)
        model->d_func()->rowsInserted(q, row, count);
    return true;
}


bool QStandardItemPrivate::insertColumns(int column, int count, const QList<QStandardItem*> &items)
{
    Q_Q(QStandardItem);
    if ((count < 1) || (column < 0) || (column > columnCount()))
        return false;
    if (model)
        model->d_func()->columnsAboutToBeInserted(q, column, column + count - 1);
    if (columnCount() == 0) {
        children.resize(rowCount() * count);
        columns = count;
    } else {
        columns += count;
        int index = childIndex(0, column);
        for (int row = 0; row < rowCount(); ++row) {
            children.insert(index, count, 0);
            index += columnCount();
        }
    }
    if (!items.isEmpty()) {
        int limit = qMin(items.count(), rowCount() * count);
        for (int i = 0; i < limit; ++i) {
            QStandardItem *item = items.at(i);
            if (item) {
                if (item->d_func()->parent == 0) {
                    item->d_func()->setParentAndModel(q, model);
                } else {
                    qWarning("QStandardItem::insertColumns: Ignoring duplicate insertion of item %p",
                             item);
                    item = 0;
                }
            }
            int r = i / count;
            int c = column + (i % count);
            int index = childIndex(r, c);
            children.replace(index, item);
        }
    }
    if (model)
        model->d_func()->columnsInserted(q, column, count);
    return true;
}

