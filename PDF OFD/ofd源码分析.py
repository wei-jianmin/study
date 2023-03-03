class TZReaderUIView
    MainWindow *main_Fram_;
    QSettings *setting_;
    int mulDoc_;
    int allDoc_;                    //多文档总数量
    int special_mulDoc_;
    bool encryptedFileOpens;        //只允许密件打开一个
    OptionType option_type_;
    QFileSystemWatcher file_watcher_;
    int prev_doc_index_;
    int user_login_status_;         //0表示未登录，1表示已登录
    time_t last_login_time_;
    QString user_login_name_;
    utils::ConfigHelper cfg_;
class MainWindow
    public:
        Ui::MainWindow *ui;
        AutoPtr<eqcore::IEqApp> eq_app_;
        QLabel *label_caps_;                        //状态栏 大小写
        QLabel *label_num_;                         //状态栏 数字键
        QLabel *label_scrl_;                        //状态栏 控制键
        MenuBarImpl *menu_bar_impl_;                //菜单栏
        ToolBarImpl *tool_bar_impl_;                //工具栏
        TZReaderUIView *reader_ui_view_;            //消息映射类
        OutLineView *outLineView_;                  //大纲导览
        ClassView *classView_;                      //资源管理器
        MutilDocView *mutilDocView_;                //多文档管理器
        AccessoryView *accessoryView_;              //附件导览
        DefindexView *defindexView_;                //语义导览
        ThumbnailView *thumbnailView_;              //缩略图导览
        LayerView *layerView_;                      //图层导览
        BookMarkView *bookMarkView_;                //书签导览
        CancelFullScreenDlg *cancleFulldlg_;        //取消全屏对话框
        FindDlg *findDlg_;                          //查找对话框
        common_tmpfolder_operator tmpfolderop_;     //文件夹操作工具
        FileEncryptionInfoDlg* fileEncryptiondlg_;  //密件保存对话框
    private:
        QTimer *update_time_;
        BtmAdvertDlalog *adView_;
        QPushButton *button_;
        QWebView  *adWebview_;
        QTimer *timer_;
        bool isTimerStop;
        std::locale _local_;        
class TZReaderUIDoc : public QLabel
    public:
        pdfapp_t   m_gapp_;
        MainWindow *main_Fram_;
        QString path_name_;
        QString secure_path_name_;
        bool isUntitled_;
        int  m_SelStart[2],m_SelEnd[2],m_MousePos[2];
        int m_SearchFromPage,m_SearchFromText;		    //记录每次查找时从第几页，第几个字开始查找
        fz_irect old_bbox;
        int m_layout_mode_,m_horiz_pages_;	            //页面布局相关
        std::vector<CAttachment> m_attachments_;
        QScrollBar *scrollH_;
        QScrollBar *scrollV_;
        double scaleH_;                                 //图片处理长度和水平滚动条长度比值
        double scaleV_;                                 //图片处理长度和垂直滚动条长度比值
        ssignTempData m_signtemp; 
        vector<int> m_vecNum;                           //多页签章时，签章区域中的各页
        int m_iSignPageType;                            //多页签章类型 0：CURRENTPAGE 1：ALLPAGE 2：RANGETPAGE
        int m_FileType;                                 //文件格式  0:pdf  1:ofd   2:xps  
        int m_encryptedFileType;                        //加密文件格式   100:未知类型  3:密件pdf  4:密件ofd;
        bool m_bSelState;
        vector<ssignData> m_vecssign;
        int			m_cursor_state;
        QCursor		m_hCursor;
        int         justcopied;
        int         oldx;
        int         oldy;
        QPoint	m_lastPos;		                        //记录上次鼠标位置，用于配合页面拖拽，WJM,2017年7月4日
        long	m_vStartPos;	                        //记录页面位置，配合页面拖拽，以像素为单位，WJM，2017年7月4日
        bool	m_bLButtonDown;	                        //记录左键是否按下
        QCursor arrowcurs, handcurs, waitcurs,fignercurs;
        QCursor sealcurs,  handcurs2, hrcurs;
        int m_last_nVPos;	                            //记录上次滚动条的位置，主要在页面非连续显示时，控制页面滚动用
        bool m_figerflag;
        ofd_anno_block *m_anno_block;                   //注释选中相关
        ofd_anno_block *m_anno_block_clicked;	        //鼠标点击过的注释
        bool m_bSnapshootState;		                    //快照用
        QCursor cursorSnapShot_;
        bool m_bShowSnapshootBox;	                    //快照用
        QPoint beginPoint_;                             //标识快照截图开始结束坐标
        QPoint endPoint_;
        vector<tzactionregion> m_vecregion;
        ssignData m_SelctedSign;                        //被选中的章
        QString    m_sigFieldName;
        QCursor *snapShootCursor_;                      //快照的游标图
        QCursor *signatureCursor_;                      //签章游标图
        act_rgn m_actrgn;                               //动作手指对应标记
        ThumbnailInfo m_thumb_info;                     //缩略图属性
        int page_no_;		                            //记录缩略图需要框选的页号 查找、缩略图等，页面跳转用
        int actionPage_;                                //文档动作显示页
        QPoint	curPos_;	                            //记录当前鼠标位置，在视口中绘制印章图片用
        QPixmap *pixmap_;	                            //存的是要在视口中绘制的印章图片
        QString url_;
        int cur_doc_index_;
        int is_show_seal;
        QString doc_modify_time_;
        stdex::string secure_file_id_;
    private: 
        int m_pageid;                                   //当前页的pageid
        int m_pictype;
        int        m_UIState;
        int        m_sigFieldPage;
        bool bFirstPaint_;
        QMenu *sealMenu_;
        QMenu *txtMenu_;
        QMenu *attributeMenu_;
        QString imageText_;
        unsigned int fontSize_;
        QColor  fontColor_;
        bool fontBold_;
        bool fontItalic_;
class GlobalUi   
    private:
        AutoPtr<IOesPool> oes_pool_;
        utils::Lock lock_;
        TZReaderUIDoc* doc_ptr_;
        MainWindow* main_Frm_;  
