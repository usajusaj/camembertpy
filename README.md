# camembertpy

Cython wrapper around https://github.com/jts/bri with pysam integration

# Installation
## From source
### conda approach (recommended)
```bash
conda env create -f environment.yml
conda activate camembert
python setup.py install
```
### pip approach
```bash
# optional virtualenv:
virtualenv camembert
source camembert/bin/activate
# 
pip install cython pysam
python setup.py install
```

# Examples
## API
### build read index
```python
import bri
b = bri.Bri(bam_file)
b.create()
```

### retrieve reads
```python
import bri
b = bri.Bri(bam_file)
b.load()
for read in b.get(read_name):
    print(read.to_string())  # read is of type pysam.AligmentSegment
```

