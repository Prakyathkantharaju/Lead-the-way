import numpy as np
from sqlite_helper import PickleSQLiteHelper
from dataclasses import dataclass

@dataclass
class Databases:
    """Class to hold the database names for the different types of data"""
    drone: str = 'databases/drone.db'
    diff_car: str = 'databases/diff_car.db'



