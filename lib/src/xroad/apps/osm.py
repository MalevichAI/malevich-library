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
    """Get links to OpenStreetMap ways by their id

    Input:
        A dataframe with columns: [ way, direction, cls, name, units, reduced_units, camera_id ]


    Output:
        A dataframe with a column named `link` containing the links to the ways on OpenStreetMap
        in format https://www.openstreetmap.org/way/id

    Args:
        links (DF[TechReport]):
            A dataframe with columns: [ way, direction, cls, name, units, reduced_units, camera_id ]

    Returns:
        A dataframe with a column named `link` containing the links to the ways on OpenStreetMap
        in format https://www.openstreetmap.org/way/id
    """  # noqa: E501
    ids = df['way'].to_list()
    ids = list(set(ids))
    links = []
    for id in ids:
        links.append(f'https://www.openstreetmap.org/way/{id}')
    return pd.DataFrame(links, columns=['link'])
