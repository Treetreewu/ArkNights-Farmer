text2image --text dicts/hr.txt --font 'Noto Sans CJK SC Regular' --fonts_dir .\fonts\ --outputbase hr.notosans.exp0 --fontconfig_tmpdir ./ --ptsize 25


tesseract hr.notosans.exp0.tif hr.notosans.exp0 nobatch box.train
unicharset_extractor .\hr.notosans.exp0.box
mftraining -F font_properties -U unicharset -O hr.unicharset hr.notosans.exp0.tr
cntraining .\hr.notosans.exp0.tr

mv normproto hr.normproto
mv inttemp hr.inttemp
mv pffmtable hr.pffmtable
mv shapetable hr.shapetable

combine_tessdata hr.