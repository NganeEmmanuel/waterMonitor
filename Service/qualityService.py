from Database import crud
from model import quality


def add_quality(quality):
    return crud.add(quality)


def get_quality_by_id(quality_readings):
    return crud.find_by("id", quality_readings, quality.Quality)
