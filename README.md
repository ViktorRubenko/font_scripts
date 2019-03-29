# Font Scripts

Different scripts to work with font files.
Fell free to use.

## Requirements
fontTools
https://github.com/fonttools/fonttools

## Scripts:

* vtt_xml_update - correlates and corrects Glyphs IDs in VTT xml between old hinted font and the new with new GlyphOrder
```
vtt_xml_update.py -o <path to old font> -u <path to new font> -x <path to vtt xml>
```


