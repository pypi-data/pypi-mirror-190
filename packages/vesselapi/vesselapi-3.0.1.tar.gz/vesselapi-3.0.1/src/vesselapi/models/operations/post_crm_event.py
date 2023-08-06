import dataclasses
from ..shared import eventcreate as shared_eventcreate
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class PostCrmEventRequestBody:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    event: Optional[shared_eventcreate.EventCreate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('event') }})
    

@dataclasses.dataclass
class PostCrmEventRequest:
    request: Optional[PostCrmEventRequestBody] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclass_json
@dataclasses.dataclass
class PostCrmEventResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PostCrmEventResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PostCrmEventResponseBody] = dataclasses.field(default=None)
    