class ofd_document_s
    public:
        fz_document super;
        fz_archive *zip;
        char m_LayerControl[6];	    //对应6个图层的显示：前景(模板)层、正文(模板)层、背景(模板)层	
        char *start_part;           /* fixed document sequence */
        ofd_fixdoc *first_fixdoc;   /* first fixed document */
        ofd_fixdoc *last_fixdoc;    /* last fixed document */
        ofd_fixpage *first_page;    /* first page of document */
        ofd_fixpage *last_page;     /* last page of document */
        template_page *first_template;
        template_page *last_template;
        bookmark_info *first_bookmark;
        bookmark_info *last_bookmark;
        ofd_action *first_actions;  //动作
        ofd_action *last_actions;   //动作
        docres_info *docinfres;     //DocumentRes
        docres_info *pubinfres;     //PublicRes
        docres_info *docinfres_tail;//DocumentRes
        docres_info *pubinfres_tail;//PublicRes
        int ResParsed;	            //表明上面的DocResRoot和PubResRoot是否被解析过，因为可能文档中两者为空
        int page_count;
        fz_rect page_default_rect;	//纵横页 page_default_rect变量声明 以磅值为单位
        ofd_sign *first_sign;       /* first sign of document */
        ofd_sign *last_sign;        /* last sign of document */
        int sign_count;
        ofd_target *target;         /* link targets */
        char *base_uri;             /* base uri for parsing XML and resolving relative paths */
        char *part_uri;             /* part uri for parsing metadata relations */
        ofd_font_cache *font_table; /* We cache font resources */
        float opacity[64];          /* Opacity attribute stack */
        int opacity_top;
        fz_colorspace *colorspace;  /* Current color */
        float color[8];
        float alpha;
        char *current_docpath;      //当前现实的文档路径
        char *current_signpath;
        fz_device *dev;             /* Current device */
        fz_cookie *cookie;
        //文档权限
        //全局设置(权限问题)
        /*是否允许编辑文档信息，管理控制范围包括更改元数据、视图
        首选项、书签、大纲、文档和页面动作等操作。默认值为true*/
        int  m_bedit;
        /*是否允许添加或修改注释对象，管理控制范围包括注释工具的
        使用，修改或删除注释对象以及关联的撤销、重做等操作。默认值为true*/
        int  m_bannot;
        int m_bexport;              //权限，是否允许使用保存、导出、另存为以及资源或附件下载功能,默认true
        int m_bsignature;           //是否允许进行数字签名，默认true
        int m_bwatermark;           //是否允许添加水印
        int m_bprintScreen;         //是否允许截屏
        ///*打印权限，若不设置Print节点，则默认可以打印，并且打印分数不受限制，
        //若设置Print节点，则具体权限*/
        int m_bprintable;           //是否允许被打印
        int m_icopies;              //打印份数
        char m_cstartdate[256];     //有效开始日期
        char m_cenddate[256];       //有效期结束日期
        ofd_eledata *eledata;       //元数据信息
        ofd_extentiondata *extdata; //扩展信息
        ofd_media   *media;         //多媒体
        ofd_fontres *fontres;       //字体资源
        ofd_version *version;       //版本信息
        int m_i_pagemode;
        int m_i_layout;
        int m_i_title;
        int m_i_zoommode;
        int m_b_hidemenu;
        int m_b_hidetool;
        int m_b_hidestatus;
        int m_b_hideui;
        float m_edit_zoom;
        ofd_anno_page * first_anno_page;
        ofd_anno_page * last_anno_page;
        char oespath[256];//oes 路径
        ofd_customtag_jumpinfo *first_customtag_jumpinfo;   
class ssignData 
    public:
        stdex::string sig_result;//签章验证结果，true 或者false
        stdex::string  sig_person;//签名人员
        stdex::string  sig_time;//签名时间
        stdex::string  sig_sealinfo;//印章名称
        stdex::string  sig_sealname;//签章名称 签章1
        char  sig_filedname[512];///Doc_0/Signs/Sign_0/Signature.xml
        stdex::string  sig_type;//签章类型
        stdex::string  sig_Method;//签名方法
        stdex::string  Sig_CheckMethod;//摘要方法
        char  sig_filter[512];//文档名称
        stdex::string  sig_validtime;//签章有效期
        char strvalueloc[512];//签章所对应的SignedValue值  /Doc_0/Signs/Sign_0/SignedValue.dat
        char sig_sealfiledname[512];///Doc_0/Signs/Sign_0/.sel
        stdex::string  sig_ID;//当前章组的ID（按照先小后大的顺序）
        int intsignloc;
        stdex::string  sig_cert;//签名证书
        stdex::string  sig_chg_after_sign;//
        stdex::string  sig_relation;//
        stdex::string  sig_reason;//
        stdex::string  sig_subfilter;// 
        stdex::vector<CheckData> veccheck;
        stdex::map <stdex::string,stdex::string> sign_mapReference;//References下的值
        stdex::vector<ssingleLoc>  vecsignloc;
        stdex::string sig_sigName;// Annot/T
        int FieldNum; // Catalog/Fields
        int sig_sigType; // Annot/SigType ;0:单页 1:多页 2:骑缝
class ssignTempData 
    public:
        int   m_SignState;			//0 准备好 1 准备好
        int   m_SignType;			//0 签章   1 骑缝章 2 签批
        char  m_Signer[256];		//签名人或者签名ID
        char  m_proverder[256];		//创建签名时所用的签章组建提供者名称
        char  m_Company[256];		//创建签名时所用的签章组件的制造商
        char  m_Version[256];		//创建签名时所用的签章组件的版本
        char  m_Method[256];		//签名方法
        char  m_CheckMethod[256];	//摘要方法
        char  m_SealPath[256];
        char  m_PicPath[256];
        char  m_SignTime[256];
        char  m_signloc[256];
        char* m_SignCert;
        char* m_ESealData;
        char m_oesDllPath[256];//签章时调用的oes路径
        int icertlen;
        int isealdatalen;
        double m_PicPath_width;
        double m_PicPath_height;
        
======================================================================

