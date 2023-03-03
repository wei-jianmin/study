数据结构：
class MainWindow
	public:
		Ui::MainWindow *ui;
		QLabel *label_caps_;
		QLabel *label_num_;
		QLabel *label_scrl_;
		//菜单栏
		MenuBarImpl *menu_bar_impl_;
		//工具栏
		ToolBarImpl *tool_bar_impl_;
		//消息映射类
		TZReaderUIView *reader_ui_view_;
		//大纲导览
		OutLineView *outLineView_;
		//资源管理器
		ClassView *classView_;
		//多文档管理器
		MutilDocView *mutilDocView_;
		//附件导览
		AccessoryView *accessoryView_;
		//语义导览
		DefindexView *defindexView_;
		//缩略图导览
		ThumbnailView *thumbnailView_;
		//图层导览
		LayerView *layerView_;
		//书签导览
		BookMarkView *bookMarkView_;
		//取消全屏对话框
		CancelFullScreenDlg *cancleFulldlg_;
		//查找对话框
		FindDlg *findDlg_;
		//加密保存对话框
		FileEncryptionInfoDlg* fileEncryptiondlg_;
		AutoPtr<eqcore::IEqApp> eq_app_;
		//封装了一些文件夹的相关操作
		common_tmpfolder_operator tmpfolderop_;
	private:
		QTimer *update_time_;
		BtmAdvertDlalog *adView_;
		QPushButton *button_;
		QWebView  *adWebview_;
		QTimer *timer_;
		bool isTimerStop;
		std::locale _local_;
class common_tmpfolder_operator	
	private:
		utils::MutexLockEx mutex;
class TZReaderUIView
	public:
		MainWindow *main_Fram_;
		QSettings *setting_;
		int mulDoc_;
		int allDoc_; 				//多文档总数量
		int special_mulDoc_;
		bool encryptedFileOpens; 	//只允许密件打开一个
		OptionType option_type_;
		QFileSystemWatcher file_watcher_;
		int prev_doc_index_;
		int user_login_status_; 	//0表示未登录，1表示已登录
		time_t last_login_time_;	
		QString user_login_name_;
		utils::ConfigHelper cfg_;
	
启动：
main中创建了ServiceImpl对象并调用了Run方法
	pMainWin_ = new MainWindow(); 
	>>数据变化
		>>内存
			初始化log4日志工具
			MainWindow::
				ui 对象创建并初始化
				>>数据变化
					>>内存
						对界面元素与响应函数进行了关联
						TZReaderUIView中数据成员完成初始化赋值
						fileEncryptiondlg_ 对象创建
				reader_ui_view_ 对象创建
				tool_bar_impl_ 对象创建
				menu_bar_impl _对象创建
				状态栏初始化
					label_caps_
					label_num_
					label_scrl_
		>>硬盘
	
	pMainWin_->InitApp()
	pMainWin_->CommandLineProcess(argc, argv);
TZReaderUIView::CreateActionConnected中将打开动作与OpenFile函数进行了绑定