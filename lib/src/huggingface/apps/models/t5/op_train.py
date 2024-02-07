# import os

# import datasets as ds
# import torch
# import transformers as tr
# from malevich.square import DF, Context, processor, scheme


# def _train(
#     d: ds.Dataset,
#     model: torch.nn.Module,
#     tokenizer: tr.AutoTokenizer,
#     batch_size: int,
#     lr: float,
#     run_id: str,
#     args: tr.TrainingArguments = None
# ):
#    if not args:
#        args = tr.TrainingArguments(
#            output_dir=os.path.join(os.getcwd(), '__t5__', run_id),
#            evaluation_strategy="epoch",
#            learning_rate=lr,
#            per_device_train_batch_size=batch_size,
#            per_device_eval_batch_size=batch_size,
#            num_train_epochs=3,
#            weight_decay=0.01,
#            load_best_model_at_end=False,
#            metric_for_best_model="accuracy",
#            save_strategy="no",
#        )

# @scheme()
# class T5TrainData:
#     text: str
#     label: str


# @processor()
# def train(data: DF[T5TrainData], context: Context):
#     pass

# @processor()
# def train_on_dataset(data: DF[T5TrainData], context: Context):
#     pass