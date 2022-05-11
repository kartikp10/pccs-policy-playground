import json
import sys
import requests
import yaml

from requests import exceptions
from pathlib import Path
from tabulate import tabulate

from pccs.common import auth


def get_custom_policies(base_url, token, query, bc_proxy=False, verbose=False):
    """
    List policies: https://prisma.pan.dev/api/cloud/cspm/policy#operation/get-policies-v2
    """
    headers = auth.get_auth_headers(token)
    try:
        if bc_proxy:
            url = f"{base_url}/bridgecrew/api/v1/policies/table/data"
            response = requests.request("GET", url, headers=headers)
            response.raise_for_status()
            res_json = json.loads(response.text)
            if verbose:
                # remove accountsData key
                for p in res_json.get("data"):
                    p.pop("accountsData")
                print(json.dumps(res_json.get("data"), indent=4))
            else:
                print(f'Found {len(res_json.get("data"))} custom policies\n')
                print("Policy ID: Title")
                for p in res_json.get("data"):
                    print(f'{p.get("id")}: {p.get("title")}')
        else:
            url = f"{base_url}/v2/policy"
            response = requests.request("GET", url, headers=headers, params=json.loads(json.dumps(query)))
            response.raise_for_status()
            res_json = json.loads(response.text)
            if verbose:
                print(json.dumps(res_json, indent=4))
            else:
                print(f'Found {len(res_json)} custom policies\n')
                print(f'PolicyId: Name')
                for p in res_json:
                    print(f'{p.get("policyId")}: {p.get("name")}')
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def get_policy_filters(base_url, token):
    """
    List available policy filters: https://prisma.pan.dev/api/cloud/cspm/policy#operation/get-policy-filters-and-options
    """
    url = f"{base_url}/filter/policy/suggest"
    headers = auth.get_auth_headers(token)
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def get_custom_policy_by_id(base_url, token, policy_id, bc_proxy=False):
    """
    Get policy by ID: https://prisma.pan.dev/api/cloud/cspm/policy#operation/get-policy
    """
    headers = auth.get_auth_headers(token)
    try:
        if bc_proxy:
            url = f"{base_url}/bridgecrew/api/v1/policies/{policy_id}"
            response = requests.request("GET", url, headers=headers)
            response.raise_for_status()
            res_json = json.loads(response.text)
            print(json.dumps(res_json, indent=4))
        else:
            url = f"{base_url}/policy/{policy_id}"
            response = requests.request("GET", url, headers=headers)
            response.raise_for_status()
            res_json = json.loads(response.text)
            print(json.dumps(res_json, indent=4))
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def create_custom_policy(base_url, token, file_path, bc_proxy=False, status=False):
    """
    Creates a new build policy: https://prisma.pan.dev/api/cloud/cspm/policy#operation/add-policy
    """
    headers = auth.get_auth_headers(token, True)
    payload = get_policy_payload(file_path, bc_proxy, status)
    try:
        if bc_proxy:
            url = f"{base_url}/bridgecrew/api/v1/policies"
        else:
            url = f"{base_url}/policy"
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
        response.raise_for_status()
        print("Policy published successfully.")
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred while publishing policy: {e}")
        sys.exit(1)


def delete_custom_policy_by_id(base_url, token, policy_id, bc_proxy=False):
    headers = auth.get_auth_headers(token)
    try:
        if bc_proxy:
            url = f"{base_url}/bridgecrew/api/v1/policies/{policy_id}"
        else:
            url = f"{base_url}/policy/{policy_id}"
        response = requests.request("DELETE", url, headers=headers)
        response.raise_for_status()
        if response.text:
            res_json = json.loads(response.text)
            print(json.dumps(res_json, indent=4))
        print("Deleted successfully.")
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while deleting policy: {e}")


def update_policy_status(base_url, token, policy_id, status):
    """
     https://prisma.pan.dev/api/cloud/cspm/policy#operation/update-policy-status
    """
    url = f"{base_url}/policy/{policy_id}/status/{status}"
    headers = auth.get_auth_headers(token)
    try:
        response = requests.request("PATCH", url, headers=headers)
        response.raise_for_status()
        print(f"{'Enabled' if status else 'Disabled'} {policy_id}")
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def update_custom_policy_by_id(base_url, token, policy_id, file_path, status, bc_proxy=False):
    """
    https://prisma.pan.dev/api/cloud/cspm/policy#operation/update-policy
    """
    headers = auth.get_auth_headers(token, True)
    payload = get_policy_payload(file_path, bc_proxy, status)
    if bc_proxy:
        url = f"{base_url}/bridgecrew/api/v1/policies/{policy_id}"
    else:
        url = f"{base_url}/policy/{policy_id}"
    try:
        response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
        response.raise_for_status()
        print("Policy updated successfully.")
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred while updating policy: {e}")
        sys.exit(1)


def get_policy_payload(file_path, bc_proxy, status):
    path = Path(file_path).resolve()
    try:
        with open(path, "r") as stream:
            try:
                policy_data = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
                sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    if policy_data["metadata"]["id"]:
        print(f"Note: Found unnecessary attribute \"id: {policy_data['metadata']['id']}\" in policy. Ignoring it for "
              f"publishing.")
        policy_data["metadata"].pop("id", None)
    if bc_proxy:
        return {"code": policy_data}
    else:
        # extra keys that cannot be parsed from a bc policy are:
        #   1. complianceMetadata
        #   2. labels
        #   3. recommendation
        #   4. enabled
        payload = {
            "cloudType": policy_data['scope']['provider'],
            "complianceMetadata": [],
            "description": policy_data['metadata']['guidelines'],
            "labels": [],
            "name": policy_data['metadata']['name'],
            "policySubTypes": ["build"],
            "policyType": "config",
            "recommendation": "",
            "rule": {
                "children": [
                    {
                        "metadata": {
                            "code": policy_data
                        },
                        "type": "build",
                        "recommendation": ""
                    }
                ],
                "name": policy_data['metadata']['name'],
                "parameters": {
                    "savedSearch": "false",
                    "withIac": "true"
                },
                "type": "Config"
            },
            "severity": policy_data['metadata']['severity'],
            "enabled": status
        }
        return payload

