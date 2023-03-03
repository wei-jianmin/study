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
						如果buf的前5个字符不是"%PDF-",报"cannot recognize version marker"
						doc->version = (int)((buf中的版本号(如1.6)+0.05)*10);
						如果doc->version小于10或大于17，且不为20，则警告不识别的pdf版本
					pdf_load_xref(ctx, doc, buf=&doc->lexbuf.base); //当不是线性化文件时调用该函数
						pdf_read_start_xref(ctx, doc); //获取doc->startxref的值，执行完后，文件指针处于文件末尾
							unsigned char buf[1024];
							fz_seek(ctx, doc->file, 0, SEEK_END);
							doc->file_size = fz_tell(ctx, doc->file);
							int64_t t = (文件大小-buf大小>0) ? 文件大小-buf大小 : 0;
							fz_seek(ctx, doc->file, t, SEEK_SET);	//定位文件指针，以便读文件最后1024字节
							n = fz_read(ctx, doc->file, buf, sizeof buf);	//执行完后，文件指针指向文件末尾
							for(i=sizeof(buf)-strlen("startxref");i>0;i--)	//从buf中找到startxref，继而获取其值
								if(找到startxref的位置)
									定位到startxref之后
									过滤空格
									doc->startxref = startxref之后的值
									return
						pdf_read_xref_sections(ctx, doc, ofs=doc->startxref, buf, read_previous=1);
							while(ofs)
								pdf_populate_next_xref_level(ctx, doc);
									doc->xref_sections增加一个pdf_xref元素
									doc->num_xref_sections元素计数+1
									返回该元素地址
								ofs_list list;	//初始化，使其可以存放10个ofs
									list.len = 0;	
									list.max = 10;
									list.list = fz_malloc_array(ctx, 10, sizeof(*list.list));
								ofs = read_xref_section(ctx, doc, ofs, buf, offsets=&list);
									查找offset，看里面有没有记录ofs的项，有，则让i指向它，否则i指向offset的第1个空元素
									如果i不是offsets中的最后一项，给出警告“ignoring xref recursion with offset %d(ofs)”
									当offsets里面的记录项达到10个后，让其容量扩大一倍
									将ofs存入offset的第一个空位置
									trailer = pdf_read_xref(ctx, doc, ofs, buf);
										定位文件到ofs(即xref处)开始位置
										跳过空白
										如果之后的那个字符是x，说明该xref是明文的
											trailer = pdf_read_old_xref(ctx, doc, buf);
												int xref_len = pdf_xref_size_from_old_trailer(ctx, doc, buf); //解析trailer，拿到size
													跳过空白
													跳过xref
													跳过空白
													while(1)	//跳过间接对象索引表，文件指针定位到之后的trailer
														探测下一个字符，是不是'0'-'9'之间的字符
														不是,break
														读取该行，得出有多少个(len)连续的间接对象索引
														跳过len个间接对象索引（一个间接对象索引的长度是20，包括回车换行符）
													pdf_token tok = pdf_lex(ctx, doc->file, buf);
													。。。
												跳过空白
												跳过xref字符串
												跳过空白
												
										如果之后的那个字符是0到9之间的字符，说明该xref是个间接引用对象
											trailer = pdf_read_new_xref(ctx, doc, buf);
										否则，报异常"cannot recognize xref format"
										return trailer
								if (!read_previous)
									break;
									
									
									
									
									
									
									
									
									
									
									
									
									
									
									
							