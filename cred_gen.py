import boto3
import argparse
import subprocess
import time
from dotenv import dotenv_values

#TODO
# doc strings and tests

class RearcSTSCredGen:
    def __init__(self, token_code, main_profile, temp_cred_profile):
        self.main_profile = main_profile
        self.temp_cred_profile = temp_cred_profile
        self.sts_client =  boto3.session.Session(profile_name=self.main_profile).client("sts")
        self.config = dotenv_values(".env")
        self.token_code = token_code

    def session_token(self):
        return self.sts_client.get_session_token(DurationSeconds=43200, SerialNumber=self.config["mfa_arn"],TokenCode=self.token_code)

    def update_profile(self):
        credentials = self.session_token()["Credentials"]
        commands = [f"aws configure set aws_access_key_id {credentials['AccessKeyId']} --profile {self.temp_cred_profile}",
            f"aws configure set aws_secret_access_key {credentials['SecretAccessKey']} --profile {self.temp_cred_profile}",
            f"aws configure set aws_session_token {credentials['SessionToken']} --profile {self.temp_cred_profile}"]

        for command in commands:
            #need to sleep between to commands to make sure we include all entries under the same profile
            #TODO
            #would prefer to do this without subprocess, but the aws configure commmand updates profiles in place if they are there.
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description='utility for updating temporary credentials to assume a role')
    parser.add_argument('--token_code', dest="token_code", type=str,
                        help='token code generated from your mfa device')
    parser.add_argument('--main_profile', dest="main_profile", type=str,
                        help="primary profile name to use.  should have credentials for your primary AWS account user")
    parser.add_argument('--temp_profile', dest="temp_profile", type=str,
                        help="temp profile name to use.  you will be able to use this profile to assume the role within the target account.")

    args = parser.parse_args()

    cred_gen = RearcSTSCredGen(token_code=args.token_code, main_profile=args.main_profile, temp_cred_profile=args.temp_profile)
    cred_gen.update_profile()

if __name__ == "__main__":
    main()