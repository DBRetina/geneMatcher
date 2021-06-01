# GeneMatcher

## Installation

```
pip install git+https://github.com/DBRetina/geneMatcher
```

## Usage

```
geneMatcher --help
```

## Simple run examples

### 1. Create a TSV file

Create a TSV file with col1: ref1_URL, col2: ref2_url

filename: `refs.tsv`

```tsv
http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/GRCh37_mapping/gencode.v28lift37.transcripts.fa.gz	http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/gencode.v38.transcripts.fa.gz
http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_20/gencode.v20.pc_transcripts.fa.gz	http://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_34/gencode.v34.pc_transcripts.fa.gz
```


### 2. Run geneMatcher

```
geneMatcher auto -k 25 --refs-tsv refs.tsv --min-jac 20 --min-cont 80 --cores 8
```