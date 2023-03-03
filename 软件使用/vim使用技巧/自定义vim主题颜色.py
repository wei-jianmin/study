使用现有主题：
    clorescheme 主题名

自定义颜色语法 （参：http://vimdoc.sourceforge.net/htmldoc/syntax.html#attr-list）
    hi [内容元素] [term=值] [cterm=值] [ctermfg=值] [ctermbg=值] 
                  [gui=值] [guifg=值] [guibg=值] [guisp=值]
        hi 命令等同于 highlight 命令
        cterm 是 colorterm 的意思
        不区分大小写
    hi clear [内容元素]     将[内容元素]颜色重置为默认
    hi [内容元素] NONE      将[内容元素]颜色重置为默认
    hi  
        展示当前所有内容元素的颜色显示效果    
    hi [内容元素]
        展示指定内容元素的颜色显示效果
    hi [内容元素] [终端类型=值]
        设置指定元素在某终端下的颜色显示效果，没有设置的，采用之前的值或默认值
        可以设置值为NONE
    内容元素：
        如注释、关键字、数字、字符串等，具体如下：
        比较常用的有
            Cursor、CursorLine、MatchParen、Normal
            DiffAdd、DiffChange、DiffDelete、DiffText
            Search
        部分内容元素介绍：
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
        注意，设置Normal的颜色时，可能会影响其他内容颜色的颜色，所以应先设置Normal的颜色方案
    term值/cterm值/gui值
        bold
		underline
		undercurl	not always available
		reverse
		inverse		same as reverse
		italic
		standout
		NONE		no attributes used (used to reset it)
        可以使用上面多个值，用空格分隔
    ctermfg值/ctermbg值
        该值为一个数字（代表颜色索引）
        16色终端    COLOR NAME 
	    0	        Black 黑
	    1	        DarkBlue 深蓝
	    2	        DarkGreen  深绿
	    3	        DarkCyan 深青
	    4	        DarkRed 深红
	    5	        DarkMagenta  品红
	    6	        Brown, DarkYellow  棕或深黄
	    7	        LightGray, Gray 浅灰或灰
	    8	        DarkGray  深灰
	    9	        Blue, LightBlue  蓝或浅蓝
	    10	        Green, LightGreen  绿或浅绿
	    11	        Cyan, LightCyan 青或浅青
	    12	        Red, LightRed 红或浅红
	    13	        Magenta, LightMagenta  浅色的品红
	    14	        Yellow, LightYellow  黄或浅黄
	    15	        White  白
        8色终端     COLOR NAME 
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
        8色终端（只能显示最多8种颜色）下，数字后面带*的，表为粗体时的颜色
        注意，上面颜色仅供参考，不同终端可能显示效果不同
    guifg值/guibg值/guisp值
        sp 是special的缩写
        真彩色
        可以指定为颜色名字
            Red		LightRed	    DarkRed
            Green	LightGreen	    DarkGreen	SeaGreen
            Blue	LightBlue	    DarkBlue	SlateBlue
            Cyan	LightCyan	    DarkCyan
            Magenta	LightMagenta	DarkMagenta
            Yellow	LightYellow	    Brown		DarkYellow
            Gray	LightGray	    DarkGray
            Black	White
            Orange	Purple		    Violet
        也可以指定为特定颜色值，如#ff0000
       
实践：
        打开vim a.cpp
        写好测试代码，如包含关键字、数字、注释等
        输入 :hi 可以查看都有哪些内容元素，及他们的当前颜色配置情况
        输入 :hi com 
        按tab键，会自动补全，如果有多个候选项，可以多次按tab
        输入 :hi comment ctermbg=1
        发现代码中的注释语句有背景色了，说明设置有效
实践2：
        当用vim -d 比较文件时，文字改变的行对比是，着色效果往往不理想
        hi diffchange termbg=1  #修改文字改变行的背景色
        或 hi clear diffchange  #文字改变行不着色（改变的文字通过difftext控制着色）
        
        