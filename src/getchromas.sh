#!/bin/bash
while read fn; do
    NUMBER=$(echo $fn | awk -F "/" '{print $6}')
    echo "python chroma_extract.py /Volumes/Data/billboard/burgoyne2011chords/$NUMBER/mirex_triad.txt $fn" >> commands.txt
done < reg.mf

while read fn; do
    NUMBER=$(echo $fn | awk -F "/" '{print $6}')
    echo "python chroma_extract.py /Volumes/Data/billboard/burgoyne2011chords/$NUMBER/mirex_triad.txt $fn" >> commands.txt
done < harm.mf
