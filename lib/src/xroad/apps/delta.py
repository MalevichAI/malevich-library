import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel


@scheme()
class DocReportDF(BaseModel):
    name : str
    direction : str
    cls : str
    units: str
    reduced_units: str

@scheme()
class TechReportDF(BaseModel):
    way: str
    direction: str
    cls: str
    name: str
    units: str
    reduced_units: str
    camera_id: str

@scheme()
class StreetWays(BaseModel):
    way: str
    name: str

@processor()
def count_delta(
    tech: DF[TechReportDF],
    doc: DF[DocReportDF],
    ways: DF[StreetWays],
    context: Context
    ):
    way_ids = {}
    for _, row in ways.iterrows():
        way_ids[row['name']] = row['way']
    way_ids = [way_ids[name] for name in doc['name'].to_list()]
    doc.insert(loc=0, column='way', value=way_ids)
    result_df = pd.DataFrame(
        columns=['way', 'direction', 'class', 'units', 'reduced_units', 'camera_id']
    )

    for _, row in tech.iterrows():
        doc_row = doc[(doc['way'] == row['way']) &
                      (doc['direction'] == row['direction']) &
                      (doc['cls'] == row['cls'])]
        if len(doc_row.index) != 0:
            doc_row = doc_row.iloc[0]
            result_df.loc[len(result_df.index)] = [
                doc_row['way'],
                doc_row['direction'],
                doc_row['cls'],
                float(doc_row['units']) - float(row['units']),
                float(doc_row['reduced_units'] - float(row['reduced_units'])),
                row['camera_id']
            ]
    return result_df
