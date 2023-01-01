import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse


PARSER_DESCRIPTION = "LM worklogs logger using JIRA REST API, version 1.0, 2023-1-1"

def parse_arguments(parser, filename,start_date, end_date):
    """Setup default parameter settings"""
    parser.add_argument("-f","--filename",
                        help="filename of the file and make sure that the sure file is in the same folder of this script. File type",
                        required=True,
                        type=str, default = filename
                        )
    parser.add_argument("-sd","--start_date",
                        help="Start date of logs you want to be recorded in JIRA, format= yyyy-mm-dd",
                        required=True,
                        type=str, default= start_date
                        ) 
    parser.add_argument("-ed", "--end_date",
                        help="End date of logs you want to be recorded in JIRA, format= yyyy-mm-dd",
                        required=True,
                        type=str, default=end_date)    


    args = parser.parse_args()
    print("returned args")
    return args


class jira_rest_api:
    def __init__(self, df, credentials, start_date, end_date):
        self.df = pd.read_excel("Worklog Entry Template.xlsx", sheet_name= 'worklog Template')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df[(self.df['Date'] >= pd.to_datetime(start_date)) & (self.df['Date'] <= pd.to_datetime(end_date))].copy()
        print(len(self.df))
        self.prep()
        
        with open(credentials) as f:
            credentials = json.load(f)
            self.account_email = credentials['email']
            self.auth_token = credentials['token']

        self.auth = HTTPBasicAuth(self.account_email, self.auth_token)
        self.headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                        }

    def prep(self):
        self.df['url'] = self.df.apply(lambda x: f"https://legalmatch.atlassian.net/rest/api/3/issue/{x['Project description'].split('/')[-1]}/worklog", axis= 1)
        self.df['timespent'] = self.df.apply(lambda x: x['Time spent (Hr)'] * 60**2, axis= 1)
        self.df.Date = self.df.Date.astype('str')
        self.df['payload'] = self.df.apply(lambda x: self.generate_payload(x['timespent'], x['Comments'], x['Date']), axis= 1)
        self.df.reset_index(drop=True, inplace= True)
        
    def log(self):
        for index, row in self.df.iterrows():
            response = self.worklog(row['url'], row['payload'])
            print(f"Working on index: {index}, {response.status_code}")
            self.df.loc[index, 'status_code'] = response.status_code
            
    
    def generate_payload(self, timespent, comment, date):
        temp_dict = {'timeSpentSeconds': 12000,
                        'comment': {'type': 'doc',
                            'version': 1,
                            'content': [{'type': 'paragraph',
                                    'content': [{'text': 'I did some work here.', 'type': 'text'}]}]},
                        'started': '2022-01-1T12:34:00.000+0000'}

        temp_dict['timeSpentSeconds'] = timespent
        temp_dict['comment']['content'][0]['content'][0]['text'] = comment
        temp_dict['started'] = str(date) + 'T00:00:00.000+0000'

        return json.dumps(temp_dict)

    def worklog(self, url, payload):
        response = requests.request(
                                    "POST",
                                    url,
                                    data=payload,
                                    headers=self.headers,
                                    auth= self.auth
                                    )
        return response
        

def main():
    global PARSER_DESCRIPTION
    parser = argparse.ArgumentParser(description=PARSER_DESCRIPTION)
    args = parse_arguments(parser, None, None, None)

    print(f"This is args.filename {args.filename}", )
    print(f"This is args.start_date {args.start_date}")
    print(f"This is args.end_date {args.end_date}")


    pd.options.display.max_columns = 999
    worklog = jira_rest_api(args.filename, 'credential.json', args.start_date, args.end_date)
    worklog.log()

    print("----------------------------------------------")
    print("----------------------------------------------")
    print("----------------------------------------------")

    print(worklog.df.head())

if __name__ == '__main__':
    main()
