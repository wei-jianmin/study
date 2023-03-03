CTZReaderUIDoc::OnOpenDocument{  获取视图对象,调用CTZReaderUIView::TZOpenPdf2{    获取文档对象    测试文档能否正常打开    将宽字节的ofd文件名m_gapp.wbuf转为多字节存到m_gapp.filename    pdfapp_open_progressive{      fz_register_document_handlers()      fz_open_document{ //准备doc->first_fixdoc链表和doc->first_page链表        ofd_open_document{  //准备doc->first_fixdoc链表和doc->first_page链表          fz_stream *file = fz_open_file(ctx, filename){            打开文件，创建文件读写流，返回流          }          return fz_document *doc=ofd_open_document_with_stream(ctx, file){ //准备doc->first_fixdoc链表和doc->first_page链表            ofd_document *doc;            为doc结构体创建堆内存            调用ofd_init_document，初始化doc            doc->zip = fz_open_zip_archive_with_stream(ctx, file);            ofd_read_page_list(ctx, doc){                 ofd_read_and_process_multofd_part(ctx,doc, "OFD.xml", NULL){  //创建并设置doc->first_fixdoc链表                调用ofd_parse_ofddata_imp解析文档{                  如果是DocRoot节点:{                    读取节点内容(Document.xml路径)                    ofd_add_fixed_document{                      如果doc->first_fixdoc中已经有相应节点，返回                      创建ofd_fixdoc *fixdoc堆内存                      Document.xml文件名存给name成员，其它成员赋空                      将fixdoc附加到doc->first_fixdoc链表中                    }                    doc->current_docpath = strdup(Document.xml路径)                  }                  如果是Signatures节点:{                    读取节点内容，获取到signature.xml文件的路径                    调用ofd_newsetSigns，解析此文件{}                  }                  迭代查询                }              }              遍历doc->first_fixdoc链表{    //完善doc->first_fixdoc链表，创建并设置doc->first_page链表                ofd_read_and_process_metadata_part{                  调用ofd_parse_metadata_imp，解析Document.xml文档{                    如果是DocRoot节点{不会用到，该文档中没有此节点}                    如果是Signature节点{}                    如果是Signatures节点{}                    如果是Page节点{ //创建并设置doc->first_page链表                      读取ID、Width、Height、BaseLoc属性值                      如果该节点下还有子节点(Annotations.xml文件中){                        找到FileLoc子节点                        遍历temppage=doc->first_page节点，找到id与当前id一致的页面节点                        读取当前节点的值(annotation.xml文件路径),存到temppage->annoname成员中                      }                      根据doc->current_docpath值，构造出BaseLoc的完整路径                      ofd_add_fixed_page{                        遍历doc->first_page链表，如果存在名字与BaseLoc相同的节点，返回                        ofd_fixpage *page;                        为page申请堆内存                        page->name记录Content.xml路径名                        page->width,height记录页面大小                        page->pageid记录ID                        page->number=doc->page_count++;                        其它成员赋空                        将page附加到doc->first_page链表中                      }                    }                    如果是Outlines节点{ //完善doc->first_fixdoc链表                      fixdoc->outline = strdup(fixdoc->name);                    }                    如果是Annotations节点{  //完善doc->first_fixdoc链表                      读取节点文本内容(Annotations.xml),存到fixdoc->annotations中                     }                    迭代查询                  }                }                如果ofddoc->annotations在上一步解析中得到值，[ofddoc为first_fixdoc链表节点]                调用ofd_read_and_process_metadata_part，解析Annotations.xml文档{                  调用ofd_parse_metadata_imp，解析Document.xml文档{                    如果是DocRoot节点{不会用到，该文档中没有此节点}                    如果是Signature节点{不会用到，该文档中没有此节点}                    如果是Signatures节点{不会用到，该文档中没有此节点}                    如果是Page节点{为页面节点设置注视文件路径，具体参上个函数解析}                    如果是Outlines节点{不会用到，该文档中没有此节点}                    如果是Annotations节点{虽然有代码，但不执行任何有意义操作}                    迭代查询                  }                }              }            }          }        }      }      fz_needs_password      根据filename(函数传来参数),设置app->doctitle      设置app->pagecount      加载文档大纲app->outline = fz_load_outline{ 略 }      设置app->pageno，app->resolution      app->shrinkwrap=1;app->rotate=0;app->panx=0;app->pany=0;      为app->pagetable申请空间      pdfapp_showpage{        设置光标样式        if(loadpage/*参数*/){          pdfapp_loadpage{  //最终主要得到页面的display_list链表节点            //为app->page=new ofd_page，并为page->super,page->fix,page->root,page->annoroot赋值            app->page = fz/*ofd*/_load_page(app->ctx,app->doc, app->pageno - 1){    //只处理某一页              遍历doc->first_page链表,找到第number(参数)个节点{
                ofd_load_fixed_page{
                  根据找到的doc->first_page[n]节点，可以得到content.xml文件的路径                  将content.xml解析成树(root)                  找到树的Area节点，得到页面大小，完善doc->first_page[n]节点的width和height                  根据找到的doc->first_page[n]节点，可以得到annotation.xml文件的路径                  将annoname.xml解析成树(annoroot)                }
                page = fz_new_derived_page(ctx, ofd_page){                  申请ofd_page大小的内存                }                为page->super指定相应的处理函数                page->doc=doc(参数传来),并增加引用计数                page->fix = doc->first_page[n]                page->root = root                page->annoroot = annoroot                返回page              }            }            fz_bound_page{              根据page->fix->width,page->fix->height,得到矩形区域，存给app->page_bbox            }            app->page_list = fz_new_display_list{申请fz_display_list结构体内存}            fz_device *mdev=fz_new_list_device{              fz_list_device *dev = fz_new_derived_device{申请fz_list_device结构体大小内存}              为dev->super指定处理函数              dev->list=app->page_list              初始化dev的其它成员              返回dev->super的地址            }            //解析app->page的内容，即app->page->root、doc->first_sign和app->page->annoroot的各个子节点            fz_run_page_contents(app->ctx, app->page, mdev, &fz_identity, &cookie){              ofd_run_page(){                ofd_parse_fixed_page(){                  参考page->fix->name，得到Doc_N/Document.xml和Doc_N/PublicRes.xml,                  解析资源文件，分别存到fz_xml *DocResRoot和fz_xml *PubResRoot中                  查找page->root(content.xml)下的Content节点,用node临时记录                  如果node不为空{                    找到node下的layer节点，用node临时记录                    如果node不为空{                      遍历得到layer的每个一级子节点，用node临时记录                      ofd_parse_element解析node节点{                        如果是"ImageObject"{}                        如果是"PathObject"{                          ofd_parse_graph{                            获取"CTM","Boundary","Fill","Stroke","join","MiterLimit",                            "LineWidth","Cap","DashOffset"等属性的值，***_att存储
                            获取"FillColor","StrokeColor","AbbreviatedData"节点的值                            if(image_ctm_att){  //如果node节点有CTM属性
                              根据该属性得到float fctmd[6],                              否则fctmd=fz_identity                            }                            if(Stroke_fillcolor_att){   //"StrokeColor"节点                              为fz_stroke_state *stroke/*线样式*/申请内存                              设置stroke的相应成员值                            }                            if(! image_boundary_att) return;                            根据fctmd和ctm(参数),得到local_ctm                            if(data_value){  //AbbreviatedData节点下的值，绘图数据                              根据Boundary属性，得到fz_path *path                              fz_path *stroke_path=path                            }                            if (Stroke_fillcolor_att){   //"StrokeColor"节点                              fz_bound_path(ctx, stroke_path, stroke, &fz_identity, &area);                              测量绘制路径所占的区域大小                            }                            else{                              fz_bound_path(ctx, path, NULL, &fz_identity, &area);                            }                            if(path_fillcolor_att){  //"FillColor"节点                              ofd_parse_color(path_fillcolor_att, &colorspace, samples){
                                colorspace = ctx->colorspace->rgb                                samples[0]=1/255.0                                samples[1]=r/255.0                                samples[2]=g/255.0                                samples[3]=b/255.0                              }                              ofd_set_color(){                                将colorspace，samples存在doc的相关成员中                                doc->alpha=1                              }                              if(alpha_att){ //"FillColor"，“StrokeColor”节点下都有Alpha属性                                doc->alpha=alpha_att/255.0                              }                              doc->alpha *= alpha/*参数*//255.0                              fz_fill_path(doc->dev,path,doc->colorspace,doc->color,doc->alpha,...){
                                fz_list_fill_path(...){
                                  fz_bound_path(ctx, path, NULL, ctm, &rect);                                  fz_append_display_node(dev,"FZ_CMD_FILL_PATH",color,colorpath,path,rect,alpha,ctm,..){}                                }                              }                            }                            if(Stroke_fillcolor_att){   //"StrokeColor"节点
                              ofd_parse_color(Stroke_fillcolor_att, &colorspace, samples){}                              ofd_set_color(doc, colorspace, samples){}                              fz_stroke_path(doc->dev,stroke_path,stroke,colorspace,color,alpha,...){}                            }                          }                        }                        如果是"TextObject"{     //生成显示节点链表(display_node)
                          获取根节点的font_uri_att="Font",                            font_size=font_size_att="Size",                            font_Weight_att="Weight",                            style_att="Italic",                            fontBoundary="Boundary",                            fontCTM="CTM"=fctmd[6]属性，再结合ctm参数，到的locat_ctm                          查找"FillColor","TextCode","CGTransform"子节点                              分别获取fill_att="Value",                            origin_x_att="X",origin_y_att="Y",delta_att="DeltaX",                            code_position="CodePosition"属性                            并在进一步查找子节点，获取                            unicode_att="具体文字内容"                            glyph_index="字符索引列表"                          fill_uri=opacity_mask_uri=base_uri(参数)                          if (!font_size_att || !font_uri_att || !origin_x_att || !origin_y_att)  return;                          在字体缓冲区里查找或在文件/本地加载字体，存给fz_font *font                          如果style_att不为空，设置font->flags的倾斜属性为true                          如果font_Weight_att属性不为空，且不为400，设置font->flags的粗体属性为true                          根据fontBoundary，得到origin_x,origin_y,再对该坐标点做locat_ctm矩阵变换                          if(glyph_index){
                            fz_text *text = ofd_parse_glyphs_imp2(...){...}                          }                          else{                            //
                            fz_text *text = ofd_parse_glyphs_imp(                              local_ctm,font,font_size,origin_x,origi_y,delta_att,                              unicode_att,[code_position,glyph_index],...){
                              fz_text *text=fz_new_text(ctx){申请fz_text内存空间，并返回该内存}                              while(处理每一个字){                                得到一个子的unicode值                                根据font和字符编码，得到字的索引位置glyph_index                                根据font和glyph_index，测量文字，得到ofd_glyph_metrics mtx(包含水平步进量、垂直步进量、水平位置)                                tm.e = x +                                 fz_show_glyph{
                                  fz_text_span *span = fz_add_text_span(ctx, text, font, wmode, bidi_level, markup_dir, lang, trm){
                                    为text->head链表创建新的fz_text_span节点，并将参数记录在节点中                                  }                                  为span下的item链表(fz_text_item)分配必要节点内存                                  将字符的unicode值、索引值、偏移量记录在span->items[span->len]下                                }                                //得到下次文字的起始位置                                if(pdelta) {   //如果为每个字专门指定了偏移量                                  x+=                                }                                else{                                  x+=                                }                              }                            }                            return text                          }                          if(fill_att){ //如果文字有填充色
                            ofd_parse_color{解析fill_att,得到float samples[32],fz_colorspace *colorspace;}                            ofd_set_color{将samples和colorspace存到doc下,并设doc->alpha=1}                            fz_fill_text{                              fz_rect rect=fz_bound_text{
                                遍历text->head的每一个链表节点{
                                  根据span->font和span->items[n]的字形索引、span->trm,参数ctm等，得到每个字的矩形大小                                  计算出所有字符所占的矩形大小                                }                                fz_list_fill_text{                                  fz_append_display_node("FZ_CMD_FILL_TEXT",rect,color,colorspace,alpha,ctm,text等){                                    ......                                  }                                }                              }                            }                          }                        }                        如果是"CompositeObject"{}                        如果是"PageBlock"{}                      }                    }                  }                  遍历doc->first_sign链表(用ofdsign临时记录){                    如果节点的id(ofdsign->pageid)和当前页面id(page->fix->pageid)一致{                      if (ofdsign->picpath != NULL){                        ofd_parse_sign{}                      }                    }                  }                  如果page->annoroot不为空{                    ......                  }                }              }            }            ？{              ？？？            }            app->page_links=fz_load_links{  //在ofd中应该不起作用              ofd_load_links{   //在ofd中应该不起作用                ofd_load_links_in_fixed_page{
                  if (!page->root) return;                  如果在page->root下能找到FixedPage.Resources子节点{
                    ofd_resource *dict = ofd_parse_resource_dictionary                  }                  for循环遍历page->root的一级子节点，临时存给node{
                    ofd_load_links_in_element{
                      如果node名字为"Path"{}                      如果node名字为"Glyphs"{}                      如果node名字为"Canvas"{}
                      如果node名字为"AlternateContent"{}                    }                  }                }              }            }          }          //ofd_bound_page{根据page->fix->width，page->fix->height，得到矩形区域，返回}           app->page_text = fz_new_stext_page{
            fz_pool *pool = fz_new_pool{    //在堆中申请一个大的存储池
              fz_pool* pool = new fz_pool              pool->head = pool->tail = new fz_pool_node              pool->pos = mem //mem为fz_pool_node中64k内存的起始位置              pool->end = mem + 64k              (**)fz_pool和fz_pool_node的定义[
                struct fz_pool_s                {                    fz_pool_node *head, *tail;                    char *pos, *end;                };                struct fz_pool_node_s   //(64k + 4)Byte 的内存区域                {                    fz_pool_node *next;                    char mem[64 << 10]; // 64k                };              ]            }            //在pool堆中获取sizeof(*page)大小的空间(4字节对齐),并返回该段空间的指针            fz_stext_page *page =fz_pool_alloc(ctx, pool, sizeof(*page)){
              size=sizeof(*page) //=28;              size +=n,使其可以被4整除              char* p=pool->pos              pool->pos += size            }            (**)fz_stext_page的定义[
              //A text page is a list of blocks, together with an overall bounding box.              struct fz_stext_page_s{                  fz_pool *pool;                  fz_rect mediabox;                  fz_stext_block *first_block, *last_block;              };              //A text block is a list of lines of text (typically a paragraph), or an image.              struct fz_stext_block_s              {                  int type;                  fz_rect bbox;                  union {                      struct { fz_stext_line *first_line, *last_line; } t;                      struct { fz_matrix transform; fz_image *image; } i;                  } u;                  fz_stext_block *prev, *next;              };              //A text line is a list of characters that share a common baseline.              struct fz_stext_line_s              {                  int wmode; /* 0 for horizontal, 1 for vertical */   //行（0）和列（1）                  fz_point dir; /* normalized direction of baseline */                  fz_rect bbox;                  fz_stext_char *first_char, *last_char;                  fz_stext_line *prev, *next;              };              //A text char is a unicode character, the style in which is appears, and              //the point at which it is positioned.              struct fz_stext_char_s              {                  int c;                  fz_point origin;                  fz_rect bbox;                  float size;                  fz_font *font;                  fz_stext_char *next;              };            ]            page->pool = pool          }          if (app->page_list || app->annotations_list){
            fz_device *tdev = fz_new_stext_device(app->ctx, app->page_text, NULL);			//注意，这里创建的tdev里面只有有关文字处理的函数指针是有值的，其它都是空的，			//所以pdfapp_runpage函数只能解析处理显示节点链表中有关文字的部分            pdfapp_runpage{ //解析处理显示节点链表
              if (app->page_list)                fz_run_display_list(){
                  for遍历app->page_list的每一个节点，用node/n依次临时存储各个节点{
                    ::说明(fz_display_node的结构特点):[
                      直观的fz_display_node只是一个占4字节的结构体区域，但实际，这个DWORD区域只是一个                      内存标志，也就是说，这4字节后面的区域才是真正的数据内容，这后面的数据往往有多个                      数据段，每个数据段与结构体中的一个成员向对应，如果结构体的每个成员是布尔类型的，                      则他对应的数据段肯定是定长的，如果是非布尔类型的，则指明了对应数据段的长度                    ]                    分析结构体的各个成员，先得到如下数据:                    rect,colorspace,color,alpha,ctm.e,ctm.f,stroke,path,clipped等                    visible:                    switch(n.cmd){
                    case FZ_CMD_FILL_PATH:                      fz_fill_path(dev,path,...){
                        fz_draw_fill_path(dev,path,even_odd,..){                          结构体说明：[
                            struct fz_draw_device_s                            {                              fz_device super;                              fz_matrix transform;                              fz_rasterizer *rast;                              fz_default_colorspaces *default_cs;                              fz_colorspace *proof_cs;                              int flags;                              int resolve_spots;                              int top;                              fz_scale_cache *cache_x;                              fz_scale_cache *cache_y;                              fz_draw_state *stack;                              int stack_cap;                              fz_draw_state init_stack[STACK_SIZE];                            };                             struct fz_scale_cache_s                            {                              int src_w;                              float x;                              float dst_w;                              fz_scale_filter *filter;                              int vertical;                              int dst_w_int;                              int patch_l;                              int patch_r;                              int n;                              int flip;                              fz_weights *weights;                            };                              struct fz_draw_state_s {                              fz_irect scissor;                              fz_pixmap *dest;                              fz_pixmap *mask;                              fz_pixmap *shape;                              fz_pixmap *group_alpha;                              int blendmode;                              int id, encache;                              float alpha;                              fz_matrix ctm;                              float xstep, ystep;                              fz_irect area;                            };                          ]
                          dev由fz_device*强转为fz_draw_device类型指针                          fz_draw_state *state = &dev->stack[dev->top];                          bbox=fz_pixmap_bbox_no_ctx(state->dest/*fz_pixmap类型*/){
                            根据state->dest->x,y,w,h成员，得到bbox                          }                          fz_intersect_irect(bbox,&state->scissor/*裁剪*/){}                          fz_flatten_fill_path(dev->rast,path,ctm,flatness/*float*/,&bbox){
                            ......                          }                          ......                        }                      }                      break;                    case FZ_CMD_STROKE_PATH:                      fz_stroke_path(dev,path,...){
                                              }                      break;                    case FZ_CMD_CLIP_PATH:                      break;                    case FZ_CMD_FILL_TEXT:                        //此时node指向显示节点后面的fz_text数据区域                      //根据显示节点，得到每个文字，填充到dev->page中                      fz_fill_text(dev,*(fz_text **)node,...){
                        fz_stext_fill_text(){
                          fz_stext_device *tdev = (fz_stext_device*)dev;                          fz_text_span *span = text->head;                          tdev->new_obj = 1;                          遍历span指向的每个节点(用span临时存储){
                            fz_stext_extract(tdev,span,ctm){    
                              遍历span->items的链表的每个节点{
                                根据span->item[n].gid/*字形索引*/和span->wmode,得到步进量adv                                fz_add_stext_char(){    //根据显示节点，得到每个文字，填充到dev->page中                                  if (!(dev->flags & FZ_STEXT_PRESERVE_LIGATURES/*预留节点*/)){
                                    switch(span->item[n].ucs){                                    case 0xFB00: /* ff */                                      fz_add_stext_char_imp(ctx, dev, font, 'f', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'f', -1, trm, 0, wmode);                                      return;                                    case 0xFB01: /* fi */                                      fz_add_stext_char_imp(ctx, dev, font, 'f', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'i', -1, trm, 0, wmode);                                      return;                                    case 0xFB02: /* fl */                                      fz_add_stext_char_imp(ctx, dev, font, 'f', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'l', -1, trm, 0, wmode);                                      return;                                    case 0xFB03: /* ffi */                                      fz_add_stext_char_imp(ctx, dev, font, 'f', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'f', -1, trm, 0, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'i', -1, trm, 0, wmode);                                      return;                                    case 0xFB04: /* ffl */                                      fz_add_stext_char_imp(ctx, dev, font, 'f', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'f', -1, trm, 0, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 'l', -1, trm, 0, wmode);                                      return;                                    case 0xFB05: /* long st */                                    case 0xFB06: /* st */                                      fz_add_stext_char_imp(ctx, dev, font, 's', glyph, trm, adv, wmode);                                      fz_add_stext_char_imp(ctx, dev, font, 't', -1, trm, 0, wmode);                                      return;                                    }                                  }
                                  if (!(dev->flags & FZ_STEXT_PRESERVE_WHITESPACE/*预留空白*/)){                                  //根据显示节点，得到每个文字，填充到dev->page中
                                    switch (c){                                    case 0x0009: /* tab */                                    case 0x0020: /* space */                                    case 0x00A0: /* no-break space */                                    case 0x1680: /* ogham space mark */                                    case 0x180E: /* mongolian vowel separator */                                    case 0x2000: /* en quad */                                    case 0x2001: /* em quad */                                    case 0x2002: /* en space */                                    case 0x2003: /* em space */                                    case 0x2004: /* three-per-em space */                                    case 0x2005: /* four-per-em space */                                    case 0x2006: /* six-per-em space */                                    case 0x2007: /* figure space */                                    case 0x2008: /* punctuation space */                                    case 0x2009: /* thin space */                                    case 0x200A: /* hair space */                                    case 0x202F: /* narrow no-break space */                                    case 0x205F: /* medium mathematical space */                                    case 0x3000: /* ideographic space */                                      c = ' ';                                    }                                  }                                  fz_add_stext_char_imp(ctx, dev, font, c, glyph, trm, adv, wmode){
                                    fz_stext_page *page = dev->page;                                      fz_stext_block *cur_block = page->last_block;                                    如果cur_block类型不是FZ_STEXT_BLOCK_TEXT，cur_block=NULL;                                    fz_stext_line *cur_line = cur_block ? cur_block->u.t.last_line : NULL;                                    根据wmode，trm得到文字方向dir,ndir                                    根据trm,得到文字大小size                                    ......                                    add_text_block_to_page(){...}                                    ......                                    add_line_to_block(){...}                                    ......                                    add_char_to_line(){...}                                    ......                                  }                                }                              }                            }                          }                        }                      }                      break;                    case FZ_CMD_STROKE_TEXT:                      break;                    ......                    }                  }                }              if (app->annotations_list)                fz_run_display_list(){
                                  }            }          }        }        if(drawpage){
                  }      }    }  }}结构体参考{struct ofd_fixdoc_s{  char *name;			//"Doc_N/Document.xml"  char *outline;		//"Doc_N/Document.xml"  char *annotations;	//"Doc_N/Annotations.xml"  ofd_fixdoc *next;};struct ofd_fixpage_s{  char *name;			//Doc_N/Pages/Page_N/Content.xml  char *annoname;		//Doc_N/Pages/Page_N/Annotation.xml  int number;  int width;  int height;  int pageid;  int links_resolved;   //bool标志  fz_link *links;  ofd_fixpage *next;};struct fz_pool_s{    fz_pool_node *head, *tail;    char *pos, *end;};struct fz_pool_node_s   //(64k + 4)Byte 的内存区域{    fz_pool_node *next;    char mem[64 << 10]; // 64k};//A text page is a list of blocks, together with an overall bounding box.struct fz_stext_page_s{  fz_pool *pool;  fz_rect mediabox;  fz_stext_block *first_block, *last_block;};//A text block is a list of lines of text (typically a paragraph), or an image.struct fz_stext_block_s{  int type;  fz_rect bbox;  union {      struct { fz_stext_line *first_line, *last_line; } t;      struct { fz_matrix transform; fz_image *image; } i;  } u;  fz_stext_block *prev, *next;};//A text line is a list of characters that share a common baseline.struct fz_stext_line_s{  int wmode; /* 0 for horizontal, 1 for vertical */   //行（0）和列（1）  fz_point dir; /* normalized direction of baseline */  fz_rect bbox;  fz_stext_char *first_char, *last_char;  fz_stext_line *prev, *next;};//A text char is a unicode character, the style in which is appears, and//the point at which it is positioned.struct fz_stext_char_s{  int c;  fz_point origin;  fz_rect bbox;  float size;  fz_font *font;  fz_stext_char *next;};}