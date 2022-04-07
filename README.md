# pccs-policy-playground


## Requirements

- Python: >= 3
- pipenv:
If you don't have pipenv installed, [install it first](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv). 


## Installation

```commandline
pip install --user pipenv
```
Install project dependencies. 
```commandline
pipenv install
```

## Usage

### Required authentication details

The following environment variables need to be set. 

```commandline
export PC_API_URL=https://api.prismacloud.io
export PC_ACCESS_KEY=<your-access-key>
export PC_SECRET_KEY=<your-secret-key>
```
Alternatively, you can pass them as a command line argument like below:

```commandline
python pccs/main.py --auth "https://api.prismacloud.io::<your-access-key>::<your-secret-key>"
```

> Note: You may need to run off VPN for using these scripts.

### List custom policies

- List all custom policies (summary):
```commandline
python pccs/main.py --list
```
- List all custom policies (verbose):
```commandline
python pccs/main.py --list --verbose
```
- Get custom policy by ID:
```commandline
python pccs/main.py --policy-id xxxxxxx 
```

### Publish custom policy

The command below will create the policy present in the filepath supplied to the `--publish` argument
```commandline
python pccs/main.py --publish policies/azure/BC_AZ_C_001.yml
```
Output:
```commandline
Note: Found unnecessary attribute "id: BC_AZ_C_001" in policy. Ignoring it for publishing.
{
    "policy": "900776649199591424_AZR_1649355555209"
}
Policy published successfully.

```

### Delete custom policy

The command below will delete the policy with the id passed to the `--delete` argument.
```commandline
python pccs/main.py --delete 900776649199591424_AZR_1649355555209
```
Output:
```commandline
{
    "policy": "900776649199591424_AZR_1649355555209"
}
Deleted successfully.
```

### Update custom policy

```commandline
python pccs/main.py --update policies/azure/BC_AZ_C_001.yml --policy-id  900776649199591424_AZR_1649355555209    
```
