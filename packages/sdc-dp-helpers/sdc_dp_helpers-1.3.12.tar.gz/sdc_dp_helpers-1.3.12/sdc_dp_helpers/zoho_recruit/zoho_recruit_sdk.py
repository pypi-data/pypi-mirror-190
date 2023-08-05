"""CUSTOM INTERFACES FOR ZOHO RECRUIT ENDPOINTS"""
# pylint: disable=broad-except,too-few-public-methods,too-few-public-methods,too-many-arguments,arguments-differ, too-many-locals

from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import Union, Any, List, Dict, Generator
import requests
from requests.exceptions import HTTPError


class Autheticator:
    """Authenticator Class for Zoho Recruit"""

    next_refresh: datetime = datetime.now()

    def authenticate(
        self, sessions: requests.Session, secrets: Dict[Any, Any]
    ) -> Dict[str, Any]:
        """Authentication method

        Args:
            sessions (requests.Session): requests.Sessions
            secrets (Dict[Any, Any]): dictionary having secrets

        Returns:
            str : the access_token for zoho
        """
        response = {
            "access_token": None,
            "api_domain": "https://www.zohoapis.com",
            "token_type": "Bearer",
            "expires_in": 0,
        }
        try:
            response = sessions.post(
                url="https://accounts.zoho.com/oauth/v2/token?",
                params={
                    "refresh_token": secrets["refresh_token"],
                    "client_id": secrets["client_id"],
                    "client_secret": secrets["client_secret"],
                    "grant_type": "refresh_token",
                },
                timeout=61,
            ).json()
        except Exception as exc:
            print(f"Error on refreshing oauth_token {exc}")
        seconds_to_expiry = int(response["expires_in"]) - 100
        self.next_refresh = datetime.now() + timedelta(seconds=seconds_to_expiry)

        print(f"new oauth_token {response['access_token']}")
        print(f"next oauth_token_refresh {self.next_refresh}")
        return response["access_token"]


class APICallHandler(ABC):
    """Interface for API Call Method"""

    def __init__(self, session: requests.Session):
        self.session = session

    @abstractmethod
    def make_api_call(self, **kwargs):
        """Make API Call"""
        raise NotImplementedError


