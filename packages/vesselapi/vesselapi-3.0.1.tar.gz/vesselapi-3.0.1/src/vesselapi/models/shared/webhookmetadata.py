import dataclasses
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class WebhookMetadata:
    connection_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('connectionId') }})
    created_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    webhook_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('webhookId') }})
    webhook_url: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('webhookUrl') }})
    