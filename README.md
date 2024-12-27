# Viral-Motif-Search
Public view of a private project. This will house all future changes

<-- Introduction -->

This is a web-based motif search progam for identifying potential matches of functional viral motifs across all frames of a given viral genome.

<-- Requirements -->

python libraries: jingja2, mysql.connector

Installation for these can be applied by running: pip install -r requirements.txt

utilities included under ~/scripts/bin/utils/project_parse.py

<-- Usage -->

Access page on server: /render.html

Click "Choose File"

Select any fasta formatted file with extentions .fasta, .fa, or .txt

These files should contain data similar in style to this: 

    >NC_077837.1 Mammalian orthoreovirus 3 Dearing strain T3D segment S3, complete sequence
    GCTAAAGTCACCCCTGTCGTCGTCACTATGGCTTCCTCACTCAGAGCTGCGATCTCCAAGATCAAGAGGG
    ATGACGTCGGTCAGCAAGTTTGTCCTAATTATGTCATGCTGCGGTCCTCTGTCACAACAAAGGTGGTACG
    AAATGTGGTTGAGTATCAAATTCGTACGGGCGGATTCTTTTCGTGCTTAGCTATGCTAAGGCCACTCCAG...

Click "Submit"

Results should populate once backend processing is complete. The summarized results contain collapsible dropboxes housing listed ids for linear motifs and can be revealed (or hidden) by clicking "Show Unique IDs"

< -- Data Availability -->

Data extracted from the Eukaryotic Linear Motif public viral database for Functional Sites in Proteins: http://elm.eu.org/viruses/

Sobhy H. (2016). A Review of Functional Motifs Utilized by Viruses. Proteomes, 4(1), 3. https://doi.org/10.3390/proteomes4010003
