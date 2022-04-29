from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['run_pyqt.py',  # 主程序文件
            '-n uuv',  # 可执行文件名称
            # '-F',  # 打包单文件
            '-D',  # 打包文件夹
            # '-w', #是否以控制台黑窗口运行 加-w 无黑窗口  不加有黑窗口
            r'--icon=F:\pythonProject\uuv\statics\logo.ico',  # 可执行程序图标
            '-y',
            '--clean',
            '--workpath=build12',
            # '--add-data=templates;templates',  # 打包包含的html页面
            # '--add-data=statics;statics',  # 打包包含的静态资源
            '--distpath=build13',
            '--specpath=./'
            ]

    run(opts)

