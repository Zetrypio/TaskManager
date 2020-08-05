variable colors
array set colors {
  -disabledfg	"DarkGrey"
  -frame  	"#424242"
  -dark	    "#222222"
  -darker 	"#121212"
  -darkest	"black"
  -lighter	"#626262"
  -lightest 	"#ffffff"
  -selectbg	"#4a6984"
  -selectfg	"#ffffff"
    }
if {[info commands ::ttk::style] ne ""} {
    set styleCmd ttk::style
  } else {
    set styleCmd style
  }

  $styleCmd theme create black -parent clam -settings {

  # -----------------------------------------------------------------
  # Theme defaults
  #
  $styleCmd configure "." \
      -background $colors(-frame) \
      -foreground white \
      -bordercolor $colors(-darkest) \
      -darkcolor $colors(-dark) \
      -lightcolor $colors(-lighter) \
      -troughcolor $colors(-darker) \
      -selectbackground $colors(-selectbg) \
      -selectforeground $colors(-selectfg) \
      -selectborderwidth 0 \
      -font TkDefaultFont \
      ;

  $styleCmd map "." \
      -background [list disabled $colors(-frame) \
      active $colors(-lighter)] \
      -foreground [list disabled $colors(-disabledfg)] \
      -selectbackground [list  !focus $colors(-darkest)] \
      -selectforeground [list  !focus white] \
      ;

  # ttk widgets.
  $styleCmd configure TSpinbox -background "#474747" -fieldbackground $colors(-lighter)
  $styleCmd configure TButton -background $colors(-lighter) -fieldbackground $colors(-dark)\
      -width -8 -padding {5 1} -relief raised
  $styleCmd configure TMenubutton \
      -width -11 -padding {5 1} -relief raised
  $styleCmd configure TCheckbutton \
      -indicatorbackground "#ffffff" -indicatormargin {1 1 4 1}
  $styleCmd configure TRadiobutton \
      -indicatorbackground "#ffffff" -indicatormargin {1 1 4 1}

  $styleCmd configure TEntry \
      -fieldbackground $colors(-lighter) -foreground white \
      -padding {2 0}
  $styleCmd configure TCombobox \
      -fieldbackground $colors(-lighter) -foreground white \
      -padding {2 0}

  $styleCmd configure TNotebook.Tab \
      -padding {6 2 6 2}

  $styleCmd map TNotebook.Tab -background [list \
      selected $colors(-lighter)]

  # tk widgets.
  $styleCmd map Menu \
      -background [list active $colors(-lighter)] \
      -foreground [list disabled $colors(-disabledfg)]

  $styleCmd configure TreeCtrl \
      -background gray30 -itembackground {gray60 gray50} \
      -itemfill white -itemaccentfill yellow

  $styleCmd map Treeview \
      -background [list selected $colors(-selectbg)] \
      -foreground [list selected $colors(-selectfg)]

  $styleCmd configure Treeview -fieldbackground $colors(-lighter)
}
