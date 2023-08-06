"""Top-level package for wis-s3api."""
import wis_s3api as main

__author__ = """Jianfeng Zhu"""
__email__ = 'zjf014@gmail.com'
__version__ = '0.0.1'

# endpoint_url = 'http://minio.waterism.com:9000'
# access_key = 'JKhbLNL0jNKqbjn4'
# secret_key = '0RDubDRBIrC2WOHAP4nHtYP28TXtVj8H'
# bucket_path = 'test/geodata/'

import os

home_path = os.environ['HOME']

if os.path.exists(os.path.join(home_path,'.wiss3api')):
    rows = 0
    for line in open(os.path.join(home_path,'.wiss3api')):
        key = line.split('=')[0].strip()
        value = line.split('=')[1].strip()
        # print(key,value)
        if key == 'endpoint_url':
            main.endpoint_url = value
        elif key == 'access_key':
            main.access_key = value
        elif key == 'secret_key':
            main.secret_key = value
        elif key == 'bucket_path':
            main.bucket_path = value
else:
    
    main.access_key = input('access_key:')
    main.secret_key = input('access_key:')

    f = open(os.path.join(home_path,'.wiss3api'),'w')
    f.write('endpoint_url = ' + main.endpoint_url)
    f.write('\naccess_key = ' + main.access_key)
    f.write('\nsecret_key = ' + main.secret_key)
    f.write('\nbucket_path = ' + main.bucket_path)
    f.close()
