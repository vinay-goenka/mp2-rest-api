import logging

logger = logging.getLogger(__name__)

class DatasetStorage:
    def __init__(self):
        self._store = {}
        self._counter = 0

    def save(self, df, filename):
        """Store a copy of the data and return a new integer ID."""
        self._counter += 1
        dataset_id = self._counter
        self._store[dataset_id] = {
            "data": df.copy(),
            "filename": filename,
        }
        no_of_rows = len(df)
        logger.debug(f"Dataset: id:{dataset_id}, rows:{no_of_rows}")
        return dataset_id

    def get(self, dataset_id):
        """Return a copy of the stored DataFrame, or None."""
        pass

    def get_metadata(self, dataset_id):
        """Return the dataset metadata, or None."""
        pass

    def update(self, dataset_id, df):
        """Replace an existing dataset; return True, or False if missing."""
        pass

    def clear(self):
        """Clear all data and reset the ID counter."""
        self._store.clear()
        self._counter = 0
