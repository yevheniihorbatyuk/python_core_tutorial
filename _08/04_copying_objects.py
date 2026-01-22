"""
Module 8.4: Shallow vs deep copy.
"""

from __future__ import annotations

import copy


class Pipeline:
    def __init__(self, steps: list[str]) -> None:
        self.steps = list(steps)

    def __repr__(self) -> str:
        return f"Pipeline(steps={self.steps})"


if __name__ == "__main__":
    print("=== Shallow vs Deep Copy on nested dict ===")
    config = {
        "thresholds": [0.1, 0.2],
        "tags": ["baseline"],
        "params": {"alpha": 0.5},
    }

    shallow = copy.copy(config)
    deep = copy.deepcopy(config)

    config["thresholds"].append(0.3)
    config["params"]["alpha"] = 0.8

    print("Original:", config)
    print("Shallow:", shallow)
    print("Deep:", deep)

    print("\n=== Copying custom objects ===")
    pipeline = Pipeline(["load", "clean", "train"])
    pipeline_shallow = copy.copy(pipeline)
    pipeline_deep = copy.deepcopy(pipeline)

    pipeline.steps.append("evaluate")

    print("Original:", pipeline)
    print("Shallow:", pipeline_shallow)
    print("Deep:", pipeline_deep)
