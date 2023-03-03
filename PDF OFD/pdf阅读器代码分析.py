TZReaderUIDoc::LoadFile
	pdfapp_open_progressive
		fz_register_document_handlers(ctx);
		app->doc = fz_open_document(ctx, filename, is_show_seal=1);
			fz_document_handler* handler = fz_recognize_document(ctx, filename);
			return handler->open(ctx, filename, showseal);
				fz_stream *file = fz_open_file(ctx, filename);
					FILE *file = fz_fopen_utf8(name, "rb");
					return fz_open_file_ptr(ctx, file);
						fz_file_stream *state = fz_malloc_struct(ctx, fz_file_stream);
						state->file = file;
						fz_stream *stm;
						stm->seek = seek_file;
						stm = fz_new_stream(ctx, state, next_file, close_file);
						return stm;
				pdf_document *doc = pdf_new_document(ctx, file);
					pdf_document *doc = fz_new_derived_document(ctx, pdf_document);
					doc->super.drop_document = (fz_document_drop_fn*)pdf_drop_document_imp;
					doc->super.get_output_intent = (fz_document_output_intent_fn*)pdf_document_output_intent;
					doc->super.needs_password = (fz_document_needs_password_fn*)pdf_needs_password;
					doc->super.authenticate_password = (fz_document_authenticate_password_fn*)pdf_authenticate_password;
					doc->super.has_permission = (fz_document_has_permission_fn*)pdf_has_permission;
					doc->super.load_outline = (fz_document_load_outline_fn*)pdf_load_outline;
					doc->super.resolve_link = (fz_document_resolve_link_fn*)pdf_resolve_link;
					doc->super.count_pages = (fz_document_count_pages_fn*)pdf_count_pages;
					doc->super.load_page = (fz_document_load_page_fn*)pdf_load_page;
					doc->super.lookup_metadata = (fz_document_lookup_metadata_fn*)pdf_lookup_metadata;
					doc->update_appearance = pdf_update_appearance;
					pdf_lexbuf_init(ctx, &doc->lexbuf.base, PDF_LEXBUF_LARGE);
					doc->file = fz_keep_stream(ctx, file);
					return doc;
				pdf_init_document(ctx, doc);
					pdf_load_version(ctx, doc);
						fz_seek(ctx, doc->file, 0, SEEK_SET);
						fz_read_line(ctx, doc->file, buf, sizeof buf);
						���buf��ǰ5���ַ�����"%PDF-",��"cannot recognize version marker"
						doc->version = (int)((buf�еİ汾��(��1.6)+0.05)*10);
						���doc->versionС��10�����17���Ҳ�Ϊ20���򾯸治ʶ���pdf�汾
					pdf_load_xref(ctx, doc, buf=&doc->lexbuf.base); //���������Ի��ļ�ʱ���øú���
						pdf_read_start_xref(ctx, doc); //��ȡdoc->startxref��ֵ��ִ������ļ�ָ�봦���ļ�ĩβ
							unsigned char buf[1024];
							fz_seek(ctx, doc->file, 0, SEEK_END);
							doc->file_size = fz_tell(ctx, doc->file);
							int64_t t = (�ļ���С-buf��С>0) ? �ļ���С-buf��С : 0;
							fz_seek(ctx, doc->file, t, SEEK_SET);	//��λ�ļ�ָ�룬�Ա���ļ����1024�ֽ�
							n = fz_read(ctx, doc->file, buf, sizeof buf);	//ִ������ļ�ָ��ָ���ļ�ĩβ
							for(i=sizeof(buf)-strlen("startxref");i>0;i--)	//��buf���ҵ�startxref���̶���ȡ��ֵ
								if(�ҵ�startxref��λ��)
									��λ��startxref֮��
									���˿ո�
									doc->startxref = startxref֮���ֵ
									return
						pdf_read_xref_sections(ctx, doc, ofs=doc->startxref, buf, read_previous=1);
							while(ofs)
								pdf_populate_next_xref_level(ctx, doc);
									doc->xref_sections����һ��pdf_xrefԪ��
									doc->num_xref_sectionsԪ�ؼ���+1
									���ظ�Ԫ�ص�ַ
								ofs_list list;	//��ʼ����ʹ����Դ��10��ofs
									list.len = 0;	
									list.max = 10;
									list.list = fz_malloc_array(ctx, 10, sizeof(*list.list));
								ofs = read_xref_section(ctx, doc, ofs, buf, offsets=&list);
									����offset����������û�м�¼ofs����У�����iָ����������iָ��offset�ĵ�1����Ԫ��
									���i����offsets�е����һ��������桰ignoring xref recursion with offset %d(ofs)��
									��offsets����ļ�¼��ﵽ10����������������һ��
									��ofs����offset�ĵ�һ����λ��
									trailer = pdf_read_xref(ctx, doc, ofs, buf);
										��λ�ļ���ofs(��xref��)��ʼλ��
										�����հ�
										���֮����Ǹ��ַ���x��˵����xref�����ĵ�
											trailer = pdf_read_old_xref(ctx, doc, buf);
												int xref_len = pdf_xref_size_from_old_trailer(ctx, doc, buf); //����trailer���õ�size
													�����հ�
													����xref
													�����հ�
													while(1)	//������Ӷ����������ļ�ָ�붨λ��֮���trailer
														̽����һ���ַ����ǲ���'0'-'9'֮����ַ�
														����,break
														��ȡ���У��ó��ж��ٸ�(len)�����ļ�Ӷ�������
														����len����Ӷ���������һ����Ӷ��������ĳ�����20�������س����з���
													pdf_token tok = pdf_lex(ctx, doc->file, buf);
													������
												�����հ�
												����xref�ַ���
												�����հ�
												
										���֮����Ǹ��ַ���0��9֮����ַ���˵����xref�Ǹ�������ö���
											trailer = pdf_read_new_xref(ctx, doc, buf);
										���򣬱��쳣"cannot recognize xref format"
										return trailer
								if (!read_previous)
									break;
									
									
									
									
									
									
									
									
									
									
									
									
									
									
									
							