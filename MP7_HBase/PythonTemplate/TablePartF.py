import happybase as hb

# DON'T CHANGE THE PRINT FORMAT, WHICH IS THE OUTPUT
# OR YOU WON'T RECEIVE POINTS FROM THE GRADER
connection = hb.Connection() #'localhost'
connection.open()

table = connection.table('powers')
# key,data: b'row1', {b'custom:color': b'black'}
for key1, data1 in table.scan():
    for key2, data2 in table.scan():
        if (data1[b'custom:color'] == data2[b'custom:color']) and (data1[b'professional:name'] != data2[b'professional:name']):
            color = data1[b'custom:color']
            name = data1[b'professional:name']
            power = data1[b'personal:power']

            color1 = data2[b'custom:color']
            name1 = data2[b'professional:name']
            power1 = data2[b'personal:power']

            print('{}, {}, {}, {}, {}'.format(name, power, name1, power1, color))


