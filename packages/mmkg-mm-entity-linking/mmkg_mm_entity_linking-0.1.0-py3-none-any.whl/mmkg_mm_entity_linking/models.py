from typing import List

import torch
from PIL import Image
from torch import nn

from .clip import load, tokenize


class MMEntityLinking(nn.Module):
    def __init__(self, model_name: str = "ViT-B/32"):
        super().__init__()

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = load(
            name=model_name,
            device=device,
            jit=True,
        )

    @property
    def device(self):
        return next(self.parameters()).device

    @torch.no_grad()
    def inference(self, image: Image.Image, texts: List[str]) -> List[float]:
        image = self.preprocess(image)[None].to(self.device)
        texts = tokenize(texts).to(self.device)

        logits_per_image, _ = self.model(image, texts)
        probs = logits_per_image.softmax(dim=-1).cpu().tolist()

        return probs
