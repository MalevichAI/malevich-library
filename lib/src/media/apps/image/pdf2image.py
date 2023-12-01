import os

import pandas as pd
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pdf2image import convert_from_path
from pydantic import BaseModel


@scheme()
class Filename(BaseModel):
    filename:str

@processor()
def convert_pdf_to_jpeg(files: DF[Filename], context: Context):
    outputs = []
    for filename in files.filename.to_list():
        pages = []
        images = convert_from_path(context.get_share_path(filename))
        for i, image in enumerate(images):
            result_path = os.path.basename(filename.replace('.pdf', f'_{i}.jpg'))
            image.save(
                    os.path.join(
                        APP_DIR,
                        result_path
                    )
            )
            print(f'Saved into {os.path.join(APP_DIR, result_path)}')
            context.share(result_path)
            pages.append(result_path)
        df = pd.DataFrame(pages, columns=['jpeg'])
        df.insert(1, 'filename', filename)
        outputs.append(df)

    return pd.concat(outputs)
