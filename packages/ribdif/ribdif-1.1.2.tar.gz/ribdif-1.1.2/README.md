# RibDif

RibDif evaluates the usefulness of a given amplicon at differentiating within a genus or species

# Installation
Ribdif is most easily installed with pip inside a virtual environment. Make sure your pip version is up to date

conda

`pip install git+https://github.com/Rob-murphys/ribdif.git`

Next we need to install some dependencies:

`conda install -c bioconda vsearch fasttree muscle barrnap -y`

# Running

`ribdif/ribdif -g <some genus name>`

Use `-h` for full options list.






