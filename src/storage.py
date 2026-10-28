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
        if dataset_id not in self._store:
            logger.debug(f"Dataset not found: {dataset_id}")
            return None
    
        df = self._store[dataset_id]["data"].copy()
        no_of_rows = len(df)
        logger.debug(f"Dataset: id:{dataset_id}, rows:{no_of_rows}")
        return df

    def get_metadata(self, dataset_id):
        """Return the dataset metadata, or None."""
        if dataset_id not in self._store:
            logger.debug(f"Dataset not found: {dataset_id}")
            return None
        
        filename = self._store[dataset_id]["filename"]
        df = self._store[dataset_id]["data"]
        no_of_rows = len(df)
        no_of_columns = len(df.columns)
        column_names = list(df.columns)
        metadata = {
            "id": dataset_id,
            "filename": filename,
            "rows": no_of_rows,
            "columns": no_of_columns,
            "column_names": column_names,
        }
        logger.debug(f"Retrieved metadata: {dataset_id}")
        return metadata

    def update(self, dataset_id, df):
        """Replace an existing dataset; return True, or False if missing."""
        if dataset_id not in self._store:
            logger.debug(f"Dataset not found: {dataset_id}")
            return False
        
        df_copy = df.copy()
        self._store[dataset_id]["data"] = df_copy
        no_of_rows = len(df_copy)
        logger.debug(f"Updated dataset: id={dataset_id}, rows={no_of_rows}")
        return True

    def clear(self):
        """Clear all data and reset the ID counter."""
        self._store.clear()
        self._counter = 0
