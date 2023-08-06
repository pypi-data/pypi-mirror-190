import dataclasses
from ..shared import eventattendeeupdate as shared_eventattendeeupdate
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class PutCrmEventAttendeeResponseBody:
    access_token: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('accessToken') }})
    event_attendee: Optional[shared_eventattendeeupdate.EventAttendeeUpdate] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('eventAttendee') }})
    

@dataclasses.dataclass
class PutCrmEventAttendeeResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[PutCrmEventAttendeeResponseBody] = dataclasses.field(default=None)
    