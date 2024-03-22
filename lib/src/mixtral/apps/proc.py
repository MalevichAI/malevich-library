import pandas as pd
import torch
from malevich.square import DF, Context, init, processor, scheme
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizerFast


#
class MixtralMessage(BaseModel):
    is_user: bool
    content: str


def prepare_batch(
    batch_messages: list[list[MixtralMessage]],
    tokenizer: LlamaTokenizerFast,
):
    # first_mes_ = True
    batches = []
    for messages in batch_messages:
        c_ = ""
        for mes in messages:
            cont_ = mes.content
            if mes.is_user:
                # if first_mes_:
                c_ += f"[INST]{cont_}[/INST]"
                # else:
                #     fir,st_mes_ = False
                #     cont_ = f'[INST]{cont_}\n{instruction}[/INST]'
            else:
                c_ += f"{cont_}{tokenizer.eos_token}"
        c_ = tokenizer.bos_token + c_
        batches.append(c_)

    return tokenizer(
        batches, add_special_tokens=False, padding=True, return_tensors="pt"
    )


@scheme()
class InferenceMixtralModel(BaseModel):
    model_id: str
    batch_size: int


@init(prepare=True)
def init_model(context: Context[InferenceMixtralModel]):
    assert torch.cuda.is_available(), "This app can only be run using GPU"
    model_id = context.app_cfg.get('model_id', "mistralai/Mixtral-8x7B-Instruct-v0.1")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print("Before", len(tokenizer))
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    print("After", len(tokenizer))
    model = AutoModelForCausalLM.from_pretrained(
        model_id, device_map="auto", torch_dtype=torch.float16
    )
    print("Before resize", len(tokenizer))
    model.resize_token_embeddings(len(tokenizer))
    context.common = (tokenizer, model)


@processor()
def mixtral(df: DF, context: Context):
    """
    ## Input:

    ## Output:

    ## Configuration:
    -----
    Args:
    """
    tokenizer, model = context.common
    indices = df["index"].unique()
    batch_messages = []
    for idx in indices:
        message = []
        for _, row in df[df["index"] == idx].iterrows():
            message.append(
                MixtralMessage(is_user=(row["role"] == "user"), content=row["content"])
            )
        batch_messages.append(message)
    inputs = prepare_batch(batch_messages, tokenizer)
    inputs = inputs.to("cuda")
    output_starts_at = inputs["input_ids"].size()[-1]
    outputs = model.generate(**inputs, max_new_tokens=120000)
    outputs = outputs[:, output_starts_at:]
    sequences = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    i = 0
    outputs = []
    for idx in indices:
        outputs.append([i, sequences[i]])
    return pd.DataFrame(outputs, columns = ['index', 'content'])
