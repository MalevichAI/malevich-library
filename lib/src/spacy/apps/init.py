from malevich.square import Context, init

import spacy
import spacy.cli

from .types import SpaCy


@init(prepare=True)
def spacy_init(ctx: Context):
    if ctx.app_cfg.get("language", "en") == "ru":
        model_name = ctx.app_cfg.get("model_name", "ru_core_news_sm")
    else:
        model_name = ctx.app_cfg.get("model_name", "en_core_web_sm")

    ctx.common = SpaCy()
    spacy.prefer_gpu()
    spacy.cli.download(model_name)
    ctx.common.model = spacy.load(model_name)