TZReaderUIView::OpenFile(QString fileName, QString url, int *index)   
    TZReaderUIDoc *doc = new TZReaderUIDoc(main_Fram_);
        main_Fram_ = 参数(main_Fram_)
        scaleH_ = scaleV_ = 1
        scrollH_ = new QScrollBar(Qt::Horizontal, this);
        scrollV_ = new QScrollBar(Qt::Vertical, this);
        connect(scrollH_, SIGNAL(valueChanged(int)), this, SLOT(OnHScroll(int)));
        connect(scrollV_, SIGNAL(valueChanged(int)), this, SLOT(OnVScroll(int)));
        justcopied =0;
        m_UIState  =0;
        m_pageid = 0;
        oldx=0;
        oldy=0;
        m_FileType = FILEOFD;
        m_iSignPageType = -1;
        m_pictype = -1;
        m_encryptedFileType = UNKNOWN;
        for(int i=0;i<2;i++)  
            m_MousePos[i]=m_SelStart[i]=m_SelEnd[i]=-1;
        m_bSelState=false;
        old_bbox.x0=old_bbox.x1=old_bbox.y0=old_bbox.y1=0;
        m_SearchFromText=m_SearchFromPage=0;
        m_cursor_state=CURSOR_ARROW;
        m_hCursor=NULL;
        m_figerflag = false;
        isUntitled_ = true;
        fz_context  *ctx = NULL;
        ctx = fz_new_context(0, 0, FZ_STORE_DEFAULT);
        ctx->log=NULL;
        pdfapp_init(fz_context *ctx=ctx, pdfapp_t *app=&m_gapp_);
            pdfapp_clear(pdfapp_t *app=app);
                app->doc=NULL;
                app->docpath=NULL;
                app->doctitle=NULL;
                app->outline=NULL;
                app->outline_deferred=0;
                app->pagetotalh=0;
                app->pagetotalw=0;
                app->layout_w=0;
                app->layout_h=0;
                app->layout_em=0;
                app->layout_css=NULL;
                app->layout_use_doc_css=0;
                app->pagecount=0;
                app->resolution=0;
                app->rotate=0;
                app->image=NULL;
                app->tmp_image=NULL;
                app->pagetable=NULL;
                app->colorspace=NULL;
                app->grayscale=0;
                app->invert=0;
                app->tint=app->tint_r=app->tint_g=app->tint_b=0;
                app->pageno=0;
                app->page=NULL;
                memset(&(app->page_bbox),0,sizeof(fz_rect));
                app->page_list=NULL;
                app->annotations_list=NULL;
                app->page_list_table=NULL;
                app->anno_list_table=NULL;
                app->page_text=NULL;
                app->page_links=NULL;
                app->incomplete=0;
                app->errored=0;
                app->presentation_mode=0;
                app->transitions_enabled=0;
                app->old_image=NULL;
                app->new_image=NULL;
                app->start_time=0;
                app->in_transit=0;
                app->duration=0;
                memset(&(app->transition),0,sizeof(fz_transition));
                app->pagetable4sel=NULL;
                app->texttable4sel=NULL;
                memset(app->hist,0,256*sizeof(int));
                app->histlen=0;
                memset(app->marks,0,10*sizeof(int));
                app->winw=app->winh=0;
                app->scrw=app->scrh=0;
                app->shrinkwrap=0;
                app->fullscreen=0;
                memset(app->number,0,256);
                app->numberlen=0;
                app->ispanning=0;
                app->panx=app->pany=0;
                app->iscopying=0;
                app->selx=app->sely=0;
                app->beyondy=0;
                memset(&(app->selr),0,sizeof(fz_rect));
                app->nowaitcursor=0;
                app->issearching=0;
                app->searchdir=0;
                memset(app->search,0,512);
                app->searchpage=0;
                memset(app->hit_bbox,0,512*sizeof(fz_rect));
                app->hit_count=0;
                app->userdata=NULL;
                app->ctx=NULL;
                app->fullcompression=false;
                app->nxChar=0;
                app->nyChar=0;
                app->nxCaps=0;
                app->nyClient=0;
                app->nxClient=0;
                app->xPos=0;
                app->yPos=0;
                app->nVPos=0;
                app->nHPos=0;
                app->NUMLINES=0;
                app->NUMCOLS=0;
                app->pageNum=0;
                app->startPage=0;
                app->endPage=0;
                app->m_pagex=app->m_pagey=0;
                app->IsQFZ=0;
                app->IsA4Rotate=0;
                memset(app->wbuf,0,sizeof(wchar_t)*1024);
                memset(app->filename,0,1024);
                app->m_ShowSignatureSeal=false;
                app->m_PrevShowSignatureSeal=false;
                app->m_HideAllText=false;
                app->pList_HitPosition=NULL;
                app->m_OriFileEndPos=0;
                app->m_multdoc=0;
                app->m_special_multdoc_=0;
                app->openstate=0;
                //m_scene;
                app->m_tzmj_decode_data="";
            app->scrw = 640;
            app->scrh = 480;
            app->resolution = 72;
            app->ctx = ctx;
            app->layout_w = 450;
            app->layout_h = 600;
            app->layout_em = 12;
            app->layout_css = NULL;
            app->layout_use_doc_css = 1;
            app->transition.duration = 0.25f;
            app->transition.type = FZ_TRANSITION_FADE;
            app->colorspace = fz_device_bgr(ctx);
            app->tint_r = 255;
            app->tint_g = 250;
            app->tint_b = 240;
            app->doc = NULL;
            app->pagetable = NULL;
            app->pagetable4sel = NULL;
            app->page_list = NULL;
            app->page_text = NULL;
            app->page_links = NULL;
            app->doctitle = NULL;
            app->image = NULL;
            app->outline = NULL;
            app->page = NULL;
            app->docpath = NULL;
            app->annotations_list = NULL;
            app->tmp_image = NULL;
            app->old_image = NULL;
            app->new_image = NULL;
            app->texttable4sel = NULL;
            app->m_multdoc = 0;
            app->m_special_multdoc_ = 0;
            app->nxChar = /*tm.tmAveCharWidth*/1;	//2017年11月28日 WJM
            app->nyChar = /*tm.tmHeight + tm.tmExternalLeading*/1; //2017年11月28日 WJM
            app->openstate = 1;
            app->anno_list_table=NULL;
            app->page_list_table=NULL;
            app->m_tzmj_decode_data = "";
        m_gapp_.m_PrevShowSignatureSeal=m_gapp_.m_ShowSignatureSeal = true;
        InitThumbnail();    //初始化缩略图属性
            m_thumb_info.m_app=NULL;
            m_thumb_info.m_bInited=false;
            m_thumb_info.m_ctx=NULL;
            m_thumb_info.m_cutLines=0;
            m_thumb_info.m_endPage=0;
            m_thumb_info.m_pageCounts=0;
            m_thumb_info.m_pageNums=0;
            m_thumb_info.m_startPage=0;
            m_thumb_info.m_tmpPageNo=0;
            m_thumb_info.m_VPos=0;
            m_thumb_info.pagetable=NULL;
            m_thumb_info.doc=NULL;
            m_thumb_info.tmp_image=NULL;
        m_horiz_pages_=1;
        m_layout_mode_=1;
        m_SearchFromText=0;
        m_SearchFromPage=0;
        page_no_ = 0;
        pixmap_ = NULL;
        m_anno_block=NULL;
        m_anno_block_clicked = NULL;
        m_bSnapshootState = false;
        m_bShowSnapshootBox=true;
        m_bLButtonDown = false;
        snapShootCursor_ = NULL;
        sealcurs = NULL;
        signatureCursor_ = NULL;
        bFirstPaint_ = false;
        actionPage_ = -1;
        TZOrinESealInfoGM(m_signtemp);
        setMouseTracking(true);
        cur_doc_index_ = 0;
        is_show_seal = 1;
        secure_file_id_ = "";
        fontSize_ = 25;
        fontColor_ = QColor(100,100,100,20);
        fontBold_ = true;
        fontItalic_ = true;
        setWatermarkImageText("TZMJ");
        setFocusPolicy(Qt::StrongFocus);
    doc->m_FileType = FILEOFD;
    main_Fram_->ui->widget_mdiArea->addSubWindow(doc);
    doc->LoadFile(fileName="E:/Desktop/文件/OFD文件/调试用/1 pages/a95.ofd")
        m_gapp_.filename = utf8(fileName);
        pdfapp_open_progressive(pdfapp_t *app=&m_gapp_, char *filename=m_gapp_.filename, 
                                int reload=0, int bps=0,int pagenum=0)
            fz_context *ctx = app->ctx;
            fz_register_document_handlers(fz_context*ctx = ctx)
            fz_set_use_document_css(fz_context *ctx=ctx, int use=app->layout_use_doc_css);
                ctx->style->use_document_css = use;
            ctx->imuldoc = app->m_multdoc;
            app->doc = fz_open_document(ctx, filename, is_show_seal);
                'fz_document_handler *handler = fz_recognize_document(ctx,filename);
                    return ctx->handler[2];     //_ofd_document_handler
                return handler->open(fz_context *ctx=ctx,char *filename=filename,
                                     int showseal=showseal);
                    'fz_stream *file=fz_open_file(ctx, filename);
                        FILE *file=fz_fopen_utf8(name, "rb");
                        return fz_open_file_ptr(ctx, file);
                            fz_file_stream *state=new fz_file_stream;
                            state->file = file;    
                            fz_stream *stm = fz_new_stream(ctx, state, next_file, close_file);
                            stm->seek = seek_file;
                            return stm;
                    fz_document *doc = ofd_open_document_with_stream(ctx, file, showseal);
                        ofd_document *doc = new ofd_document
                        ofd_init_document(ctx, doc);
                        	doc->super.refs = 1;
                            doc->super.drop_document = ofd_drop_document;
                            doc->super.load_outline = ofd_load_outline;
                            doc->super.resolve_link = ofd_lookup_link_target;
                            doc->super.count_pages = ofd_count_pages;
                            doc->super.load_page = ofd_load_page;
                            doc->super.lookup_metadata = ofd_lookup_metadata;
                            doc->m_bedit = 1;
                            /*是否允许添加或修改注释对象，管理控制范围包括注释工具的
                            使用，修改或删除注释对象以及关联的撤销、重做等操作。默认值为true*/
                            doc->m_bannot = 1;
                            doc->m_bexport = 1;//权限，是否允许使用保存、导出、另存为以及资源或附件下载功能,默认true
                            doc->m_bsignature = 1;//是否允许进行数字签名，默认true
                            doc->m_bwatermark = 1;//是否允许添加水印
                            doc->m_bprintScreen = 1;//是否允许截屏
                            ///*打印权限，若不设置Print节点，则默认可以打印，并且打印分数不受限制，
                            //若设置Print节点，则具体权限*/
                            doc->m_bprintable = 1;//是否允许被打印
                            doc->m_icopies = -1;//打印份数
                            memset(doc->m_cstartdate,0,256);
                            memset(doc->m_cenddate,0,256);
                            doc->first_fixdoc=NULL;
                            doc->last_fixdoc=NULL;
                            doc->first_page=NULL;
                            doc->last_page=NULL;
                            doc->first_sign=NULL;
                            doc->last_sign=NULL;
                            doc->first_template=NULL;
                            doc->last_template=NULL;
                            doc->first_bookmark=NULL;
                            doc->last_bookmark=NULL;
                            doc->ResParsed=0;
                            doc->m_LayerControl[0]=1;
                            doc->m_LayerControl[1]=1;
                            doc->m_LayerControl[2]=1;
                            doc->m_LayerControl[3]=1;
                            doc->m_LayerControl[4]=1;
                            doc->m_LayerControl[5]=1;
                            doc->m_i_pagemode=0;
                            doc->m_i_layout=1;
                            doc->m_i_title=0;
                            doc->m_i_zoommode=0;
                            doc->m_b_hidemenu=0;
                            doc->m_b_hidetool=0;
                            doc->m_b_hidestatus=0;
                            doc->m_b_hideui=0;
                            doc->m_edit_zoom=1;
                            doc->page_default_rect.x0=0;
                            doc->page_default_rect.x1=210*DPICHANGE;
                            doc->page_default_rect.y0=0;
                            doc->page_default_rect.y1=297*DPICHANGE;
                        doc->zip = fz_open_zip_archive_with_stream(ctx, file);
                        ofd_read_page_list(ctx, doc, showseal);
                            'fz_xml *root = NULL;
                            'fz_xml *currentbody = NULL;
                            #获取OFD.xml结构及DocBody子节点
                            'ofd_read_ofd_currentnode(ctx,doc, char *name="OFD.xml",
                                fz_xml **root=&root,fz_xml **currentbody=&currentbody);
                                    'ofd_part *part = ofd_read_part(ctx, doc, name);
                                    char buf[1024] = part->name = "OFD.xml"
                                    *root = fz_parse_xml(ctx, part->data,XML_PRESERVE_WHITE_SPACE);
                                    *currentbody 指向root的ofd:DocBody子节点
                                    'ofd_drop_part(ctx, doc, part);
                            ofd_parse_ofddata_version(ctx,doc, fz_xml *item=currentbody);
                            #处理DocBody子节点下的DocInfo、DocRoot、Signatures子节点
                            ofd_parse_ofddata_imp2(ctx,doc,fz_xml *item=currentbody,showseal);
                                item的下级节点，如果是DocInfo
                                    ofd_newseteleinfo(ctx,doc,node=item的下级节点);
                                        ofd_eledata *eledata=new ofd_eledata；
                                        将元数据放到eledata相应成员中
                                            eledata->docid = <"DocID">
                                            eledata->doctitle = <"Title">
                                            eledata->autor = <"Author">
                                            eledata->subject = <"Subject">
                                            eledata->docabstract = <"Abstract">
                                            eledata->cteatedate = <"CreationDate">
                                            eledata->modedate = <"ModDate">
                                            eledata->doctype = <"DocUsage">
                                            eledata->doccover = <"Cover">
                                            eledata->keyword = <"Keywords">
                                            eledata->doccreator = <"Creator">
                                            eledata->creatorversion = <"CreatorVersion">
                                            eledata->userele = <"CustomDatas">
                                        doc->eledata = eledata;
                                item的下级节点，如果是DocRoot
                                    char *srcbuf = fz_xml_text(node) = "Doc_0/Document.xml"
                                    ofd_add_fixed_document(ctx,doc, srcbuf);
                                        ofd_fixdoc *fixdoc = new ofd_fixdoc
                                        fixdoc->name = "Doc_0/Document.xml"
                                        fixdoc->outline = NULL;
                                        fixdoc->next = NULL;
                                        fixdoc->annotations=NULL;
                                        fixdoc->attachments=NULL;
                                        fixdoc->defineindexpath=NULL;
                                        fixdoc追加到 doc->first_fixdoc 链表中
                                    doc->current_docpath = "Doc_0/Document.xml"
                                item的下级节点，如果是Signatures, 且showseal
                                    char *srcbuf = 获取节点文本 = "Doc_0/Signatures.xml"
                                    ofd_newsetSigns(ctx,doc,char *name=srcbuf)
                                        'ofd_part *part = ofd_read_part(ctx,doc, name);
                                        'root = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE);
                                        遍历root的子节点
                                            如果是"Signature"节点
                                                'char *srcbuf =  "BaseLoc"属性值 = "Signs/Sign_0/Signature.xml"
                                                'char *signtype = "Type"属性值 = "Seal"
                                                'char str[80] = 绝对路径(srcbuf) = "Doc_0/Signs/Sign_0/Signature.xml"
                                                ofd_newsetsigndata2(ctx,doc,char *name=str,signtype)
                                                    'ofd_part *part = ofd_read_part(ctx,doc, name);
                                                    'fz_xml *root = fz_parse_xml(ctx, part->data,XML_PRESERVE_WHITE_SPACE);
                                                    ofd_parse_signdata_imp3(ctx,doc,fz_xml *item=root,name,signtype);
                                                        递归遍历子节点
                                                            如果是"StampAnnot"节点
                                                                'char *boundary = fz_xml_att(item,"Boundary");
                                                                'char *pageref = fz_xml_att(item, "PageRef");
                                                                'char *clippath = fz_xml_att(item,"Clip");
                                                                'int pageid = pageref
                                                                'fz_xml *node = fz_xml_next(item) = <"Seal">
                                                                int bret = ofd_parse_signdata_Stamp(ctx,doc,fz_xml *item=node,name,
                                                                                                    signtype,pageid,boundary,clippath);
                                                                    遍历item及其后续兄弟节点
                                                                        如果是"Seal"节点
                                                                            item = <"Seal">的子节点
                                                                                如果是"BaseLoc"
                                                                                    'char *Sealpath = <"BaseLoc">节点值 = "Seal.esl"
                                                                                    'char str[260] = 绝对路径(Sealpath) = "Doc_0/Signs/Sign_0/Seal.esl"
                                                                                    ofd_add_fixed_sign2(ctx,doc,name,pageid,signtype,boundary,clippath,char *picpath=str);
                                                                                        ofd_sign *fixsign = new ofd_sign
                                                                                        fixsign->name = name
                                                                                        fixsign->number = doc->sign_count++
                                                                                        fixsign->signtype = signtype
                                                                                        fixsign->locboundary = boundary
                                                                                        fixsign->clippath = clippath
                                                                                        fixsign->picpath = picpath
                                                                                        fixsign->pageid = pageid
                                                                                        fixsign->next = NULL
                                                                                        fixsign 追加到 doc->first_sign 链表
                                                    'fz_drop_xml(ctx, root);
                                                    'ofd_drop_part(ctx,doc, part);
                                        'fz_drop_xml(ctx, root);
                                        'ofd_drop_part(ctx,doc, part);
                                    doc->current_signpath = srcbuf
                            #统计root下DocBody节点个数
                            ofd_read_ofd_multnum(ctx,root);
                                ctx->ismulflagnum = 统计root下DocBody子节点个数
                            'fz_drop_xml(ctx, root);
                            foreach(ofd_fixdoc *ofddoc = doc->first_fixdoc)
                                ofd_read_and_process_metadata_part(ctx,doc, char *name=ofddoc->name, ofd_fixdoc *fixdoc=ofddoc)
                                    'ofd_part *part = ofd_read_part(ctx, doc, name="Doc_0/Document.xml");
                                    ofd_parse_metadata(ctx, doc, part, fixdoc);
                                        'char buf[1024]=part->name="Doc_0/Document.xml"
                                        'fz_xml *root = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE);
                                        ofd_parse_metadata_imp(ctx, doc, root, fixdoc);
                                            递归遍历子节点
                                                Actions：
                                                    ofd_prase_action(ctx,item,doc,0,0,NULL);
                                                Extensions：
                                                Bookmark：
                                                Page：
                                                    遍历子节点
                                                        如果是"FileLoc"
                                                    如果存在"BaseLoc"项，参考值："Pages/Page_0/Content.xml"
                                                    char buf11[1024] = "Doc_0/Pages/Page_0/Content.xml"   
                                                    ofd_add_fixed_page(ctx,doc, char *name=buf11, width, height,pageid);
                                                        ofd_fixpage *page = new ofd_fixpage
                                                        page->name = "Doc_0/Pages/Page_0/Content.xml"
                                                        page->annoname=NULL;	//2017年5月8日
                                                        page->number = doc->page_count++;
                                                        page->width = width;
                                                        page->height = height;
                                                        page->links = NULL;
                                                        page->links_resolved = 0;
                                                        page->next = NULL;
                                                        page->pageid = pageid;
                                                        page->pageres = NULL;
                                                        page追加到doc->first_page链表
                                                Outlines：
                                                    fixdoc->outline = fixdoc->name
                                                Attachments：
                                                    fixdoc->attachments=节点值
                                                Annotations：
                                                    fixdoc->annotations=节点值=注释文件的路径
                                                Edit：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bedit = 0
                                                Annot：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bannot = 0
                                                Export：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bexport = 0
                                                Signature：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bsignature = 0 #控制不显示印章
                                                Watermark：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bwatermark = 0
                                                PrintScreen：
                                                    取节点的值
                                                    如果是false
                                                        doc->m_bprintScreen = 0
                                                Print：
                                                    取节点的值
                                                    'char *sprintable = fz_xml_att(item, "Printable");
                                                    'char *ncopy = fz_xml_att(item, "Copies")
                                                    如果sprintable是false
                                                        doc->m_bprintable = 0
                                                    否则
                                                        ncopy>0 : doc->m_icopies = ncopy
                                                        ncopy=0 : doc->m_bprintable = 0 , doc->m_icopies = 0
                                                        ncopy<0 : doc->m_icopies = -1
                                                ValidPeriod：
                                                CustomTags：
                                                CommonData：
                                                    找到PageArea/PhysicalBox子节点，如果存在，计算得到doc->page_default_rect
                                                    如果存在TemplatePage子节点（模板页）
                                                    如果doc->ResParsed为0
                                                        如果存在PublicRes节点
                                                            char srcbuf[50]=公共资源文件路径="Doc_0/PublicRes.xml"
                                                            ofd_get_docpubres(ctx,doc,char *respath=srcbuf,int ifalg=0);
                                                                'ofd_part *part = ofd_read_part(ctx,doc,respath);
                                                                fz_xml *PageResRoot = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE);
                                                                'ofd_drop_part(ctx,doc,part);
                                                                docres_info *docinfo = new docres_info
                                                                docinfo->DocResRoot = PageResRoot
                                                                docinfo->next = NULL
                                                                docinfo 添加到 doc->pubinfres 链表
                                                            检查下一个"PublicRes"节点
                                                        doc->ResParsed = 1
                                                    如果doc->current_docpath="Doc_0/Document.xml"不为空
                                                        char base_uri[1024] = doc->current_docpath的所在文件夹 = "Doc_0/"
                                                        ofd_set_docres(ctx,base_uri="Doc_0/",doc,docres_info *resinfo=doc->pubinfres)
                                                            while(docres_info *p=resinfo)   #提示：resinfo是个链表
                                                                ofd_set_mediares(ctx,base_uri,fz_xml *FontResroot=p->DocResRoot,doc);
                                                                    遍历FontResroot的子节点，找到"MultiMedias"子节点                                                                        
                                                                ofd_set_fontres(ctx,base_uri,fz_xml *FontResroot=p->DocResRoot,doc);
                                                                    遍历FontResroot的子节点，找到"Fonts"子节点
                                                                        遍历每个"Font"子节点
                                                                            ofd_fontres *fontres = new ofd_fontres
                                                                            根据节点信息设置fontres的每个值：
                                                                                fontres->fontname = "ABCDEF+TimesNewRomanPSMT"
                                                                                fontres->familayname = "Times New Roman"
                                                                                fontres->charset = NULL
                                                                                fontres->fontfile = "font_1.otf"
                                                                                fontres->iserif
                                                                                fontres->ibold
                                                                                fontres->iitalic
                                                                                fontres->ifixedwidth
                                                                            fontres追加到doc->fontres链表
                                                                p = p->next;
                                                        ofd_set_docres(ctx,base_uri="Doc_0/",doc,docres_info *resinfo=doc->docinfres);
                                                VPreferences：
                                        'fz_drop_xml(ctx, root);
                                        doc->base_uri = NULL;
                                        doc->part_uri = NULL;
                                    'ofd_drop_part(ctx, doc, part);
                                if(ofddoc->annotations)
                                    ofd_read_and_process_metadata_part(ctx,doc, ofddoc->annotations,NULL);
                    'fz_drop_stream(ctx, file);
                    return doc;
            app->docpath="E:/Desktop/鏂囦欢/OFD鏂囦欢/璋冭瘯鐢?1 pages/a95.ofd"
            app->doctitle="a95.ofd"
            fz_layout_document(app->ctx, app->doc, app->layout_w, app->layout_h, app->layout_em);
            app->pagecount = fz_count_pages(app->ctx, app->doc);
                int ofd_count_pages(fz_context *ctx, fz_document *doc_)
                    return doc->page_count;
            app->outline = fz_load_outline(app->ctx, app->doc);
                fz_outline *ofd_load_outline(fz_context *ctx, fz_document *doc_)
                    foreach(ofd_fixdoc *fixdoc=doc->first_fixdoc)
                        if(fixdoc->outline)
            TZLoadAttactments((ofd_document*)app->doc, &m_attachments_);            
                foreach(ofd_fixdoc *fixdoc=doc->first_fixdoc)    
                    if (fixdoc->attachments)   
                        char* pattachs = fixdoc->attachments   
                        break 
            if (app->pageno < 1)                app->pageno = 1;
            if (app->pageno > app->pagecount)   app->pageno = app->pagecount;
            if (app->resolution < MINRES)       app->resolution = MINRES;
            if (app->resolution > MAXRES)       app->resolution = MAXRES;
            app->shrinkwrap = 1;
            app->rotate = 0;
            app->panx = 0;
            app->pany = 0;
            app->pagetable = (pdf_page_entry *)fz_calloc(app->ctx, app->pagecount, sizeof(pdf_page_entry));
            app->pagetable4sel = (ofd_text_pages *)fz_calloc(app->ctx,app->pagecount,sizeof(ofd_text_pages));
            app->page_list_table = (fz_display_list **)fz_calloc(app->ctx,app->pagecount,sizeof(fz_display_list*));
            app->anno_list_table = (fz_display_list **)fz_calloc(app->ctx,app->pagecount,sizeof(fz_display_list*));
            for(int i=0;i<app->pagecount;i++)
                app->pagetable4sel[i].page=NULL;
                app->page_list_table[i]=NULL;
                app->anno_list_table[i]=NULL;
            app->m_scene.init(app->pagecount,((ofd_document*)(app->doc))->page_default_rect);
            pdfapp_showpage(app, int loadpage=1, int drawpage=1, int repaint=1, 
                            int transition=0, int searching=0,int set_preferenct=1);
                if(loadpage)
                    pdfapp_loadpage(app, searching=0);
                        fz_device *mdev = NULL
                        fz_cookie cookie = { 0 }
                        app->page = fz_load_page(app->ctx,app->doc, app->pageno-1);
                            return ofd_load_page(fz_context *ctx, fz_document *doc_, int number)
                                'ofd_document *doc = (ofd_document*)doc_;
                                foreach(ofd_fixpage *fix = doc->first_page)
                                    找到与number对应的链表节点
                                        fz_xml *annoroot = NULL;
                                        fz_xml *root = ofd_load_fixed_page(ctx, doc, ofd_fixpage *page=fix, fz_xml **annoroot=&annoroot);
                                            'ofd_part *part = ofd_read_part(ctx, doc, page->name); //"Doc_0/Pages/Page_0/Content.xml"
                                            fz_xml *root = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE)
                                            'ofd_drop_part(ctx, doc, part);
                                            'char *Area = NULL
                                            遍历root子节点
                                                如果是"Area"
                                                    'Area = "PhysicalBox"子节点的值
                                                如果是"Actions"
                                                    ofd_prase_action(ctx,node,doc,1,page->pageid,NULL);
                                                如果是"PageRes"
                                            '如果Area = NULL，设为默认值210*297
                                            根据Area，得到page->height，page->width
                                            if(page->annoname!=NULL)
                                                'part = ofd_read_part(ctx,doc, page->annoname)
                                                (*annoroot) = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE);
                                                'ofd_drop_part(ctx, doc, part);
                                            return root;
                                        ofd_page *page = new ofd_page
                                        page->super.load_links = ofd_load_links;
                                        page->super.bound_page = ofd_bound_page;
                                        page->super.run_page_contents = ofd_run_page;
                                        page->super.drop_page = ofd_drop_page_imp;
                                        page->fix = fix;
                                        page->root = root;
                                        page->annoroot = annoroot;
                                        page->doc = doc;
                                        return page;
                        if(m_FileType == FILEPDF)
                            pdfUpdatePageAnnots(app,app->page,is_show_seal);
                        fz_bound_page(app->ctx, app->page, &app->page_bbox);
                            根据page->fix->width、page->fix->height，设置app->page_bbox
                        app->m_scene.setPageRect(app->pageno-1,app->page_bbox);
                        app->page_list = app->page_list_table[app->pageno-1];
                        app->annotations_list=app->anno_list_table[app->pageno-1];
                        if(app->page_list==NULL && app->annotations_list==NULL)  //说明该页面还没解析过
                            app->page_list_table[app->pageno-1] = app->page_list = fz_new_display_list(app->ctx, NULL);
                            'fz_device *mdev = fz_new_list_device(app->ctx, app->page_list);
                            cookie.incomplete_ok = 1;
                            fz_run_page_contents(app->ctx, app->page, mdev, &fz_identity, &cookie);
                                ofd_run_page(fz_context *ctx, fz_page *page_=app->page, fz_device *dev=mdev, 
                                             const fz_matrix *ctm=&fz_identity, fz_cookie *cookie=&cookie)
                                    'ofd_page *page = (ofd_page*)page_;
                                    'ofd_document *doc = page->doc;
                                    'fz_matrix page_ctm = *ctm;
                                    'doc->cookie = cookie;
                                    'doc->dev = dev;
                                    ofd_parse_fixed_page(ctx, doc, &page_ctm, page);
                                        'char base_uri[1024] = page->fix->name = "Doc_0/Pages/Page_0/Content.xml"
                                        'base_uri = "Doc_0/"
                                        doc->opacity_top = 0;
                                        doc->opacity[0] = 1;
                                        'fz_rect area = fz_unit_rect;
                                        'fz_matrix scm;
                                        '根据page->fix->width, page->fix->height，设置scm和area
                                            'scm.a = 209, scm.d=296, scm其它值为0
                                            'area = [0,0,209,296]
                                        'fz_xml *page_node = page->root
                                        'fz_xml *content_node=page_node的"Content"子节点
                                        if(doc->m_LayerControl[5])  //处理背景模板层
                                        if(doc->m_LayerControl[4] && content_node)  //处理背景层Layer
                                        if(doc->m_LayerControl[3])	//处理正文模板层
                                        if(doc->m_LayerControl[2] && content_node)  //处理正文层Layer
                                            'fz_xml *node = content_node/<"Layer">
                                            遍历node的兄弟节点
                                                确保节点的"Type"属性为"Body"
                                                foreach(fz_xml *tempnode=node的子节点)
                                                    ofd_parse_element(ctx,doc,(fz_matrix *)ctm, area, base_uri, dict,
                                                                      tempnode, 255,page,page->fix->pageid,NULL);
                                        if(doc->m_LayerControl[1])  //处理前景模板层
                                        if(doc->m_LayerControl[0] && content_node)	//处理前景层Layer
                                        foreach(ofd_sign *ofdsign = doc->first_sign)
                                            找到doc->first_sign链表中与page->fix->pageid对应的节点
                                                if (ofdsign->picpath != NULL)   //"Doc_0/Signs/Sign_0/Seal.esl"
                                                    'base_uri = "Doc_0/Signs/Sign_0/Seal.esl"
                                                    ofd_parse_sign(ctx,doc,(fz_matrix*)ctm, &area, base_uri, dict, ofdsign);
                                                        ofd_parse_signpath(ctx,doc, ctm, base_uri, dict,ofdsign);   //没用area参数
                                                            'char *image_boundary_att = ofdsign->locboundary = "54.561 26.1969 42 42"
                                                            'char *image_resourcepatf_att = ofdsign->picpath = "Doc_0/Signs/Sign_0/Seal.esl"
                                                            'char *image_clippath_att = ofdsign->clippath = "0 0 42 42"
                                                            'fz_matrix transform = fz_identity
                                                            'fz_matrix local_ctm = fz_identity
                                                            'int fill_rule=0
                                                            'fz_path *clippath, *path
                                                            if(image_clippath_att)
                                                                'char clippath2[50] = path_add(image_boundary_att,image_clippath_att) = "54.56 26.20 42.00 42.00 "
                                                                'char *data_value = ModifyAbbreviatedData(clippath2) = "M 154.66 74.27 L 154.66 193.32 L 273.71 193.32 L 273.71 74.27 C"
                                                                'clippath = ofd_parse_abbreviated_geometry(data_value)
                                                            if (image_boundary_att)
                                                                'char *data_value = ModifyAbbreviatedData(image_boundary_att) = "M 154.66 74.26 L 154.66 193.31 L 273.72 193.31 L 273.72 74.26 C"
                                                                'path = ofd_parse_abbreviated_geometry(data_value)
                                                            'fz_path *stroke_path = path
                                                            'clippath为空时，clippath = path
                                                            ofd_parse_sign_image_brush(ctx,doc, &local_ctm,  &area, image_resourcepatf_att, 
                                                                                       dict, image_resourcepatf_att,ofdsign);
                                                                'ofd_part *part = ofd_read_part(ctx, doc, base_uri);
                                                                'int ilength = 0;   印章数据长度
                                                                'int piSealWidth = 0;
                                                                'int piSealHeight = 0;
                                                                'unsigned char* puchSealImage = OESEX_GetSealImage(part->data->data,&ilength,&piSealWidth,&piSealWidth)
                                                                如果印章数据puchSealImage是一个ofd文件
                                                                    解析该ofd文件，将文件中的内容节点添加到显示链表
                                                                'fz_buffer *buffer = fz_new_buffer_from_data(ctx, puchSealImage,ilength);
                                                                'fz_image *image = fz_new_image_from_buffer(ctx,buffer);
                                                                'fz_drop_buffer(ctx,buffer);
                                                                ofd_parse_signpictiling_brush(ctx,doc, ctm, area, base_uri, dict,    #将印章图片加入显示链表
                                                                                              ofdsign, ofd_paint_image_brush, image);
                                                                'fz_drop_image(ctx, image);
                                    'doc->cookie = NULL;
                                    'doc->dev = NULL;
                            fz_run_annot
                            'fz_close_device(app->ctx, mdev);
                            'fz_drop_device(app->ctx, mdev);
                            if(app->page_list)
                                维护文字布局表，文字查找/选择/复制时，会参考该表
                if(drawpage)
                if(transition)
                if(repaint)

