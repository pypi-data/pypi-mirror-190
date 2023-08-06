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

from openworld.sdk.core.constant import header
import platform

from openworld.sdk.fraudpreventiontest.model.order_purchase_update_request import OrderPurchaseUpdateRequest

import platform
from openworld.sdk.core.client.api import ApiClient
from openworld.sdk.core.configuration.client_config import ClientConfig
from furl import furl
from uuid import UUID, uuid4


class OrderPurchaseUpdateClient:
    def __init__(self, client_config: ClientConfig):
        python_version = platform.python_version()
        os = platform.platform().split('-')
        os_name = os[0]
        os_version = os[1]
        sdk_metadata = f'open-world-sdk-python-fraudpreventiontest/v4'

        self.__api_client = ApiClient(client_config)
        self.__user_agent = f'{sdk_metadata} (Python {python_version}; {os_name} {os_version})'

    def update(self, order_purchase_update_request: OrderPurchaseUpdateRequest,
            transaction_id: UUID = uuid4()) -> None:
        """

        Args:

            order_purchase_update_request(OrderPurchaseUpdateRequest): An OrderPurchaseUpdate request may be of one of the following types `ORDER_UPDATE`, `CHARGEBACK_FEEDBACK`, `INSULT_FEEDBACK`, `REFUND_UPDATE`, `PAYMENT_UPDATE`. 
        """
        request_url = furl(self.__api_client.endpoint)
        request_url /= '/order/purchase/update'
        request_url.path.normalize()

        return self.__api_client.call(
            request_headers={  header.TRANSACTION_ID: str(transaction_id), header.USER_AGENT: header.OPENWORLD_SDK_PYTHON + str(self.__user_agent)},
            method='post',
            obj=order_purchase_update_request,
            response_model=None,
            url=request_url
        )

