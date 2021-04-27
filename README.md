# aws_sts_mfa_gen

Command line utility for generating and refreshing temporary IAM credentials for role assumption where MFA is required.
See https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/ and https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html for more details.
## Installation
- clone the repo
- navigate to cloned directory, execute ```touch .env```
- populate .env file with ```mfa_arn=$ARN_OF_YOUR_MFA_DEVICE```
- ensure you are using python 3.8.2+ (use virtualenv, pyenv, etc.)
- execute: ```pip install -r requirements.txt```

## Requirements
A named profile under ~/.aws/credentials for your main account.  This profile must have permission to assume the role declared in the role profile.
```
[main]
aws_access_key_id=REDACTED
aws_secret_access_key=REDACTED
region=us-east-1
```

A named profile that you will use in conjunction with the temporary credentials that you will generate.  
You must supply the arn of the role that you want to assume.  Name this role relative to the account/role you will be working with. 

```
[role_profile]
role_arn = REDACTED
source_profile = temp_account_profile
```

## Usage
Given the profiles configured above, execute:
``` 
python cred_gen.py --token_code=$CODE_GENERATED_FROM_MFA_DEVICE --main_profile=main --temp_profile=temp_account_profile
```


This will generate a new profile within ~/.aws/credentials or update it in place, populated with:
```
[temp_account_profile]
aws_access_key_id = REDACTED
aws_secret_access_key = REDACTED
aws_session_token = REDACTED
```

For clarity's sake, **this will update the profile entries if it already exists.**  make sure you are passing the command a profile you want to update.

You can now use these temporary credentials to assume the role within the target account.  Ex:
```aws s3 ls --profile=role_profile```




