//���ڹ�ϵ
������{
  �˵�������
  ����������
  ״̬������
  ��������1
  ��������2
  ������
  ��������n
  MDIClient����/*�ͻ�������*/{
    ��ͼ����1
    ��ͼ����2
    ������
    ��ͼ����n
  }
}
//���ĵ���������ļ�ʱ(!!��ͷ���У���ʾ��ǰ��û��ִ�е�)
CDocument* CTZReaderUIApp::OpenDocumentFile(LPCTSTR lpszFileName) {
  return CWinAppEx::OpenDocumentFile(lpszFileName){
    return m_pDocManager/*CMultiDocTemplate*/->OpenDocumentFile(lpszFileName){
      ����ļ���
      �����ļ���ݷ�ʽ
      ����m_templateList���õ�CDocTemplate*/*�ĵ�ģ��*/�ڵ�{
        !!�����ĵ�ģ���е��ļ���/*m_docList*/,�����lpszFileNameһ�£�����yesAlreadyOpen��ͬʱ�����ĵ�ָ��
        �����һ�£����ļ��ĺ�׺�����ĵ�ģ���д洢�ĺ�׺��һ�£�����yesAttemptNative ( �� )
        !!������������������㣬����yesAttemptForeign
      }
      !!�������һ�����ҵ���Ӧ�Ĵ��ĵ����򼤻���ĵ���Ӧ�Ĵ��ڣ����������ĵ�ָ��
      ��������ҵ����ʵ��ĵ�ģ�壬�������ؿ�
      return pBestTemplate/*CMultiDocTemplate*/->OpenDocumentFile(szPath) {
        CDocument* pDocument = CreateNewDocument() {
          ��̬����CTZReaderUIDoc����
          Ϊ�ö���m_pDocTemplate��ֵthis/*��ǰ�ĵ�ģ��*/
          ���ĵ���ӵ�m_DocList/*ģ��ĳ�Ա����*/��
        }  
        CFrameWnd* pFrame = CreateNewFrame(pDocument, NULL) {
          CFrameWnd* pFrame = ��̬����ChildFrame����
          pFrame/*CMDIChildWnd*/->LoadFrame(...) {
            Create/*CMDIChildWnd*/(...){
              ����������������ھ��Ϊ�գ�ʹ�ó��������ھ����Ϊ�����
              ע�ᴰ����
              HWND hWnd = ��pParentWnd->m_hWndMDIClient����WM_MDICREATE��Ϣ {
                ����CMDIChildWndEx::OnCreate(LPCREATESTRUCT lpCreateStruct) {
                //�ú���Ӧ�þ��ǿͻ������ڵ���Ӧ���� 
                  m_pMDIFrame = ��ȡ����������ָ��
                  CMDIChildWnd::OnCreate(...) {
                    return CFrameWnd::OnCreateHelper(...) {
                      OnCreateClient/*CFrameWnd*/(lpcs, pContext) {
                        CreateView/*CreateView*/(...) {
                          CWnd* pView = ������ͼ���ڶ���;
                          pView/*CTZReaderUIView*/->Create(...) {
                            ����CTZReaderUIView::OnCreate(..) {
                              CView::OnCreate(..) {
                                CWnd::OnCreate(..) {}
                                ���û�ĵ���AddView {
                                  m_viewList.AddTail(pView);
                                  pView->m_pDocument = this/*��ĵ�*/;
                                }
                              }
                              ������
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
              ���ô�����ʽ������ڡ���pParentWnd->m_hWndMDIClient����ˢ�²˵���Ϣ(WM_MDIREFRESHMENU)
              ��������
            }
          }
        }
        if(����ָ�����ļ�·��Ϊ��){
          �½��հ��ĵ�
        }
        else{
          pDocument/*CTZReaderUIDoc*/->OnOpenDocument(lpszPathName){
            ...�Զ���ʵ��(��TZOpenPdf2...)
          }
          pDocument->SetPathName(lpszPathName);
        }
        InitialUpdateFrame/*CDocTemplate*/{
          pFrame/*CFrameWnd*/->InitialUpdateFrame(pDoc, bMakeVisible) {
            ������û�д洢���ͼָ�룬�����ø�ֵ(SetActiveView)
            �������ָ������Ϊvisible {
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