void TZReaderUIDoc::OnRButtonDown(QMouseEvent *event)
    oldx = event->pos().x();
	oldy = event->pos().y();
    if(m_signtemp.m_SignState==1)	//鼠标当前鼠标处于签章状态
        m_signtemp.m_SignState=0;
        m_signtemp.m_SignType =-1;
        根据m_cursor_state，设置鼠标形状
    #获取鼠标点击页面和位置
    'fz_point p;
	'int SignPage = TZGetMousePageNum(event->pos().x(),event->pos().y(),p);
    'pdfapp_t *app=&m_gapp_;
    app->page = fz_load_page(app->ctx,app->doc,SignPage-1); #因为当前可能同时显示了多个页面，app->page需要指向点击页面
        return ofd_load_page(fz_context *ctx, fz_document *doc_, int number)
            'ofd_document *doc = (ofd_document*)doc_;
            foreach(ofd_fixpage *fix = doc->first_page)
                找到与number对应的链表节点
                    fz_xml *annoroot = NULL;
                    fz_xml *root = ofd_load_fixed_page(ctx, doc, ofd_fixpage *page=fix, fz_xml **annoroot=&annoroot);
                        'ofd_part *part = ofd_read_part(ctx, doc, page->name); //"Doc_0/Pages/Page_0/Content.xml"
                        fz_xml *root = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE)
                        'ofd_drop_part(ctx, doc, part);
                        'char *Area = NULL
                        遍历root子节点
                            如果是"Area"
                                'Area = "PhysicalBox"子节点的值
                            如果是"Actions"
                                ofd_prase_action(ctx,node,doc,1,page->pageid,NULL);
                            如果是"PageRes"
                        '如果Area = NULL，设为默认值210*297
                        根据Area，得到page->height，page->width
                        if(page->annoname!=NULL)
                            'part = ofd_read_part(ctx,doc, page->annoname)
                            (*annoroot) = fz_parse_xml(ctx, part->data, XML_PRESERVE_WHITE_SPACE);
                            'ofd_drop_part(ctx, doc, part);
                        return root;
                    ofd_page *page = new ofd_page
                    page->super.load_links = ofd_load_links;
                    page->super.bound_page = ofd_bound_page;
                    page->super.run_page_contents = ofd_run_page;
                    page->super.drop_page = ofd_drop_page_imp;
                    page->fix = fix;
                    page->root = root;
                    page->annoroot = annoroot;
                    page->doc = doc;
                    return page;
    if(m_FileType == FILEOFD)
        m_pageid = app->page->fix->pageid;
    'std::vector<ssignData> *pvecssign=NULL;
	'char sigFieldName[256]={0};
	'ssignData *pselctedSign = NULL;
    RightDownBox2(app,p,&pvecssign,sigFieldName,&pselctedSign,en_TYPE_OFD,OutputMsg);
        if(docType == en_TYPE_OFD)
            RightDownofdBox2(app,p1,pvecssign,sigFieldName,pselctedSign,pmsgbox);
                stdex::vector<ssignData> *mvecssign = new stdex::vector<ssignData>;
                ssignData *selctedSign = new ssignData;
                'ofd_page  *page	=(ofd_page *)app->page;
                'ofd_document* xref = (ofd_document *)app->doc;
                'stdex::vector<stdex::string> vecstrsign;
                'stdex::vector<stdex::string> vecIDsign;
                COFDFuction::GetSignNum(app->ctx,xref,vecstrsign,vecIDsign);
                    读xref->current_signpath="Doc_0/Signatures.xml"
                        定位到"Signature"节点，
                            定位到"BaseLoc"节点，获取节点值，并转为绝对值 = "Doc_0/Signs/Sign_0/Signature.xml"
                                将该值压入 vecstrsign
                            定位到"ID"节点，获取节点值
                                将该值压入 vecIDsign
                COFDFuction::SetSigndataInit(*selctedSign)  #将selctedSign的成员值赋值为空
                'stdex::vector<ssignData> vecssign;
                遍历vecstrsign
                    #读取签章信息
                    COFDFuction::GetSignDataCommon(app->ctx,xref,stdex::string strsignxmlname=vecstrsign[i],
                                                   stdex::string strparid=vecIDsign[i],vecssign);
                        'ssignData sign;
                        'SetSigndataInit(sign);
                        'char *fill_uri = strsignxmlname = "Doc_0/Signs/Sign_0/Signature.xml"
                        'ofd_part *part = ofd_read_part(ctx,xref, fill_uri);
                        'fz_xml *root = fz_parse_xml(ctx, part->data,0)
                        根据root内容，设置sign的成员值
                            sign.sig_sigType
                            sign.vecsignloc
                            sign.veccheck
                            sign.sig_filedname
                            sign.sig_ID 
                            sign.sig_time
                            sign.sig_person
                            sign.sig_sealname 
                            sign.sig_sealinfo 
                            sign.sig_cert 
                            sign.sign_mapReference 
                            sign.strvalueloc
                            sign.sig_sealfiledname
                            sign.sig_type 
                            sign.sig_relation 
                            sign.sig_Method 
                            sign.Sig_CheckMethod 
                        vecssign.push_back(sign);
                遍历vecssign
                    vecssign[k].sig_filter=WTA(app->wbuf)="E:/Desktop/文件/OFD文件/调试用/1 pages/a19.ofd"
                    COFDFuction::GetCurrentInfo(app->ctx,xref,ssignData &signdata=vecssign[k],int itype=1,pmsgbox);
                        'char *fill_uri = signdata.strvalueloc = "Doc_0/Signs/Sign_0/SignedValue.dat"
                        'ofd_part *part = ofd_read_part(ctx,xref, fill_uri);
                        size_t n = part->data长度
                        if (itype == 2)
                            rlt = CTZSignCommon::TZGetCurentSignGM (part->data->data,n,
                                                                    signdata.sig_sealinfo,
                                                                    signdata.sig_person,
                                                                    signdata.sig_validtime,
                                                                    signdata.sig_type,
                                                                    pmsgbox);
                        else if(itype == 1)
                            rlt = CTZSignCommon::TZGetCurentCert (part->data->data,n,signdata.sig_cert,pmsgbox);
                                从签章数据中提取签名证书
                        'ofd_drop_part(ctx,xref,part);
                    将 vecssign[k] 压入 mvecssign 中
                *pvecssign = mvecssign;  
                遍历vecssign
                    遍历vecssign[j].vecsignloc #如多页定点签章，一个章可能有多个位置索引
                        找到与 page->fix->pageid 一致的位置索引
                            'fz_rect rect = vecssign[j].vecsignloc[k].sig_location
                                if(鼠标点击位置p in rect)
                                    *selctedSign = vecssign[j]
                                    (*selctedSign).intsignloc = k
                    如果找到了鼠标点击的印章
                        sigFieldName = vecssign[j].sig_filedname = "Doc_0/Signs/Sign_0/Signature.xml"
                        *pselctedSign = selctedSign;
                        结束循环
    m_vecssign = *(pvecssign)；
    'deletesignp(pvecssign);
        delete pvecssign
    m_sigFieldName = sigFieldName
    m_SelctedSign = *pselctedSign
    'deletesignssigndata(pselctedSign);
        delete pselctedSign
    
=======================================================================================