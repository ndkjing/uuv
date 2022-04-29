import sys
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QHBoxLayout, \
    QListWidgetItem
from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtCore import Qt, QSize, QByteArray, QDataStream, QIODevice, QMimeData, QPoint


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 必须有(当然，图标模式的列表控件已默认打开）

    # 拖动时依次调用

    # dragEnterEvent不是必需的
    # dragMoveEvent也不是必需的，没它的副作用是拖动图标有个禁止的小标志
    # dragMoveEvent会在拖动的过程中频繁调用，计算量大的代码不宜放在此处

    def dragEnterEvent(self, event):  # 拖动开始时，以及刚进入目标控件时调用
        print("进入%s" % self.objectName())
        if event.mimeData().hasFormat('application/x-阿猫'):
            '''
            if event.keyboardModifiers() & Qt.ControlModifier:#按住ctrol键则拖动复制
                self.dragOption = Qt.CopyAction  #Qt.CopyAction 复制
            else:
                self.dragOption = Qt.MoveAction # Qt.MoveAction 移动
            '''
            event.accept()
        else:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()  # 返回一个ulr路径列表
                print(urls)
            # 以上三行只是为了演示，若拖动文件到程序，如何获取文件的全路径
            event.ignore()

    def dragMoveEvent(self, event):
        print("在%s中开始移动" % self.objectName())
        if event.mimeData().hasFormat('application/x-阿猫'):

            event.accept()
        else:
            event.ignore()

    def startDrag(self):  # self是源控件
        item = self.currentItem()
        if item is None:  # 没有选中可拖动项
            return
        print("在%s中开始拖动" % self.objectName())
        icon = item.icon()
        # 这里可以创建自定义数据可供在拖动事件中使用
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())  # Pyqt5 中向数据流写入字符串
        stream << icon  # 向数据流写入图标数据
        mimeData = QMimeData()
        mimeData.setData('application/x-阿猫', data)  # 自定义数据的格式名'application/x-阿猫
        # 当然，此例中可使用列表控件项目的默认格式名'application/x-qabstractitemmodeldatalist'

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        width, height = 100, 100
        pixmap = icon.pixmap(width, height)  # 拖动过程中的图标尺寸
        drag.setHotSpot(QPoint(width // 2, height // 2))  # 设置拖动过程中鼠标在图标中的位置
        drag.setPixmap(pixmap)
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:  # Qt.CopyAction 复制# Qt.MoveAction 移动
            index = self.row(item)  # 返回拖动项在源列表控件的索引
            print("在拖动源控件中的索引是%d" % index)
            self.takeItem(index)

    def dropEvent(self, event):
        print("目标控件是%s" % self.objectName())
        # print(event.mimeData() .formats())
        if event.mimeData().hasFormat('application/x-阿猫'):
            data = event.mimeData().data('application/x-阿猫')
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = str()
            icon = QIcon()
            text = stream.readQString()  # 读出数据流中的字符串
            stream >> icon  # 读出数据流中的图标数据
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            # print(event.source())
            event.accept()
        else:
            event.ignore()

    # 确保startDrag被调用的最简单的方法就是对mouseMoveEvent()重新实现
    def mouseMoveEvent(self, event):
        print("mouseMoveEvent")
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义拖放事件")
        listWidget = MyListWidget()  # 使用自定义列表组件
        listWidget.setObjectName("普通列表控件")
        iconList = ["英短", "布偶", "折耳", "波斯", "缅因", "森林"]
        for i in iconList:
            listWidget.addItem(QListWidgetItem(QIcon(i + ".jpg"), i))
        iconListWidget = MyListWidget()  # 使用自定义列表组件
        iconListWidget.setObjectName("图标列表控件")
        iconListWidget.setViewMode(QListWidget.IconMode)  # 设置为图标模式
        iconListWidget.setIconSize(QSize(300, 300))  # 可设置图标大小
        layout = QHBoxLayout()
        layout.addWidget(listWidget)
        layout.addWidget(iconListWidget)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = Widget()
    mw.show()
    sys.exit(app.exec_())