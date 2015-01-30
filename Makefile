ASSIGNMENT=3

all: doc clean zip

#Builds the docs
doc: 
	./build/build_doc.sh
    
.PHONY: zip clean squeaky doc
new:
	mkdir build src doc
zip:
	rm -rf zip
	mkdir zip
	zip --exclude=*.svn* -r zip/Assignment${ASSIGNMENT}_qjn162 .
clean:
	rm -f *.o *.log *.aux src/*~ 
squeaky: clean
	rm -rf zip
	rm *.pdf
	mkdir zip
