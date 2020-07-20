import pandas as pd
from collections import Counter
import ast

# Nielsen Insight Functions
#-------------------------------------------------------------------------------------------------
# function to count items in a list
def count_element(x, dic):
        for item in x:
            dic[item]+=1


def query_audience(**kwargs):
    if kwargs["audience_type"] == "exposed users" and len(kwargs["campaign_id"]) > 1:
        query = ['''
        CREATE OR REPLACE VIEW exposed_view comment='View of distinct lids' as 
        (SELECT DATE_TIME, listener_id, creative, CLIENT, target, USERAGENT, IPADDRESS FROM exposed_table
        WHERE {} IN {} AND CAST(TO_TIMESTAMP(DATE_TIME) as DATE) BETWEEN '{}' AND '{}')
        '''.format(kwargs["campaign_type"], kwargs["campaign_id"], kwargs["campaign_from_dt"], kwargs["campaign_to_dt"]),

        '''
        CREATE OR REPLACE VIEW lid_exposed_match_view comment='View of lid exposed ids matched with LID graph' as
        (SELECT
        ew.listener_id, lid.device_id, lid.user_id as global_id, ew.target, ew.creative
        FROM exposed_view ew
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_LID_GRAPH" lid ON lid.device_id = ew.listener_id);
        ''',

        '''
        CREATE OR REPLACE VIEW exposed_lid_to_nid comment='View of global id and its resepctive nielsen id' as
        (SELECT 
        lv.global_id as exposed_global_id, nv.user_id as nielsen_global_id, nv.device_id as nielsen_id
        FROM lid_exposed_match_view lv
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_NID_GRAPH" nv ON nv.user_id = lv.global_id)
        ''',

        '''
        CREATE OR REPLACE VIEW matched_xd_nielsen_data_view comment='View of global ids, nielsen id and segments associated with nielsen id' as
        (SELECT 
        eln.exposed_global_id, eln.nielsen_id, nd.nielsen_segments
        FROM exposed_lid_to_nid eln
        INNER JOIN "DS_NIELSEN"."CURATED"."AUDIENCE" nd ON nd.nielsen_id = eln.nielsen_id)
        ''']
    elif kwargs["audience_type"] == "exposed users" and len(kwargs["campaign_id"]) == 1:
        query = ['''
        CREATE OR REPLACE VIEW exposed_view comment='View of distinct lids' as 
        (SELECT DATE_TIME, listener_id, creative, CLIENT, target, USERAGENT, IPADDRESS FROM exposed_table
        WHERE {} = '{}' AND CAST(TO_TIMESTAMP(DATE_TIME) as DATE) BETWEEN '{}' AND '{}')
        '''.format(kwargs["campaign_type"], kwargs["campaign_id"][0], kwargs["campaign_from_dt"], kwargs["campaign_to_dt"]),

        '''
        CREATE OR REPLACE VIEW lid_exposed_match_view comment='View of lid exposed ids matched with LID graph' as
        (SELECT
        ew.listener_id, lid.device_id, lid.user_id as global_id, ew.target, ew.creative
        FROM exposed_view ew
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_LID_GRAPH" lid ON lid.device_id = ew.listener_id);
        ''',

        '''
        CREATE OR REPLACE VIEW exposed_lid_to_nid comment='View of global id and its resepctive nielsen id' as
        (SELECT 
        lv.global_id as exposed_global_id, nv.user_id as nielsen_global_id, nv.device_id as nielsen_id
        FROM lid_exposed_match_view lv
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_NID_GRAPH" nv ON nv.user_id = lv.global_id)
        ''',

        '''
        CREATE OR REPLACE VIEW matched_xd_nielsen_data_view comment='View of global ids, nielsen id and segments associated with nielsen id' as
        (SELECT 
        eln.exposed_global_id, eln.nielsen_id, nd.nielsen_segments
        FROM exposed_lid_to_nid eln
        INNER JOIN "DS_NIELSEN"."CURATED"."AUDIENCE" nd ON nd.nielsen_id = eln.nielsen_id)
        ''']
    elif kwargs["audience_type"] == "clientsite users":
        query = ['''
        CREATE OR REPLACE VIEW pageview_view comment = 'View of distinct oaids' as
        (SELECT DATE_TIME, OAID, CLIENT, EVENT, USERAGENT, IPADDRESS,REFERRER FROM clientsite_table
        WHERE CLIENT = '{}' AND CAST(TO_TIMESTAMP(DATE_TIME) as DATE) BETWEEN '{}' AND '{}');
        '''.format(kwargs["client_name"],kwargs["campaign_from_dt"], kwargs["campaign_to_dt"]),
        '''
        CREATE OR REPLACE VIEW oaid_pageview_match_view comment='View of oaids pageview ids matched with OAID graph' as
        (SELECT
        pv.oaid, oad.device_id, oad.user_id as global_id
        FROM pageview_view pv
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_OAID_GRAPH" oad ON oad.device_id = pv.oaid);
        ''',
        '''
        CREATE OR REPLACE VIEW exposed_oaid_to_nid comment='View of global id and its resepctive nielsen id' as
        (SELECT 
        opm.global_id as clientsite_global_id, nv.user_id as nielsen_global_id, nv.device_id as nielsen_id
        FROM oaid_pageview_match_view opm
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_NID_GRAPH" nv ON nv.user_id = opm.global_id);
        ''',
        '''
        CREATE OR REPLACE VIEW clientsite_xd_nielsen_data_view comment='View of global ids, nielsen id and segments associated with nielsen id for clientsite users' as
        (SELECT 
        eon.clientsite_global_id, eon.nielsen_id, nd.nielsen_segments
        FROM exposed_oaid_to_nid eon
        INNER JOIN "DS_NIELSEN"."CURATED"."AUDIENCE" nd ON nd.nielsen_id = eon.nielsen_id);
        ''']
    else:
        query = ['''
        CREATE OR REPLACE VIEW exposed_view comment='View of distinct lids' as 
        (SELECT DATE_TIME, listener_id, creative, CLIENT, target, USERAGENT, IPADDRESS FROM exposed_table
        WHERE {} = '{}' AND CAST(TO_TIMESTAMP(DATE_TIME) as DATE) BETWEEN '{}' AND '{}')
        '''.format(campaign_type, campaign_id, from_dt, to_dt),

        '''
        CREATE OR REPLACE VIEW lid_exposed_match_view comment='View of lid exposed ids matched with LID graph' as
        (SELECT
        ew.listener_id, lid.device_id, lid.user_id as global_id, ew.target, ew.creative
        FROM exposed_view ew
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_LID_GRAPH" lid ON lid.device_id = ew.listener_id);
        ''',

        '''
        CREATE OR REPLACE VIEW exposed_lid_to_nid comment='View of global id and its resepctive nielsen id' as
        (SELECT 
        lv.global_id as exposed_global_id, nv.user_id as nielsen_global_id, nv.device_id as nielsen_id
        FROM lid_exposed_match_view lv
        INNER JOIN "RD_DAX_AUDIENCE"."SANDBOX"."DETERM_NID_GRAPH" nv ON nv.user_id = lv.global_id)
        ''',

        '''
        CREATE OR REPLACE VIEW matched_xd_nielsen_data_view comment='View of global ids, nielsen id and segments associated with nielsen id' as
        (SELECT 
        eln.exposed_global_id, eln.nielsen_id, nd.nielsen_segments
        FROM exposed_lid_to_nid eln
        INNER JOIN "DS_NIELSEN"."CURATED"."AUDIENCE" nd ON nd.nielsen_id = eln.nielsen_id)
        ''']
        
    return query

