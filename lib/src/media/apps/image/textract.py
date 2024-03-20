import os

import boto3
import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel

from .models import TextractTables


@scheme()
class TextracTable(BaseModel):
    filename: str

@processor()
def textract_tables(files: DF[TextracTable], context: Context[TextractTables]):
    """Extracts tables from PDF files using AWS Textract.

    ## Input:
        A dataframe with a column
        - `filename` (str): the name of the file to process.

    ## Output:
        A dataframe with the following columns:

        - `filename` (str): The name of the file.
        - `table` (str): If `write_contents` is False, the name of the markdow file containing the table, otherwise the contents of the file.

    ## Configuration:

        - `aws_access_key_id`: str.
            Your AWS access key ID.
        - `aws_secret_access_key`: str.
            Your AWS secret access key.
        - `write_contents`: bool, default False.
            Whether to write the contents of the table to the output.

    -----

    Args:
        files (DF[TextracTable]): The files to process.
        context (Context): The context.

    Returns:
        The processed dataframe
    """  # noqa: E501
    secret_key = context.app_cfg.get('aws_secret_access_key', None)
    key_id = context.app_cfg.get('aws_access_key_id', None)
    assert key_id and secret_key, 'Must provide AWS Key credentials'
    textract = boto3.client(
            'textract',
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
    outputs = []
    for filename in files.filename.to_list():
        response = textract.analyze_document(
                    Document={
                        "Bytes": open(context.get_share_path(filename), 'rb').read()
                    },
                    FeatureTypes=['TABLES']
                )
        all_cells = {}
        all_words = {}
        tables = []
        columns = 0
        rows = 0
        for d in response['Blocks']:
            if(d['BlockType'] == 'TABLE'):
                for rel in d['Relationships']:
                    if rel['Type'] == 'CHILD':
                        tables.append(rel['Ids'])
            elif(d['BlockType'] == 'CELL'):
                columns = max(columns, d.get('ColumnIndex', 0))
                rows = max(rows, d.get('RowIndex', 0))
                all_cells[d['Id']] = {
                    'text': d.get('Relationships', [{}])[0].get("Ids", []),
                    'column': d['ColumnIndex'],
                    'row': d['RowIndex'],
                    'entity': d.get('EntityTypes', [])
                    }
            elif(d['BlockType'] == 'WORD'):
                all_words[d['Id']] = d['Text']

        for cell_id in all_cells.keys():
                all_cells[cell_id]['text'] = ' '.join(
                    [all_words[word_id] for word_id in all_cells[cell_id]['text']]
                )

        for i, table_cells in enumerate(tables):
            first_row_column = False
            for cell_id in table_cells:
                rows = max(rows, all_cells[cell_id].get('row', 0))
                columns = max(columns, all_cells[cell_id].get('column', 0))
                if 'COLUMN_HEADER' in all_cells[cell_id]['entity']:
                    first_row_column = True

            table = [[0 for _ in range(columns)] for _ in range(rows)]

            for cell_id in table_cells:
                cell = all_cells[cell_id]
                table[cell['row']-1][cell['column']-1] = cell['text']

            if first_row_column:
                data = pd.DataFrame(table[1:], columns=table[0])
            else:
                data = pd.DataFrame(table)
            new_filename = os.path.basename(
                os.path.splitext(filename)[0] + f'_{i}.md'
            )
            data.to_markdown(
                os.path.join(
                    APP_DIR,
                    new_filename
                )
            )
            context.share(new_filename)
            if context.app_cfg.get('write_contents', False):
                outputs.append(
                    [filename, open(os.path.join(APP_DIR, new_filename)).read()]
                )
            else:
                outputs.append([filename, new_filename])
    return pd.DataFrame(outputs, columns=['filename', 'table'])
