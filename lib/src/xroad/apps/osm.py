import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class TechReport(BaseModel):
    way: str
    direction: str
    cls: str
    name: str
    units: str
    reduced_units: str
    camera_id: str

@processor()
def get_osm_way_links(df: DF[TechReport], context: Context):
    ids = df['way'].to_list()
    ids = list(set(ids))
    links = []
    for id in ids:
        links.append(f'https://www.openstreetmap.org/way/{id}')
    return pd.DataFrame(links, columns=['link'])
