import argparse
import sys
import os

from pccs.common import auth, utils
from pccs.actions import policy_actions, suppression_actions


def run():
    parser = argparse.ArgumentParser('Manage PCCS policies')
    parser.add_argument('--auth', help='String with credentials and API endpoint - '
                                       '"https://api.prismacloud.io::<your-access-key>::<your-secret-key>"',
                        required=False)
    parser.add_argument('--list', '-l', help='List custom policies', required=False, action='store_true')
    parser.add_argument('--publish', '-p', help='Publish policy from file', required=False)
    parser.add_argument('--delete', '-d', help='Delete policy by ID', required=False)
    parser.add_argument('--update', '-u', help='Update policy by ID from file', required=False)
    parser.add_argument('--verbose', '-v', help='Print verbose response', required=False, action='store_true',
                        default=False)
    parser.add_argument('--policy-id', '-id', help='Get policy by ID', required=False)
    parser.add_argument('--create-suppression', '-s',
                        help='Suppress a custom policy. Use in conjunction with -id or -p or -u',
                        required=False, action='store_true', default=False)
    parser.add_argument('--list-suppressions', '-ls', help='List custom policy suppressions', action='store_true',
                        default=False)
    parser.add_argument('--delete-suppression', '-ds', help='Delete custom policy suppressions by suppression ID',
                        action='store_true',
                        default=False)
    parser.add_argument('--query', '-q', help='Query string format key1=value1,key2=value2', default='', required=False)
    parser.add_argument('--bc-proxy', '-bc', help="Use Bridgecrew API proxy (not recommended)", action='store_true',
                        default=False, required=False)
    parser.add_argument('--version', action='version', version='2.0')
    args = parser.parse_args()

    base_url = os.getenv('PRISMA_API_URL', '')
    username = os.getenv('PC_ACCESS_KEY', '')
    password = os.getenv('PC_SECRET_KEY', '')

    if args.auth:
        base_url, username, password = [i for i in args.auth.split("::")]
    if base_url and username and password:
        token = auth.login(base_url, username, password)
    else:
        print("Please set PRISMA_API_URL, PC_ACCESS_KEY and PC_SECRET_KEY environment variables or use the --auth "
              "argument")
        sys.exit(1)
    if not token:
        sys.exit(1)

    if args.query:
        args.query = utils.parse_query_string(args.query)

    if args.list:
        if args.policy_id:
            policy_actions.get_custom_policy_by_id(base_url, token, args.policy_id, args.bc_proxy, args.verbose)
        else:
            policy_actions.get_custom_policies(base_url, token, args.query, args.bc_proxy, args.verbose)

    if args.update and args.policy_id:
        policy_actions.update_custom_policy_by_id(base_url, token, args.policy_id, args.update)

    if args.publish:
        policy_actions.create_custom_policy(base_url, token, args.publish, args.bc_proxy)

    # TODO:
    # if args.delete:
    #     policy_actions.delete_custom_policy_by_id(base_url, token, args.delete)
    #
    # if args.list_suppressions:
    #     policy_actions.get_custom_policy_suppressions(base_url, token, args.verbose)


if __name__ == '__main__':
    run()
