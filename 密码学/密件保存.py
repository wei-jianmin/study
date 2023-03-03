void TZReaderUIView::OpenFile(QString fileName, QString url, int *index)
	doc->LoadFile(fileName)
	#bool TZReaderUIDoc::LoadFile(const QString &fileName)
		检查文件是否可读
		检查文件是否为空
		pdfapp_open_progressive(&m_gapp_, m_gapp_.filename, 0, 0, 0)
		#bool TZReaderUIDoc::pdfapp_open_progressive(pdfapp_t *app, char *filename, int reload, int bps,int pagenum)
			fz_context *ctx = app->ctx;
			fz_register_document_handlers(ctx);
			ctx->imuldoc = app->m_multdoc;
			if (bps == 0)	app->doc = fz_open_document(ctx, filename, is_show_seal);
				::fz_document *fz_open_document(fz_context *ctx, const char *filename, int showseal)
					const fz_document_handler *handler;
					fz_stream *file;
					fz_document *doc = NULL;
					handler = fz_recognize_document(ctx, filename); #根据文件名(后缀),找到匹配的handler
					if (handler->open)	return handler->open(ctx, filename, showseal);
						::fz_document * ofd_open_document(fz_context *ctx, const char *filename, int showseal)
							fz_stream *file = fz_open_file(ctx, filename);
							  FILE *file = fz_fopen_utf8(name,"rb");	●●●●●●●●
							  return fz_open_file_ptr(ctx, file);
								  fz_stream *stm;
								  fz_file_stream *state = fz_malloc_struct(ctx, fz_file_stream);
								  state->file = file;
								  stm = fz_new_stream(ctx, state, next_file, close_file);
								  stm->seek = seek_file;
								  return stm;
							fz_document *doc = ofd_open_document_with_stream(ctx, file, showseal);
							fz_drop_stream(ctx, file);
							return (fz_document*)doc;
						::pdf_document *pdf_open_document(fz_context *ctx, const char *filename)
							fz_stream *file = fz_open_file(ctx, filename);
							  FILE *file = fz_fopen_utf8(name,"rb");	●●●●●●●●
							  return fz_open_file_ptr(ctx, file);
							pdf_document *doc = pdf_new_document(ctx, file);
							pdf_init_document(ctx, doc);
							fz_drop_stream(ctx, file);
							return doc;
			其它。。。