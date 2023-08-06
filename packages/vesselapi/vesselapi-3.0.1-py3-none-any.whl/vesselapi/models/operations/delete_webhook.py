import dataclasses
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class DeleteWebhookRequestBody:
    access_token: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    webhook_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('webhookId') }})
    

@dataclasses.dataclass
class DeleteWebhookRequest:
    request: Optional[DeleteWebhookRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class DeleteWebhookResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    