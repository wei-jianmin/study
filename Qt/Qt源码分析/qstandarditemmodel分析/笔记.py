��QStandardItemModelPrivate.hpp�����Է�������Ҫ���ݳ�Ա��
    QVector<QStandardItem*> columnHeaderItems;
    QVector<QStandardItem*> rowHeaderItems;
    QScopedPointer<QStandardItem> root;

��QStandardItemPrivate.hpp�����Է�������Ҫ���ݳ�Ա��   
    QStandardItemModel *model;          //��¼�������Ǹ�ģ����    
    QStandardItem *parent;              //��¼��QStandardItem*
    QVector<QWidgetItemData> values;    //��Ÿ��ֽ�ɫ��Ϣ����ͼ�ꡢ�ı������塢ǰ��ɫ�ȵ�
    QVector<QStandardItem*> children;   //�������δ�Ÿ�����Ԫ�أ���ζ��һ��QStandardItem�п��Դ��һ����QStandardItem��
    int rows;                           //��¼�ӱ��ж�����
    int columns;                        //��¼�ӱ��ж�����
    QStandardItem *q_ptr;               //ָ��QStandardItem
    int lastIndexOf;                    //��¼�ϴβ��ҵ���QStandardItem*��λ��

Ҳ����˵ QStandardItem �������ͨ��QVector��ά��һ���� QStandardItem* ���

���� QStandardItemModel �е����ݳ�Ա root ���ڲ�ά��һ���� QStandardItem* ���
������QStandardItem*��Ԫ�ص�parentָ��root����Ԫ�ص�modelָ��QStandardItemModel