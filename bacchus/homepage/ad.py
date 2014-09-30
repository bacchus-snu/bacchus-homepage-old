'''
{'info': '00002024: LdapErr: DSID-0C060598, comment: No other operations may be performed on the connection while a bind is outstanding., data 0, v1db1', 'desc': 'Server is busy'}
[[('CN=jsryu21,OU=2008,OU=Bachelor,OU=Users,OU=CSE,DC=snucse,DC=org', {'primaryGroupID': ['1132'], 'logonCount': ['86'], 'cn': ['jsryu21'], 'countryCode': ['0'], 'dSCorePropagationData': ['20120308123357.0Z', '20120308120956.0Z', '20111031063427.0Z', '20111031063339.0Z', '16020808193736.0Z'], 'objectClass': ['top', 'person', 'organizationalPerson', 'user'], 'userPrincipalName': ['jsryu21@snucse.org'], 'lastLogonTimestamp': ['130563526088368465'], 'instanceType': ['4'], 'sAMAccountName': ['jsryu21'], 'distinguishedName': ['CN=jsryu21,OU=2008,OU=Bachelor,OU=Users,OU=CSE,DC=snucse,DC=org'], 'sAMAccountType': ['805306368'], 'logonHours': ['\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'], 'objectSid': ['\x01\x05\x00\x00\x00\x00\x00\x05\x15\x00\x00\x00\x11\x99\xb9x*\xd07\\#_ck\x03F\x00\x00'], 'whenCreated': ['20080303100836.0Z'], 'uSNCreated': ['10048'], 'badPasswordTime': ['130565829853907507'], 'pwdLastSet': ['130486640712750972'], 'description': ['\xec\x9c\xa0\xec\x9e\xac\xec\x84\xb1'], 'objectCategory': ['CN=Person,CN=Schema,CN=Configuration,DC=snucse,DC=org'], 'objectGUID': ['73\xf0\xc2O#{@\x96m\xf3\xb9\x97/\x81\xc4'], 'whenChanged': ['20140928043648.0Z'], 'badPwdCount': ['0'], 'accountExpires': ['0'], 'profilePath': ['\\\\kof.snucse.org\\Profile\\jsryu21'], 'displayName': ['\xec\x9c\xa0\xec\x9e\xac\xec\x84\xb1'], 'name': ['jsryu21'], 'homeDrive': ['Z:'], 'codePage': ['0'], 'userAccountControl': ['66048'], 'lastLogon': ['130565830057487864'], 'uSNChanged': ['76150600'], 'homeDirectory': ['\\\\147.46.240.44\\CSEHOME'], 'lastLogoff': ['0']})]]
'''
import ldap
def login(user_id, password):
    try:
        l = ldap.open("147.46.240.37")
        l.protocol_version = ldap.VERSION3      
        username = user_id + "@snucse.org"
        l.simple_bind(username, password)
    except ldap.LDAPError, e:
        return False
    baseDN = "OU=Users,OU=CSE,DC=snucse,DC=org"
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    searchFilter = "CN=*" + user_id + "*"
    while True:
        try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            return result_set[0][0][1]['displayName'][0]
        except ldap.LDAPError, e:
            continue

if __name__=="__main__":
    name = login("user_id", "password")
    print name
