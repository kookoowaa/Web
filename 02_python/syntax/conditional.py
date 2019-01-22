userId = input('ID? ')
userPwd = int(input('password? '))


#user = {userId: userPwd}
master = {'kookoowaa': 1010, 'admin':2}

'''
if userPwd == '111111':
    print("hello user")
else:
    print('unknown user')
'''

if (userId in list(master.keys())) & (userPwd==master[userId]):
    print('welcome')
else:
    print('unknown user')