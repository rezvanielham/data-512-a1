import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#Step1: load page view mobile-app and mobile-web data into memory to combine both
pv_mobile_app_json = json.load(open(r'''pageViews_mobile-app_201507_201712.json'''))
pv_mobile_web_json = json.load(open(r'''pageViews_mobile-web_201507_201712.json'''))

#Initialize a result set
pv_mobile_combined = dict()
pv_mobile_combined['items'] = list()

for app_item in pv_mobile_app_json['items']:
    for web_item in pv_mobile_web_json['items']:
        if app_item['timestamp'] == web_item['timestamp']:
            app_item['views'] = app_item['views'] + web_item['views']
            break
    pv_mobile_combined['items'].append(app_item)

json.dump(pv_mobile_combined, open(r'''pageViews_mobile_combined_201507_201712.json''', "w"), indent=4)

#adding year and month columns to the combined mobile data for page views
for combined_item in pv_mobile_combined['items']:
    combined_item['year'] = combined_item['timestamp'][0:4]
    combined_item['month'] = combined_item['timestamp'][4:6]


#load page view desktop data into memory to add the month and year columns
pv_desktop_json = json.load(open(r'''pageViews_desktop_201507_201712.json'''))
for desktop_item in pv_desktop_json['items']:
    desktop_item['year'] = desktop_item['timestamp'][0:4]
    desktop_item['month'] = desktop_item['timestamp'][4:6]

#create a list of items with a new column called total_views for page views
pv_total_views = dict()
pv_total_views['items'] = list()

#sum up the values for mobile and desktop for pageview data (adding columns according to the final result format
for mobile_item in pv_mobile_combined['items']:
    for desktop_item in pv_desktop_json['items']:
        if mobile_item['month'] == desktop_item['month'] and mobile_item['year'] == desktop_item['year']:
            #add the base item including the monthly view information for desktop first
            #we then add the following columns to match the final result format
            # 1. pageview_desktop_views columns which has the same value as the exisiting 'views' columns
            # 2. pageview_mobile_views which is the value of the 'views' from the corresponding month from mobile data
            # 3. pageview_all_views the sum of mobile and desktop views
            desktop_item['pageview_desktop_views'] = desktop_item['views']
            desktop_item['pageview_mobile_views'] = mobile_item['views']
            desktop_item['pageview_all_views'] = desktop_item['views'] + mobile_item['views']
            pv_total_views['items'].append(desktop_item)


#load page count mobile into memory to add the year and month columns
pc_mobile_json = json.load(open(r'''pageCounts_mobile-site_200801_201608.json'''))
for mobile_item in pc_mobile_json['items']:
    mobile_item['year'] = mobile_item['timestamp'][0:4]
    mobile_item['month'] = mobile_item['timestamp'][4:6]

#load page count desktop into memory to add the year and month columns
pc_desktop_json = json.load(open(r'''pageCounts_desktop-site_200801_201608.json'''))
for desktop_item in pc_desktop_json['items']:
    desktop_item['year'] = desktop_item['timestamp'][0:4]
    desktop_item['month'] = desktop_item['timestamp'][4:6]


#Create the final results for page count
pc_total_views = dict()
pc_total_views['items'] = list()

#sum up the values for mobile and desktop for page count data (adding columns according to the final result format
for desktop_item in pc_desktop_json['items']:
    mobViews = 0
    for mobile_item in pc_mobile_json['items']:
            if mobile_item['month'] == desktop_item['month'] and mobile_item['year'] == desktop_item['year']:
                mobViews = mobile_item['count']
    #add the base item including the monthly view information for desktop first
    #we then add the following columns to match the final result format
    # 1. pagecount_desktop_views columns which has the same value as the exisiting 'views' columns
    # 2. pagecount_mobile_views which is the value of the 'views' from the corresponding month from mobile data
    # 3. pagecount_all_views the sum of mobile and desktop views
    desktop_item['pagecount_desktop_views'] = desktop_item['count']
    desktop_item['pagecount_mobile_views'] = mobViews
    desktop_item['pagecount_all_views'] = desktop_item['count'] + mobViews
    pc_total_views['items'].append(desktop_item)

