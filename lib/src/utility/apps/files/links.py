import os
import re
import shutil

from malevich.square import APP_DIR, DF, Context, processor


@processor()
def get_links_to_files(df: DF, ctx: Context):
    """Get links to files produced during the workflow execution.

    ## Input:
        An arbitrary dataframe.

    ## Output:
        The same dataframe, but with all file paths replaced
        with openable links to the files.

    ## Configuration:
        - `expiration`: int.
        The number of seconds after which the link will expire. Defaults to 6 hours. Maximum is 24 hours.

    -----

    Args:
        df (DF):
            An arbitrary dataframe.
        ctx (Context):
            The context object.

    Returns:
        DF:
            The same dataframe, but with all file paths replaced
            with openable links to the files.
    """  # noqa: E501

    _expire_secs = ctx.app_cfg.get('expiration', 6 * 3600)
    _expire_secs = min(_expire_secs, 24 * 3600)
    _expire_secs = max(_expire_secs, 0)

    def _exst(path: str, all_runs=False) -> bool:
        return os.path.exists(
            ctx.get_share_path(
                path, not_exist_ok=True, all_runs=all_runs
            )
        )

    def _exst_obj(path: str) -> bool:
        return (
            os.path.exists(path) and
            ctx.has_object(
                re.search(
                    r"\/mnt_obj\/(?P<USERNAME>\w+\/)(?P<KEY>.+)",
                    path
                ).group("KEY")
            )
        )

    def _get(_obj: str) -> tuple[str, str]:
        if _exst(_obj, all_runs=False) or (is_asset := _exst_obj(_obj)):
            # /FOLDER/FILE.EXT -> /FOLDER/FILE__RUNID.EXT
            _fbase = os.path.basename(_obj)
            _fext = os.path.splitext(_fbase)[1]
            _fbase = os.path.splitext(_fbase)[0]
            _fbase += '__' + ctx.run_id + _fext
            _ffull = os.path.join(APP_DIR, _fbase)

            if is_asset:
                shutil.move(
                    _obj,
                    _ffull
                )
            else:
                shutil.move(
                    ctx.get_share_path(_obj, all_runs=False),
                    _ffull
                )

            ctx.share(_fbase, all_runs=True)
            ctx.synchronize([_fbase], all_runs=True)
            return _fbase, ctx.get_share_path(_fbase, all_runs=True)
        elif _exst(_obj, all_runs=True):
            return _obj, ctx.get_share_path(_obj, all_runs=True)
        else:
            return None


    _links = []
    _fo2zip = {}
    def _collect(_obj: object) -> object:
        if not isinstance(_obj, str):
            try:
                _obj = str(_obj)
            except Exception as _:
                return _obj

        if (x := _get(_obj)) is not None:
            _key, _path = x
            nonlocal _links
            if os.path.isdir(_path):
                _fbase = _key
                _freal = _path
                fname = os.path.join(
                    APP_DIR,
                    _fbase
                )
                shutil.make_archive(
                    fname,
                    'zip',
                    _freal
                )
                _fbase += '.zip'
                ctx.share(_fbase, all_runs=True)
                ctx.synchronize([_fbase], all_runs=True)
                _links.append(_fbase)
                _fo2zip[_obj] = _fbase
                return _fbase
            else:
                _links.append(_key)
                print('KEY', _key)
                return _key

        return _obj


    for _col in df.columns:
        df[_col] = df[_col].apply(_collect)


    key_link = ctx.object_storage.update(
        keys=_links, presigned_expire=_expire_secs
    )


    def _set(_obj: object) -> object:
        if not isinstance(_obj, str):
            try:
                _obj = str(_obj)
            except Exception as _:
                return _obj
        if _obj in _fo2zip:
            return key_link.get(_fo2zip[_obj])
        else:
            return key_link.get(_obj, _obj)

    for _col in df.columns:
        df[_col] = df[_col].apply(_set)

    return df
