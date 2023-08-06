import dataclasses
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional
from vesselapi import utils

class ConnectionIntegrationIDEnum(str, Enum):
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    PIPEDRIVE = "pipedrive"

class ConnectionStatusEnum(str, Enum):
    NEW_CONNECTION = "NEW_CONNECTION"
    INITIAL_SYNC = "INITIAL_SYNC"
    READY = "READY"


@dataclass_json
@dataclasses.dataclass
class Connection:
    connection_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('connectionId') }})
    created_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('createdTime') }})
    integration_id: Optional[ConnectionIntegrationIDEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('integrationId') }})
    last_activity_date: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('lastActivityDate') }})
    native_org_url: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('nativeOrgURL') }})
    status: Optional[ConnectionStatusEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('status') }})
    