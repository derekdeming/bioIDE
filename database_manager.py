from db_wrapper.biorxiv import BiorxivDatabase
from db_wrapper.geo import GeoDatabase


class DatabaseManager:
    def __init__(self):
        self.databases = {
            "biorxiv": BiorxivDatabase(),
            # "geo": GeoDatabase(),
            # need to add the other databases below this -- will get to this later 
        }

    def fetch(self, db_name, func_name, *args, **kwargs):
        if db_name not in self.databases:
            raise ValueError(f"No database named {db_name}")

        db = self.databases[db_name]
        func = getattr(db, func_name, None)
        
        if not func:
            raise ValueError(f"No function named {func_name} in {db_name}")
        
        return func(*args, **kwargs)
