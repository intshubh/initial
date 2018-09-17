#!/usr/bin/env python2.7


import os, sys
import argparse
import json
import shutil
from collections import OrderedDict


NEW_USER_DEFAULTS = {
    "gid_number": 100,
    "ssh_pubkey": "",
    }


class DataOperationException(Exception):
    pass

class UnknownEntryException(DataOperationException):
    pass

class DuplicateEntryException(DataOperationException):
    pass


class DataProxy:
    def __init__(self):
        # preserve order of entries in input file
        with open('paytm_users.json') as f:
        		self.data = json.loads(f.read(), object_pairs_hook=OrderedDict)

    def get_group(self, namex):
        """ Return group as a dict
        """

        try:
            return dict(self.data['groups'][namex])
        except KeyError:
            raise UnknownEntryException('Unknown group %s' % (namex,))

    def modify_group(self, namex, value):
        if namex not in self.data['groups']:
            raise UnknownEntryException('Unknown group %s' % (namex,))

        self.data['groups'][namex] = value

    def _update_group_members(self, groupname, diffx):
        gx = self.get_group(groupname)
        members = gx['members']
        
        for i in diffx.get('add', []):
            if i not in members:
                members.append(i)

        for i in diffx.get('remove', []):
            members.remove(i)

        gx['members'] = sorted(members)[:]        
        self.modify_group(groupname, gx)
    
    def add_grps(self, groupname, usrname):
        gx = self.get_group(groupname)
        members = gx['members']

	if usrname not in members:
		members.append(usrname)
        
        

        gx['members'] = sorted(members)[:]        
        self.modify_group(groupname, gx)

    def add_users_to_group(self, users, groupname):
        self._update_group_members(groupname, {'add' : users})
        
    def set_group_members(self, groupname, members):
        gx = self.get_group(groupname)
        gx['members'] = sorted(members)[:]
        self.modify_group(groupname, gx)

        
    def get_group_members(self, groupname):
        return self.get_group(groupname)['members'][:]

    def _put_user(self, username, val):
        self.data['users'][username] = val
    
    #puts new user to multiple groups
    def _put_user_to_mg(self, username, val,groups):
        self.data['users'][username] = val
	for gp in groups:
		self.add_grps(gp,username)
		
		
    
    #puts existing user to multiple groups
    def put_euser_mg(self, username,groups):
	for gp in groups:
		self.add_grps(gp,username)

    def _put_group(self, groupname, val):
        self.data['groups'][groupname] = val

    def add_user(self, username, val):
        if self.is_valid_user(username):
            raise DuplicateEntryException("User already exists: %s" % (username,))

        self._put_user(username, val)

    def add_user_to_mg(self, username, val, groups):
	
        if self.is_valid_user(username):
            raise DuplicateEntryException("User already exists: %s" % (username,))

        self._put_user_to_mg(username, val,groups)

    def add_group(self, groupname, val):
        if self.is_valid_group(groupname):
            raise DuplicateEntryException("Group already exists: %s" % (groupname,))

        self._put_group(groupname, val)

    def is_valid_user(self, username):
        return username in self.data['users']

    def is_valid_group(self, groupname):
        return groupname in self.data['groups']

    def get_max_uid(self):
        # TODO get rid of exception for 'platfora'
        return max([x['uid_number'] for u,x in self.data['users'].iteritems() if u != 'platfora'])

    def get_max_gid(self):
        return max([x['gid_number'] for _,x in self.data['groups'].iteritems()])

    def export(self):
        with open('paytm_users_new.json','w') as outfile: 
		json.dump(self.data,outfile,indent=4, separators=(',', ': '))

    def update_user_attribute(self, username, attrx, valx):
        if not self.is_valid_user(username):
            raise UnknownEntryException("Unknown user: %s" % (username,))

        self.data['users'][username][attrx] = valx
        
    def get_user_by_attribute(self, attrx, valx):
	
        for k,v in self.data['users'].iteritems():
            if v.get(attrx, None) == valx:
		print "key is"+k
		return k
		
                

        #raise UnknownEntryException('No user with %s=%s' % (attrx, valx))


