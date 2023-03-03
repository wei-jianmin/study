class Q_GUI_EXPORT QStandardItem
{
public:
    QStandardItem();
    QStandardItem(const QString &text);
    QStandardItem(const QIcon &icon, const QString &text);
    explicit QStandardItem(int rows, int columns = 1);
    virtual ~QStandardItem();

    virtual QVariant data(int role = Qt::UserRole + 1) const;
    virtual void setData(const QVariant &value, int role = Qt::UserRole + 1);

    inline QString text() const {
        return qvariant_cast<QString>(data(Qt::DisplayRole));
    }
    inline void setText(const QString &text);

    inline QIcon icon() const {
        return qvariant_cast<QIcon>(data(Qt::DecorationRole));
    }
    inline void setIcon(const QIcon &icon);

#ifndef QT_NO_TOOLTIP
    inline QString toolTip() const {
        return qvariant_cast<QString>(data(Qt::ToolTipRole));
    }
    inline void setToolTip(const QString &toolTip);
#endif

#ifndef QT_NO_STATUSTIP
    inline QString statusTip() const {
        return qvariant_cast<QString>(data(Qt::StatusTipRole));
    }
    inline void setStatusTip(const QString &statusTip);
#endif

#ifndef QT_NO_WHATSTHIS
    inline QString whatsThis() const {
        return qvariant_cast<QString>(data(Qt::WhatsThisRole));
    }
    inline void setWhatsThis(const QString &whatsThis);
#endif

    inline QSize sizeHint() const {
        return qvariant_cast<QSize>(data(Qt::SizeHintRole));
    }
    inline void setSizeHint(const QSize &sizeHint);

    inline QFont font() const {
        return qvariant_cast<QFont>(data(Qt::FontRole));
    }
    inline void setFont(const QFont &font);

    inline Qt::Alignment textAlignment() const {
        return Qt::Alignment(qvariant_cast<int>(data(Qt::TextAlignmentRole)));
    }
    inline void setTextAlignment(Qt::Alignment textAlignment);

    inline QBrush background() const {
        return qvariant_cast<QBrush>(data(Qt::BackgroundRole));
    }
    inline void setBackground(const QBrush &brush);

    inline QBrush foreground() const {
        return qvariant_cast<QBrush>(data(Qt::ForegroundRole));
    }
    inline void setForeground(const QBrush &brush);

    inline Qt::CheckState checkState() const {
        return Qt::CheckState(qvariant_cast<int>(data(Qt::CheckStateRole)));
    }
    inline void setCheckState(Qt::CheckState checkState);

    inline QString accessibleText() const {
        return qvariant_cast<QString>(data(Qt::AccessibleTextRole));
    }
    inline void setAccessibleText(const QString &accessibleText);

    inline QString accessibleDescription() const {
        return qvariant_cast<QString>(data(Qt::AccessibleDescriptionRole));
    }
    inline void setAccessibleDescription(const QString &accessibleDescription);

    Qt::ItemFlags flags() const;
    void setFlags(Qt::ItemFlags flags);

    inline bool isEnabled() const {
        return (flags() & Qt::ItemIsEnabled) != 0;
    }
    void setEnabled(bool enabled);

    inline bool isEditable() const {
        return (flags() & Qt::ItemIsEditable) != 0;
    }
    void setEditable(bool editable);

    inline bool isSelectable() const {
        return (flags() & Qt::ItemIsSelectable) != 0;
    }
    void setSelectable(bool selectable);

    inline bool isCheckable() const {
        return (flags() & Qt::ItemIsUserCheckable) != 0;
    }
    void setCheckable(bool checkable);

    inline bool isTristate() const {
        return (flags() & Qt::ItemIsTristate) != 0;
    }
    void setTristate(bool tristate);

#ifndef QT_NO_DRAGANDDROP
    inline bool isDragEnabled() const {
        return (flags() & Qt::ItemIsDragEnabled) != 0;
    }
    void setDragEnabled(bool dragEnabled);

    inline bool isDropEnabled() const {
        return (flags() & Qt::ItemIsDropEnabled) != 0;
    }
    void setDropEnabled(bool dropEnabled);
#endif // QT_NO_DRAGANDDROP

    QStandardItem *parent() const;
    int row() const;
    int column() const;
    QModelIndex index() const;
    QStandardItemModel *model() const;

    int rowCount() const;
    void setRowCount(int rows);
    int columnCount() const;
    void setColumnCount(int columns);

    bool hasChildren() const;
    QStandardItem *child(int row, int column = 0) const;
    void setChild(int row, int column, QStandardItem *item);
    inline void setChild(int row, QStandardItem *item);

    void insertRow(int row, const QList<QStandardItem*> &items);
    void insertColumn(int column, const QList<QStandardItem*> &items);
    void insertRows(int row, const QList<QStandardItem*> &items);
    void insertRows(int row, int count);
    void insertColumns(int column, int count);

    void removeRow(int row);
    void removeColumn(int column);
    void removeRows(int row, int count);
    void removeColumns(int column, int count);

    inline void appendRow(const QList<QStandardItem*> &items);
    inline void appendRows(const QList<QStandardItem*> &items);
    inline void appendColumn(const QList<QStandardItem*> &items);
    inline void insertRow(int row, QStandardItem *item);
    inline void appendRow(QStandardItem *item);

    QStandardItem *takeChild(int row, int column = 0);
    QList<QStandardItem*> takeRow(int row);
    QList<QStandardItem*> takeColumn(int column);

    void sortChildren(int column, Qt::SortOrder order = Qt::AscendingOrder);

    virtual QStandardItem *clone() const;

    enum ItemType { Type = 0, UserType = 1000 };
    virtual int type() const;

#ifndef QT_NO_DATASTREAM
    virtual void read(QDataStream &in);
    virtual void write(QDataStream &out) const;
#endif
    virtual bool operator<(const QStandardItem &other) const;

protected:
    QStandardItem(const QStandardItem &other);
    QStandardItem(QStandardItemPrivate &dd);
    QStandardItem &operator=(const QStandardItem &other);
    QScopedPointer<QStandardItemPrivate> d_ptr;

    void emitDataChanged();

private:
    Q_DECLARE_PRIVATE(QStandardItem)
    friend class QStandardItemModelPrivate;
    friend class QStandardItemModel;
};

