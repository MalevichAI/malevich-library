from malevich.square import Context, input_true


@input_true(id='download_from_collection', collection_from='download_filename_s3')
def download_from_collection(context: Context):
    pass
