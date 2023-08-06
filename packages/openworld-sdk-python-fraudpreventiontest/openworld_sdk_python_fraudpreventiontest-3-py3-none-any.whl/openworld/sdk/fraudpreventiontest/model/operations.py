# Copyright 2022 Expedia, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .authorize import Authorize
from .verify import Verify
from .refund import Refund
from .capture import Capture
from .authorize_reversal import AuthorizeReversal
from dataclasses_json import config
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import List

def require_value(var: str):
    raise TypeError(f'None value not allowed for attribute {var}!')


@dataclass_json
@dataclass
class Operations:
    """@dataclass Operations All operations related to a payment throughout its lifespan. An operation represents an event external to Fraud Prevention Service that specifies to perform a payment operation. Possible operation types include:  - `Verify`  - `Authorize`  - `AuthorizeReversal`  - `Capture`  - `Refund` 

    Attributes:
        verify(Verify):

        authorize(Authorize):

        authorize_reversal(AuthorizeReversal):

        capture(Capture):

        refunds([Refund]):
    """
    verify: Optional[Verify] = field(default=None, metadata=config(exclude=lambda f: f is None))
    authorize: Optional[Authorize] = field(default=None, metadata=config(exclude=lambda f: f is None))
    authorize_reversal: Optional[AuthorizeReversal] = field(default=None, metadata=config(exclude=lambda f: f is None))
    capture: Optional[Capture] = field(default=None, metadata=config(exclude=lambda f: f is None))
    refunds: Optional[List[Refund]] = field(default=None, metadata=config(exclude=lambda f: f is None))