inline void QStandardItem::setText(const QString &atext)
{ setData(atext, Qt::DisplayRole); }

inline void QStandardItem::setIcon(const QIcon &aicon)
{ setData(aicon, Qt::DecorationRole); }

#ifndef QT_NO_TOOLTIP
inline void QStandardItem::setToolTip(const QString &atoolTip)
{ setData(atoolTip, Qt::ToolTipRole); }
#endif

#ifndef QT_NO_STATUSTIP
inline void QStandardItem::setStatusTip(const QString &astatusTip)
{ setData(astatusTip, Qt::StatusTipRole); }
#endif

#ifndef QT_NO_WHATSTHIS
inline void QStandardItem::setWhatsThis(const QString &awhatsThis)
{ setData(awhatsThis, Qt::WhatsThisRole); }
#endif

inline void QStandardItem::setSizeHint(const QSize &asizeHint)
{ setData(asizeHint, Qt::SizeHintRole); }

inline void QStandardItem::setFont(const QFont &afont)
{ setData(afont, Qt::FontRole); }

inline void QStandardItem::setTextAlignment(Qt::Alignment atextAlignment)
{ setData(int(atextAlignment), Qt::TextAlignmentRole); }

inline void QStandardItem::setBackground(const QBrush &abrush)
{ setData(abrush, Qt::BackgroundRole); }

inline void QStandardItem::setForeground(const QBrush &abrush)
{ setData(abrush, Qt::ForegroundRole); }

inline void QStandardItem::setCheckState(Qt::CheckState acheckState)
{ setData(acheckState, Qt::CheckStateRole); }

inline void QStandardItem::setAccessibleText(const QString &aaccessibleText)
{ setData(aaccessibleText, Qt::AccessibleTextRole); }

inline void QStandardItem::setAccessibleDescription(const QString &aaccessibleDescription)
{ setData(aaccessibleDescription, Qt::AccessibleDescriptionRole); }

inline void QStandardItem::setChild(int arow, QStandardItem *aitem)
{ setChild(arow, 0, aitem); }

inline void QStandardItem::appendRow(const QList<QStandardItem*> &aitems)
{ insertRow(rowCount(), aitems); }

inline void QStandardItem::appendRows(const QList<QStandardItem*> &aitems)
{ insertRows(rowCount(), aitems); }

inline void QStandardItem::appendColumn(const QList<QStandardItem*> &aitems)
{ insertColumn(columnCount(), aitems); }

inline void QStandardItem::insertRow(int arow, QStandardItem *aitem)
{ insertRow(arow, QList<QStandardItem*>() << aitem); }

inline void QStandardItem::appendRow(QStandardItem *aitem)
{ insertRow(rowCount(), aitem); }

QStandardItem::QStandardItem()
    : d_ptr(new QStandardItemPrivate)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
}


QStandardItem::QStandardItem(const QString &text)
    : d_ptr(new QStandardItemPrivate)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
    setText(text);
}


QStandardItem::QStandardItem(const QIcon &icon, const QString &text)
    : d_ptr(new QStandardItemPrivate)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
    setIcon(icon);
    setText(text);
}


QStandardItem::QStandardItem(int rows, int columns)
    : d_ptr(new QStandardItemPrivate)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
    setRowCount(rows);
    setColumnCount(columns);
}


QStandardItem::QStandardItem(QStandardItemPrivate &dd)
    : d_ptr(&dd)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
}


