from malevich.square import Context, init

import spacy
import spacy.cli

from .types import SpaCy


@init()
def spacy_init(ctx: Context):
    model_name = ctx.app_cfg.get("model_name", "en_core_web_sm")

    ctx.common = SpaCy()
    spacy.prefer_gpu()
    spacy.cli.download(model_name)
    ctx.common.model = spacy.load(model_name)
