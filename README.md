### Scripts to reproduce my Tara Oceans analysis

Paper is here [https://www.biorxiv.org/content/10.1101/2022.07.30.502162v2](https://www.biorxiv.org/content/10.1101/2022.07.30.502162v2)

Clone the respository and run the `runme.bash` script. Dependencies are `python3` and `scikit-learn`.

![Figure](http://drive5.com/images/tara_oceans_figure2.png)

The figure below was created by making charts for the histogram from `inf_clustercount.tsv` and ARI graph from `adjusted_rand_index.tsv` in Excel then manually editing in Inkscape.

![Figure](http://drive5.com/images/tara_oceans_figure.svg)

The `tara_bowtie2_mega_counts.py` script generates per-mega-taxon counts from bowtie2 SAM files, deposited at Zenodo [https://zenodo.org/record/7194888](https://zenodo.org/record/7194888).
