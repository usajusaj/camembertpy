from pysam import AlignmentFile

"""
    Expose bare minimum from jts/bri headers
"""
cdef extern from "bri_index.h":
    struct bam_read_idx_record:
        size_t file_offset

    struct bam_read_idx:
        bam_read_idx_record* records

    bam_read_idx* bam_read_idx_load(const char* input_bam)
    bam_read_idx* bam_read_idx_build(const char* input_bam)
    void bam_read_idx_save(bam_read_idx* bri, const char* filename)
    void bam_read_idx_destroy(bam_read_idx* bri)

cdef extern from "bri_get.h":
    void bam_read_idx_get_range(const bam_read_idx* bri,
                            const char* readname,
                            bam_read_idx_record** start,
                            bam_read_idx_record** end)
    int bam_read_idx_get_main(int argc, char** argv)

cdef bam_read_idx* _build_index(in_path, out_path):
    """ Create bri index from bam file
    Args:
        in_path (bytes): path to bam file
        out_path (bytes): path to bri file
    Returns:
        bam_read_idx*: built index 
    """
    cdef bam_read_idx* bri = bam_read_idx_build(in_path)
    bam_read_idx_save(bri, out_path)
    return bri


cdef bam_read_idx* _load_index(in_path):
    """ Read existing bri index
    Args:
        in_path (bytes): path to bam file. bri extension is automatically added
    Returns:
        bam_read_idx*: loaded index 
    """
    return bam_read_idx_load(in_path)


cdef class Bri:
    """ Wrapper class for Jared's bri, supports creating and reading .bri index and extracting reads using pysam

    Attributes:
        index (bam_read_idx*): Bri index instance
        input_bam_path (bytes): Path to bam file
        input_bri_path (bytes): Path to bri file
        hts (pysam.AlignmentFile): Bam file instance
    """
    cdef:
        bam_read_idx* index
        object hts
        bytes input_bam_path
        bytes input_bri_path

    def __init__(self, input_bam):
        """
        Args:
            input_bam (str): Path to .bam file
        """
        self.input_bam_path = input_bam.encode('utf-8')
        self.input_bri_path = (input_bam + '.bri').encode('utf-8')

    def create(self):
        """ Create bri index for bam file by calling bam_read_idx_build and bam_read_idx_save. Index is immediately
        destroyed to prevent segfaulting
        """
        index = _build_index(self.input_bam_path, self.input_bri_path)
        bam_read_idx_destroy(index)

    # noinspection PyAttributeOutsideInit
    def load(self):
        """ Load the index from .bri file """
        self.index = _load_index(self.input_bam_path)
        self.hts = AlignmentFile(self.input_bam_path, 'rb')

    def get(self, read_name):
        """ Get reads for read_name from the bam file using .bri index
        Args:
            read_name (str): Reads to search for
        Yields:
            pysam.AlignedSegment: found reads
        """
        cdef:
            bam_read_idx_record* start
            bam_read_idx_record* end

        bam_read_idx_get_range(self.index, read_name.encode('utf-8'), &start, &end)

        hts_iter = iter(self.hts)

        while start != end:
            self.hts.seek(start.file_offset)
            read = next(hts_iter)
            yield read
            start += 1

    def __del__(self):
        bam_read_idx_destroy(self.index)
