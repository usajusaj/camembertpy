# camembertpy

Cython wrapper around https://github.com/jts/bri with pysam integration

# Examples:
## build read index
```python
import bri
b = bri.Bri(bam_file)
b.create()
```

## retrieve reads
```python
import bri
b = bri.Bri(bam_file)
b.load()
for read in b.get(read_name):
    print(read.to_string())  # read is of type pysam.AligmentSegment
```
