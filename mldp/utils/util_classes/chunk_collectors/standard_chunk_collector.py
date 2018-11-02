from base_chunk_collector import BaseChunkCollector
from collections import OrderedDict
from mldp.utils.util_classes import DataChunk
import numpy as np


class StandardChunkCollector(BaseChunkCollector):
    """
    Chunk collector that is based on the number of data-units in it.
    """

    def __init__(self, max_size):
        super(StandardChunkCollector, self).__init__(max_size)
        # key: field_names, values: chunk field values in a list
        self._chunk_data_collector = None
        self.reset()

    @property
    def chunk(self):
        """Returns a compiled data-chunk."""
        dc = DataChunk()
        for k, v in self._chunk_data_collector.items():
            dc[k] = np.concatenate(v)
        return dc

    def _append(self, k, v):
        self._validate_input_value(v)
        if k not in self._chunk_data_collector:
            self._chunk_data_collector[k] = []
        self._chunk_data_collector[k].append(v)

    def __getitem__(self, key):
        return self._chunk_data_collector[key]

    def __len__(self):
        keys = self._chunk_data_collector.keys()
        if len(keys) == 0:
            return 0
        return sum([len(el) for el in self._chunk_data_collector[keys[0]]])

    def absorb_and_yield_if_full(self, data_chunk):
        """
        Adds the data-chunk to the collector, yields a new data_chunk if the
        collector is full.
        """
        start_indx = 0
        end_indx = len(data_chunk)

        while start_indx < end_indx:
            size_before = len(self)
            missing_count = self.max_size - size_before
            tmp_end_indx = min(start_indx + missing_count, end_indx)
            self._collect_missing_units(data_chunk, start_indx,
                                        end_indx=tmp_end_indx)
            start_indx += (len(self) - size_before)

            # if it's full yield and reset
            if self.full():
                yield self.chunk
                self.reset()

    def _collect_missing_units(self, data_chunk, start_indx, end_indx):
        """Stores units from the data-chunk to the collector."""
        slice_indx = range(start_indx, end_indx)
        for k in data_chunk:
            self._append(k, data_chunk[k][slice_indx])

    def reset(self):
        self._chunk_data_collector = OrderedDict()