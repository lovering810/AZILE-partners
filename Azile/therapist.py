from pathlib import Path
import yaml


class Therapist:
    def __init__(self, personality_yaml) -> None:
        self.from_file(personality_yaml=personality_yaml)

    def from_file(self, personality_yaml: Path):
        with open(personality_yaml, "r+") as fyle:
            personality = yaml.load(fyle)
        for key in personality:
            setattr(self, key, personality[key])
