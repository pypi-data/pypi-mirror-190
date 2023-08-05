#!/usr/bin/env python
# coding: utf-8

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz
from zeno_etl_libs.helper.websocket.websocket import Websocket

import json
from datetime import datetime, timedelta

import argparse
import pandas as pd
import numpy as np
import time
import traceback

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-st', '--start1', default="NULL", type=str, required=False)
parser.add_argument('-ed', '--start2', default="NULL", type=str, required=False)
parser.add_argument('-ct', '--cluster_to_exclude_if_blank_none', default="NULL", type=str, required=False)
parser.add_argument('-wt', '--write_to_mysql', default="1", type=str, required=False)
parser.add_argument('-ah', '--api_hit', default="1", type=str, required=False)
parser.add_argument('-rfm', '--read_from_mysql', default="0", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
start1 = args.start1
start2 = args.start2
cluster_to_exclude_if_blank_none = args.cluster_to_exclude_if_blank_none
write_to_mysql = args.write_to_mysql
api_hit = args.api_hit
read_from_mysql = args.read_from_mysql

if int(read_from_mysql) == 1:
    read_from_mysql = True
else:
    read_from_mysql = False

os.environ['env'] = env

logger = get_logger(level='INFO')

rs_db = DB()

rs_db.open_connection()

mysql_write = MySQL(read_only=False)
mysql_write.open_connection()

# Reason for using Mysql read - Just after writing We want to hit API with Incremetally added ID

mysql_read = MySQL()

mysql_read.open_connection()

s3 = S3()

ws = Websocket()

start_time = datetime.now(tz=gettz('Asia/Kolkata'))
today_date = start_time.strftime('%Y-%m-%d')
logger.info('Script Manager Initialized')
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("write_to_mysql- " + write_to_mysql)
logger.info("api_hit- " + api_hit)
logger.info("read_from_mysql- " + str(read_from_mysql))
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.now(tz=gettz('Asia/Kolkata')).strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

code_started_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
code_started_at_datetime = datetime.now(tz=gettz('Asia/Kolkata'))
# =============================================================================
# set parameters
# =============================================================================

if start1 == "NULL" and start2 == "NULL":
    # pick orders from to last night 2030 to today morning 0800
    logger.info("Read automated dates")
    if datetime.now(tz=gettz('Asia/Kolkata')).strftime('%H:%M:%S') < '18:30:00':
        start1 = (datetime.now(tz=gettz('Asia/Kolkata')) -
                  timedelta(days=1)).strftime('%Y-%m-%d 19:00:00')
        start2 = (datetime.now(tz=gettz('Asia/Kolkata'))).strftime('%Y-%m-%d 13:00:00')
        logger.info("start1 {}".format(start1))
        logger.info("start2 {}".format(start2))
        logger.info("")
        round_number = 1
    elif datetime.now(tz=gettz('Asia/Kolkata')).strftime('%H:%M:%S') > '18:30:00':
        start1 = (datetime.now(tz=gettz('Asia/Kolkata'))).strftime('%Y-%m-%d 13:00:01')
        start2 = (datetime.now(tz=gettz('Asia/Kolkata'))).strftime('%Y-%m-%d 19:00:00')
        logger.info("start1 {}".format(start1))
        logger.info("start2 {}".format(start2))
        logger.info("")
        round_number = 2

else:
    start1 = start1
    start2 = start2
    logger.info("Read manual dates")
    logger.info("start1 {}".format(start1))
    logger.info("start2 {}".format(start2))
    round_number = 1


# Writng this function so that we can get list of stores irrespective of input format in parameter
def fetch_number(list):
    list2 = []
    for i in list:
        try:
            int(i)
            list2.append(int(i))
        except:
            pass
    return list2


if cluster_to_exclude_if_blank_none == "NULL":
    logger.info('Missing parameter for cluster exclusion, Taking all cluster')
    cluster_to_exclude_if_blank_none = []
else:
    cluster_to_exclude_if_blank_none = cluster_to_exclude_if_blank_none
    cluster_to_exclude_if_blank_none = fetch_number(cluster_to_exclude_if_blank_none[1:-1].split(','))
    logger.info('read parameters for cluster exclusion, cluster id to exclude are - {}'.format(
        cluster_to_exclude_if_blank_none))

# =============================================================================
# store clusters
# =============================================================================

if read_from_mysql:
    qc = """
         select
            sf.`feature-id`,
            f.feature,
            sf.`store-id`,
            sf.`is-active`,
            sc.`cluster-id`
        from
            features f 
        join `store-features` sf on
            f.id = sf.`feature-id`
        join `store-clusters` sc on
            sc.`store-id` = sf.`store-id`
        where
            sf.`feature-id` = 69
            and sf.`is-active` = 1
            and sc.`is-active` = 1
    """

    store_clusters = pd.read_sql_query(qc, mysql_read.connection)

else:
    qc = """
        select
            sf."feature-id",
            f.feature,
            sf."store-id",
            sf."is-active", 
            sc."cluster-id"
        from
            "prod2-generico".features f
        join "prod2-generico"."store-features" sf on
            f.id = sf."feature-id"
        join "prod2-generico"."store-clusters" sc on 
            sc."store-id" = sf."store-id"
        where
            sf."feature-id" = 69
            and sf."is-active" = 1
            and sc."is-active" = 1
    """

    store_clusters = rs_db.get_df(qc)


cluster_list = list(set(store_clusters['cluster-id'].unique()) - set(cluster_to_exclude_if_blank_none))
cluster_auto_killed = pd.DataFrame()
pr_auto_killed = pd.DataFrame()

for cluster in cluster_list:
    logger.info("")
    logger.info("cluster {}".format(cluster))
    temp = store_clusters[store_clusters['cluster-id'] == cluster]

    cluster_stores = tuple(map(int, list(temp['store-id'].unique())))

    # cluster_stores = tuple(map(int, list([2, 4, 7, 8, 230, 244, 264])))
    logger.info("cluster stores {}".format(cluster_stores))
    logger.info("")

    for i in cluster_stores:
        logger.info("running for store {}".format(i))
        logger.info("")
        # analysis_store = tuple(map(int, list([i])))
        analysis_store = i
        # analysis_cluster = tuple(map(int, [x for x in cluster_stores if x != i]))
        analysis_cluster = cluster_stores

        # for manual run
        # i = 8
        # analysis_store = tuple(map(int, list([i])))
        # analysis_cluster = tuple(map(int, [x for x in cluster_stores if x != i]))

        # =============================================================================
        # Fetch open PSOs for selected time period
        # =============================================================================
        if read_from_mysql:
            orde = """
              	select
                    pso.`order-number`,
                    pso.`patient-request-id`,
                    pso.`zeno-order-id` ,
                    pso.`patient-id` ,
                    pso.id as `pso-id`,
                    pso.`order-source` ,
                    pso.`order-type` ,
                    pso.`status`,
                    pso.`created-at`,
                    pso.`store-id` ,
                    s.`name` as `store-name`,
                    pso.`drug-id` ,
                    pso.`drug-name` ,
                    pso.`requested-quantity` as `pso-requested-quantity`,
                    pr.`requested-quantity` ,
                    pso.`inventory-quantity` as `inventory-at-creation`,
                    pr.`required-quantity`,
                    pr.`quantity-to-order`
                from
                    `prod2-generico`.`patients-store-orders` pso
                left join `prod2-generico`.`patient-requests` pr on
                    pso.`patient-request-id` = pr.id
                join `prod2-generico`.`stores` s on
                    s.`id` = pso.`store-id`
                where
                    pr.`created-at` > '{start1}'
                    and pr.`created-at` <= '{start2}'
                    and pso.`store-id` = {analysis_store}
                    and pr.status in ('saved','initiate-stock-transfer','store-initiated-stock-transfer')
                    and pso.status not in ('billed', 'completed')
                order by
                    pso.`created-at` DESC
            """.format(start1=start1, start2=start2, analysis_store=analysis_store)

            orders = pd.read_sql_query(orde, mysql_read.connection)

        else:
            orde = """
                    select
                        pso."order-number",
                        pso."patient-request-id",
                        pso."zeno-order-id" ,
                        pso."patient-id" ,
                        pso.id as "pso-id",
                        pso."order-source" ,
                        pso."order-type" ,
                        pso."status",
                        pso."created-at", 
                        pso."store-id" ,
                        s."name" as "store-name",
                        pso."drug-id" ,
                        pso."drug-name" ,
                        pso."requested-quantity" as "pso-requested-quantity",
                        pr."requested-quantity",
                        pso."inventory-quantity" as "inventory-at-creation", 
                        pr."required-quantity", 
                        pr."quantity-to-order" 
                    from
                        "prod2-generico"."patients-store-orders" pso
                    left join "prod2-generico"."patient-requests" pr on
                            pso."patient-request-id" = pr.id
                    join "prod2-generico"."stores" s on s."id" = pso."store-id"
                    where
                        pr."created-at" > '{start1}'
                        and pr."created-at" <= '{start2}'
                        and pso."store-id" = {analysis_store}
                        and pr.status in ('saved','initiate-stock-transfer','store-initiated-stock-transfer')
                        and pso.status not in ('billed', 'completed')
                    order by pso."created-at" DESC;
            """.format(start1=start1, start2=start2, analysis_store=analysis_store)

            orders = rs_db.get_df(orde)

        orders = orders[~orders['drug-id'].isnull()]

        # =============================================================================
        # cluster transfer
        # =============================================================================
        if read_from_mysql:
            clust_transfers_query = """
                select
                    pso.`order-number` ,
                    pso.`patient-id` ,
                    pso.id as "pso-id",
                    pstm.id as 'pstm-id',
                    pstm.`item-quantity` ,
                    pstm.`scanned-quantity` ,
                    pstm.`from-store-id` as 'clus-store-id',
                    pstm.`to-store-id` as 'store-id-x',
                    pstm.status ,
                    pstm.`created-at` 
                FROM
                    `prod2-generico`.`pso-stock-transfer-mapping` pstm
                left join `prod2-generico`.`patients-store-orders` pso 
                                    on
                    pso.id = pstm.`patient-store-order-id`
                left join `prod2-generico`.`patient-requests` pr 
                                    on
                    pso.`patient-request-id` = pr.id
                where
                    pr.`created-at` > '{start1}'
                    and pr.`created-at` <= '{start2}'
                    and pso.`store-id` = {analysis_store}
                    and pr.status in ('saved', 'initiate-stock-transfer', 'store-initiated-stock-transfer')
                    and pso.status not in ('billed', 'completed')
                order by
                    pso.`created-at` DESC
            """.format(start1=start1, start2=start2, analysis_store=analysis_store)

            clust_transfers = pd.read_sql_query(clust_transfers_query, mysql_read.connection)

        else:
            clust_transfers_query = """
                select
                    pso."order-number" ,
                    pso."patient-id" ,
                    pso.id as "pso-id",
                    pstm.id as "pstm-id",
                    pstm."item-quantity" ,
                    pstm."scanned-quantity" ,
                    pstm."from-store-id" as "clus-store-id",
                    pstm."to-store-id" as "store-id-x",
                    pstm.status ,
                    pstm."created-at" 
                FROM
                    "prod2-generico"."pso-stock-transfer-mapping" pstm
                left join "prod2-generico"."patients-store-orders" pso 
                                    on
                    pso.id = pstm."patient-store-order-id"
                left join "prod2-generico"."patient-requests" pr 
                                    on
                    pso."patient-request-id" = pr.id
                where
                    pr."created-at" > '{start1}'
                    and pr."created-at" <= '{start2}'
                    and pso."store-id" = {analysis_store}
                    and pr.status in ('saved', 'initiate-stock-transfer', 'store-initiated-stock-transfer')
                    and pso.status not in ('billed', 'completed')
                order by
                    pso."created-at" DESC
            """.format(start1=start1, start2=start2, analysis_store=analysis_store)

            clust_transfers = rs_db.get_df(clust_transfers_query)

        # =============================================================================
        # Check Transfer Status, Expire Active orders
        # =============================================================================

        # auto kill open transfer orders

        conditions = [(clust_transfers['status'].isin(['active','accepted']))]
        choices = ['auto-rejected']
        clust_transfers['new-status'] = np.select(conditions, choices,default=clust_transfers['status'])

        cluster_auto_killed_temp = clust_transfers[clust_transfers['new-status']=='auto-rejected']
        cluster_auto_killed = cluster_auto_killed.append(cluster_auto_killed_temp)

        # check whether order is fulfilled completely with stock transfer
        clust_transfers_pso_level = clust_transfers[clust_transfers['new-status'].isin(['transfer-note-created'])].groupby(['order-number',
                                        'pso-id'],
                                           as_index=False).agg({'scanned-quantity': ['sum']
        }).reset_index(drop=True)
        clust_transfers_pso_level.columns = ["-".join(x) for x in clust_transfers_pso_level.columns.ravel()]
        clust_transfers_pso_level.rename(columns={'order-number-': 'order-number',
                                        'pso-id-': 'pso-id',
                                        'scanned-quantity-sum': 'quantity-in-cluster-transfer'}, inplace=True)

        # Categorise orders for further processing
        orders = orders.merge(clust_transfers_pso_level,on = ['order-number','pso-id'],how = 'left')
        orders['quantity-in-cluster-transfer'] = orders['quantity-in-cluster-transfer'].fillna(0)

        # If requested-quantity <= quantity-in-cluster-transfer, Then change pr to status to -"auto-killed"

        conditions = [(orders['requested-quantity']>orders['quantity-in-cluster-transfer']),(orders['requested-quantity']<=orders['quantity-in-cluster-transfer'])]
        choices = ['auto-killed','transfer-request-fulfilled-by-cluster']
        orders['pr-new-status'] = np.select(conditions, choices)

        pr_auto_killed_temp = orders[orders['pr-new-status']=='auto-killed']

        pr_auto_killed = pr_auto_killed.append(pr_auto_killed_temp)

# =============================================================================
# for pushing to PROD
# =============================================================================
# pso-stock-transfer-mapping auto-killed
kill_ids_in_pso_stock_transfer_mapping_flag  = False
if len(cluster_auto_killed)> 0:
    kill_ids_in_pso_stock_transfer_mapping_flag = True
    pstm_ids_to_auto_kill = tuple(map(int,cluster_auto_killed['pstm-id'].unique()))

# patient-request auto-killed
kill_ids_in_pr_flag = False
if len(pr_auto_killed)>0:
    kill_ids_in_pr_flag = True
    pr_ids_to_auto_kill = tuple(map(int,pr_auto_killed['patient-request-id']))

# =============================================================================
# writing to PG
# =============================================================================

# pushing pso_cluster_fulfillment table to redshift table
status2 = False
number_of_writing_attempts = 0

if int(write_to_mysql) == 1:
    try:
        if env == 'dev':
            schema = '`test-generico`'
            logger.info('development env setting schema and table accordingly')
        elif env == 'stage':
            schema = '`prod2-generico`'
            logger.info('staging env setting schema and table accordingly')
        elif env == 'prod':
            schema = '`prod2-generico`'
            logger.info('prod env setting schema and table accordingly')

        table_name = '`pso-stock-transfer-mapping`'
        table_name2 = '`patient-requests`'

        if kill_ids_in_pso_stock_transfer_mapping_flag:

            logger.info(f'start : update table {schema}.{table_name}')

            update1_query = """
                                 update
                                     {schema}.{table_name} pstm
                                 SET
                                     pstm.`is-active` = 0,
                                     pstm.status = 'auto-rejected',
                                     pstm.`killed-by` = 'ds-cron',
                                     pstm.`killed-at` = CURRENT_TIMESTAMP
                                 WHERE
                                      pstm.status != 'transfer-note-created'
                                      and pstm.id in {pstm_ids_to_auto_kill}
                             """.format(schema=schema, table_name=table_name,
                                        pstm_ids_to_auto_kill=pstm_ids_to_auto_kill+(0,0))

            mysql_write.engine.execute(update1_query)

            logger.info(f'End : update table {schema}.{table_name}')
        else:
            logger.info(f'Not updating table {schema}.{table_name}, len of id to update{len(cluster_auto_killed)}')

        if kill_ids_in_pr_flag:

            logger.info(f'start : update table {schema}.{table_name2}')

            update2_query = """
                                update
                                    {schema}.{table_name2} pr
                                SET
                                    pr.status = 'auto-killed',
                                    pr.`auto-killed-by` = 'ds-cron',
                                    pr.`auto-killed-at` = CURRENT_TIMESTAMP
                                WHERE
                                     pr.status not in ('completed')
                                     and pr.id in {pr_ids_to_auto_kill}
                            """.format( schema=schema, table_name2=table_name2,
                                                  pr_ids_to_auto_kill=pr_ids_to_auto_kill+(0,0))

            mysql_write.engine.execute(update2_query)

            logger.info(f'End : update table {schema}.{table_name2}')
        else:
            logger.info(f'Not updating table {schema}.{table_name2}, len of id to update{len(pr_auto_killed)}')

        status2 = True

        # =============================================================================
        # TODO : Fire API Here
        # =============================================================================

        # if int(api_hit) == 1:
        #     logger.info('sleep for 10 second')
        #     time.sleep(10)
        #
        #     mysql_read2 = MySQL()
        #     mysql_read2.open_connection()
        #
        #     # Reading Newly added queried
        #     if env == 'dev':
        #         mysql_schema = '`test-generico`'
        #     else:
        #         mysql_schema = '`prod2-generico`'
        #
        #     mysql_inserted_items_query = """
        #     SELECT
        #         pstm.id ,
        #         pstm.`to-store-id` ,
        #         pstm.`from-store-id`
        #     FROM
        #         {schema}.`pso-stock-transfer-mapping` pstm
        #     WHERE
        #         pstm.`created-at` >= '{code_started_at}'
        #     """.format(code_started_at=code_started_at, schema=mysql_schema)
        #
        #     inserted_items = pd.read_sql_query(mysql_inserted_items_query, mysql_read2.connection)
        #     # logger.info(inserted_items)
        #     # logger.info(mysql_inserted_items_query)
        #     mysql_read2.close()
        #
        #     for index, row in inserted_items.iterrows():
        #         payload = {
        #             "destinations": [
        #                 row['from-store-id'].astype(str)
        #             ],
        #             "message": "cluster-request",
        #             "payload": f"{row['id']}-{row['to-store-id']}"
        #         }
        #         response = ws.send(payload=payload)
        #
        #     logger.info('API hit successful for Notification in billing panel')
        # else:
        #     logger.info('No API hit - Parameter is set as 0')

    except Exception as error:
        logger.exception(error)
        logger.info(f'writing to mysql failed - attempt - {number_of_writing_attempts}')
        status2 = False

    if status2 == False:
        logger.info('Writing to mysql table failed, Mostly it is due to deadlock issue, sleep for 30 seconds')
        time.sleep(30)
        logger.info('slept for 30 seconds')

        try:
            if env == 'dev':
                schema = '`test-generico`'
                logger.info('development env setting schema and table accordingly')
            elif env == 'stage':
                schema = '`prod2-generico`'
                logger.info('staging env setting schema and table accordingly')
            elif env == 'prod':
                schema = '`prod2-generico`'
                logger.info('prod env setting schema and table accordingly')

            table_name = '`pso-stock-transfer-mapping`'
            table_name2 = '`patient-requests`'

            if kill_ids_in_pso_stock_transfer_mapping_flag:

                logger.info(f'start : update table {schema}.{table_name}')

                update1_query = """
                                      update
                                          {schema}.{table_name} pstm
                                      SET
                                          pstm.`is-active` = 0,
                                          pstm.status = 'auto-rejected',
                                          pstm.`killed-by` = 'ds-cron',
                                          pstm.`killed-at` = CURRENT_TIMESTAMP
                                      WHERE
                                           pstm.status != 'transfer-note-created'
                                           and pstm.id in {pstm_ids_to_auto_kill}
                                  """.format(schema=schema, table_name=table_name,
                                             pstm_ids_to_auto_kill=pstm_ids_to_auto_kill+(0,0))

                mysql_write.engine.execute(update1_query)

                logger.info(f'End : update table {schema}.{table_name}')
            else:
                logger.info(
                    f'Not updating table {schema}.{table_name}, len of id to update{len(cluster_auto_killed)}')

            if kill_ids_in_pr_flag:

                logger.info(f'start : update table {schema}.{table_name2}')

                update2_query = """
                                     update
                                         {schema}.{table_name2} pr
                                     SET
                                         pr.status = 'auto-killed',
                                         pr.`auto-killed-by` = 'ds-cron',
                                         pr.`auto-killed-at` = CURRENT_TIMESTAMP
                                     WHERE
                                          pr.status not in ('completed')
                                          and pr.id in {pr_ids_to_auto_kill}
                                 """.format(schema=schema, table_name2=table_name2,
                                            pr_ids_to_auto_kill=pr_ids_to_auto_kill+(0,0))

                mysql_write.engine.execute(update2_query)

                logger.info(f'End : update table {schema}.{table_name2}')
            else:
                logger.info(f'Not updating table {schema}.{table_name2}, len of id to update{len(pr_auto_killed)}')

            status2 = True

            # =============================================================================
            # TODO : Fire API Here
            # =============================================================================

            # if int(api_hit) == 1:
            #     logger.info('sleep for 10 second')
            #     time.sleep(10)
            #
            #     mysql_read2 = MySQL()
            #     mysql_read2.open_connection()
            #
            #     # Reading Newly added queried
            #     if env == 'dev':
            #         mysql_schema = '`test-generico`'
            #     else:
            #         mysql_schema = '`prod2-generico`'
            #
            #     mysql_inserted_items_query = """
            #     SELECT
            #         pstm.id ,
            #         pstm.`to-store-id` ,
            #         pstm.`from-store-id`
            #     FROM
            #         {schema}.`pso-stock-transfer-mapping` pstm
            #     WHERE
            #         pstm.`created-at` >= '{code_started_at}'
            #     """.format(code_started_at=code_started_at, schema=mysql_schema)
            #
            #     inserted_items = pd.read_sql_query(mysql_inserted_items_query, mysql_read2.connection)
            #     # logger.info(inserted_items)
            #     # logger.info(mysql_inserted_items_query)
            #     mysql_read2.close()
            #
            #     for index, row in inserted_items.iterrows():
            #         payload = {
            #             "destinations": [
            #                 row['from-store-id'].astype(str)
            #             ],
            #             "message": "cluster-request",
            #             "payload": f"{row['id']}-{row['to-store-id']}"
            #         }
            #         response = ws.send(payload=payload)
            #
            #     logger.info('API hit successful for Notification in billing panel')
            # else:
            #     logger.info('No API hit - Parameter is set as 0')

        except Exception as error:
            logger.exception(error)
            logger.info(f'writing to mysql failed - attempt - {number_of_writing_attempts}')
            status2 = False

    if status2 is True:
        status = 'Success'
    else:
        status = 'Failed'
else:
    status = 'test'

cluster_auto_killed_uri = s3.save_df_to_s3(df=cluster_auto_killed,
                                 file_name='cluster_auto_killed_{}_{}.csv'.format(start1, start2))
pr_auto_killed_uri = s3.save_df_to_s3(df=pr_auto_killed,
                                 file_name='pr_auto_killed_{}_{}.csv'.format(start1, start2))

end_time = datetime.now(tz=gettz('Asia/Kolkata'))
difference = end_time - start_time
min_to_complete = round(difference.total_seconds() / 60, 2)
email = Email()


email.send_email_file(subject='{}-{}, round-{}, {} pstm auto-killed, {} pr auto-Killed from {} to {}'.format(
    env, status, round_number,
    len(cluster_auto_killed),
    len(pr_auto_killed),
    start1, start2),
    mail_body=f" Auto kill status - {status}\n"
              f" Round - {round_number}\n"
              f"Time for job completion - {min_to_complete} mins\n"
              f" Number of writing attempts - {number_of_writing_attempts}",
    to_emails=email_to, file_uris=[cluster_auto_killed_uri,pr_auto_killed_uri])

rs_db.close_connection()
mysql_write.close()
mysql_read.close()