class LDAPModHelper:

    def __init__(self, datastore):
        self.datastore = datastore

    def is_valid_user(self, username):
        return self.datastore.is_valid_user(username)

    def is_valid_group(self, groupname):
        try:
            self.datastore.get_group(groupname)
            return True
        except UnknownEntryException:
            return False

    def add_user(self, firstname, lastname, email):
        try:
            u = self.get_user_by_email(email)
	    username= self.get_username_by_email(email)
	    
            raise DataOperationException('user already exists: %s' % (u,))
	    
	    
	    
        except UnknownEntryException, e:
            pass

        
        newuid = self.datastore.get_max_uid() + 1
        username_base = ('%s%s' % (firstname[0], lastname)).lower()

        username = username_base
        suff = 1
        max_suff = 30 # WHY ?
 
        while self.is_valid_user(username):
            username = '%s%s' % (username_base, suff)
            suff += 1
            if suff > max_suff:
                raise DataOperationException('Exhaused suffix limit - could not find unique username for %s %s %s' % (firstname, lastname, email))

        assert(self.is_valid_user(username) == False)
        # messy.. doesn't belong here
        new_user_dict = {
            "firstname": firstname.lower().capitalize(),
            "gid_number": 100,
            "mail": email,
            "ssh_pubkey": "NONE",
            "surname": lastname.lower().capitalize(),
            "uid_number": newuid
        }
	print username
        self.datastore.add_user(username, new_user_dict)

    #to add user to mg by checking user's existance
    def add_user_to_mg(self, firstname, lastname, email, groups):
	
	    
            u = self.get_user_by_email(email)
  	    
	    
	    
	    if u:	
		print "user existing is "+u
		self.datastore.put_euser_mg(u, groups)
	    else:
		newuid = self.datastore.get_max_uid() + 1
		username_base = ('%s%s' % (firstname[0], lastname)).lower()

		username = username_base
		suff = 1
		max_suff = 30 # WHY ?
	 
		while self.is_valid_user(username):
		    username = '%s%s' % (username_base, suff)
		    suff += 1
		    if suff > max_suff:
		        raise DataOperationException('Exhaused suffix limit - could not find unique username for %s %s %s' % (firstname, lastname, email))

		assert(self.is_valid_user(username) == False)
		# messy.. doesn't belong here
		new_user_dict = {
		    "firstname": firstname.lower().capitalize(),
		    "gid_number": 100,
		    "mail": email,
		    "ssh_pubkey": "NONE",
		    "surname": lastname.lower().capitalize(),
		    "uid_number": newuid
		}
		print username
		self.datastore.add_user_to_mg(username, new_user_dict,groups)
	    
	    
	    
            
	    
	    
	    
        #except UnknownEntryException, e:
            #pass

        
        

    def add_group(self, groupname, members):
        if self.is_valid_group(groupname):
            raise DataOperationException('group already exists: %s' % (groupname,))

        for i in members:
            if not self.is_valid_user(i):
                raise DataOperationException('Unknown user in group "%s" member list: %s' % (groupname, i))

        newgid = self.datastore.get_max_gid() + 1
        # messy.. doesn't belong here
        new_group_dict = {
            "gid_number": newgid,
            "members": list(sorted(members))
        }

        self.datastore.add_group(groupname, new_group_dict)

    def get_user_by_email(self, email):
	
        val=self.datastore.get_user_by_attribute('mail', email)
	return val

    def add_user_to_group(self, username, groupname):
        if not (self.is_valid_user(username) and self.is_valid_group(groupname)):
            raise ValueError('Invalid user %s or group %s' % (username, groupname))
        
        self.datastore.add_users_to_group([username], groupname)

    def add_user_ssh_key(self, username, ssh_pub_key):
        if not self.is_valid_user(username):
            raise ValueError('Invalid user %s' % (username,))
        
        self.datastore.update_user_attribute(username, 'ssh_pubkey', ssh_pub_key)
        

    def disable_user(self, username):
        if not self.is_valid_user(username):
            raise ValueError('Invalid user %s' % (username,))

        self.datastore.update_user_attribute(username, 'action', 'delete')
        
def handle_user_add(args):
    
    l = LDAPModHelper(DataProxy())
    l.add_user(args.firstname, args.surname, args.email)
    l.datastore.export()

def module_user_add(*args):
    
    l = LDAPModHelper(DataProxy())
    l.add_user(args[0], args[1], args[2])
    l.datastore.export()


def handle_user_add_to_mg(args):
    
    l = LDAPModHelper(DataProxy())
    l.add_user_to_mg(args.fname, args.lname, args.email, args.groups)
    l.datastore.export()
    usr = findusr()
    test(args.groups,usr)

def module_user_add_mg(*args):
    groups=[]
    i=0
    for arg in args:
	if i>=3:
		groups.append(arg)
	i=i+1
	
    l = LDAPModHelper(DataProxy())
    l.add_user_to_mg(args[0],args[1],args[2], groups)
    l.datastore.export()
    usr = findusr()
    test(groups,usr)
    

def handle_user_disable(args):
    l = LDAPModHelper(DataProxy())
    l.disable_user(args.username)
    l.datastore.export()

def module_user_disable(args):
    l = LDAPModHelper(DataProxy())
    l.disable_user(args)
    l.datastore.export()
    
    
def handle_user_add_to_group(args):
    
    l = LDAPModHelper(DataProxy())
    l.add_user_to_group(args.username, args.groupname)
    l.datastore.export()

def module_user_add_to_group(*args):
    
    l = LDAPModHelper(DataProxy())
    l.add_user_to_group(args[0], args[1])
    l.datastore.export()

def handle_user_add_ssh_key(args):
    l = LDAPModHelper(DataProxy())
    l.add_user_ssh_key(args.username, file(args.ssh_pubkey_file).read().strip())
    l.datastore.export()

def module_user_add_ssh_key(*args):
    l = LDAPModHelper(DataProxy())
    l.add_user_ssh_key(args[0], file(args[1]).read().strip())
    l.datastore.export()


'''def handle_group_add(*args):
    members=[]
    i=0
    for arg in args:
	if i>=1:
		members.append(arg)
	i=i+1
    l = LDAPModHelper(DataProxy())
    l.add_group(args[0], members)
    l.datastore.export()'''

def test(grp_list,usr):
    with open('paytm_users_new.json','r') as f:
        	
		listone = json.loads(f.read(), object_pairs_hook=OrderedDict)
		for grp in grp_list:
			if usr in listone['groups'][grp]['members']:
				print "read done for group "+grp
def findusr():
	with open('paytm_users_new.json','r') as f:
		listone = json.loads(f.read(), object_pairs_hook=list)
		username=listone[-1][-1][-1][0]
		return username



        	





