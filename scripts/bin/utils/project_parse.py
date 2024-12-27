#!/usr/local/bin/python3

## function to split input into header and sequence
def parse_file(input_fasta):
    header = None
    body = "" 
    for line in input_fasta.splitlines():
        line = line.strip()
        if line.startswith(">"):
            header = line
        else:
            body += line.upper()
    return header, body
## should specify something like header, sequence = header, body

## function to determine if sequence is DNA or Amino acid
def check_DNA_or_Prot(sequence):
    dna_seq = True
    aa_diff = ['D', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'V', 'W', 'Y']
    for item in sequence:
        if item in aa_diff:
            dna_seq = False
            break
    return dna_seq
## if check_DNA_or_Prot(sequence) == True, then sequence is frames 1-3 and reverse_complement is frames 4-6

complement_dict = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

## function to creaete reverse complement of dna seq for frames 4-6
def reverse_complement(dna_seq):
    reverse_comp = ""
    for base in reversed(dna_seq):
        reverse_comp += complement_dict[base]
    return reverse_comp
## set rev_comp_dna_seq = reverse_comp

"""
Must insert line to convert sequences to RNA: '.replace('T', 'U')'
"""

## set function to read three frames and parse into codons of three bases
def parse_frames(sequence_input):
    frame_dict = {}
    for frame in range(0,3):
        framed_seq = sequence_input[frame:]
        codons = [framed_seq[i:i+3] for i in range(0, len(framed_seq), 3)]
        frame_dict[frame + 1] = codons
    return frame_dict
## this should return a dictionary of {frame:[codon], etc...} for the three frames in one direction
## this function should be run twice, once for the forward direction and the next for reverse comp

codon_dict = {'UUU':'F', 'UUC':'F', 'UUA':'L', 'UUG':'L'
            , 'UCU':'S', 'UCC':'S', 'UCA':'S', 'UCG':'S'
            , 'UAU':'Y', 'UAC':'Y', 'UAA':'j', 'UAG':'j'
            , 'UGU':'C', 'UGC':'C', 'UGA':'j', 'UGG':'W'
            , 'CUU':'L', 'CUC':'L', 'CUA':'L', 'CUG':'L'
            , 'CCU':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P'
            , 'CAU':'H', 'CAC':'H', 'CAA':'Q', 'CAG':'Q'
            , 'CGU':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R'
            , 'AUU':'I', 'AUC':'I', 'AUA':'I', 'AUG':'M'
            , 'ACU':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T'
            , 'AAU':'N', 'AAC':'N', 'AAA':'K', 'AAG':'K'
            , 'AGU':'S', 'AGC':'S', 'AGA':'R', 'AGG':'R'
            , 'GUU':'V', 'GUC':'V', 'GUA':'V', 'GUG':'V'
            , 'GCU':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A'
            , 'GAU':'D', 'GAC':'D', 'GAA':'E', 'GAG':'E'
            , 'GGU':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G'
            }

## function to translate codons into amino acid sequences
def translate(framed_dictionary):
    translational_dict = {}
    for i in framed_dictionary:
        codon_list = framed_dictionary[i]
        translation = ""
        for codon in codon_list:
            if len(codon) == 3:
                try:
                    translation += codon_dict[codon]
                except KeyError():
                    print("")
        translational_dict[i] = translation
    return translational_dict
## this functional should be run once because you should combine forward and reverse into one dictionary

## function breaks translation into peptide segments from M to stop codon, which is not added in as no aa actually represents it
def parse_translation(translated_dict):
    peptide_frame_dict = {}
    for i in translated_dict:
        translation = translated_dict[i]
        peptide_list = []
        peptide_chain = ""
        peptide_grow = False
        for aa in translation:
            if aa == 'M' and peptide_grow == False:
                peptide_chain = 'M'
                peptide_grow = True
            elif aa == 'j':
                if len(peptide_chain) >= 3:
                    peptide_list.append(peptide_chain)
                peptide_grow = False
            elif aa and peptide_grow == True:
                peptide_chain += aa
            
        peptide_frame_dict[i] = peptide_list
    return peptide_frame_dict
## should return something like {frame#:[MASADAKASG, MALSKLQ, etc.], frame#: ...}


