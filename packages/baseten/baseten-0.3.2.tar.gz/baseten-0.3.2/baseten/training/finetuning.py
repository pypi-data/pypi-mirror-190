import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from typing import List, Optional

from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.common import settings
from baseten.common.api import (
    cancel_training_run,
    deploy_from_training_run,
    finetune_zoo_model,
    get_all_training_runs,
    get_blueprint_projects,
)
from baseten.common.api import get_training_run as get_training_run_api
from baseten.common.files import DatasetTrainingType
from baseten.training.datasets import DatasetIdentifier
from baseten.training.logs import TrainingLogsConsumer
from baseten.training.utils import encode_base64_json

logger = logging.getLogger(__name__)


class FinetuningConfig(ABC):
    """
    Base abstract class for defining fine tuning configs. Each new fine-tuning
    algorithm that we support must support a subclass of this.

    Each fine-tuning algorithm will have a different set of variables that
    need to be provided.
    """

    @property
    @abstractmethod
    def dataset_training_type(self) -> DatasetTrainingType:
        """
        The dataset training type associated with this config type.
        """

    @property
    @abstractmethod
    def training_truss_name(self) -> str:
        """
        The name of the truss associated with this config.
        """

    @abstractmethod
    def resolve_fine_tuning_variables(self) -> dict:
        """
        Method that must be implemented that returns a variables dictionary
        for this type of FineTuning configuration.
        """


@dataclass
class DreamboothConfig(FinetuningConfig):
    """
    Fine-tuning config for Dreambooth fine-tuning with Stable Diffusion.

    Attributes:
        instance_prompt: The name of the object that you're teaching Stable Diffusion to generate
        input_dataset: An identifier, either an ID or a public URL, for the Dataset that Dreambooth should use
        wandb_api_key: [API key](https://docs.wandb.ai/quickstart) for Weights & Biases
        pretrained_model_name_or_path: TODO
        revision: TODO
        tokenizer_name: TODO
        class_prompt: TODO
        with_prior_preservation: TODO
        prior_loss_weight: TODO
        num_class_images: TODO
        seed: TODO
        resolution: TODO
        center_crop: TODO
        train_text_encoder: TODO
        train_batch_size: TODO
        sample_batch_size: TODO
        num_train_epochs: TODO
        max_train_steps: TODO
        gradient_accumulation_steps: TODO
        learning_rate: TODO
        lr_scheduler: TODO
        lr_warmup_steps: TODO
        adam_beta1: TODO
        adam_beta2: TODO
        adam_weight_decay: TODO
        adam_epsilon: TODO
        max_grad_norm: TODO
        mixed_precision: TODO

    **Examples:**

    ```python
    from baseten.training import Dataset, DreamboothConfig
    from baseten.training import DreamboothConfig

    config = DreamboothConfig(
        instance_prompt="photo of sks myname",
        input_dataset=Dataset("abcd1234"),
        train_text_encoder=False,
        num_train_epochs=10,
        max_train_steps=1000,
    )
    ```
    """

    instance_prompt: str
    input_dataset: DatasetIdentifier
    wandb_api_key: Optional[str] = None

    pretrained_model_name_or_path: Optional[str] = None
    revision: Optional[str] = None
    tokenizer_name: Optional[str] = None

    class_prompt: Optional[str] = None
    with_prior_preservation: Optional[bool] = None

    prior_loss_weight: Optional[float] = None
    num_class_images: Optional[int] = None
    seed: Optional[int] = None
    resolution: Optional[int] = None
    center_crop: Optional[bool] = None
    train_text_encoder: Optional[bool] = None
    train_batch_size: Optional[int] = None
    sample_batch_size: Optional[int] = None
    num_train_epochs: Optional[int] = None
    max_train_steps: Optional[int] = None
    gradient_accumulation_steps: Optional[int] = None
    learning_rate: Optional[float] = None
    lr_scheduler: Optional[str] = None
    lr_warmup_steps: Optional[int] = None
    adam_beta1: Optional[float] = None
    adam_beta2: Optional[float] = None
    adam_weight_decay: Optional[float] = None
    adam_epsilon: Optional[float] = None
    max_grad_norm: Optional[float] = None
    mixed_precision: Optional[str] = None

    def _resolve_dataset(self) -> str:
        return self.input_dataset.resolve_dataset_url(training_type=self.dataset_training_type)

    def resolve_fine_tuning_variables(self) -> dict:
        """
        Returns fine-tuning variables dict to send when triggering the fine-tuning
        job. The dataset URLs here are resolved to S3 URLs.
        """
        resolved_variables = asdict(self)

        resolved_variables.update({"dataset_zip_url": self._resolve_dataset()})

        del resolved_variables["input_dataset"]

        return {key: value for key, value in resolved_variables.items() if value is not None}

    @property
    def training_truss_name(self) -> str:
        return "dreambooth"

    @property
    def dataset_training_type(self) -> DatasetTrainingType:
        return DatasetTrainingType.DREAMBOOTH


