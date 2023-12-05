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
    start_page = context.app_cfg.get('start_page', 0)
    page_num = context.app_cfg.get('page_num', None)
    for filename in files.filename.to_list():
        pages = []
        images = convert_from_path(context.get_share_path(filename),
                                   first_page=start_page+1,
                                   last_page=page_num if page_num is None \
                                    else start_page+page_num)
        for i, image in enumerate(images):
            result_path = os.path.basename(filename.replace('.pdf',
                                                            f'_{start_page+i}.jpg'))
            image.save(
                    os.path.join(
                        APP_DIR,
                        result_path
                    )
            )
            context.share(result_path)
            pages.append(result_path)
        df = pd.DataFrame(pages, columns=['jpeg'])
        df.insert(1, 'filename', filename)
        outputs.append(df)

    return pd.concat(outputs)
