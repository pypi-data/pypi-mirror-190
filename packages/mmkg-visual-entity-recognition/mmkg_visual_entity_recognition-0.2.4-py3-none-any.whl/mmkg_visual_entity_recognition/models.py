from typing import Tuple
from pathlib import Path

import torch
from PIL import Image
from torch import nn
from torchvision.models import get_model, get_model_weights


class ImageEntityRecognition(nn.Module):
    def __init__(self, model_name: str = "resnet50"):
        super().__init__()

        weights = get_model_weights(model_name).DEFAULT
        self.model = get_model(model_name, weights=weights)
        self.transforms = weights.transforms()

        with open(Path(__file__).parent / "classes.txt") as f:
            labels = map(lambda x: x.strip(), f.readlines())
            labels = list(labels)
        self.labels = labels

    @property
    def device(self):
        return next(self.parameters()).device

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        return self.model(images)

    @torch.no_grad()
    def inference(self, image: Image.Image) -> Tuple[int, str, float]:
        image = self.transforms(image).to(self.device)
        logits = self.forward(image[None])[0]
        probs = logits.softmax(0)
        prob, label_id = probs.max(0)

        label_id = label_id.item()
        label = self.labels[label_id]
        prob = prob.item()

        return label_id, label, prob
