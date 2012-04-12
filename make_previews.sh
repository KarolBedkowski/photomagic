#!/bin/sh
./photomagick.pyw --list-filter-names | while read fname
do 
	./photomagick.pyw -b -F $fname -o data/previews/ -p _$fname data/previews/input.png
done
