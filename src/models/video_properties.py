from dataclasses import dataclass
from uuid import UUID


@dataclass
class VideoProperties:
    external_id: UUID
    link: str
    text: str

    def to_dict(self):
        return {
            'external_id': str(self.external_id),
            'link': self.link,
            'text': ".".join(self.text)
        }
