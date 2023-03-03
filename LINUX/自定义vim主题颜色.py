ʹ���������⣺
    clorescheme ������

�Զ�����ɫ�﷨ ���Σ�http://vimdoc.sourceforge.net/htmldoc/syntax.html#attr-list��
    hi [����Ԫ��] [term=ֵ] [cterm=ֵ] [ctermfg=ֵ] [ctermbg=ֵ] 
                  [gui=ֵ] [guifg=ֵ] [guibg=ֵ] [guisp=ֵ]
        hi �����ͬ�� highlight ����
        cterm �� colorterm ����˼
        �����ִ�Сд
    hi clear [����Ԫ��]     ��[����Ԫ��]��ɫ����ΪĬ��
    hi [����Ԫ��] NONE      ��[����Ԫ��]��ɫ����ΪĬ��
    hi  
        չʾ��ǰ��������Ԫ�ص���ɫ��ʾЧ��    
    hi [����Ԫ��]
        չʾָ������Ԫ�ص���ɫ��ʾЧ��
    hi [����Ԫ��] [�ն�����=ֵ]
        ����ָ��Ԫ����ĳ�ն��µ���ɫ��ʾЧ����û�����õģ�����֮ǰ��ֵ��Ĭ��ֵ
        ��������ֵΪNONE
    ����Ԫ�أ�
        ��ע�͡��ؼ��֡����֡��ַ����ȣ��������£�
        �Ƚϳ��õ���
            Cursor��CursorLine��MatchParen��Normal
            DiffAdd��DiffChange��DiffDelete��DiffText
            Search
        ��������Ԫ�ؽ��ܣ�
        ColorColumn	    used for the columns set with 'colorcolumn'
        Conceal		placeholder characters substituted for concealed text (see 'conceallevel')
        Cursor		the character under the cursor
        CursorIM	like Cursor, but used when in IME mode |CursorIM|
        CursorColumn	the screen column that the cursor is in when 'cursorcolumn' is set
                                    
        CursorLine	the screen line that the cursor is in when 'cursorline' is set
        Directory	directory names (and other special names in listings)
        DiffAdd		diff mode: Added line |diff.txt|
        DiffChange	diff mode: Changed line |diff.txt|
        DiffDelete	diff mode: Deleted line |diff.txt|
        DiffText	diff mode: Changed text within a changed line |diff.txt|
        ErrorMsg	error messages on the command line
        VertSplit	the column separating vertically split windows
        Folded		line used for closed folds
        FoldColumn	'foldcolumn'
        SignColumn	column where |signs| are displayed
        IncSearch	'incsearch' highlighting; also used for the text replaced with  ":s///c"
        LineNr		Line number for ":number" and ":#" commands, 
                    and when 'number' or 'relativenumber' option is set.
        MatchParen	The character under the cursor or just before it, 
                    if it is a paired bracket, and its match. |pi_paren.txt|
        ModeMsg		'showmode' message (e.g., "-- INSERT --")
        MoreMsg		|more-prompt|
        NonText		'~' and '@' at the end of the window, characters from
                    'showbreak' and other characters that do not really exist in
                    the text (e.g., ">" displayed when a double-wide character
                    doesn't fit at the end of the line).
        Normal		normal text
        Pmenu		Popup menu: normal item.
        PmenuSel	Popup menu: selected item.
        PmenuSbar	Popup menu: scrollbar.
        PmenuThumb	Popup menu: Thumb of the scrollbar.
        Question	|hit-enter| prompt and yes/no questions
        Search		Last search pattern highlighting (see 'hlsearch').
                    Also used for highlighting the current line in the quickfix
                    window and similar items that need to stand out.
        SpecialKey	Meta and special keys listed with ":map", also for text used
                    to show unprintable characters in the text, 'listchars'.
                    Generally: text that is displayed differently from what it
                    really is.
        SpellBad	Word that is not recognized by the spellchecker. |spell|
                    This will be combined with the highlighting used otherwise.
        SpellCap	Word that should start with a capital. |spell|
                    This will be combined with the highlighting used otherwise.
        SpellLocal	Word that is recognized by the spellchecker as one that is
                    used in another region. |spell|
                    This will be combined with the highlighting used otherwise.
        SpellRare	Word that is recognized by the spellchecker as one that is
                    hardly ever used. |spell|
                    This will be combined with the highlighting used otherwise.
        StatusLine	status line of current window
        StatusLineNC	status lines of not-current windows
                        Note: if this is equal to "StatusLine" Vim will use "^^^" in
                        the status line of the current window.
        TabLine		tab pages line, not active tab page label
        TabLineFill	tab pages line, where there are no labels
        TabLineSel	tab pages line, active tab page label
        Title		titles for output from ":set all", ":autocmd" etc.
        Visual		Visual mode selection
        VisualNOS	Visual mode selection when vim is "Not Owning the Selection".
                    Only X11 Gui's |gui-x11| and |xterm-clipboard| supports this.
        WarningMsg	warning messages
        WildMenu	current match in 'wildmenu' completion
                    The 'statusline' syntax allows the use of 9 different highlights in the
                    statusline and ruler (via 'rulerformat').  The names are User1 to User9.
                    For the GUI you can use the following groups to set the colors for the menu,
                    scrollbars and tooltips.  They don't have defaults.  This doesn't work for the
                    Win32 GUI.  Only three highlight arguments have any effect here: font, guibg,
                    and guifg.
        Menu		Current font, background and foreground colors of the menus.
                    Also used for the toolbar.
                    Applicable highlight arguments: font, guibg, guifg.
                    NOTE: For Motif and Athena the font argument actually
                    specifies a fontset at all times, no matter if 'guifontset' is
                    empty, and as such it is tied to the current |:language| when set.
        Scrollbar	Current background and foreground of the main window's scrollbars.
                    Applicable highlight arguments: guibg, guifg.
        Tooltip		Current font, background and foreground of the tooltips.
                    Applicable highlight arguments: font, guibg, guifg.
                    NOTE: For Motif and Athena the font argument actually
                    specifies a fontset at all times, no matter if 'guifontset' is
                    empty, and as such it is tied to the current |:language| when set.
        ע�⣬����Normal����ɫʱ�����ܻ�Ӱ������������ɫ����ɫ������Ӧ������Normal����ɫ����
    termֵ/ctermֵ/guiֵ
        bold
		underline
		undercurl	not always available
		reverse
		inverse		same as reverse
		italic
		standout
		NONE		no attributes used (used to reset it)
        ����ʹ��������ֵ���ÿո�ָ�
    ctermfgֵ/ctermbgֵ
        ��ֵΪһ�����֣�������ɫ������
        16ɫ�ն�    COLOR NAME 
	    0	        Black ��
	    1	        DarkBlue ����
	    2	        DarkGreen  ����
	    3	        DarkCyan ����
	    4	        DarkRed ���
	    5	        DarkMagenta  Ʒ��
	    6	        Brown, DarkYellow  �ػ����
	    7	        LightGray, Gray ǳ�һ��
	    8	        DarkGray  ���
	    9	        Blue, LightBlue  ����ǳ��
	    10	        Green, LightGreen  �̻�ǳ��
	    11	        Cyan, LightCyan ���ǳ��
	    12	        Red, LightRed ���ǳ��
	    13	        Magenta, LightMagenta  ǳɫ��Ʒ��
	    14	        Yellow, LightYellow  �ƻ�ǳ��
	    15	        White  ��
        8ɫ�ն�     COLOR NAME 
        0	        Black
        1	        DarkRed
        2	        DarkGreen
        3	        Brown, DarkYellow
        4	        DarkBlue
        6	        DarkCyan
        5	        DarkMagenta
        7	        LightGray, LightGrey, Gray, Grey
        0*	        DarkGray, DarkGrey
        1*	        Red, LightRed
        2*	        Green, LightGreen
        3*	        Yellow, LightYellow
        4*	        Blue, LightBlue
        5*	        Magenta, LightMagenta
        6*	        Cyan, LightCyan
        7*	        White
        8ɫ�նˣ�ֻ����ʾ���8����ɫ���£����ֺ����*�ģ���Ϊ����ʱ����ɫ
        ע�⣬������ɫ�����ο�����ͬ�ն˿�����ʾЧ����ͬ
    guifgֵ/guibgֵ/guispֵ
        sp ��special����д
        ���ɫ
        ����ָ��Ϊ��ɫ����
            Red		LightRed	    DarkRed
            Green	LightGreen	    DarkGreen	SeaGreen
            Blue	LightBlue	    DarkBlue	SlateBlue
            Cyan	LightCyan	    DarkCyan
            Magenta	LightMagenta	DarkMagenta
            Yellow	LightYellow	    Brown		DarkYellow
            Gray	LightGray	    DarkGray
            Black	White
            Orange	Purple		    Violet
        Ҳ����ָ��Ϊ�ض���ɫֵ����#ff0000
       
ʵ����
        ��vim a.cpp
        д�ò��Դ��룬������ؼ��֡����֡�ע�͵�
        ���� :hi ���Բ鿴������Щ����Ԫ�أ������ǵĵ�ǰ��ɫ�������
        ���� :hi com 
        ��tab�������Զ���ȫ������ж����ѡ����Զ�ΰ�tab
        ���� :hi comment ctermbg=1
        ���ִ����е�ע������б���ɫ�ˣ�˵��������Ч
ʵ��2��
        ����vim -d �Ƚ��ļ�ʱ�����ָı���жԱ��ǣ���ɫЧ������������
        hi diffchange termbg=1  #�޸����ָı��еı���ɫ
        �� hi clear diffchange  #���ָı��в���ɫ���ı������ͨ��difftext������ɫ��
        
        