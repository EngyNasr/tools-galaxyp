#!/usr/bin/env python
import os
import sys

class Sequence:
    ''' Holds protein sequence information '''
    def __init__(self):
        self.header = ""
        self.sequence = ""

class FASTAReader:
    """
        FASTA db iterator. Returns a single FASTA sequence object.
    """
    def __init__(self, fasta_name):
        self.fasta_file = open(fasta_name)

    def __iter__(self):
        return self

    def __next__(self):
        ''' Iteration '''
        while True:
            line = self.fasta_file.readline()
            if not line:
                raise StopIteration
            if line[0] == '>':
                break

        seq = Sequence()
        seq.header = line.rstrip().replace('\n','').replace('\r','')

        while True:
            tail = self.fasta_file.tell()
            line = self.fasta_file.readline()
            if not line:
                break
            if line[0] == '>':
                self.fasta_file.seek(tail)
                break
            seq.sequence = seq.sequence + line.rstrip().replace('\n','').replace('\r','')
        return seq

    # Python 2/3 compat
    next = __next__


def main():
    seen_sequences = set([])
    seen_headers = set([])

    out_file = open(sys.argv[1], 'w')
    if sys.argv[2] == "sequence":
        unique_sequences = True
    elif sys.argv[2] == "accession":
        unique_sequences = False
    else:
        sys.exit("2nd argument must be 'sequence' or 'accession'")

    for fasta_file in sys.argv[3:]:
        fa_reader = FASTAReader(fasta_file)
        for protein in fa_reader:
            if unique_sequences:
                if protein.sequence in seen_sequences or protein.header in seen_headers:
                    continue
                else:
                    seen_sequences.add(protein.sequence)
                    seen_headers.add(protein.header)
            else:
                if protein.header in seen_headers:
                    continue
                else:
                    seen_headers.add(protein.header)
            out_file.write(protein.header)
            out_file.write(os.linesep)
            out_file.write(protein.sequence)
            out_file.write(os.linesep)
    out_file.close()

if __name__ == "__main__":
    main()
