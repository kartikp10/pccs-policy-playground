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
export PRISMA_API_URL=https://api.prismacloud.io
export PC_ACCESS_KEY=<your-access-key>
export PC_SECRET_KEY=<your-secret-key>
```
Alternatively, you can pass them as a command line argument in addition to other arguments:

```commandline
python -m pccs.main --auth "https://api.prismacloud.io::<your-access-key>::<your-secret-key>" --list <any additinoal args>
```

> 💡 Note: You may need to turn off VPN for using these scripts.

### List custom policies

- Filter all custom policies (more on filters https://prisma.pan.dev/api/cloud/cspm/policy#operation/get-policy-filters-and-options):
```commandline
python -m pccs.main --list -q policy.policyMode=custom
```
- List all policies (custom and otb):
```commandline
python -m pccs.main --list
```
- List all policies (verbose):
```commandline
python -m pccs.main --list --verbose
```
- Get custom policy by ID:
```commandline
python -m pccs.main -id xxxxxxx --list
```

### Publish custom policy

The command below will create the policy present in the filepath supplied to the `--publish` argument
```commandline
python -m pccs.main -p -f policies/azure/BC_AZ_C_001.yml
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
python -m pccs.main --delete -id 900776649199591424_AZR_1649355555209
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
python -m pccs.main --update -f policies/azure/BC_AZ_C_001.yml -id  900776649199591424_AZR_1649355555209    
```
