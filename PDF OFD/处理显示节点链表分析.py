struct fz_storable
    int refs;
    fz_store_drop_fn *drop;
struct fz_display_node  占4字节长度
	unsigned int cmd    : 5;
	unsigned int size   : 9;
	unsigned int rect   : 1;
	unsigned int path   : 1;
	unsigned int cs     : 3;
	unsigned int color  : 1;
	unsigned int alpha  : 2;
	unsigned int ctm    : 3;
	unsigned int stroke : 1;
	unsigned int flags  : 6;
struct fz_display_list
    fz_storable storable;
	fz_display_node *list;  //以数组存放
	fz_rect mediabox;
	int max;    
	int len;                //指示list数组元素个数
enum fz_display_command
	FZ_CMD_FILL_PATH            = 0,
	FZ_CMD_STROKE_PATH          = 1,
	FZ_CMD_CLIP_PATH            = 2,
	FZ_CMD_CLIP_STROKE_PATH     = 3,
	FZ_CMD_FILL_TEXT            = 4,
	FZ_CMD_STROKE_TEXT          = 5,
	FZ_CMD_CLIP_TEXT            = 6,
	FZ_CMD_CLIP_STROKE_TEXT     = 7,
	FZ_CMD_IGNORE_TEXT          = 8,
	FZ_CMD_FILL_SHADE           = 9,
	FZ_CMD_FILL_IMAGE           = 10,
	FZ_CMD_FILL_IMAGE_MASK      = 11,
	FZ_CMD_CLIP_IMAGE_MASK      = 12,
	FZ_CMD_POP_CLIP             = 13,
	FZ_CMD_BEGIN_MASK           = 14,
	FZ_CMD_END_MASK             = 15,
	FZ_CMD_BEGIN_GROUP          = 16,
	FZ_CMD_END_GROUP            = 17,
	FZ_CMD_BEGIN_TILE           = 18,
	FZ_CMD_END_TILE             = 19,
	FZ_CMD_RENDER_FLAGS         = 20,
	FZ_CMD_DEFAULT_COLORSPACES  = 21 

struct fz_text
	int refs;
	fz_text_span *head, *tail;

struct fz_text_span
	fz_font *font;
	fz_matrix trm;
	unsigned wmode : 1;		/* 0 horizontal, 1 vertical */
	unsigned bidi_level : 7;	/* The bidirectional level of text */
	unsigned markup_dir : 2;	/* The direction of text as marked in the original document */
	unsigned language : 15;		/* The language as marked in the original document */
	int len, cap;
	fz_text_item *items;
	fz_text_span *next;

struct fz_text_item_s
{
	float x, y;
	int gid; /* -1 for one gid to many ucs mappings */
	int ucs; /* -1 for one ucs to many gid mappings */
};

==========================================================================================
''' 
    fz_display_list结构：
    一个fz_display_node结构的大小是4字节
    fz_display_node的元素值标示了后面紧跟了哪些成员
    如：rect不为0，说明后面至少跟了sizeof(fz_rect)个字节，存放rect信息
    注意fz_display_node中的这些rect、path、cs、color等标明
    fz_display_node之后的rect、path、cs、color（如果有的话）也是按这个顺序出现的
    注：cs是不占fz_display_node之后的空间的，它的值直接标明了使用哪种颜色空间
    注：cmd对应的成员是出现在最后的
'''
==========================================================================================
fz_rect mediabox;
app->page_text = fz_new_stext_page(app->ctx, fz_bound_page(app->ctx, app->page, &mediabox));
tdev = fz_new_stext_device(app->ctx, app->page_text, NULL);
ctm=fz_identity;
fz_run_display_list(app->ctx,fz_display_list *list=app->page_list,fz_device *dev=tdev,
                    fz_matrix *top_ctm=&ctm,fz_rect * scissor=&fz_infinite_rect, cookie);
    遍历list->list
        fz_display_node n = 当前list节点内容
        fz_display_node *next_node = 当前节点位置 + n.size
        。。。
        void fz_stext_fill_text(fz_context *ctx, fz_device *dev, fz_text *text,
                                fz_matrix *ctm, fz_colorspace *colorspace, float *color, 
                                float alpha, fz_color_params *color_params)
            fz_stext_device *tdev = (fz_stext_device*)dev;
            fz_text_span *span;
            tdev->new_obj = 1;                    
            遍历text->head节点
                fz_stext_extract(ctx, tdev, span, ctm);
                    float adv = 根据字形索引gid，计算得到的步进量，如果gid<0，则adv=0
                    fz_add_stext_char(ctx, dev, font, int c=span->items[i].ucs, int glyph=span->items[i].gid, &trm, adv, int wmode=span->wmode);
                        ...
                        fz_add_stext_char_imp(ctx, dev, font, c, glyph, trm, adv, wmode);
fz_close_device(app->ctx,tdev);
fz_drop_device(app->ctx,tdev);