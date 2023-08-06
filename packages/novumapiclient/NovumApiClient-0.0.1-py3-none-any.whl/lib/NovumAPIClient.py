import json
import requests
import urllib
from http import HTTPStatus

host = "https://novum-batteries.com/"


class APIClient:
    def __init__(self, _user):
        self._user = _user

    def _fetch(self, use, url, host=host, data={}, filter=None, option=None, header={}, timeout=4):
        full_url = host + url
        header.update(dict({"Content-Type": "application/json", "Authorization": "Bearer " + self._user["jwt"]}))
        headers = header
        param = {"filter": json.dumps(filter), "option": json.dumps(option)}
        params = urllib.parse.urlencode(param)
        data = json.dumps(data)

        if use == "get":
            response = requests.get(
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
            )
        if use == "post":
            response = requests.post(
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
            )
        if use == "put":
            response = requests.put(
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
            )
        if use == "delete":
            response = requests.delete(
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
            )
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error: ", response.status_code)

    # ********************************************************
    # Section for the Service Center info
    # ********************************************************

    def ping(self) -> dict:
        response = self._fetch("get", "api/batman/v1/")
        return response

    def get_info(self) -> dict:
        response = self._fetch("get", "api/batman/v1/info")
        return response

    def get_version(self) -> dict:
        response = self._fetch("get", "api/batman/v1/version")
        return response

    # ********************************************************
    # Section for the users
    # ********************************************************

    def login(self, email, password, storeUser=True) -> dict:
        header = {"authorization": "auth", "content-type": "application/json"}
        payload = {"username": email, "password": password}
        response = requests.post(
            "https://novum-batteries.com/api/batman/v1/login", data=json.dumps(payload), headers=header
        )
        if response.status_code != HTTPStatus.OK and storeUser == True:
            print("%s (%s)", response.text, response.status_code)
            return dict(profile=dict(email=None), jwt=None, user_id=None, token=None, jwt_auth_header=None)
        user = response.json()
        self._user = user
        return user

    def logout(self) -> dict:
        response = self._fetch("get", "api/batman/v1/logout")
        return response

    def check_current_user_still_authenticated(self) -> dict:
        response = self._fetch("get", "api/batman/v1/check_token")
        return response

    # ********************************************************
    # Section for the Battery Types
    # ********************************************************

    def get_battery_types(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/batteryTypes", filter=filter, option=option, timeout=timeout)
        return response

    def get_battery_types_count(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/batteryTypes/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_battery_types_by_id(self, battery_type_id, timeout=4) -> dict:
        response = self._fetch("get", f"api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout)
        return response

    def remove_battery_types_by_id(self, battery_type_id, timeout=4) -> dict:
        response = self._fetch("delete", f"api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout)
        return response

    def create_batttery_type(
        self,
        battery_type={
            "name": "name",
            "manufacturer": "manufacturer",
            "nominal_voltage": "nominal_voltage",
            "nominal_capacity": "nominal_capacity",
        },
        timeout=4,
        **kwargs,
    ) -> dict:
        battery_dict = battery_type
        battery_dict.update(kwargs)
        response = self._fetch("post", "api/batman/v1/batteryTypes", data=battery_dict, timeout=timeout)
        return response

    def update_batttery_type_by_id(self, battery_type_id, battery_type_info, timeout=4) -> dict:
        response = self._fetch(
            "put", f"api/batman/v1/batteryTypes/{battery_type_id}", data=battery_type_info, timeout=timeout
        )
        return response

    # ********************************************************
    # Section for the Datasets
    # ********************************************************

    def dataset_exists_on_remote(self, id, timeout=4) -> bool:
        response = self._fetch("get", f"api/batman/v1/datasets/{id}", timeout=timeout)
        try:
            len(response["measured"]["measurement_cycles"]) != 0
            return True
        except:
            return False

    def create_dataset(self, dataset, timeout=4) -> dict:
        response = self._fetch("post", "api/batman/v1/datasets/", data=dataset, timeout=timeout)
        return response

    def post_dataset(self, dataset, timeout=4) -> dict:
        response = self._fetch("post", "api/batman/v1/datasets/", data=dataset, timeout=timeout)
        return response

    def get_dataset_by_id(self, dataset_id, timeout) -> dict:
        response = self._fetch("get", f"api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    def get_datasets(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/datasets", filter=filter, option=option, timeout=timeout)
        return response

    def get_datasets_count(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/datasets/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_datasets_count_by_battery(self, battery, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"meta.battery._id": battery.id}
        filter_with_id.update(filter)
        response = self._fetch(
            "get", "api/batman/v1/datasets/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def update_dataset_by_id(self, dataset_id, timeout) -> dict:
        response = self._fetch("post", f"api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    def remove_dataset_by_id(self, dataset_id, timeout) -> dict:
        response = self._fetch("delete", f"api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    # ********************************************************
    # Section for the Battery
    # ********************************************************

    def create_battery(self, battery, timeout=4) -> dict:
        response = self._fetch("post", "api/batman/v1/", data=battery, timeout=timeout)
        return response

    def get_battery_by_id(self, battery_id, timeout) -> dict:
        response = self._fetch("get", f"api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return response

    def update_battery(self, battery, header, timeout=4) -> dict:
        response = self._fetch("put", f"api/batman/v1/batteries/{battery.id}", header=header, timeout=timeout)
        return response

    def update_battery_by_id(self, battery_id, battery_update, header, timeout=4) -> dict:
        response = self._fetch(
            "put", f"api/batman/v1/batteries/{battery_id}", data=battery_update, header=header, timeout=timeout
        )
        return response

    def remove_battery_by_id(self, battery_id, timeout) -> dict:
        response = self._fetch("delete", f"api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return response

    def get_batteries(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/batteries", filter=filter, option=option, timeout=timeout)
        return response

    def get_batteries_count(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch("get", "api/batman/v1/batteries/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_children_of_battery_by_id(self, parent_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.parent": parent_battery_id}
        filter_with_id.update(filter)
        response = self._fetch("get", "api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_children_of_battery_by_id_count(self, parent_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.parent": parent_battery_id}
        filter_with_id.update(filter)
        response = self._fetch(
            "get", "api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def get_leaves_of_battery_by_id(self, ancestor_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch("get", "api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_leaves_of_battery_by_id_count(self, ancestor_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch(
            "get", "api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def get_decendants_of_battery_by_id(self, ancestor_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch("get", "api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_decendants_of_battery_by_id_count(self, ancestor_battery_id, filter={}, option={}, timeout=4) -> dict:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch(
            "get", "api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    # ********************************************************
    # Section for the CapacityMeasurement
    # ********************************************************

    def create_capacity_measurement(self, capacity_measurement, timeout=4) -> dict:
        response = self._fetch("post", "api/batman/v1/capacityMeasurements", data=capacity_measurement, timeout=timeout)
        return response

    def update_capacity_measurement_by_id(self, capacity_measurement_id, capacity_measurement, timeout=4) -> dict:
        response = self._fetch(
            "put",
            f"api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            data=capacity_measurement,
            timeout=timeout,
        )
        return response

    def remove_capacity_measurement_by_id(self, capacity_measurement_id, timeout=4) -> dict:
        response = self._fetch(
            "delete", f"api/batman/v1/capacityMeasurements/{capacity_measurement_id}", timeout=timeout
        )
        return response

    def get_capacity_measurement(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch(
            "get", "api/batman/v1/capacityMeasurements", filter=filter, option=option, timeout=timeout
        )
        return response

    def get_capacity_measurement_count(self, filter={}, option={}, timeout=4) -> dict:
        response = self._fetch(
            "get", "api/batman/v1/capacityMeasurements/count", filter=filter, option=option, timeout=timeout
        )
        return response

    def get_capacity_measurement_by_id(self, capacity_measurement_id, timeout=4) -> dict:
        response = self._fetch("get", f"api/batman/v1/capacityMeasurements/{capacity_measurement_id}", timeout=timeout)
        return response

    def get_capacity_measurements_count_by_battery(self, battery, timeout=4) -> dict:
        filter = {"battery._id": battery.id}
        response = self._fetch("get", "api/batman/v1/capacityMeasurements/count", filter=filter, timeout=timeout)
        return response

    def capacity_measuremente_exists_on_remote(self, id, timeout=4) -> dict:
        response = self._fetch("get", f"api/batman/v1/capacityMeasurements/{id}", filter=filter, timeout=timeout)
        return response.id == id

    # ********************************************************
    # Section for the Measurements
    # ********************************************************

    def get_latest_measurement(self, device_id, count=1, timeout=4) -> dict:
        response = self._fetch("get", f"api/batman/v1/devices/{device_id}/measurements/last/${count}", timeout=timeout)
        return response

    def write_device_measurements(self, device_measurements, timeout=4) -> dict:
        response = self._fetch("post", "api/time-series/v1/measurements", data=device_measurements, timeout=timeout)
        return response
