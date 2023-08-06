import dataclasses
from ..shared import contactupdate as shared_contactupdate
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class PutCrmContactApplicationJSON:
    access_token: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    contact: shared_contactupdate.ContactUpdate = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('contact') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutCrmContactRequests:
    application_xml: bytes = dataclasses.field(metadata={'request': { 'media_type': 'application/xml' }})
    object: Optional[PutCrmContactApplicationJSON] = dataclasses.field(default=None, metadata={'request': { 'media_type': 'application/json' }})
    

@dataclasses.dataclass
class PutCrmContactRequest:
    request: Optional[PutCrmContactRequests] = dataclasses.field(default=None)
    

@dataclass_json
@dataclasses.dataclass
class PutCrmContactResponseBody:
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('id') }})
    

@dataclasses.dataclass
class PutCrmContactResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutCrmContactResponseBody] = dataclasses.field(default=None)
    