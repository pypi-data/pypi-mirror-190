"""READER FILE FOR ZOHO RECRUIT"""
# pylint: disable=wrong-import-order,arguments-differ, broad-except, too-few-public-methods

from datetime import datetime
from typing import List, Dict, Union, Any, Generator

from sdc_dp_helpers.base_readers import APIRequestsSessionsReader
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import date_string_handler
from sdc_dp_helpers.zoho_recruit.zoho_recruit_sdk import EndPointFactory


class ZohoRecruitReader(APIRequestsSessionsReader):
    """Zoho Recruit Reader Class

    Args:
        BaseReader (_type_): API Reader Class
    """

    def __init__(self, secrets_filepath: str, config_filepath: str):
        self.configs: Dict[Any, Any] = load_file(config_filepath)
        self.secrets: Dict[Any, Any] = load_file(secrets_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        handler_factory = EndPointFactory()
        handler = handler_factory.get_end_point_handler(
            end_point=self.configs["end_point"],
            session=self.sessions,
            secrets=self.secrets,
        )
        handler.get_oauth_token()
        return handler

    def _query_handler(
        self, configs: Dict[Any, Any]
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Method ot get the endpoint handler to use

        Args:
            config (Dict[Any, Any]): configs passed to the API endpoint handler

        Returns:
            List[Dict[Any, Any]]:  A list of dictionary of each response
        """

        results = self.service.fetch_data(configs=configs)

        for result in results:
            yield result

    def run_query(self):
        """Calls the Query Handler"""
        modified_since = None
        run_date = datetime.now().date().isoformat().replace("-", "")
        if self.configs.get("modified_since"):
            modified_since = date_string_handler(self.configs["modified_since"])
            modified_since = datetime.strftime(
                modified_since, "%Y-%m-%dT%H:%M:%S+00:00"
            )

        self.configs["modified_since"] = modified_since
        end_point = self.configs["end_point"]
        results = self._query_handler(configs=self.configs)

        for payload in results:
            if payload["data"] != []:
                payload["end_point"] = end_point
                payload["date"] = run_date
                self.is_success()
                yield payload
                continue
            self.not_success()