QStandardItem::QStandardItem(const QStandardItem &other)
    : d_ptr(new QStandardItemPrivate)
{
    Q_D(QStandardItem);
    d->q_ptr = this;
    operator=(other);
}


QStandardItem &QStandardItem::operator=(const QStandardItem &other)
{
    Q_D(QStandardItem);
    d->values = other.d_func()->values;
    return *this;
}


QStandardItem::~QStandardItem()
{
}


QStandardItem *QStandardItem::parent() const
{
    Q_D(const QStandardItem);
    if (!d->model || (d->model->d_func()->root.data() != d->parent))
        return d->parent;
    return 0;
}


void QStandardItem::setData(const QVariant &value, int role)
{
    Q_D(QStandardItem);
    role = (role == Qt::EditRole) ? Qt::DisplayRole : role;
    QVector<QWidgetItemData>::iterator it;
    for (it = d->values.begin(); it != d->values.end(); ++it) {
        if ((*it).role == role) {
            if (value.isValid()) {
                if ((*it).value.type() == value.type() && (*it).value == value)
                    return;
                (*it).value = value;
            } else {
                d->values.erase(it);
            }
            if (d->model)
                d->model->d_func()->itemChanged(this);
            return;
        }
    }
    d->values.append(QWidgetItemData(role, value));
    if (d->model)
        d->model->d_func()->itemChanged(this);
}


QVariant QStandardItem::data(int role) const
{
    Q_D(const QStandardItem);
    role = (role == Qt::EditRole) ? Qt::DisplayRole : role;
    QVector<QWidgetItemData>::const_iterator it;
    for (it = d->values.begin(); it != d->values.end(); ++it) {
        if ((*it).role == role)
            return (*it).value;
    }
    return QVariant();
}


void QStandardItem::emitDataChanged()
{
    Q_D(QStandardItem);
    if (d->model)
        d->model->d_func()->itemChanged(this);
}


void QStandardItem::setFlags(Qt::ItemFlags flags)
{
    setData((int)flags, Qt::UserRole - 1);
}


Qt::ItemFlags QStandardItem::flags() const
{
    QVariant v = data(Qt::UserRole - 1);
    if (!v.isValid())
        return (Qt::ItemIsSelectable|Qt::ItemIsEnabled|Qt::ItemIsEditable
                |Qt::ItemIsDragEnabled|Qt::ItemIsDropEnabled);
    return Qt::ItemFlags(v.toInt());
}

int QStandardItem::row() const
{
    Q_D(const QStandardItem);
    QPair<int, int> pos = d->position();
    return pos.first;
}


int QStandardItem::column() const
{
    Q_D(const QStandardItem);
    QPair<int, int> pos = d->position();
    return pos.second;
}


QModelIndex QStandardItem::index() const
{
    Q_D(const QStandardItem);
    return d->model ? d->model->indexFromItem(this) : QModelIndex();
}


QStandardItemModel *QStandardItem::model() const
{
    Q_D(const QStandardItem);
    return d->model;
}


void QStandardItem::setRowCount(int rows)
{
    int rc = rowCount();
    if (rc == rows)
        return;
    if (rc < rows)
        insertRows(qMax(rc, 0), rows - rc);
    else
        removeRows(qMax(rows, 0), rc - rows);
}


int QStandardItem::rowCount() const
{
    Q_D(const QStandardItem);
    return d->rowCount();
}


void QStandardItem::setColumnCount(int columns)
{
    int cc = columnCount();
    if (cc == columns)
        return;
    if (cc < columns)
        insertColumns(qMax(cc, 0), columns - cc);
    else
        removeColumns(qMax(columns, 0), cc - columns);
}


int QStandardItem::columnCount() const
{
    Q_D(const QStandardItem);
    return d->columnCount();
}


void QStandardItem::insertRow(int row, const QList<QStandardItem*> &items)
{
    Q_D(QStandardItem);
    if (row < 0)
        return;
    if (columnCount() < items.count())
        setColumnCount(items.count());
    d->insertRows(row, 1, items);
}


void QStandardItem::insertRows(int row, const QList<QStandardItem*> &items)
{
    Q_D(QStandardItem);
    if (row < 0)
        return;
    d->insertRows(row, items);
}


void QStandardItem::insertColumn(int column, const QList<QStandardItem*> &items)
{
    Q_D(QStandardItem);
    if (column < 0)
        return;
    if (rowCount() < items.count())
        setRowCount(items.count());
    d->insertColumns(column, 1, items);
}


void QStandardItem::insertRows(int row, int count)
{
    Q_D(QStandardItem);
    if (rowCount() < row) {
        count += row - rowCount();
        row = rowCount();
    }
    d->insertRows(row, count, QList<QStandardItem*>());
}


void QStandardItem::insertColumns(int column, int count)
{
    Q_D(QStandardItem);
    if (columnCount() < column) {
        count += column - columnCount();
        column = columnCount();
    }
    d->insertColumns(column, count, QList<QStandardItem*>());
}
