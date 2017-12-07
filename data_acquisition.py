#coding utf-8

import requests
import json

projects = { 'pageCounts': 'legacy', 'pageViews':'curr'}

endpoint = {
    'curr' :'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/{project}/{access}/{agent}/{granularity}/{start}/{end}',
    'legacy' : 'https://wikimedia.org/api/rest_v1/metrics/legacy/pagecounts/aggregate/{project}/{access-site}/{granularity}/{start}/{end}'
}

access = {
    'curr' : {'desktop', 'mobile-app', 'mobile-web'},
    'legacy' : {'desktop-site', 'mobile-site'}
}

date_range = {
    'legacy' : { 'start' : '2008010100', 'end' : '2016080100'},
    'curr' : { 'start' : '2015070100','end' : '2017120100'}
}

page_count_endpoint = ''
headers={'User-Agent' : 'https://github.com/rezvanielham', 'From' : 'rezvanil@uw.edu'}

def get_params(access, start, end, project):
    '''

    :param endpoint:
    :param access:
    :return:
    '''

    params = dict()

    if(project =='curr'):
        params['access'] = access
        params['agent'] = 'user'
    else:
        params['access-site'] = access
    params['project'] = 'en.wikipedia.org'
    params['granularity'] = "monthly"
    params['start'] = start
    params['end'] = end
    return params

def get_ym_date(ymd_start, ymd_end):
    '''

    :param ymd_start: the start date with YYYYMMDD format
    :param ymd_end: the end date with YYYYMMDD format
    :return: the param dict of start and end dates with YYYYMM format removing the rest of the string
    '''
    params = dict()
    params['ym-start'] = ymd_start[0:6]
    params['ym-end'] = ymd_end[0:6]
    return params


def get_page_view_formatted_dates(project):
    return get_ym_date(date_range[project]['start'], date_range[project]['end'])

for project in projects:
   prj = projects[project]
   for acs in access[prj]:
        api_call = requests.get(endpoint[projects[project]].format(**get_params(acs, date_range[prj]['start'], date_range[prj]['end'], prj)))
        response = api_call.json()
        #print to files with names with this format:
        out_file_name = project + '_{}_{}_{}.json'.format(acs, get_page_view_formatted_dates(prj)['ym-start'],
                                                          get_page_view_formatted_dates(prj)['ym-end'])
        json.dump(response, open(out_file_name, "w"), indent=4)