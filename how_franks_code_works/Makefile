TARGET = how_franks_code_works
PANDOC_FLAGS = --standalone -f markdown
REMOVE = rm -f
PANDOC = pandoc

%.pdf: %.md Makefile
	$(PANDOC) $(PANDOC_FLAGS) -o $@ $<

%.tex: %.md Makefile
	$(PANDOC) $(PANDOC_FLAGS) -o $@ $<

all: $(TARGET).tex $(TARGET).pdf

clean:
	$(REMOVE) $(TARGET).pdf $(TARGET).tex