def nielsen_insights (data, path, client_name):
    
    df = pd.DataFrame(data, columns=['GLOBAL_ID','NIELSEN_ID','NIELSEN_SEGMENTS'])

    # create dictionairy
    segment_count_dic = Counter()

    df["NIELSEN_SEGMENTS"] =  df["NIELSEN_SEGMENTS"].apply(lambda x: x.replace('\n',''))
    df["NIELSEN_SEGMENTS"] =  df["NIELSEN_SEGMENTS"].apply(lambda x: ast.literal_eval(x))

    campaign_pop = df.NIELSEN_ID.nunique()

    df.sort_values(by='NIELSEN_ID', ascending=False, inplace=True)
    df["SEGMENT_LENGTH"] = df['NIELSEN_SEGMENTS'].astype(str).map(len)

    test_filter = df.loc[df.groupby('NIELSEN_ID')['SEGMENT_LENGTH'].idxmax()]

    test_filter.NIELSEN_SEGMENTS.apply(count_element, dic=segment_count_dic)

    df_seg_count = pd.DataFrame.from_dict(segment_count_dic, orient='index', columns=['COUNT'])
    df_seg_count["SEGMENT_ID"] = df_seg_count.index
    df_seg_count.reset_index(inplace=True, drop=True)

    segment_name_df = pd.read_csv("segment_names.csv")
    segment_name_df = segment_name_df.astype({"ID": str})

    df_merge = pd.merge(df_seg_count, segment_name_df, left_on='SEGMENT_ID',right_on='ID',how='left')

    df_merge.drop(columns=['ID'], inplace=True)
    df_merge["CAMPAIGN_POP"] = campaign_pop
    df_merge["SEGMENT_OVERLAP"] = df_merge.COUNT/df_merge.CAMPAIGN_POP

    df_final = df_merge[["FULL_NAME", "SEGMENT_ID", "COUNT", "CAMPAIGN_POP","SEGMENT_OVERLAP"]]
    df_final.sort_values(by='COUNT', ascending=False, inplace=True)
    
    print(df_final.head())

    df_final.to_csv(path + client_name + '.csv', index=False)
    


