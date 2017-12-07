## Human Centered Data Science First Assignment: Data Curation on English Wikipedia View Metrics

The goal of this project is to analyze the view metrics on the data provided by wikimedia foundation and provide reproducible steps to repeat this study by publishing the results in form of a Jupyter Notebook.
In this analysis we will collect and analyze the monthly traffic metric data in the time window of January 1 2008 through September 30 2017 on English Wikipedia from two different source API servers.

  This README file and the Jupyter Notebook file, `hcds-a1-data-curation.ipynb`, contain the information and  
  references needed to reproduce the analysis, including a description of the data and all relevant resources  
  and documentation, with hyperlinks to those resources.  
  

### Copyright  

The Wikipedia data was gathered from the Wikimedia REST API, Wikimedia Foundation, 2017. CC-BY-SA 3.0  

### License 

This Wikimedia Foundation data is licensed under an Apache 2.0 License, which includes in part:  

> Unless required by applicable law or agreed to in writing, software  
> distributed under the License is distributed on an "AS IS" BASIS,  
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
> See the License for the specific language governing permissions and  
> limitations under the License.  

For more information on this license, see [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).

### Terms of Use
The use of Wikipedia data is subject to the Wikimedia Foundation Terms of Use (TOU). A summary of these TOU, along with the complete terms are available [here](https://wikimediafoundation.org/wiki/Terms_of_Use/en).   

### API Documentation

 Pagecounts API and Pageviews API. 

 - __Pagecounts API__ ([documentation](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Legacy_Pagecounts), [endpoint](https://wikimedia.org/api/rest_v1/#!/Pagecounts_data_(legacy)/get_metrics_legacy_pagecounts_aggregate_project_access_site_granularity_start_end)) provides access to desktop and mobile traffic data from Jan. 2008 through July 2016.  
    * This older, legacy Pagecount API does not allow you to filter by user, so the monthly counts include all  
  the views by people, bots, and web crawlers.  

 - __Pageviews API__ ([documentation](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews), [endpoint](https://wikimedia.org/api/rest_v1/#!/Pageviews_data/get_metrics_pageviews_aggregate_project_access_agent_granularity_start_end)) provides access to desktop, mobile web, and mobile app traffic data from July 2015 through current day.  
    * Each API endpoint can be accessed in multiple ways. In the legacy data, the only distinguished access types were mobile and desktop sites, however after July 2015, in order to distiguish the automated (web-crawlers) access from the real-user access mechanisms, the new API provider introduced the 'agent' parameter. Thus by specifying the agent as 'user' we are able to further filter access by users.