#At this point, our current pageview results are in pv_total_views and page count results are stored in pc_total_views
#we need to create a single csv file using these two sets of data
print(pc_total_views)
print(pv_total_views)

#open a file and initialize a csv writer
#with open("en-wikipedia_traffic_200801-201709.csv", "w") as fp:
with open("en-wikipedia_traffic_200801-201709.csv", "w") as fp:
    csv_writer = csv.DictWriter(fp, fieldnames= \
        ["year", "month", "pagecount_all_views", "pagecount_desktop_views",\
         "pagecount_mobile_views","pageview_all_views","pageview_desktop_views","pageview_mobile_views"])
    csv_writer.writeheader()
    #Create list of years and months going through both data sets and adding what doesnt already exist
    for pc_item in pc_total_views['items']:
        added = False
        for pv_item in pv_total_views['items']:
            if pc_item['year'] == pv_item['year'] and pc_item['month'] == pv_item['month']:
                csv_writer.writerow({'year': pc_item['year'], 'month' : pc_item['month'], \
                                     'pagecount_all_views': pc_item['pagecount_all_views'], \
                                     'pagecount_desktop_views' : pc_item['pagecount_desktop_views'], \
                                     'pagecount_mobile_views' : pc_item['pagecount_mobile_views'], \
                                     'pageview_all_views': pv_item['pageview_all_views'], \
                                     'pageview_desktop_views': pv_item['pageview_desktop_views'],\
                                     'pageview_mobile_views': pv_item['pageview_mobile_views']})
                added = True
                break
        if added == False:
            csv_writer.writerow({'year': pc_item['year'], 'month': pc_item['month'], \
                                 'pagecount_all_views': pc_item['pagecount_all_views'], \
                                 'pagecount_desktop_views': pc_item['pagecount_desktop_views'], \
                                 'pagecount_mobile_views': pc_item['pagecount_mobile_views'], \
                                 'pageview_all_views': 0, \
                                 'pageview_desktop_views': 0, \
                                 'pageview_mobile_views': 0})

#now we can move to plotting step
merged_csv = pd.read_csv("final_csv.csv")
print(merged_csv)
plt.figure(figsize=(20, 8));

df = pd.DataFrame({'year':merged_csv['year'], 'month':merged_csv['month'], 'day':[1]*103})
dt = pd.to_datetime(df, format = '%Y%m%')

plt.plot(dt[0:103], merged_csv['pagecount_desktop_views'][0:103]/1e6,'g--', label="main site");
plt.plot(dt[81:103], merged_csv['pagecount_mobile_views'][81:103]/1e6,'b--', label="mobile site");
plt.plot(dt[0:103], merged_csv['pagecount_all_views'][0:103]/1e6,'k--', label="total");

plt.legend(['main site', 'mobile site', 'total'], fontsize = 15);

plt.plot(dt[90:103], merged_csv['pageview_desktop_views'][90:103]/1e6,'g', label="main site");
plt.plot(dt[90:103], merged_csv['pageview_mobile_views'][90:103]/1e6,'b', label="mobile site");
plt.plot(dt[90:103], merged_csv['pageview_all_views'][90:103]/1e6,'k', label="total",);

plt.title("Page Views on English Wikipedia (x 1,000,000)", fontsize = 20);
plt.ylim((0,12000))
plt.yticks(fontsize = 16);
plt.xticks(fontsize = 16);
plt.grid(True)
plt.xlabel("May 2015: a new pageview definition took effect, which eliminated all crawler traffic.  Dashed lines mark old definition", fontsize = 14);
plt.savefig('pageviews_english_wikipedia.png')