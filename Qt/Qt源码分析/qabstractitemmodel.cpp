#include "qabstractitemmodel.h"
#include <private/qabstractitemmodel_p.h>
#include <qdatastream.h>
#include <qstringlist.h>
#include <qsize.h>
#include <qmimedata.h>
#include <qdebug.h>
#include <qvector.h>
#include <qstack.h>
#include <qbitarray.h>
#include <limits.h>
QT_BEGIN_NAMESPACE
QPersistentModelIndexData *QPersistentModelIndexData::create(const QModelIndex &index)
{
    Q_ASSERT(index.isValid()); // we will _never_ insert an invalid index in the list
    QPersistentModelIndexData *d = 0;
    QAbstractItemModel *model = const_cast<QAbstractItemModel *>(index.model());
    QHash<QModelIndex, QPersistentModelIndexData *> &indexes = model->d_func()->persistent.indexes;
    const QHash<QModelIndex, QPersistentModelIndexData *>::iterator it = indexes.find(index);
    if (it != indexes.end()) {
        d = (*it);
    } else {
        d = new QPersistentModelIndexData(index);
        indexes.insert(index, d);
    }
    Q_ASSERT(d);
    return d;
}
void QPersistentModelIndexData::destroy(QPersistentModelIndexData *data)
{
    Q_ASSERT(data);
    Q_ASSERT(data->ref == 0);
    QAbstractItemModel *model = const_cast<QAbstractItemModel *>(data->model);
    // a valid persistent model index with a null model pointer can only happen if the model was destroyed
    if (model) {
        QAbstractItemModelPrivate *p = model->d_func();
        Q_ASSERT(p);
        p->removePersistentIndexData(data);
    }
    delete data;
}
QPersistentModelIndex::QPersistentModelIndex()
    : d(0)
{
}
QPersistentModelIndex::QPersistentModelIndex(const QPersistentModelIndex &other)
    : d(other.d)
{
    if (d) d->ref.ref();
}
QPersistentModelIndex::QPersistentModelIndex(const QModelIndex &index)
    : d(0)
{
    if (index.isValid()) {
        d = QPersistentModelIndexData::create(index);
        d->ref.ref();
    }
}
QPersistentModelIndex::~QPersistentModelIndex()
{
    if (d && !d->ref.deref()) {
        QPersistentModelIndexData::destroy(d);
        d = 0;
    }
}
bool QPersistentModelIndex::operator==(const QPersistentModelIndex &other) const
{
    if (d && other.d)
        return d->index == other.d->index;
    return d == other.d;
}
bool QPersistentModelIndex::operator<(const QPersistentModelIndex &other) const
{
    if (d && other.d)
        return d->index < other.d->index;
    return d < other.d;
}
QPersistentModelIndex &QPersistentModelIndex::operator=(const QPersistentModelIndex &other)
{
    if (d == other.d)
        return *this;
    if (d && !d->ref.deref())
        QPersistentModelIndexData::destroy(d);
    d = other.d;
    if (d) d->ref.ref();
    return *this;
}
QPersistentModelIndex &QPersistentModelIndex::operator=(const QModelIndex &other)
{
    if (d && !d->ref.deref())
        QPersistentModelIndexData::destroy(d);
    if (other.isValid()) {
        d = QPersistentModelIndexData::create(other);
        if (d) d->ref.ref();
    } else {
        d = 0;
    }
    return *this;
}
QPersistentModelIndex::operator const QModelIndex&() const
{
    static const QModelIndex invalid;
    if (d)
        return d->index;
    return invalid;
}
bool QPersistentModelIndex::operator==(const QModelIndex &other) const
{
    if (d)
        return d->index == other;
    return !other.isValid();
}
bool QPersistentModelIndex::operator!=(const QModelIndex &other) const
{
    if (d)
        return d->index != other;
    return other.isValid();
}
int QPersistentModelIndex::row() const
{
    if (d)
        return d->index.row();
    return -1;
}
int QPersistentModelIndex::column() const
{
    if (d)
        return d->index.column();
    return -1;
}
void *QPersistentModelIndex::internalPointer() const
{
    if (d)
        return d->index.internalPointer();
    return 0;
}
qint64 QPersistentModelIndex::internalId() const
{
    if (d)
        return d->index.internalId();
    return 0;
}
QModelIndex QPersistentModelIndex::parent() const
{
    if (d)
        return d->index.parent();
    return QModelIndex();
}
QModelIndex QPersistentModelIndex::sibling(int row, int column) const
{
    if (d)
        return d->index.sibling(row, column);
    return QModelIndex();
}
QModelIndex QPersistentModelIndex::child(int row, int column) const
{
    if (d)
        return d->index.child(row, column);
    return QModelIndex();
}
QVariant QPersistentModelIndex::data(int role) const
{
    if (d)
        return d->index.data(role);
    return QVariant();
}
Qt::ItemFlags QPersistentModelIndex::flags() const
{
    if (d)
        return d->index.flags();
    return 0;
}
const QAbstractItemModel *QPersistentModelIndex::model() const
{
    if (d)
        return d->index.model();
    return 0;
}
bool QPersistentModelIndex::isValid() const
{
    return d && d->index.isValid();
}
#ifndef QT_NO_DEBUG_STREAM
QDebug operator<<(QDebug dbg, const QModelIndex &idx)
{
#ifndef Q_BROKEN_DEBUG_STREAM
    dbg.nospace() << "QModelIndex(" << idx.row() << ',' << idx.column()
                  << ',' << idx.internalPointer() << ',' << idx.model() << ')';
    return dbg.space();
#else
    qWarning("This compiler doesn't support streaming QModelIndex to QDebug");
    return dbg;
    Q_UNUSED(idx);
#endif
}
QDebug operator<<(QDebug dbg, const QPersistentModelIndex &idx)
{
    if (idx.d)
        dbg << idx.d->index;
    else
        dbg << QModelIndex();
    return dbg;
}
#endif
class QEmptyItemModel : public QAbstractItemModel
{
public:
    explicit QEmptyItemModel(QObject *parent = 0) : QAbstractItemModel(parent) {}
    QModelIndex index(int, int, const QModelIndex &) const { return QModelIndex(); }
    QModelIndex parent(const QModelIndex &) const { return QModelIndex(); }
    int rowCount(const QModelIndex &) const { return 0; }
    int columnCount(const QModelIndex &) const { return 0; }
    bool hasChildren(const QModelIndex &) const { return false; }
    QVariant data(const QModelIndex &, int) const { return QVariant(); }
};
Q_GLOBAL_STATIC(QEmptyItemModel, qEmptyModel)
QAbstractItemModel *QAbstractItemModelPrivate::staticEmptyModel()
{
    return qEmptyModel();
}
namespace {
    struct DefaultRoleNames : public QHash<int, QByteArray>
    {
        DefaultRoleNames() {
            (*this)[Qt::DisplayRole] = "display";
            (*this)[Qt::DecorationRole] = "decoration";
            (*this)[Qt::EditRole] = "edit";
            (*this)[Qt::ToolTipRole] = "toolTip";
            (*this)[Qt::StatusTipRole] = "statusTip";
            (*this)[Qt::WhatsThisRole] = "whatsThis";
        }
    };
}
Q_GLOBAL_STATIC(DefaultRoleNames, qDefaultRoleNames)
const QHash<int,QByteArray> &QAbstractItemModelPrivate::defaultRoleNames()
{
    return *qDefaultRoleNames();
}
static uint typeOfVariant(const QVariant &value)
{
    //return 0 for integer, 1 for floating point and 2 for other
    switch (value.userType()) {
        case QVariant::Bool:
        case QVariant::Int:
        case QVariant::UInt:
        case QVariant::LongLong:
        case QVariant::ULongLong:
        case QVariant::Char:
        case QMetaType::Short:
        case QMetaType::UShort:
        case QMetaType::UChar:
        case QMetaType::ULong:
        case QMetaType::Long:
            return 0;
        case QVariant::Double:
        case QMetaType::Float:
            return 1;
        default:
            return 2;
    }
}
bool QAbstractItemModelPrivate::variantLessThan(const QVariant &v1, const QVariant &v2)
{
    switch(qMax(typeOfVariant(v1), typeOfVariant(v2)))
    {
    case 0: //integer type
        return v1.toLongLong() < v2.toLongLong();
    case 1: //floating point
        return v1.toReal() < v2.toReal();
    default:
        return v1.toString().localeAwareCompare(v2.toString()) < 0;
    }
}
void QAbstractItemModelPrivate::removePersistentIndexData(QPersistentModelIndexData *data)
{
    if (data->index.isValid()) {
        int removed = persistent.indexes.remove(data->index);
        Q_ASSERT_X(removed == 1, "QPersistentModelIndex::~QPersistentModelIndex",
                   "persistent model indexes corrupted"); //maybe the index was somewhat invalid?
        // This assert may happen if the model use changePersistentIndex in a way that could result on two
        // QPersistentModelIndex pointing to the same index.
        Q_UNUSED(removed);
    }
    // make sure our optimization still works
    for (int i = persistent.moved.count() - 1; i >= 0; --i) {
        int idx = persistent.moved[i].indexOf(data);
        if (idx >= 0)
            persistent.moved[i].remove(idx);
    }
    // update the references to invalidated persistent indexes
    for (int i = persistent.invalidated.count() - 1; i >= 0; --i) {
        int idx = persistent.invalidated[i].indexOf(data);
        if (idx >= 0)
            persistent.invalidated[i].remove(idx);
    }
}
void QAbstractItemModelPrivate::rowsAboutToBeInserted(const QModelIndex &parent,
                                                      int first, int last)
{
    Q_Q(QAbstractItemModel);
    Q_UNUSED(last);
    QVector<QPersistentModelIndexData *> persistent_moved;
    if (first < q->rowCount(parent)) {
        for (QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it = persistent.indexes.constBegin();
             it != persistent.indexes.constEnd(); ++it) {
            QPersistentModelIndexData *data = *it;
            const QModelIndex &index = data->index;
            if (index.row() >= first && index.isValid() && index.parent() == parent) {
                persistent_moved.append(data);
            }
        }
    }
    persistent.moved.push(persistent_moved);
}
void QAbstractItemModelPrivate::rowsInserted(const QModelIndex &parent,
                                             int first, int last)
{
    QVector<QPersistentModelIndexData *> persistent_moved = persistent.moved.pop();
    int count = (last - first) + 1; // it is important to only use the delta, because the change could be nested
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_moved.constBegin();
         it != persistent_moved.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        QModelIndex old = data->index;
        persistent.indexes.erase(persistent.indexes.find(old));
        data->index = q_func()->index(old.row() + count, old.column(), parent);
        if (data->index.isValid()) {
            persistent.insertMultiAtEnd(data->index, data);
        } else {
            qWarning() << "QAbstractItemModel::endInsertRows:  Invalid index (" << old.row() + count << ',' << old.column() << ") in model" << q_func();
        }
    }
}
void QAbstractItemModelPrivate::itemsAboutToBeMoved(const QModelIndex &srcParent, int srcFirst, int srcLast, const QModelIndex &destinationParent, int destinationChild, Qt::Orientation orientation)
{
    QVector<QPersistentModelIndexData *> persistent_moved_explicitly;
    QVector<QPersistentModelIndexData *> persistent_moved_in_source;
    QVector<QPersistentModelIndexData *> persistent_moved_in_destination;
    QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it;
    const QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator begin = persistent.indexes.constBegin();
    const QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator end = persistent.indexes.constEnd();
    const bool sameParent = (srcParent == destinationParent);
    const bool movingUp = (srcFirst > destinationChild);
    for ( it = begin; it != end; ++it) {
        QPersistentModelIndexData *data = *it;
        const QModelIndex &index = data->index;
        const QModelIndex &parent = index.parent();
        const bool isSourceIndex = (parent == srcParent);
        const bool isDestinationIndex = (parent == destinationParent);
        int childPosition;
        if (orientation == Qt::Vertical)
            childPosition = index.row();
        else
            childPosition = index.column();
        if (!index.isValid() || !(isSourceIndex || isDestinationIndex ) )
            continue;
        if (!sameParent && isDestinationIndex) {
            if (childPosition >= destinationChild)
                persistent_moved_in_destination.append(data);
            continue;
        }
        if (sameParent && movingUp && childPosition < destinationChild)
            continue;
        if (sameParent && !movingUp && childPosition < srcFirst )
            continue;
        if (!sameParent && childPosition < srcFirst)
            continue;
        if (sameParent && (childPosition > srcLast) && (childPosition >= destinationChild ))
            continue;
        if ((childPosition <= srcLast) && (childPosition >= srcFirst)) {
            persistent_moved_explicitly.append(data);
        } else {
            persistent_moved_in_source.append(data);
        }
    }
    persistent.moved.push(persistent_moved_explicitly);
    persistent.moved.push(persistent_moved_in_source);
    persistent.moved.push(persistent_moved_in_destination);
}
void QAbstractItemModelPrivate::movePersistentIndexes(QVector<QPersistentModelIndexData *> indexes, int change, const QModelIndex &parent, Qt::Orientation orientation)
{
    QVector<QPersistentModelIndexData *>::const_iterator it;
    const QVector<QPersistentModelIndexData *>::const_iterator begin = indexes.constBegin();
    const QVector<QPersistentModelIndexData *>::const_iterator end = indexes.constEnd();
    for (it = begin; it != end; ++it)
    {
        QPersistentModelIndexData *data = *it;
        int row = data->index.row();
        int column = data->index.column();
        if (Qt::Vertical == orientation)
            row += change;
        else
            column += change;
        persistent.indexes.erase(persistent.indexes.find(data->index));
        data->index = q_func()->index(row, column, parent);
        if (data->index.isValid()) {
            persistent.insertMultiAtEnd(data->index, data);
        } else {
            qWarning() << "QAbstractItemModel::endMoveRows:  Invalid index (" << row << "," << column << ") in model" << q_func();
        }
    }
}
void QAbstractItemModelPrivate::itemsMoved(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild, Qt::Orientation orientation)
{
    QVector<QPersistentModelIndexData *> moved_in_destination = persistent.moved.pop();
    QVector<QPersistentModelIndexData *> moved_in_source = persistent.moved.pop();
    QVector<QPersistentModelIndexData *> moved_explicitly = persistent.moved.pop();
    const bool sameParent = (sourceParent == destinationParent);
    const bool movingUp = (sourceFirst > destinationChild);
    const int explicit_change = (!sameParent || movingUp) ? destinationChild - sourceFirst : destinationChild - sourceLast - 1 ;
    const int source_change = (!sameParent || !movingUp) ? -1*(sourceLast - sourceFirst + 1) : sourceLast - sourceFirst + 1 ;
    const int destination_change = sourceLast - sourceFirst + 1;
    movePersistentIndexes(moved_explicitly, explicit_change, destinationParent, orientation);
    movePersistentIndexes(moved_in_source, source_change, sourceParent, orientation);
    movePersistentIndexes(moved_in_destination, destination_change, destinationParent, orientation);
}
void QAbstractItemModelPrivate::rowsAboutToBeRemoved(const QModelIndex &parent,
                                                     int first, int last)
{
    QVector<QPersistentModelIndexData *>  persistent_moved;
    QVector<QPersistentModelIndexData *>  persistent_invalidated;
    // find the persistent indexes that are affected by the change, either by being in the removed subtree
    // or by being on the same level and below the removed rows
    for (QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it = persistent.indexes.constBegin();
         it != persistent.indexes.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        bool level_changed = false;
        QModelIndex current = data->index;
        while (current.isValid()) {
            QModelIndex current_parent = current.parent();
            if (current_parent == parent) { // on the same level as the change
                if (!level_changed && current.row() > last) // below the removed rows
                    persistent_moved.append(data);
                else if (current.row() <= last && current.row() >= first) // in the removed subtree
                    persistent_invalidated.append(data);
                break;
            }
            current = current_parent;
            level_changed = true;
        }
    }
    persistent.moved.push(persistent_moved);
    persistent.invalidated.push(persistent_invalidated);
}
void QAbstractItemModelPrivate::rowsRemoved(const QModelIndex &parent,
                                            int first, int last)
{
    QVector<QPersistentModelIndexData *> persistent_moved = persistent.moved.pop();
    int count = (last - first) + 1; // it is important to only use the delta, because the change could be nested
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_moved.constBegin();
         it != persistent_moved.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        QModelIndex old = data->index;
        persistent.indexes.erase(persistent.indexes.find(old));
        data->index = q_func()->index(old.row() - count, old.column(), parent);
        if (data->index.isValid()) {
            persistent.insertMultiAtEnd(data->index, data);
        } else {
            qWarning() << "QAbstractItemModel::endRemoveRows:  Invalid index (" << old.row() - count << ',' << old.column() << ") in model" << q_func();
        }
    }
    QVector<QPersistentModelIndexData *> persistent_invalidated = persistent.invalidated.pop();
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_invalidated.constBegin();
         it != persistent_invalidated.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        persistent.indexes.erase(persistent.indexes.find(data->index));
        data->index = QModelIndex();
        data->model = 0;
    }
}
void QAbstractItemModelPrivate::columnsAboutToBeInserted(const QModelIndex &parent,
                                                         int first, int last)
{
    Q_Q(QAbstractItemModel);
    Q_UNUSED(last);
    QVector<QPersistentModelIndexData *> persistent_moved;
    if (first < q->columnCount(parent)) {
        for (QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it = persistent.indexes.constBegin();
             it != persistent.indexes.constEnd(); ++it) {
            QPersistentModelIndexData *data = *it;
            const QModelIndex &index = data->index;
            if (index.column() >= first && index.isValid() && index.parent() == parent)
                persistent_moved.append(data);
        }
    }
    persistent.moved.push(persistent_moved);
}
void QAbstractItemModelPrivate::columnsInserted(const QModelIndex &parent,
                                                int first, int last)
{
    QVector<QPersistentModelIndexData *> persistent_moved = persistent.moved.pop();
    int count = (last - first) + 1; // it is important to only use the delta, because the change could be nested
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_moved.constBegin();
         it != persistent_moved.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        QModelIndex old = data->index;
        persistent.indexes.erase(persistent.indexes.find(old));
        data->index = q_func()->index(old.row(), old.column() + count, parent);
        if (data->index.isValid()) {
            persistent.insertMultiAtEnd(data->index, data);
        } else {
            qWarning() << "QAbstractItemModel::endInsertColumns:  Invalid index (" << old.row() << ',' << old.column() + count << ") in model" << q_func();
        }
     }
}
void QAbstractItemModelPrivate::columnsAboutToBeRemoved(const QModelIndex &parent,
                                                        int first, int last)
{
    QVector<QPersistentModelIndexData *> persistent_moved;
    QVector<QPersistentModelIndexData *> persistent_invalidated;
    // find the persistent indexes that are affected by the change, either by being in the removed subtree
    // or by being on the same level and to the right of the removed columns
    for (QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it = persistent.indexes.constBegin();
         it != persistent.indexes.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        bool level_changed = false;
        QModelIndex current = data->index;
        while (current.isValid()) {
            QModelIndex current_parent = current.parent();
            if (current_parent == parent) { // on the same level as the change
                if (!level_changed && current.column() > last) // right of the removed columns
                    persistent_moved.append(data);
                else if (current.column() <= last && current.column() >= first) // in the removed subtree
                    persistent_invalidated.append(data);
                break;
            }
            current = current_parent;
            level_changed = true;
        }
    }
    persistent.moved.push(persistent_moved);
    persistent.invalidated.push(persistent_invalidated);
}
void QAbstractItemModelPrivate::columnsRemoved(const QModelIndex &parent,
                                               int first, int last)
{
    QVector<QPersistentModelIndexData *> persistent_moved = persistent.moved.pop();
    int count = (last - first) + 1; // it is important to only use the delta, because the change could be nested
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_moved.constBegin();
         it != persistent_moved.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        QModelIndex old = data->index;
        persistent.indexes.erase(persistent.indexes.find(old));
        data->index = q_func()->index(old.row(), old.column() - count, parent);
        if (data->index.isValid()) {
            persistent.insertMultiAtEnd(data->index, data);
        } else {
            qWarning() << "QAbstractItemModel::endRemoveColumns:  Invalid index (" << old.row() << ',' << old.column() - count << ") in model" << q_func();
        }
    }
    QVector<QPersistentModelIndexData *> persistent_invalidated = persistent.invalidated.pop();
    for (QVector<QPersistentModelIndexData *>::const_iterator it = persistent_invalidated.constBegin();
         it != persistent_invalidated.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        persistent.indexes.erase(persistent.indexes.find(data->index));
        data->index = QModelIndex();
        data->model = 0;
    }
}
void QAbstractItemModel::resetInternalData()
{
}
QAbstractItemModel::QAbstractItemModel(QObject *parent)
    : QObject(*new QAbstractItemModelPrivate, parent)
{
}
QAbstractItemModel::QAbstractItemModel(QAbstractItemModelPrivate &dd, QObject *parent)
    : QObject(dd, parent)
{
}
QAbstractItemModel::~QAbstractItemModel()
{
    d_func()->invalidatePersistentIndexes();
}
bool QAbstractItemModel::hasIndex(int row, int column, const QModelIndex &parent) const
{
    if (row < 0 || column < 0)
        return false;
    return row < rowCount(parent) && column < columnCount(parent);
}
bool QAbstractItemModel::hasChildren(const QModelIndex &parent) const
{
    return (rowCount(parent) > 0) && (columnCount(parent) > 0);
}
QMap<int, QVariant> QAbstractItemModel::itemData(const QModelIndex &index) const
{
    QMap<int, QVariant> roles;
    for (int i = 0; i < Qt::UserRole; ++i) {
        QVariant variantData = data(index, i);
        if (variantData.isValid())
            roles.insert(i, variantData);
    }
    return roles;
}
bool QAbstractItemModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    Q_UNUSED(index);
    Q_UNUSED(value);
    Q_UNUSED(role);
    return false;
}
bool QAbstractItemModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)
{
    bool b = true;
    for (QMap<int, QVariant>::ConstIterator it = roles.begin(); it != roles.end(); ++it)
        b = b && setData(index, it.value(), it.key());
    return b;
}
QStringList QAbstractItemModel::mimeTypes() const
{
    QStringList types;
    types << QLatin1String("application/x-qabstractitemmodeldatalist");
    return types;
}
QMimeData *QAbstractItemModel::mimeData(const QModelIndexList &indexes) const
{
    if (indexes.count() <= 0)
        return 0;
    QStringList types = mimeTypes();
    if (types.isEmpty())
        return 0;
    QMimeData *data = new QMimeData();
    QString format = types.at(0);
    QByteArray encoded;
    QDataStream stream(&encoded, QIODevice::WriteOnly);
    encodeData(indexes, stream);
    data->setData(format, encoded);
    return data;
}
bool QAbstractItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action,
                                      int row, int column, const QModelIndex &parent)
{
    // check if the action is supported
    if (!data || !(action == Qt::CopyAction || action == Qt::MoveAction))
        return false;
    // check if the format is supported
    QStringList types = mimeTypes();
    if (types.isEmpty())
        return false;
    QString format = types.at(0);
    if (!data->hasFormat(format))
        return false;
    if (row > rowCount(parent))
        row = rowCount(parent);
    if (row == -1)
        row = rowCount(parent);
    if (column == -1)
        column = 0;
    // decode and insert
    QByteArray encoded = data->data(format);
    QDataStream stream(&encoded, QIODevice::ReadOnly);
    return decodeData(row, column, parent, stream);
}
Qt::DropActions QAbstractItemModel::supportedDropActions() const
{
    return Qt::CopyAction;
}
Qt::DropActions QAbstractItemModel::supportedDragActions() const
{
    // ### Qt 5: make this virtual or these properties
    Q_D(const QAbstractItemModel);
    if (d->supportedDragActions != -1)
        return d->supportedDragActions;
    return supportedDropActions();
}
void QAbstractItemModel::setSupportedDragActions(Qt::DropActions actions)
{
    Q_D(QAbstractItemModel);
    d->supportedDragActions = actions;
}
bool QAbstractItemModel::insertRows(int, int, const QModelIndex &)
{
    return false;
}
bool QAbstractItemModel::insertColumns(int, int, const QModelIndex &)
{
    return false;
}
bool QAbstractItemModel::removeRows(int, int, const QModelIndex &)
{
    return false;
}
bool QAbstractItemModel::removeColumns(int, int, const QModelIndex &)
{
    return false;
}
void QAbstractItemModel::fetchMore(const QModelIndex &)
{
    // do nothing
}
bool QAbstractItemModel::canFetchMore(const QModelIndex &) const
{
    return false;
}
Qt::ItemFlags QAbstractItemModel::flags(const QModelIndex &index) const
{
    Q_D(const QAbstractItemModel);
    if (!d->indexValid(index))
        return 0;
    return Qt::ItemIsSelectable|Qt::ItemIsEnabled;
}
void QAbstractItemModel::sort(int column, Qt::SortOrder order)
{
    Q_UNUSED(column);
    Q_UNUSED(order);
    // do nothing
}
QModelIndex QAbstractItemModel::buddy(const QModelIndex &index) const
{
    return index;
}
QModelIndexList QAbstractItemModel::match(const QModelIndex &start, int role,
                                          const QVariant &value, int hits,
                                          Qt::MatchFlags flags) const
{
    QModelIndexList result;
    uint matchType = flags & 0x0F;
    Qt::CaseSensitivity cs = flags & Qt::MatchCaseSensitive ? Qt::CaseSensitive : Qt::CaseInsensitive;
    bool recurse = flags & Qt::MatchRecursive;
    bool wrap = flags & Qt::MatchWrap;
    bool allHits = (hits == -1);
    QString text; // only convert to a string if it is needed
    QModelIndex p = parent(start);
    int from = start.row();
    int to = rowCount(p);
    // iterates twice if wrapping
    for (int i = 0; (wrap && i < 2) || (!wrap && i < 1); ++i) {
        for (int r = from; (r < to) && (allHits || result.count() < hits); ++r) {
            QModelIndex idx = index(r, start.column(), p);
            if (!idx.isValid())
                 continue;
            QVariant v = data(idx, role);
            // QVariant based matching
            if (matchType == Qt::MatchExactly) {
                if (value == v)
                    result.append(idx);
            } else { // QString based matching
                if (text.isEmpty()) // lazy conversion
                    text = value.toString();
                QString t = v.toString();
                switch (matchType) {
                case Qt::MatchRegExp:
                    if (QRegExp(text, cs).exactMatch(t))
                        result.append(idx);
                    break;
                case Qt::MatchWildcard:
                    if (QRegExp(text, cs, QRegExp::Wildcard).exactMatch(t))
                        result.append(idx);
                    break;
                case Qt::MatchStartsWith:
                    if (t.startsWith(text, cs))
                        result.append(idx);
                    break;
                case Qt::MatchEndsWith:
                    if (t.endsWith(text, cs))
                        result.append(idx);
                    break;
                case Qt::MatchFixedString:
                    if (t.compare(text, cs) == 0)
                        result.append(idx);
                    break;
                case Qt::MatchContains:
                default:
                    if (t.contains(text, cs))
                        result.append(idx);
                }
            }
            if (recurse && hasChildren(idx)) { // search the hierarchy
                result += match(index(0, idx.column(), idx), role,
                                (text.isEmpty() ? value : text),
                                (allHits ? -1 : hits - result.count()), flags);
            }
        }
        // prepare for the next iteration
        from = 0;
        to = start.row();
    }
    return result;
}
QSize QAbstractItemModel::span(const QModelIndex &) const
{
    return QSize(1, 1);
}
void QAbstractItemModel::setRoleNames(const QHash<int,QByteArray> &roleNames)
{
    Q_D(QAbstractItemModel);
    d->roleNames = roleNames;
}
const QHash<int,QByteArray> &QAbstractItemModel::roleNames() const
{
    Q_D(const QAbstractItemModel);
    return d->roleNames;
}
bool QAbstractItemModel::submit()
{
    return true;
}
void QAbstractItemModel::revert()
{
    // do nothing
}
QVariant QAbstractItemModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    Q_UNUSED(orientation);
    if (role == Qt::DisplayRole)
        return section + 1;
    return QVariant();
}
bool QAbstractItemModel::setHeaderData(int section, Qt::Orientation orientation,
                                       const QVariant &value, int role)
{
    Q_UNUSED(section);
    Q_UNUSED(orientation);
    Q_UNUSED(value);
    Q_UNUSED(role);
    return false;
}
void QAbstractItemModel::encodeData(const QModelIndexList &indexes, QDataStream &stream) const
{
    QModelIndexList::ConstIterator it = indexes.begin();
    for (; it != indexes.end(); ++it)
        stream << (*it).row() << (*it).column() << itemData(*it);
}
bool QAbstractItemModel::decodeData(int row, int column, const QModelIndex &parent,
                                    QDataStream &stream)
{
    int top = INT_MAX;
    int left = INT_MAX;
    int bottom = 0;
    int right = 0;
    QVector<int> rows, columns;
    QVector<QMap<int, QVariant> > data;
    while (!stream.atEnd()) {
        int r, c;
        QMap<int, QVariant> v;
        stream >> r >> c >> v;
        rows.append(r);
        columns.append(c);
        data.append(v);
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
    if (colCount == 0) {
        insertColumns(colCount, dragColumnCount - colCount, parent);
        colCount = columnCount(parent);
    }
    insertRows(row, dragRowCount, parent);
    row = qMax(0, row);
    column = qMax(0, column);
    QVector<QPersistentModelIndex> newIndexes(data.size());
    // set the data in the table
    for (int j = 0; j < data.size(); ++j) {
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
            newIndexes[j] = index(destinationRow, destinationColumn, parent);
            isWrittenTo.setBit(flat);
        }
    }
    for(int k = 0; k < newIndexes.size(); k++) {
        if (newIndexes.at(k).isValid())
            setItemData(newIndexes.at(k), data.at(k));
    }
    return true;
}
void QAbstractItemModel::beginInsertRows(const QModelIndex &parent, int first, int last)
{
    Q_ASSERT(first >= 0);
    Q_ASSERT(last >= first);
    Q_D(QAbstractItemModel);
    d->changes.push(QAbstractItemModelPrivate::Change(parent, first, last));
    emit rowsAboutToBeInserted(parent, first, last);
    d->rowsAboutToBeInserted(parent, first, last);
}
void QAbstractItemModel::endInsertRows()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change change = d->changes.pop();
    d->rowsInserted(change.parent, change.first, change.last);
    emit rowsInserted(change.parent, change.first, change.last);
}
void QAbstractItemModel::beginRemoveRows(const QModelIndex &parent, int first, int last)
{
    Q_ASSERT(first >= 0);
    Q_ASSERT(last >= first);
    Q_D(QAbstractItemModel);
    d->changes.push(QAbstractItemModelPrivate::Change(parent, first, last));
    emit rowsAboutToBeRemoved(parent, first, last);
    d->rowsAboutToBeRemoved(parent, first, last);
}
void QAbstractItemModel::endRemoveRows()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change change = d->changes.pop();
    d->rowsRemoved(change.parent, change.first, change.last);
    emit rowsRemoved(change.parent, change.first, change.last);
}
bool QAbstractItemModelPrivate::allowMove(const QModelIndex &srcParent, int start, int end, const QModelIndex &destinationParent, int destinationStart, Qt::Orientation orientation)
{
    // Don't move the range within itself.
    if (destinationParent == srcParent)
        return !(destinationStart >= start && destinationStart <= end + 1);
    QModelIndex destinationAncestor = destinationParent;
    int pos = (Qt::Vertical == orientation) ? destinationAncestor.row() : destinationAncestor.column();
    forever {
        if (destinationAncestor == srcParent) {
            if (pos >= start && pos <= end)
                return false;
            break;
        }
        if (!destinationAncestor.isValid())
          break;
        pos = (Qt::Vertical == orientation) ? destinationAncestor.row() : destinationAncestor.column();
        destinationAncestor = destinationAncestor.parent();
    }
    return true;
}
bool QAbstractItemModel::beginMoveRows(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)
{
    Q_ASSERT(sourceFirst >= 0);
    Q_ASSERT(sourceLast >= sourceFirst);
    Q_ASSERT(destinationChild >= 0);
    Q_D(QAbstractItemModel);
    if (!d->allowMove(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild, Qt::Vertical)) {
        return false;
    }
    QAbstractItemModelPrivate::Change sourceChange(sourceParent, sourceFirst, sourceLast);
    sourceChange.needsAdjust = sourceParent.isValid() && sourceParent.row() >= destinationChild && sourceParent.parent() == destinationParent;
    d->changes.push(sourceChange);
    int destinationLast = destinationChild + (sourceLast - sourceFirst);
    QAbstractItemModelPrivate::Change destinationChange(destinationParent, destinationChild, destinationLast);
    destinationChange.needsAdjust = destinationParent.isValid() && destinationParent.row() >= sourceLast && destinationParent.parent() == sourceParent;
    d->changes.push(destinationChange);
    emit rowsAboutToBeMoved(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild);
    emit layoutAboutToBeChanged();
    d->itemsAboutToBeMoved(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild, Qt::Vertical);
    return true;
}
void QAbstractItemModel::endMoveRows()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change insertChange = d->changes.pop();
    QAbstractItemModelPrivate::Change removeChange = d->changes.pop();
    QModelIndex adjustedSource = removeChange.parent;
    QModelIndex adjustedDestination = insertChange.parent;
    const int numMoved = removeChange.last - removeChange.first + 1;
    if (insertChange.needsAdjust)
      adjustedDestination = createIndex(adjustedDestination.row() - numMoved, adjustedDestination.column(), adjustedDestination.internalPointer());
    if (removeChange.needsAdjust)
      adjustedSource = createIndex(adjustedSource.row() + numMoved, adjustedSource.column(), adjustedSource.internalPointer());
    d->itemsMoved(adjustedSource, removeChange.first, removeChange.last, adjustedDestination, insertChange.first, Qt::Vertical);
    emit rowsMoved(adjustedSource, removeChange.first, removeChange.last, adjustedDestination, insertChange.first);
    emit layoutChanged();
}
void QAbstractItemModel::beginInsertColumns(const QModelIndex &parent, int first, int last)
{
    Q_ASSERT(first >= 0);
    Q_ASSERT(last >= first);
    Q_D(QAbstractItemModel);
    d->changes.push(QAbstractItemModelPrivate::Change(parent, first, last));
    emit columnsAboutToBeInserted(parent, first, last);
    d->columnsAboutToBeInserted(parent, first, last);
}
void QAbstractItemModel::endInsertColumns()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change change = d->changes.pop();
    d->columnsInserted(change.parent, change.first, change.last);
    emit columnsInserted(change.parent, change.first, change.last);
}
void QAbstractItemModel::beginRemoveColumns(const QModelIndex &parent, int first, int last)
{
    Q_ASSERT(first >= 0);
    Q_ASSERT(last >= first);
    Q_D(QAbstractItemModel);
    d->changes.push(QAbstractItemModelPrivate::Change(parent, first, last));
    emit columnsAboutToBeRemoved(parent, first, last);
    d->columnsAboutToBeRemoved(parent, first, last);
}
void QAbstractItemModel::endRemoveColumns()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change change = d->changes.pop();
    d->columnsRemoved(change.parent, change.first, change.last);
    emit columnsRemoved(change.parent, change.first, change.last);
}
bool QAbstractItemModel::beginMoveColumns(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)
{
    Q_ASSERT(sourceFirst >= 0);
    Q_ASSERT(sourceLast >= sourceFirst);
    Q_ASSERT(destinationChild >= 0);
    Q_D(QAbstractItemModel);
    if (!d->allowMove(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild, Qt::Horizontal)) {
        return false;
    }
    QAbstractItemModelPrivate::Change sourceChange(sourceParent, sourceFirst, sourceLast);
    sourceChange.needsAdjust = sourceParent.isValid() && sourceParent.row() >= destinationChild && sourceParent.parent() == destinationParent;
    d->changes.push(sourceChange);
    int destinationLast = destinationChild + (sourceLast - sourceFirst);
    QAbstractItemModelPrivate::Change destinationChange(destinationParent, destinationChild, destinationLast);
    destinationChange.needsAdjust = destinationParent.isValid() && destinationParent.row() >= sourceLast && destinationParent.parent() == sourceParent;
    d->changes.push(destinationChange);
    d->itemsAboutToBeMoved(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild, Qt::Horizontal);
    emit columnsAboutToBeMoved(sourceParent, sourceFirst, sourceLast, destinationParent, destinationChild);
    emit layoutAboutToBeChanged();
    return true;
}
void QAbstractItemModel::endMoveColumns()
{
    Q_D(QAbstractItemModel);
    QAbstractItemModelPrivate::Change insertChange = d->changes.pop();
    QAbstractItemModelPrivate::Change removeChange = d->changes.pop();
    QModelIndex adjustedSource = removeChange.parent;
    QModelIndex adjustedDestination = insertChange.parent;
    const int numMoved = removeChange.last - removeChange.first + 1;
    if (insertChange.needsAdjust)
      adjustedDestination = createIndex(adjustedDestination.row(), adjustedDestination.column() - numMoved, adjustedDestination.internalPointer());
    if (removeChange.needsAdjust)
      adjustedSource = createIndex(adjustedSource.row(), adjustedSource.column() + numMoved, adjustedSource.internalPointer());
    d->itemsMoved(adjustedSource, removeChange.first, removeChange.last, adjustedDestination, insertChange.first, Qt::Horizontal);
    emit columnsMoved(adjustedSource, removeChange.first, removeChange.last, adjustedDestination, insertChange.first);
    emit layoutChanged();
}
void QAbstractItemModel::reset()
{
    Q_D(QAbstractItemModel);
    emit modelAboutToBeReset();
    d->invalidatePersistentIndexes();
    QMetaObject::invokeMethod(this, "resetInternalData");
    emit modelReset();
}
void QAbstractItemModel::beginResetModel()
{
    emit modelAboutToBeReset();
}
void QAbstractItemModel::endResetModel()
{
    Q_D(QAbstractItemModel);
    d->invalidatePersistentIndexes();
    QMetaObject::invokeMethod(this, "resetInternalData");
    emit modelReset();
}
void QAbstractItemModel::changePersistentIndex(const QModelIndex &from, const QModelIndex &to)
{
    Q_D(QAbstractItemModel);
    if (d->persistent.indexes.isEmpty())
        return;
    // find the data and reinsert it sorted
    const QHash<QModelIndex, QPersistentModelIndexData *>::iterator it = d->persistent.indexes.find(from);
    if (it != d->persistent.indexes.end()) {
        QPersistentModelIndexData *data = *it;
        d->persistent.indexes.erase(it);
        data->index = to;
        if (to.isValid())
            d->persistent.insertMultiAtEnd(to, data);
        else
            data->model = 0;
    }
}
void QAbstractItemModel::changePersistentIndexList(const QModelIndexList &from,
                                                   const QModelIndexList &to)
{
    Q_D(QAbstractItemModel);
    if (d->persistent.indexes.isEmpty())
        return;
    QVector<QPersistentModelIndexData *> toBeReinserted;
    toBeReinserted.reserve(to.count());
    for (int i = 0; i < from.count(); ++i) {
        if (from.at(i) == to.at(i))
            continue;
        const QHash<QModelIndex, QPersistentModelIndexData *>::iterator it = d->persistent.indexes.find(from.at(i));
        if (it != d->persistent.indexes.end()) {
            QPersistentModelIndexData *data = *it;
            d->persistent.indexes.erase(it);
            data->index = to.at(i);
            if (data->index.isValid())
                toBeReinserted << data;
            else
                data->model = 0;
        }
    }
    for (QVector<QPersistentModelIndexData *>::const_iterator it = toBeReinserted.constBegin();
         it != toBeReinserted.constEnd() ; ++it) {
        QPersistentModelIndexData *data = *it;
        d->persistent.insertMultiAtEnd(data->index, data);
    }
}
QModelIndexList QAbstractItemModel::persistentIndexList() const
{
    Q_D(const QAbstractItemModel);
    QModelIndexList result;
    for (QHash<QModelIndex, QPersistentModelIndexData *>::const_iterator it = d->persistent.indexes.constBegin();
         it != d->persistent.indexes.constEnd(); ++it) {
        QPersistentModelIndexData *data = *it;
        result.append(data->index);
    }
    return result;
}
QAbstractTableModel::QAbstractTableModel(QObject *parent)
    : QAbstractItemModel(parent)
{
}
QAbstractTableModel::QAbstractTableModel(QAbstractItemModelPrivate &dd, QObject *parent)
    : QAbstractItemModel(dd, parent)
{
}
QAbstractTableModel::~QAbstractTableModel()
{
}
QModelIndex QAbstractTableModel::index(int row, int column, const QModelIndex &parent) const
{
    return hasIndex(row, column, parent) ? createIndex(row, column, 0) : QModelIndex();
}
QModelIndex QAbstractTableModel::parent(const QModelIndex &) const
{
    return QModelIndex();
}
bool QAbstractTableModel::hasChildren(const QModelIndex &parent) const
{
    if (parent.model() == this || !parent.isValid())
        return rowCount(parent) > 0 && columnCount(parent) > 0;
    return false;
}
QAbstractListModel::QAbstractListModel(QObject *parent)
    : QAbstractItemModel(parent)
{
}
QAbstractListModel::QAbstractListModel(QAbstractItemModelPrivate &dd, QObject *parent)
    : QAbstractItemModel(dd, parent)
{
}
QAbstractListModel::~QAbstractListModel()
{
}
QModelIndex QAbstractListModel::index(int row, int column, const QModelIndex &parent) const
{
    return hasIndex(row, column, parent) ? createIndex(row, column, 0) : QModelIndex();
}
QModelIndex QAbstractListModel::parent(const QModelIndex &  ) const
{
    return QModelIndex();
}
int QAbstractListModel::columnCount(const QModelIndex &parent) const
{
    return parent.isValid() ? 0 : 1;
}
bool QAbstractListModel::hasChildren(const QModelIndex &parent) const
{
    return parent.isValid() ? false : (rowCount() > 0);
}
bool QAbstractTableModel::dropMimeData(const QMimeData *data, Qt::DropAction action,
                                       int row, int column, const QModelIndex &parent)
{
    if (!data || !(action == Qt::CopyAction || action == Qt::MoveAction))
        return false;
    QStringList types = mimeTypes();
    if (types.isEmpty())
        return false;
    QString format = types.at(0);
    if (!data->hasFormat(format))
        return false;
    QByteArray encoded = data->data(format);
    QDataStream stream(&encoded, QIODevice::ReadOnly);
    // if the drop is on an item, replace the data in the items
    if (parent.isValid() && row == -1 && column == -1) {
        int top = INT_MAX;
        int left = INT_MAX;
        QVector<int> rows, columns;
        QVector<QMap<int, QVariant> > data;
        while (!stream.atEnd()) {
            int r, c;
            QMap<int, QVariant> v;
            stream >> r >> c >> v;
            rows.append(r);
            columns.append(c);
            data.append(v);
            top = qMin(r, top);
            left = qMin(c, left);
        }
        for (int i = 0; i < data.size(); ++i) {
            int r = (rows.at(i) - top) + parent.row();
            int c = (columns.at(i) - left) + parent.column();
            if (hasIndex(r, c))
                setItemData(index(r, c), data.at(i));
        }
        return true;
    }
    // otherwise insert new rows for the data
    return decodeData(row, column, parent, stream);
}
bool QAbstractListModel::dropMimeData(const QMimeData *data, Qt::DropAction action,
                                      int row, int column, const QModelIndex &parent)
{
    if (!data || !(action == Qt::CopyAction || action == Qt::MoveAction))
        return false;
    QStringList types = mimeTypes();
    if (types.isEmpty())
        return false;
    QString format = types.at(0);
    if (!data->hasFormat(format))
        return false;
    QByteArray encoded = data->data(format);
    QDataStream stream(&encoded, QIODevice::ReadOnly);
    // if the drop is on an item, replace the data in the items
    if (parent.isValid() && row == -1 && column == -1) {
        int top = INT_MAX;
        int left = INT_MAX;
        QVector<int> rows, columns;
        QVector<QMap<int, QVariant> > data;
        while (!stream.atEnd()) {
            int r, c;
            QMap<int, QVariant> v;
            stream >> r >> c >> v;
            rows.append(r);
            columns.append(c);
            data.append(v);
            top = qMin(r, top);
            left = qMin(c, left);
        }
        for (int i = 0; i < data.size(); ++i) {
            int r = (rows.at(i) - top) + parent.row();
            if (columns.at(i) == left && hasIndex(r, 0))
                setItemData(index(r), data.at(i));
        }
        return true;
    }
    if (row == -1)
        row = rowCount(parent);
    // otherwise insert new rows for the data
    return decodeData(row, column, parent, stream);
}
void QAbstractItemModelPrivate::Persistent::insertMultiAtEnd(const QModelIndex& key, QPersistentModelIndexData *data)
{
    QHash<QModelIndex,QPersistentModelIndexData *>::iterator newIt =
            indexes.insertMulti(key, data);
    QHash<QModelIndex,QPersistentModelIndexData *>::iterator it = newIt + 1;
    while (it != indexes.end() && it.key() == key) {
        qSwap(*newIt,*it);
        newIt = it;
        ++it;
    }
}
QT_END_NAMESPACE