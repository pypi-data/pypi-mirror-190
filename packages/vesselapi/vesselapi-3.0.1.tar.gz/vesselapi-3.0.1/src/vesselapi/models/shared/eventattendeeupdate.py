import dataclasses
from dataclasses_json import dataclass_json
from typing import Optional
from vesselapi import utils


@dataclass_json
@dataclasses.dataclass
class EventAttendeeUpdate:
    status: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('status') }})
    