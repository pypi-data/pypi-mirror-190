import dataclasses
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional
from vesselapi import utils

class IntegrationIntegrationIDEnum(str, Enum):
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    PIPEDRIVE = "pipedrive"


@dataclass_json
@dataclasses.dataclass
class Integration:
    icon_url: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('iconURL') }})
    integration_id: Optional[IntegrationIntegrationIDEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('integrationId') }})
    name: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('name') }})
    