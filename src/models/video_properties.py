from dataclasses import dataclass
from uuid import UUID


@dataclass
class VideoProperties:
    external_id: UUID
    link: str
    text: str
    valid: bool
    description: str

    def to_dict(self):
        return {
            'external_id': str(self.external_id),
            'link': self.link,
            'text': self.text,
            'valid': self.valid,
            'description': self.description
        }
