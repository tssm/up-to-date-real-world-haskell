

data/chapter_links.txt : setup
	grep 'file:[^ ]*.html]' *.org | cut -d':' -f 3-4 | cut -d']' -f1 | sort | uniq > $@

setup:
	mkdir -p data

htmlLinks:
	grep '\[file:[^ ]*.html#' *.org
