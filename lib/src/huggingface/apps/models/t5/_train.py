import os

import datasets as ds
import torch
import transformers as tr


def callback_factory() -> tr.TrainerCallback:
    """Callback factory to control training process."""
    class Callback(tr.TrainerCallback):
        def on_init_end(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):

            pass

        def on_train_begin(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_train_end(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_epoch_begin(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_epoch_end(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_step_begin(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_substep_end(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_step_end(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_evaluate(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_predict(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            metrics,
            **kwargs
        ):
            pass

        def on_save(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_log(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            pass

        def on_prediction_step(
            self,
            args: tr.TrainingArguments,
            state: tr.TrainerState,
            control: tr.TrainerControl,
            **kwargs
        ):
            """
            Event called after a prediction step.
            """
            pass

    return Callback()


def _train(
    d: ds.Dataset,
    model: torch.nn.Module,
    tokenizer: tr.AutoTokenizer,
    batch_size: int,
    lr: float,
    run_id: str,
    args: tr.TrainingArguments = None
) -> tr.Trainer:
    if not args:
        args = tr.TrainingArguments(
            output_dir=os.path.join(os.getcwd(), '__t5__', run_id),
            evaluation_strategy="epoch",
            learning_rate=lr,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=3,
            weight_decay=0.01,
            load_best_model_at_end=False,
            metric_for_best_model="accuracy",
            save_strategy="no",
        )

    trainer = tr.Trainer(
        model=model,
        args=args,
        train_dataset=d,
        tokenizer=tokenizer,
        callbacks=[callback_factory()]
    )
    trainer.train()
    return trainer


