#!/usr/bin/env python3

from operator import itemgetter
import pandas as pd
import pandasql as ps

rawTableColumns = ['#Fields:', 'date', 'time', 'x-edge-location', 'sc-bytes', 'c-ip', 'cs-method', 'cs(Host)', 'cs-uri-stem', 'sc-status', 'cs(Referer)', 'cs(User-Agent)', 'cs-uri-query', 'cs(Cookie)', 'x-edge-result-type', 'x-edge-request-id', 'x-host-header', 'cs-protocol', 'cs-bytes', 'time-taken', 'x-forwarded-for', 'ssl-protocol', 'ssl-cipher', 'x-edge-response-result-type', 'cs-protocol-version', 'fle-status', 'fle-encrypted-fields', 'c-port', 'time-to-first-byte', 'x-edge-detailed-result-type', 'sc-content-type', 'sc-content-len', 'sc-range-start', 'sc-range-end']
tableColumns = ['date', 'time', 'x-edge-location', 'sc-bytes', 'c-ip', 'cs-method', 'cs(Host)', 'cs-uri-stem', 'sc-status', 'cs(Referer)', 'cs(User-Agent)', 'cs-uri-query', 'cs(Cookie)', 'x-edge-result-type', 'x-edge-request-id', 'x-host-header', 'cs-protocol', 'cs-bytes', 'time-taken', 'x-forwarded-for', 'ssl-protocol', 'ssl-cipher', 'x-edge-response-result-type', 'cs-protocol-version', 'fle-status', 'fle-encrypted-fields', 'c-port', 'time-to-first-byte', 'x-edge-detailed-result-type', 'sc-content-type', 'sc-content-len', 'sc-range-start', 'sc-range-end']
finalTableColumns = list(itemgetter(0, 1, 4, 5, 7, 8, 9)(tableColumns))



bigLogList = [['2022-01-29', '02:11:17', 'EWR52-C4', '18891', '162.223.124.26', 'GET', 'd2ne5p4hvscza0.cloudfront.net', '/en-US/administrator', '404', 'https://shop.dccomics.com/', 'Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010.7;%20rv:13.0)%20Gecko/20100101%20Firefox/13.0.1%20WhiteHat%20Security', '-', '-', 'Error', 'BN9YPuILe1k0PNcQvLMIQ82LsKW2VksOTZdtokEMAqXO0AT85ZUgFA==', 'shop.dccomics.com', 'https', '592', '0.160', '-', 'TLSv1.2', 'ECDHE-RSA-AES128-GCM-SHA256', 'Error', 'HTTP/1.1', '-', '-', '37902', '0.160', 'Error', 'text/html;%20charset=utf-8', '-', '-', '-'], ['2022-01-29', '02:11:17', 'EWR52-C4', '18891', '162.223.124.26', 'GET', 'd2ne5p4hvscza0.cloudfront.net', '/en-US/administrator', '404', 'https://shop.dccomics.com/', 'Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010.7;%20rv:13.0)%20Gecko/20100101%20Firefox/13.0.1%20WhiteHat%20Security', '-', '-', 'Error', 'BN9YPuILe1k0PNcQvLMIQ82LsKW2VksOTZdtokEMAqXO0AT85ZUgFA==', 'shop.dccomics.com', 'https', '592', '0.160', '-', 'TLSv1.2', 'ECDHE-RSA-AES128-GCM-SHA256', 'Error', 'HTTP/1.1', '-', '-', '37902', '0.160', 'Error', 'text/html;%20charset=utf-8', '-', '-', '-'], ['2022-01-29', '02:11:17', 'EWR52-C4', '18891', '162.223.124.26', 'GET', 'd2ne5p4hvscza0.cloudfront.net', '/en-US/administrator', '404', 'https://shop.dccomics.com/', 'Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010.7;%20rv:13.0)%20Gecko/20100101%20Firefox/13.0.1%20WhiteHat%20Security', '-', '-', 'Error', 'BN9YPuILe1k0PNcQvLMIQ82LsKW2VksOTZdtokEMAqXO0AT85ZUgFA==', 'shop.dccomics.com', 'https', '592', '0.160', '-', 'TLSv1.2', 'ECDHE-RSA-AES128-GCM-SHA256', 'Error', 'HTTP/1.1', '-', '-', '37902', '0.160', 'Error', 'text/html;%20charset=utf-8', '-', '-', '-']]

processedBigLogList = []
for bigLogListElement in bigLogList:
    processedBigLogListElement = list(itemgetter(0, 1, 4, 5, 7, 8, 9)(bigLogListElement))
    processedBigLogList.append(processedBigLogListElement)

df = pd.DataFrame(processedBigLogList, 
              columns=finalTableColumns)

defaultQuery = """ SELECT * FROM df """
default4xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status" FROM df WHERE "sc-status" BETWEEN 400 AND 499 """
default5xxQuery = """ SELECT date, time, "cs-uri-stem", "sc-status" FROM df WHERE "sc-status" BETWEEN 500 AND 599 """
query = input(f"Enter in your query below for database called 'df' (default: {defaultQuery} ) \n\tOR \nEnter '1' for default 4XX error query [{default4xxQuery}] \nEnter '2' for default 5XX query [{default5xxQuery}]:\n")

if not query:
    print(f"No query entered! Using the default query: {defaultQuery}\n")
    finalQuery = defaultQuery
elif query in ('1', '2'):
    if query == '1':
        print(f"Option '1' selected! Using the default 4XX query: {default4xxQuery}\n")
        finalQuery = default4xxQuery
    if query == '2':
        print(f"Option '2' selected! Using the default 5XX query: {default5xxQuery}\n")
        finalQuery = default5xxQuery
else:
    print(f"Manual query entered! Using a custom query: {query}\n")
    finalQuery = query

queryResult = ps.sqldf(finalQuery, locals())
queryResultString = queryResult.to_string()
print(queryResultString)


#q1 = """SELECT * FROM df """
#print(ps.sqldf(q1, locals()))
