import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class TechReport(BaseModel):
    filename: str

@processor()
def get_osm_way_links(df: DF[TechReport], context: Context):
    ids = []
    for _, filename in df['filename'].to_list():
        report = pd.read_csv(context.get_share_path(filename))
        ids.extend(report['way'].to_list())
    ids = list(set(ids))
    links = []
    for id in ids:
        links.append(f'https://www.openstreetmap.org/way/{id}')
    return pd.DataFrame(links, columns=['link'])
