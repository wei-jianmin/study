class QStandardItemModelLessThan
{
public:
    inline QStandardItemModelLessThan()
        { }

    inline bool operator()(const QPair<QStandardItem*, int> &l,
                           const QPair<QStandardItem*, int> &r) const
    {
        return *(l.first) < *(r.first);
    }
};