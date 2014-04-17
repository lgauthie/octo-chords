#!/bin/bash
while read fn; do
    echo $fn
    NUMBER=$(echo $fn | awk -F "/" '{print $6}')
    echo $NUMBER
    python chroma_extract.py /Volumes/Data/billboard/burgoyne2011chords/$NUMBER/mirex_triad.txt $fn
done < reg.mf

while read fn; do
    echo $fn
    NUMBER=$(echo $fn | awk -F "/" $5)
    python chroma_extract.py /Volumes/Data/billboard/burgoyne2011chords/$NUMBER/mirex_triad.txt $fn
done < harm.mf