class AssessmentAPICallHandler(APICallHandler):
    """Class for Making API Call"""

    def make_api_call(
        self,
        oauth_tokens: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            json={
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Zoho-oauthtoken {oauth_tokens}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )
        response.raise_for_status()
        status_code, reason = response.status_code, response.reason
        data = None
        more_records = False
        if response.status_code == 200:
            results = response.json()
            data = results["Assessments"]
            more_records = False
        return data, more_records, status_code, reason


class RecordsAPICallHandler(APICallHandler):
    """Class for Making API Call"""

    def make_api_call(
        self,
        oauth_tokens: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            params={
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Authorization": f"Zoho-oauthtoken {oauth_tokens}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )
        response.raise_for_status()
        status_code, reason = response.status_code, response.reason
        data = None
        more_records = False
        if response.status_code == 200:
            results = response.json()
            data = results["data"]
            more_records = results.get("info", {"more_records": False}).get(
                "more_records"
            )
        return data, more_records, status_code, reason


class UsersAPICallHandler(APICallHandler):
    """Class for Making API Call"""

    def make_api_call(
        self,
        oauth_tokens: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            json={
                "type": kwargs.get("users_type"),
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Zoho-oauthtoken {oauth_tokens}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )
        response.raise_for_status()
        status_code, reason = response.status_code, response.reason
        data = None
        more_records = False
        if response.status_code == 200:
            results = response.json()
            data = results["users"]
            more_records = results.get("info", {"more_records": False}).get(
                "more_records"
            )
        return data, more_records, status_code, reason


class APICallHandlerFactory:
    """Gets Us the API Call Handler"""

    def get_api_call_handler(self, method: str, session: requests.Session):
        """Gets for use the API Call Handler to Use"""
        api_call_handlers = {
            "assessments": AssessmentAPICallHandler,
            "records": RecordsAPICallHandler,
            "users": UsersAPICallHandler,
        }
        return api_call_handlers[method](session=session)


class BaseZohoRecruitHandler(ABC):
    """Base Class For Handling the Different Endpoints of Zoho Recruit"""

    base_url: str = "https://recruit.zoho.com/recruit/v2"
    file_size_limit: int = 104857  # 52428800
    authenticator = Autheticator()

    def __init__(
        self,
        session: requests.Session,
        secrets: Dict[Any, Any],
        file_size_limit: int = 5242880,  # 5MB
    ):
        self.session = session
        self.secrets = secrets
        self.oauth_tokens = None
        self.file_size_limit = file_size_limit

    def get_oauth_token(self):
        """Get zoho recruit oauth_token"""
        self.oauth_tokens = self.authenticator.authenticate(
            sessions=self.session, secrets=self.secrets
        )

    @abstractmethod
    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Make API Call and Paginate to End Point"""
        raise NotImplementedError

    def api_call(self, api_call_handler: APICallHandler, **kwargs):
        """Makes API Call"""
        results = None
        status_code = None
        reason = None
        more_records = True

        try:
            response = api_call_handler.make_api_call(
                # session=self.sessions,a
                oauth_tokens=self.oauth_tokens,
                url=kwargs.get("url"),
                module=kwargs.get("module"),
                page=kwargs.get("page"),
                per_page=kwargs.get("per_page"),
                sort_by=kwargs.get("sort_by"),
                sort_order=kwargs.get("sort_order"),
                modified_since=kwargs.get("modified_since"),
                users_type=kwargs.get("users_type"),
            )
            status_code, reason = response[2], response[3]
            results = response[0]
            more_records = response[1]

        except HTTPError as exc:
            print(
                f"error code: {exc.response.status_code} error message: {exc.response}"
            )
            if exc.response.status_code != 204:
                raise exc
            print("no more data to import. full import complete")
        except requests.exceptions.JSONDecodeError:
            print("no data for module modified after time limit provided")
        except Exception as err:
            print(f"failed with status {status_code} reason {reason}\n")
            raise err
        return results, more_records

    def paginate(
        self,
        api_call_handler: APICallHandler,
        module: str,
        configs: Dict[str, Any],
        **kwargs,
    ) -> Generator[Dict[Any, Any], None, None]:
        """Method to actually make the API call

        Args:
            configs: dict of parameters and headers for the API call

        Returns:
            Generator[Dict[Any, Any], None, None]: A generator of dictionary
        """

        result_array = []
        avg_record_size: int = 0
        current_size: int = 0
        page: int = configs.get("page", 1)
        per_page: int = configs.get("per_page", 200)
        modified_since: Union[None, str] = configs.get("modified_since")
        sort_by = configs.get("sort_by", "Modified_Time")
        sort_order = configs.get("sort_order", "desc")
        users_type = kwargs.get("users_type")
        page_limit: int = configs.get("page_limit", 1000)
        self.file_size_limit = configs.get("file_size_limit", 5242880)
        counter: int = 0

        more_records = True
        url = f"{self.base_url}/{module}"
        while more_records:
            print(
                f"getting module {module} page {page} "
                f"more_records {more_records} current_size {current_size}"
            )

            if self.authenticator.next_refresh <= datetime.now():
                print("Tokens Expired Refreshing ...")
                self.get_oauth_token()

            response = self.api_call(
                api_call_handler,
                url=url,
                module=module,
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
                modified_since=modified_since,
                users_type=users_type,
            )

            results, more_records = response[0], response[1]
            if results is None:
                yield {"start_page": page, "data": result_array}
                break

            if avg_record_size == 0:
                avg_record_size = results[0].__sizeof__()

            result_array = result_array + results
            current_size = len(result_array) * avg_record_size
            # current_size = sys.getsizeof(result_array)
            if counter > page_limit:  # exit if we go past page_limit
                print(f"\nExiting, we have reached page_limit {page_limit}\n")
                yield {"start_page": page, "data": result_array}
                break
            counter += 1

            if (current_size >= self.file_size_limit) or (more_records is False):
                yield {"start_page": page, "data": result_array}
                result_array = []
                current_size = 0
            page += 1


class RecordsEndpointHandler(BaseZohoRecruitHandler):
    """Class to Handle Get Records Endpoint"""

    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:

        api_factory = APICallHandlerFactory()
        for module in configs["modules"]:
            method = "records" if module != "Assessments" else "assessments"

            api_call_handler = api_factory.get_api_call_handler(
                method, session=self.session
            )
            results = self.paginate(api_call_handler, module=module, configs=configs)
            for result in results:
                result["module"] = module
                yield result


class UsersEndpointHandler(BaseZohoRecruitHandler):
    """Handler Class for Users Endpoint"""

    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:

        api_factory = APICallHandlerFactory()
        method = "users"
        api_call_handler = api_factory.get_api_call_handler(
            method, session=self.session
        )
        users_types = configs.get("types", ["AllUsers"])
        for users_type in users_types:
            results = self.paginate(
                api_call_handler, module=method, configs=configs, users_type=users_type
            )
            for result in results:
                result["module"] = users_type
                yield result


class EndPointFactory:
    """Factory For Getting the Endspoint Handler to Use"""

    def get_end_point_handler(
        self, end_point: str, session, secrets: Dict[Any, Any]
    ) -> BaseZohoRecruitHandler:
        """Factory Method That Decided the Endpoint Handler to Pass Along

        Args:
            end_point (str): end point to call see the url e.g records, users, profiles
            session (_type_): requests sessions
            secrets (Dict[Any, Any]): details for getting oauth_token i.e:
                    refresh_token: str
                    client_id: str
                    client_secret: str
                    grant_type: 'refresh_token'
                see link:
                    https://www.zoho.com/recruit/developer-guide/apiv2/refresh.html

        Raises:
            KeyError: if provided end point is not yet implemented

        Returns:
            BaseRecruitAPIHandler: instance of BaseRecruitAPIHandler
        """
        endpoints = {"records": RecordsEndpointHandler, "users": UsersEndpointHandler}
        if end_point not in endpoints:
            raise KeyError(f"provided endpoint not yet implemented: {end_point}")

        return endpoints[end_point](session=session, secrets=secrets)


if __name__ == "__main__":
    pass
