//窗口关系
主窗口{
  菜单栏窗口
  工具栏窗口
  状态栏窗口
  浮动窗口1
  浮动窗口2
  。。。
  浮动窗口n
  MDIClient窗口/*客户区窗口*/{
    视图窗口1
    视图窗口2
    。。。
    视图窗口n
  }
}
//多文档程序打开新文件时(!!开头的行，表示当前行没有执行到)
CDocument* CTZReaderUIApp::OpenDocumentFile(LPCTSTR lpszFileName) {
  return CWinAppEx::OpenDocumentFile(lpszFileName){
    return m_pDocManager/*CMultiDocTemplate*/->OpenDocumentFile(lpszFileName){
      检查文件名
      处理文件快捷方式
      遍历m_templateList，得到CDocTemplate*/*文档模板*/节点{
        !!遍历文档模板中的文件名/*m_docList*/,如果与lpszFileName一致，返回yesAlreadyOpen，同时返回文档指针
        如果不一致，但文件的后缀名与文档模板中存储的后缀名一致，返回yesAttemptNative ( √ )
        !!如果上面两条都不满足，返回yesAttemptForeign
      }
      !!如果在上一步中找到对应的打开文档，则激活该文档对应的窗口，函数返回文档指针
      如果不能找到合适的文档模板，函数返回空
      return pBestTemplate/*CMultiDocTemplate*/->OpenDocumentFile(szPath) {
        CDocument* pDocument = CreateNewDocument() {
          动态创建CTZReaderUIDoc对象
          为该对象m_pDocTemplate赋值this/*当前文档模板*/
          将文档添加到m_DocList/*模板的成员变量*/中
        }  
        CFrameWnd* pFrame = CreateNewFrame(pDocument, NULL) {
          CFrameWnd* pFrame = 动态创建ChildFrame对象
          pFrame/*CMDIChildWnd*/->LoadFrame(...) {
            Create/*CMDIChildWnd*/(...){
              如果参数传来父窗口句柄为空，使用程序主窗口句柄作为父句柄
              注册窗口类
              HWND hWnd = 向pParentWnd->m_hWndMDIClient发送WM_MDICREATE消息 {
                引发CMDIChildWndEx::OnCreate(LPCREATESTRUCT lpCreateStruct) {
                //该函数应该就是客户区窗口的响应函数 
                  m_pMDIFrame = 获取程序主窗口指针
                  CMDIChildWnd::OnCreate(...) {
                    return CFrameWnd::OnCreateHelper(...) {
                      OnCreateClient/*CFrameWnd*/(lpcs, pContext) {
                        CreateView/*CreateView*/(...) {
                          CWnd* pView = 创建视图窗口对象;
                          pView/*CTZReaderUIView*/->Create(...) {
                            触发CTZReaderUIView::OnCreate(..) {
                              CView::OnCreate(..) {
                                CWnd::OnCreate(..) {}
                                调用活动文档的AddView {
                                  m_viewList.AddTail(pView);
                                  pView->m_pDocument = this/*活动文档*/;
                                }
                              }
                              。。。
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
              设置窗口样式、激活窗口、向pParentWnd->m_hWndMDIClient发送刷新菜单消息(WM_MDIREFRESHMENU)
              函数返回
            }
          }
        }
        if(参数指定的文件路径为空){
          新建空白文档
        }
        else{
          pDocument/*CTZReaderUIDoc*/->OnOpenDocument(lpszPathName){
            ...自定义实现(含TZOpenPdf2...)
          }
          pDocument->SetPathName(lpszPathName);
        }
        InitialUpdateFrame/*CDocTemplate*/{
          pFrame/*CFrameWnd*/->InitialUpdateFrame(pDoc, bMakeVisible) {
            如果框架没有存储活动视图指针，则设置该值(SetActiveView)
            如果参数指定窗口为visible {
              SendMessageToDescendants(WM_INITIALUPDATE, 0, 0, TRUE, TRUE);
              if (pView != NULL) pView->OnActivateFrame(WA_INACTIVE, this);
              ActivateFrame(nCmdShow);
              if (pView != NULL) pView->OnActivateView(TRUE, pView, pView);
            }
            if (pDoc != NULL) pDoc->UpdateFrameCounts();
            OnUpdateFrameTitle(TRUE);
          }
        }
      }
    }
  }
}