class FinetuningRun:
    """
    Class to represent a single finetuning run.
    """

    @staticmethod
    def create(trained_model_name: str, fine_tuning_config: FinetuningConfig) -> "FinetuningRun":
        """
        Fine-tune a model by creating a FinetuningRun

        Args:
            trained_model_name: The name you want your fine-tuned model to have
            fine_tuning_config: The configuration for the fine-tuning process

        Returns:
            FinetuningRun (str): A string with the id of the newly created FinetuningRun on Blueprint
        """
        variables_dict = fine_tuning_config.resolve_fine_tuning_variables()
        encoded_variables = encode_base64_json(variables_dict)

        logger.info("Starting fine-tuning of %s", fine_tuning_config.training_truss_name)

        run_id = finetune_zoo_model(
            trained_model_name, fine_tuning_config.training_truss_name, encoded_variables
        )
        return FinetuningRun(run_id)

    @staticmethod
    def list() -> List["FinetuningRun"]:
        """List all finetuning runs for user."""
        resolved_runs = get_all_training_runs()
        return list(
            [FinetuningRun(r["id"], r["trained_model_name"], refresh=False) for r in resolved_runs]
        )

    class Status(Enum):
        """Status of FinetuningRun on Baseten."""

        PENDING = "PENDING"
        RUNNING = "RUNNING"
        SUCCEEDED = "SUCCEEDED"
        FAILED = "FAILED"
        CANCELLED = "CANCELLED"

    def __init__(
        self,
        id: str,
        trained_model_name: Optional[str] = None,
        refresh: bool = False,
    ):
        """Initialize the object with the given id.

        Args:
            id (str): The ID of the FinetuningRun on Blueprint
        """
        self.id = id
        self.trained_model_name = trained_model_name
        if refresh:
            self.refresh()

    def __repr__(self) -> str:
        trained_name = ""
        if self.trained_model_name:
            trained_name = f", name: {self.trained_model_name}"
        return f"""<FinetuningRun id: {self.id}{trained_name}>"""

    @property
    def is_pending(self) -> bool:
        return self.status == FinetuningRun.Status.PENDING.value

    @property
    def is_running(self) -> bool:
        return self.status == FinetuningRun.Status.RUNNING.value

    @property
    def is_succeeded(self) -> bool:
        return self.status == FinetuningRun.Status.SUCCEEDED.value

    @property
    def is_failed(self) -> bool:
        return self.status == FinetuningRun.Status.FAILED.value

    @property
    def is_cancelled(self) -> bool:
        return self.status == FinetuningRun.Status.CANCELLED.value

    def refresh(self):
        """Re-fetch training data from the server."""
        training_run_data = get_training_run_api(self.id)

        # TODO (Sid): Handle case of training run not found

        self.status = training_run_data["status"]
        self.created = training_run_data["created"]
        self.started = training_run_data["started"]
        self.stopped = training_run_data["stopped"]
        self.trained_model_name = training_run_data["trained_model_name"]

        self.variables = {
            variable["key"]: variable["value"] for variable in training_run_data["variables"]
        }

    # Mutations
    def deploy(self, idle_time_minutes: int = 30) -> BasetenDeployedModel:
        """
        Deploy the fine-tuned model created during the FinetuningRun

        Args:
            idle_time_minutes: How long the deployed model should wait between invocations
                before scaling resources to zero

        Returns:
            BasetenDeployedModel: A model object deployed on Baseten that can be invoked
        """
        model_id, _ = deploy_from_training_run(
            training_run_id=self.id,
            name=self.trained_model_name,
            idle_time_minutes=idle_time_minutes,
        )
        return BasetenDeployedModel(model_id=model_id)

    def cancel(self) -> bool:
        """
        Cancels this FinetuningRun.

        Returns:
            bool: True if the run was successfully canceled
        """
        return cancel_training_run(training_run_id=id)

    def stream_logs(self):
        """Stream logs from the FinetuningRun."""
        TrainingLogsConsumer(self).stream_logs()

    @property
    def blueprint_url(self) -> str:
        """Link to view FinetuningRun on Blueprint"""
        try:
            blueprint_project_id = get_blueprint_projects()[0]["id"]
            return (
                f"{settings.get_server_url()}/blueprint/projects/"
                f"{blueprint_project_id}?est=trained-model--{self.id}"
            )
        except IndexError:
            raise ValueError("User does not have any blueprint projects.")
