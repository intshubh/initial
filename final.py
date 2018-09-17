#!/usr/bin/env python2.7


import module
import os, sys
import argparse
import json
import shutil
import subprocess


def main():


    p = argparse.ArgumentParser(description = "Tool to edit JSON file containing users and groups")
    action_sp = p.add_subparsers(help='commands', dest='action')

    # handle "user" cmd
    do_action_p = action_sp.add_parser('user', help='Add user, update user groups')
    do_action_g = action_sp.add_parser('group', help='Add group')


    ## new user add to multiple groups
    do_action_sp = do_action_p.add_subparsers(help='Method to perform', dest='action')
    do_action_gp = do_action_g.add_subparsers(help='Method to perform', dest='action')

    do_action_add_p = do_action_sp.add_parser('add-new-user-groups',help='Add new user please.')

    do_action_add_p.add_argument('-f', '--fname', required=True, help='First Name')
    do_action_add_p.add_argument('-s', '--lname', required=True, help='Surname')
    do_action_add_p.add_argument('-e', '--email', required=True, help='Email address')
    do_action_add_p.add_argument('--groups', nargs='*', help='<Required> Set flag', required=True)
    do_action_add_p.set_defaults(func=module.handle_user_add_to_mg)


    # add user to group
    do_action_addgr_p = do_action_sp.add_parser('add-to-group',help='Add user to group.')

    do_action_addgr_p.add_argument('-u', '--username', required=True, help='User name')
    do_action_addgr_p.add_argument('-g', '--groupname', required=True, help='Group name')
    do_action_addgr_p.set_defaults(func=module.handle_user_add_to_group)

    # add ssh key for user
    do_action_addgr_p = do_action_sp.add_parser('add-ssh-key',help='Add SSH public key to user.')

    do_action_addgr_p.add_argument('-u', '--username', required=True, help='User name')
    do_action_addgr_p.add_argument('-f', '--ssh-pubkey-file', required=True, help='Path to SSH public key.')
    do_action_addgr_p.set_defaults(func=module.handle_user_add_ssh_key)

    # disable user
    do_action_addgr_p = do_action_sp.add_parser('disable-user', help='Disable and delete user.')

    do_action_addgr_p.add_argument('-u', '--username', required=True, help='User name')
    do_action_addgr_p.set_defaults(func=module.handle_user_disable)


    options = p.parse_args()
    options.func(options)

    if os.path.getsize('/home/shubhambhatia/paytm_users_new.json') > 0:
				shutil.copy2('/home/shubhambhatia/paytm_users_new.json', '/home/shubhambhatia/pl.txt')
				print "copied"
    else:
				print "file is empty"
				sys.exit(1)
    

    print(subprocess.call("git --version", shell=True))
    #print(subprocess.call("git status", shell=True))


    print(subprocess.call("git diff", shell=True))

    print "okay very gud"

    print(subprocess.call("git add .", shell=True))
    print(subprocess.call("git commit -m hellos ", shell=True))
    print(subprocess.call("git push origin four ", shell=True))
    print "helllo"


    

if __name__ == '__main__':
    main()
