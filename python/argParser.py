#!/usr/bin/env python3

import argparse
import os, sys

# Create the Store parser
store_parser = argparse.ArgumentParser(description="Store name to run")
# Add the Store argument
store_parser.add_argument('--store', type=str, help="Store name to run")
# Execute the parse_args() method for the Store parser
args = store_parser.parse_args()


dcSecretNameArray = ['/dc-shop-strapi/staging/DATABASE_PASSWORD', '/dc-shop-strapi/staging/DATABASE_HOST',\
    '/dc-shop-strapi/staging/AWS_ACCESS_SECRET', '/dc-shop-strapi/staging/AWS_BUCKET_NAME', '/dc-shop-strapi/staging/AWS_ACCESS_KEY',\
    '/dc-shop-strapi/staging/BASTION_HOST_IP', '/dc-shop-strapi/staging/BASTION_KEY_PAIR', '/dc-shop-strapi/staging/PREVIEW_SECRET', '/dc-shop-strapi/staging/CDN_URL', '/dc-shop-strapi/staging/ADMIN_JWT_SECRET']
ltSecretNameArray = ['/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_DATABASE_PASSWORD', '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_DATABASE_HOST',\
    '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_AWS_ACCESS_SECRET', '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_AWS_BUCKET_NAME', '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_AWS_ACCESS_KEY',
    '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_BASTION_HOST_IP', '/lt-strapi/staging/LOONEY_TOONS_STRAPI_STAGING_BASTION_KEY_PAIR', '/lt-strapi/staging/PREVIEW_SECRET', '/dc-shop-strapi/staging/CDN_URL']

if args.store:
    print(f"Store value present. Value is: {args.store}")
    # Check if the value for "--store" is either "lt" or "dc"
    if args.store == "lt":
        print("The store is Looney Tunes Shop")
        secretNameArray = ltSecretNameArray
    elif args.store == "dc":
        print("The store is DC Shop")
        secretNameArray = dcSecretNameArray
    else:
        raise("ERROR: No acceptable store given after the '--store' tag! Must be 'lt' or 'dc'.")
else:
    print("No store named")

print(secretNameArray)
