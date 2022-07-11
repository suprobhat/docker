import streamlit as st
from atlassian import Jira
import pandas as pd
import json
import re
import warnings

warnings.filterwarnings('ignore')



st.set_page_config(page_title='DEF_DENSE_AUTO', page_icon='bar_chart', layout='wide')

# https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
st.title('QUALITY METRICS AUTOMATION')
st.markdown('*by CHANDRAPRAKASH*')
col1, col2, col3 = st.columns(3)
col1.write("PROJECT")
col2.write("METRIC NAME")
col3.write("OPERATION")


def project_code(project):
    if project=='ID20':
        projectcde='ID20'
    elif project=='SOUCS':
        projectcde='SOUCS'
    elif project=='EODBT':
        projectcde='EODBT'
    elif project=='ACA':
        projectcde='ACA'
    return projectcde


# Three different columns:
col1, col2, col3 = st.columns([1, 1, 1])
# col1 is larger.
# You can also use "with" notation:
with col1:
    activities = st.selectbox('METRIC NAME', ('Select', 'DEFECT DENSITY', 'RE OPENRATE'))
    project = st.selectbox('PROJECT NAME', ('Select', 'ID20', 'SOUCS', 'EODBT', 'ACA'))
    #sprintname = st.selectbox('SPRINTNAME', ('Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5', 'Sprint 6', 'Sprint 7', 'Sprint 8', 'Sprint 9', 'Sprint 10',  'Sprint 11', 'Sprint 12', 'Sprint 13', 'Sprint 14', 'Sprint 15', 'Sprint 16', 'Sprint 17', 'Sprint 18', 'Sprint 19', 'Sprint 20', 'Sprint 21', 'Sprint 22', 'Sprint 23', 'Sprint 24', 'Sprint 25', 'Sprint 26', 'Sprint 27', 'Sprint 28', 'Sprint 29', 'Sprint 30', 'Sprint 31', 'Sprint 32', 'Sprint 33', 'Sprint 34', 'Sprint 35', 'Sprint 36', 'Sprint 37', 'Sprint 38', 'Sprint 39', 'Sprint 40', 'Sprint 41', 'Sprint 42', 'Sprint 43', 'Sprint 44', 'Sprint 45', 'Sprint 46', 'Sprint 47', 'Sprint 48', 'Sprint 49', 'Sprint 50', 'Sprint 51', 'Sprint 52', 'Sprint 53', 'Sprint 54', 'Sprint 55', 'Sprint 56', 'Sprint 57', 'Sprint 58', 'Sprint 59', 'Sprint 60'))
    if activities =='DEFECT DENSITY':
        st.markdown('')    
        st.markdown('**SELECT SPRINT NAME**')
        st.markdown('**Selected project :** ' + project)
        sp1 = st.checkbox(project + '- Sprint 1')
        if sp1:
            jira = Jira(url='https://www.inadev.net/tracker', username='s.chandra', password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key']=df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i), flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +1', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i      
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))  
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points1 = chandru['story_points'].sum()
            total_number_bugs_count1 = sum(num_count)
            d_d1 = (total_number_bugs_count1/total_number_story_points1)*100
            nnn = {'Sprint Name' : ['Sprint 1'],
            'Numbers of bugs associated A':[total_number_bugs_count1],
            'total number of story points B':[total_number_story_points1],
            'defect density (A/B)*100':[d_d1]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 2')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker', username='s.chandra', password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key']=df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +2', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i      
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))  
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points2 = chandru['story_points'].sum()
            total_number_bugs_count2 = sum(num_count)
            d_d2 = (total_number_bugs_count2/total_number_story_points2)*100
            nnn = {'Sprint Name' : ['Sprint 2'],
            'Numbers of bugs associated A':[total_number_bugs_count2],
             'total number of story points':[total_number_story_points2],
            'defect density':[d_d2]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 3')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1,limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +3', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points3 = chandru['story_points'].sum()
            total_number_bugs_count3 = sum(num_count)
            d_d3 = (total_number_bugs_count3/total_number_story_points3)*100
            nnn = {'Sprint Name': ['Sprint 3'], 'Numbers of bugs associated A': [total_number_bugs_count3], 'total number of story points': [total_number_story_points3], 'defect density': [d_d3]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 4')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker', username='s.chandra', password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +4', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points4 = chandru['story_points'].sum()
            total_number_bugs_count4 = sum(num_count)
            d_d4 = (total_number_bugs_count4/total_number_story_points4)*100
            nnn = {'Sprint Name': ['Sprint 4'], 'Numbers of bugs associated A': [total_number_bugs_count4], 'total number of story points': [total_number_story_points4], 'defect density': [d_d4]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 5')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +5', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points5 = chandru['story_points'].sum()
            total_number_bugs_count5 = sum(num_count)
            d_d5 = (total_number_bugs_count5/total_number_story_points5)*100
            nnn = {'Sprint Name': ['Sprint 5'], 'Numbers of bugs associated A': [total_number_bugs_count5],  'total number of story points': [total_number_story_points5],  'defect density': [d_d5]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 6')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker', username='s.chandra',  password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +6', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points6 = chandru['story_points'].sum()
            total_number_bugs_count6 = sum(num_count)
            d_d6 = (total_number_bugs_count6/total_number_story_points6)*100
            nnn = {'Sprint Name': ['Sprint 6'], 'Numbers of bugs associated A': [total_number_bugs_count6],  'total number of story points': [total_number_story_points6],  'defect density': [d_d6]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)


        sp1 = st.checkbox(project+ '- Sprint 7')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +7', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points7 = chandru['story_points'].sum()
            total_number_bugs_count7 = sum(num_count)
            d_d7 = (total_number_bugs_count7/total_number_story_points7)*100
            nnn = {'Sprint Name': ['Sprint 7'], 'Numbers of bugs associated A': [total_number_bugs_count7],  'total number of story points': [total_number_story_points7],  'defect density': [d_d7]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 8')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +8', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points8 = chandru['story_points'].sum()
            total_number_bugs_count8 = sum(num_count)
            d_d8 = (total_number_bugs_count8/total_number_story_points8)*100
            nnn = {'Sprint Name': ['Sprint 8'], 'Numbers of bugs associated A': [total_number_bugs_count8],  'total number of story points': [total_number_story_points8],  'defect density': [d_d8]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 9')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            new = []
            for i in dat['sprint_num']:
                use = re.findall('Sprint +[1-9]', str(i),flags=0)
                new.append(use)
            dat['sprint_numbers']=new
            cp = []
            for i in dat['sprint_numbers']:
                zus = re.findall('Sprint +9', str(i),flags=0)
                cp.append(zus)
            dat['new']=cp
            e = []
            d = []
            for i,j in enumerate(dat['new']):
                if len(j)==0:
                    e.append(i)
                else:
                    d.append(i)
            sovan = dat.iloc[d,:]
            dfs = {}
            for i,j in zip(sovan['link'].values,range(len(sovan['link']))):
                dfs[j]=i
            dfs_dic = {}
            for i in dfs.keys():
                data = dfs[i]
                json_string = json.dumps(data)
                dfs_dic[i] = json_string
            new_list = []
            for i in dfs_dic.values():
                new_list.append(i.partition(':'))
            final = []
            num_count = []
            for i in range(len(new_list)):
                temp = []
                num = 0
                for j in new_list[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num +=1
                final.append(temp)
                num_count.append(num)
            sovan['link_Bug_count']=num_count

            col = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new']
            chandru = sovan[col]
            total_number_story_points9 = chandru['story_points'].sum()
            total_number_bugs_count9 = sum(num_count)
            d_d9 = (total_number_bugs_count9/total_number_story_points9)*100
            nnn = {'Sprint Name': ['Sprint 9'], 'Numbers of bugs associated A': [total_number_bugs_count9],  'total number of story points': [total_number_story_points9],  'defect density': [d_d9]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 10')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +10', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points10 = chandruu['story_points'].sum()
            total_number_bugs_count10 = sum(num_countt)
            d_d10 = (total_number_bugs_count10/total_number_story_points10) * 100
            nnn = {'Sprint Name': ['Sprint 10'], 'Numbers of bugs associated A': [total_number_bugs_count10],  'total number of story points': [total_number_story_points10],  'defect density': [d_d10]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 11')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +11', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points11 = chandruu['story_points'].sum()
            total_number_bugs_count11 = sum(num_countt)
            d_d11 = (total_number_bugs_count11/total_number_story_points11) * 100
            nnn = {'Sprint Name': ['Sprint 11'], 'Numbers of bugs associated A': [total_number_bugs_count11],  'total number of story points': [total_number_story_points11],  'defect density': [d_d11]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 12')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +12', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points12 = chandruu['story_points'].sum()
            total_number_bugs_count12 = sum(num_countt)
            d_d12 = (total_number_bugs_count12/total_number_story_points12) * 100
            nnn = {'Sprint Name': ['Sprint 12'], 'Numbers of bugs associated A': [total_number_bugs_count12],  'total number of story points': [total_number_story_points12],  'defect density': [d_d12]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 13')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +13', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points13 = chandruu['story_points'].sum()
            total_number_bugs_count13 = sum(num_countt)
            d_d13 = (total_number_bugs_count13/total_number_story_points13) * 100
            nnn = {'Sprint Name': ['Sprint 13'], 'Numbers of bugs associated A': [total_number_bugs_count13],  'total number of story points': [total_number_story_points13],  'defect density': [d_d13]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 14')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +14', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points14 = chandruu['story_points'].sum()
            total_number_bugs_count14 = sum(num_countt)
            d_d14 = (total_number_bugs_count14/total_number_story_points14) * 100
            nnn = {'Sprint Name': ['Sprint 14'], 'Numbers of bugs associated A': [total_number_bugs_count14],  'total number of story points': [total_number_story_points14],  'defect density': [d_d14]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 15')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +15', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points15 = chandruu['story_points'].sum()
            total_number_bugs_count15 = sum(num_countt)
            d_d15 = (total_number_bugs_count15/total_number_story_points15) * 100
            nnn = {'Sprint Name': ['Sprint 15'], 'Numbers of bugs associated A': [total_number_bugs_count15],  'total number of story points': [total_number_story_points15],  'defect density': [d_d15]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 16')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +16', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points16 = chandruu['story_points'].sum()
            total_number_bugs_count16 = sum(num_countt)
            d_d16 = (total_number_bugs_count16/total_number_story_points16) * 100
            nnn = {'Sprint Name': ['Sprint 16'], 'Numbers of bugs associated A': [total_number_bugs_count16],  'total number of story points': [total_number_story_points16],  'defect density': [d_d16]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 17')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +17', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points17 = chandruu['story_points'].sum()
            total_number_bugs_count17 = sum(num_countt)
            d_d17 = (total_number_bugs_count17/total_number_story_points17) * 100
            nnn = {'Sprint Name': ['Sprint 17'], 'Numbers of bugs associated A': [total_number_bugs_count17],  'total number of story points': [total_number_story_points17],  'defect density': [d_d17]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 18')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +18', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points18 = chandruu['story_points'].sum()
            total_number_bugs_count18 = sum(num_countt)
            d_d18 = (total_number_bugs_count18/total_number_story_points18) * 100
            nnn = {'Sprint Name': ['Sprint 18'], 'Numbers of bugs associated A': [total_number_bugs_count18],  'total number of story points': [total_number_story_points18],  'defect density': [d_d18]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 19')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +19', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points19 = chandruu['story_points'].sum()
            total_number_bugs_count19 = sum(num_countt)
            d_d19 = (total_number_bugs_count19/total_number_story_points19) * 100
            nnn = {'Sprint Name': ['Sprint 19'], 'Numbers of bugs associated A': [total_number_bugs_count19],  'total number of story points': [total_number_story_points19],  'defect density': [d_d19]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 20')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +20', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points20 = chandruu['story_points'].sum()
            total_number_bugs_count20 = sum(num_countt)
            d_d20 = (total_number_bugs_count20/total_number_story_points20) * 100
            nnn = {'Sprint Name': ['Sprint 20'], 'Numbers of bugs associated A': [total_number_bugs_count20],  'total number of story points': [total_number_story_points20],  'defect density': [d_d20]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 21')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +21', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points21 = chandruu['story_points'].sum()
            total_number_bugs_count21 = sum(num_countt)
            d_d21 = (total_number_bugs_count21/total_number_story_points21) * 100
            nnn = {'Sprint Name': ['Sprint 21'], 'Numbers of bugs associated A': [total_number_bugs_count21],  'total number of story points': [total_number_story_points21],  'defect density': [d_d21]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 22')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +22', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points22 = chandruu['story_points'].sum()
            total_number_bugs_count22 = sum(num_countt)
            d_d22 = (total_number_bugs_count22/total_number_story_points22) * 100
            nnn = {'Sprint Name': ['Sprint 22'], 'Numbers of bugs associated A': [total_number_bugs_count22],  'total number of story points': [total_number_story_points22],  'defect density': [d_d22]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 23')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +23', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points23 = chandruu['story_points'].sum()
            total_number_bugs_count23 = sum(num_countt)
            d_d23 = (total_number_bugs_count23/total_number_story_points23) * 100
            nnn = {'Sprint Name': ['Sprint 23'], 'Numbers of bugs associated A': [total_number_bugs_count23],  'total number of story points': [total_number_story_points23],  'defect density': [d_d23]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 24')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +24', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points24 = chandruu['story_points'].sum()
            total_number_bugs_count24 = sum(num_countt)
            d_d24 = (total_number_bugs_count24/total_number_story_points24) * 100
            nnn = {'Sprint Name': ['Sprint 24'], 'Numbers of bugs associated A': [total_number_bugs_count24],  'total number of story points': [total_number_story_points24],  'defect density': [d_d24]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 25')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +25', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points25 = chandruu['story_points'].sum()
            total_number_bugs_count25 = sum(num_countt)
            d_d25 = (total_number_bugs_count25/total_number_story_points25) * 100
            nnn = {'Sprint Name': ['Sprint 25'], 'Numbers of bugs associated A': [total_number_bugs_count25],  'total number of story points': [total_number_story_points25],  'defect density': [d_d25]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 26')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +26', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points26 = chandruu['story_points'].sum()
            total_number_bugs_count26 = sum(num_countt)
            d_d26 = (total_number_bugs_count26/total_number_story_points26) * 100
            nnn = {'Sprint Name': ['Sprint 26'], 'Numbers of bugs associated A': [total_number_bugs_count26],  'total number of story points': [total_number_story_points26],  'defect density': [d_d26]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 27')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +27', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points27 = chandruu['story_points'].sum()
            total_number_bugs_count27 = sum(num_countt)
            d_d27 = (total_number_bugs_count27/total_number_story_points27) * 100
            nnn = {'Sprint Name': ['Sprint 27'], 'Numbers of bugs associated A': [total_number_bugs_count27],  'total number of story points': [total_number_story_points27],  'defect density': [d_d27]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 28')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +28', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points28 = chandruu['story_points'].sum()
            total_number_bugs_count28 = sum(num_countt)
            d_d28 = (total_number_bugs_count28/total_number_story_points28) * 100
            nnn = {'Sprint Name': ['Sprint 28'], 'Numbers of bugs associated A': [total_number_bugs_count28],  'total number of story points': [total_number_story_points28],  'defect density': [d_d28]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 29')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +29', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points29 = chandruu['story_points'].sum()
            total_number_bugs_count29 = sum(num_countt)
            d_d29 = (total_number_bugs_count29/total_number_story_points29) * 100
            nnn = {'Sprint Name': ['Sprint 29'], 'Numbers of bugs associated A': [total_number_bugs_count29],  'total number of story points': [total_number_story_points29],  'defect density': [d_d29]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 30')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +30', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points30 = chandruu['story_points'].sum()
            total_number_bugs_count30 = sum(num_countt)
            d_d30 = (total_number_bugs_count30/total_number_story_points30) * 100
            nnn = {'Sprint Name': ['Sprint 30'], 'Numbers of bugs associated A': [total_number_bugs_count30],  'total number of story points': [total_number_story_points30],  'defect density': [d_d30]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 31')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +31', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points31 = chandruu['story_points'].sum()
            total_number_bugs_count31 = sum(num_countt)
            d_d31 = (total_number_bugs_count31/total_number_story_points31) * 100
            nnn = {'Sprint Name': ['Sprint 31'], 'Numbers of bugs associated A': [total_number_bugs_count31],  'total number of story points': [total_number_story_points31],  'defect density': [d_d31]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 32')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +32', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points32 = chandruu['story_points'].sum()
            total_number_bugs_count32 = sum(num_countt)
            d_d32 = (total_number_bugs_count32/total_number_story_points32) * 100
            nnn = {'Sprint Name': ['Sprint 32'], 'Numbers of bugs associated A': [total_number_bugs_count32],  'total number of story points': [total_number_story_points32],  'defect density': [d_d32]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 33')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +33', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points33 = chandruu['story_points'].sum()
            total_number_bugs_count33 = sum(num_countt)
            d_d33 = (total_number_bugs_count33/total_number_story_points33) * 100
            nnn = {'Sprint Name': ['Sprint 33'], 'Numbers of bugs associated A': [total_number_bugs_count33],  'total number of story points': [total_number_story_points33],  'defect density': [d_d33]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 34')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +34', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points34 = chandruu['story_points'].sum()
            total_number_bugs_count34 = sum(num_countt)
            d_d34 = (total_number_bugs_count34/total_number_story_points34) * 100
            nnn = {'Sprint Name': ['Sprint 34'], 'Numbers of bugs associated A': [total_number_bugs_count34],  'total number of story points': [total_number_story_points34],  'defect density': [d_d34]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)


        sp1 = st.checkbox(project+ '- Sprint 35')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +35', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points35 = chandruu['story_points'].sum()
            total_number_bugs_count35 = sum(num_countt)
            d_d35 = (total_number_bugs_count35/total_number_story_points35) * 100
            nnn = {'Sprint Name': ['Sprint 35'], 'Numbers of bugs associated A': [total_number_bugs_count35],  'total number of story points': [total_number_story_points35],  'defect density': [d_d35]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 36')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +36', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points36 = chandruu['story_points'].sum()
            total_number_bugs_count36 = sum(num_countt)
            d_d36 = (total_number_bugs_count36/total_number_story_points36) * 100
            nnn = {'Sprint Name': ['Sprint 36'], 'Numbers of bugs associated A': [total_number_bugs_count36],  'total number of story points': [total_number_story_points36],  'defect density': [d_d36]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)


        sp1 = st.checkbox(project+ '- Sprint 37')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +37', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points37 = chandruu['story_points'].sum()
            total_number_bugs_count37 = sum(num_countt)
            d_d37 = (total_number_bugs_count37/total_number_story_points37) * 100
            nnn = {'Sprint Name': ['Sprint 37'], 'Numbers of bugs associated A': [total_number_bugs_count37],  'total number of story points': [total_number_story_points37],  'defect density': [d_d37]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 38')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +38', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points38 = chandruu['story_points'].sum()
            total_number_bugs_count38 = sum(num_countt)
            d_d38 = (total_number_bugs_count38/total_number_story_points38) * 100
            nnn = {'Sprint Name': ['Sprint 38'], 'Numbers of bugs associated A': [total_number_bugs_count38],  'total number of story points': [total_number_story_points38],  'defect density': [d_d38]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 39')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +39', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points39 = chandruu['story_points'].sum()
            total_number_bugs_count39 = sum(num_countt)
            d_d39 = (total_number_bugs_count39/total_number_story_points39) * 100
            nnn = {'Sprint Name': ['Sprint 39'], 'Numbers of bugs associated A': [total_number_bugs_count39],  'total number of story points': [total_number_story_points39],  'defect density': [d_d39]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 40')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +40', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points40 = chandruu['story_points'].sum()
            total_number_bugs_count40 = sum(num_countt)
            d_d40 = (total_number_bugs_count40/total_number_story_points40) * 100
            nnn = {'Sprint Name': ['Sprint 40'], 'Numbers of bugs associated A': [total_number_bugs_count40],  'total number of story points': [total_number_story_points40],  'defect density': [d_d40]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)
        sp1 = st.checkbox(project+ '- Sprint 41')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +41', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points41 = chandruu['story_points'].sum()
            total_number_bugs_count41 = sum(num_countt)
            d_d41 = (total_number_bugs_count41/total_number_story_points41) * 100
            nnn = {'Sprint Name': ['Sprint 41'], 'Numbers of bugs associated A': [total_number_bugs_count41],  'total number of story points': [total_number_story_points41],  'defect density': [d_d41]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 42')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +42', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points42 = chandruu['story_points'].sum()
            total_number_bugs_count42 = sum(num_countt)
            d_d42 = (total_number_bugs_count42/total_number_story_points42) * 100
            nnn = {'Sprint Name': ['Sprint 42'], 'Numbers of bugs associated A': [total_number_bugs_count42],  'total number of story points': [total_number_story_points42],  'defect density': [d_d42]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 43')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +43', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points43 = chandruu['story_points'].sum()
            total_number_bugs_count43 = sum(num_countt)
            d_d43 = (total_number_bugs_count43/total_number_story_points43) * 100
            nnn = {'Sprint Name': ['Sprint 43'], 'Numbers of bugs associated A': [total_number_bugs_count43],  'total number of story points': [total_number_story_points43],  'defect density': [d_d43]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 44')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +44', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points44 = chandruu['story_points'].sum()
            total_number_bugs_count44 = sum(num_countt)
            d_d44 = (total_number_bugs_count44/total_number_story_points44) * 100
            nnn = {'Sprint Name': ['Sprint 44'], 'Numbers of bugs associated A': [total_number_bugs_count44],  'total number of story points': [total_number_story_points44],  'defect density': [d_d44]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 45')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +45', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points45 = chandruu['story_points'].sum()
            total_number_bugs_count45 = sum(num_countt)
            d_d45 = (total_number_bugs_count45/total_number_story_points45) * 100
            nnn = {'Sprint Name': ['Sprint 45'], 'Numbers of bugs associated A': [total_number_bugs_count45], 'total number of story points': [total_number_story_points45],  'defect density': [d_d45]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 46')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +46', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points46 = chandruu['story_points'].sum()
            total_number_bugs_count46 = sum(num_countt)
            d_d46 = (total_number_bugs_count46/total_number_story_points46) * 100
            nnn = {'Sprint Name': ['Sprint 46'], 'Numbers of bugs associated A': [total_number_bugs_count46],  'total number of story points': [total_number_story_points46],  'defect density': [d_d46]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 47')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +47', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points47 = chandruu['story_points'].sum()
            total_number_bugs_count47 = sum(num_countt)
            d_d47 = (total_number_bugs_count47/total_number_story_points47) * 100
            nnn = {'Sprint Name': ['Sprint 47'], 'Numbers of bugs associated A': [total_number_bugs_count47],  'total number of story points': [total_number_story_points47],  'defect density': [d_d47]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 48')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +48', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points48 = chandruu['story_points'].sum()
            total_number_bugs_count48 = sum(num_countt)
            d_d48 = (total_number_bugs_count48/total_number_story_points48) * 100
            nnn = {'Sprint Name': ['Sprint 48'], 'Numbers of bugs associated A': [total_number_bugs_count48],  'total number of story points': [total_number_story_points48],  'defect density': [d_d48]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 49')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +49', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points49 = chandruu['story_points'].sum()
            total_number_bugs_count49 = sum(num_countt)
            d_d49 = (total_number_bugs_count49/total_number_story_points49) * 100
            nnn = {'Sprint Name': ['Sprint 49'], 'Numbers of bugs associated A': [total_number_bugs_count49],  'total number of story points': [total_number_story_points49],  'defect density': [d_d49]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 50')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +50', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points50 = chandruu['story_points'].sum()
            total_number_bugs_count50 = sum(num_countt)
            d_d50 = (total_number_bugs_count50/total_number_story_points50) * 100
            nnn = {'Sprint Name': ['Sprint 50'], 'Numbers of bugs associated A': [total_number_bugs_count50],  'total number of story points': [total_number_story_points50],  'defect density': [d_d50]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 51')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +51', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points51 = chandruu['story_points'].sum()
            total_number_bugs_count51 = sum(num_countt)
            d_d51 = (total_number_bugs_count51/total_number_story_points51) * 100
            nnn = {'Sprint Name': ['Sprint 51'], 'Numbers of bugs associated A': [total_number_bugs_count51],  'total number of story points': [total_number_story_points51],  'defect density': [d_d51]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 52')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +52', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points52 = chandruu['story_points'].sum()
            total_number_bugs_count52 = sum(num_countt)
            d_d52 = (total_number_bugs_count52/total_number_story_points52) * 100
            nnn = {'Sprint Name': ['Sprint 52'], 'Numbers of bugs associated A': [total_number_bugs_count52],  'total number of story points': [total_number_story_points52],  'defect density': [d_d52]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 53')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +53', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points53 = chandruu['story_points'].sum()
            total_number_bugs_count53 = sum(num_countt)
            d_d53 = (total_number_bugs_count53/total_number_story_points53) * 100
            nnn = {'Sprint Name': ['Sprint 53'], 'Numbers of bugs associated A': [total_number_bugs_count53],  'total number of story points': [total_number_story_points53],  'defect density': [d_d53]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 54')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +54', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points54 = chandruu['story_points'].sum()
            total_number_bugs_count54 = sum(num_countt)
            d_d54 = (total_number_bugs_count54/total_number_story_points54) * 100
            nnn = {'Sprint Name': ['Sprint 54'], 'Numbers of bugs associated A': [total_number_bugs_count54],  'total number of story points': [total_number_story_points54],  'defect density': [d_d54]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 55')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +55', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points55 = chandruu['story_points'].sum()
            total_number_bugs_count55 = sum(num_countt)
            d_d55 = (total_number_bugs_count55/total_number_story_points55) * 100
            nnn = {'Sprint Name': ['Sprint 55'], 'Numbers of bugs associated A': [total_number_bugs_count55],  'total number of story points': [total_number_story_points55],  'defect density': [d_d55]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)


        sp1 = st.checkbox(project+ '- Sprint 56')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +56', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points56 = chandruu['story_points'].sum()
            total_number_bugs_count56 = sum(num_countt)
            d_d56 = (total_number_bugs_count56/total_number_story_points56) * 100
            nnn = {'Sprint Name': ['Sprint 56'], 'Numbers of bugs associated A': [total_number_bugs_count56],  'total number of story points': [total_number_story_points56],  'defect density': [d_d56]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 57')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +57', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points57 = chandruu['story_points'].sum()
            total_number_bugs_count57 = sum(num_countt)
            d_d57 = (total_number_bugs_count57/total_number_story_points57) * 100
            nnn = {'Sprint Name': ['Sprint 57'], 'Numbers of bugs associated A': [total_number_bugs_count57],  'total number of story points': [total_number_story_points57],  'defect density': [d_d57]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 58')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +58', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points58 = chandruu['story_points'].sum()
            total_number_bugs_count58 = sum(num_countt)
            d_d58 = (total_number_bugs_count58/total_number_story_points58) * 100
            nnn = {'Sprint Name': ['Sprint 58'], 'Numbers of bugs associated A': [total_number_bugs_count58],  'total number of story points': [total_number_story_points58],  'defect density': [d_d58]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 59')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +59', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points59 = chandruu['story_points'].sum()
            total_number_bugs_count59 = sum(num_countt)
            d_d59 = (total_number_bugs_count59/total_number_story_points59) * 100
            nnn = {'Sprint Name': ['Sprint 59'], 'Numbers of bugs associated A': [total_number_bugs_count59],  'total number of story points': [total_number_story_points59],  'defect density': [d_d59]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)

        sp1 = st.checkbox(project+ '- Sprint 60')
        if sp1:
            jira  = Jira(url='https://www.inadev.net/tracker',username='s.chandra',password='Ctb@181E25575')
            JQL1='project = '+project_code(project)+' AND issuetype = Story ORDER BY priority DESC, updated DESC'
            data = jira.jql(JQL1, limit=5000)
            df = pd.json_normalize(data['issues'])
            FF = ['key', 'fields.issuetype.name', 'fields.issuetype.description', 'fields.fixVersions', 'fields.issuelinks', 'fields.created', 'fields.versions', 'fields.summary', 'fields.customfield_10008', 'fields.customfield_10000']
            dat = pd.DataFrame()
            dat['key'] = df['key']
            dat['issue_type'] = df['fields.issuetype.name']
            dat['created'] = df['fields.created']
            dat['description'] = df['fields.issuetype.description']
            dat['summary'] = df['fields.summary']
            dat['link'] = df['fields.issuelinks']
            dat['fixversion'] = df['fields.fixVersions']
            dat['affectversion'] = df['fields.versions']
            dat['story_points'] = df['fields.customfield_10008']
            dat['sprint_num'] = df['fields.customfield_10000']
            dat_1 = dat.copy()
            new_1 = []
            for i in dat_1['sprint_num']:
                usee=re.findall('Sprint +[1-9][1-9]', str(i), flags=0)
                new_1.append(usee)
            dat_1['sprint_numbers'] = new_1
            ap = []
            for i in dat_1['sprint_numbers']:
                sus = re.findall('Sprint +60', str(i), flags=0)
                ap.append(sus)
            dat_1['new_1'] = ap
            x = []
            y = []
            for i, j in enumerate(dat_1['new_1']):
                if len(j) == 0:
                    x.append(i)
                else:
                    y.append(i)
            neha = dat_1.iloc[y, :]
            dfss = {}
            for i, j in zip(neha['link'].values, range(len(neha['link']))):
                dfss[j] = i
            dfs_dicc = {}
            for i in dfss.keys():
                data = dfss[i]
                json_string = json.dumps(data)
                dfs_dicc[i] = json_string
            new_list1 = []
            for i in dfs_dicc.values():
                new_list1.append(i.partition(':'))
            finall = []
            num_countt = []
            for i in range(len(new_list1)):
                temp = []
                num = 0
                for j in new_list1[i][2].split():
                    if 'Bug",' in j:
                        temp.append(j)
                        num += 1
                finall.append(temp)
                num_countt.append(num)
            neha['link_Bug_count'] = num_countt
            coll = ['key', 'issue_type', 'summary', 'story_points', 'link_Bug_count', 'new_1']
            chandruu = neha[coll]
            total_number_story_points60 = chandruu['story_points'].sum()
            total_number_bugs_count60 = sum(num_countt)
            d_d60 = (total_number_bugs_count60/total_number_story_points60) * 100
            nnn = {'Sprint Name': ['Sprint 60'], 'Numbers of bugs associated A': [total_number_bugs_count60],  'total number of story points': [total_number_story_points60],  'defect density': [d_d60]}
            cod = pd.DataFrame.from_dict(nnn)
            st.table(cod)


        else:
            st.error('please think Master Mind You will Complete')
    

with col2:
    if st.button('DATA VISUALISATION'):
        st.markdown('**TYPES OF VISUALISATION**')
        x=chandru['story_points']
        y=chandru['link_Bug_count']
        front = ['story_points','link_Bug_count']
        dff = pd.DataFrame(chandru)
        dft = dff[front]
        st.write('This is a line chart')
        st.line_chart(dft)
    else:
        st.error('please think master mind you will complete the program')


with col3:
    if st.button('EXECUTE DATA FRAME'):
        nnn = {'Sprint Name' : ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5', 'Sprint 6', 'Sprint 7', 'Sprint 8', 'Sprint 9', 'Sprint 10',  'Sprint 11', 'Sprint 12', 'Sprint 13', 'Sprint 14', 'Sprint 15', 'Sprint 16', 'Sprint 17', 'Sprint 18', 'Sprint 19', 'Sprint 20', 'Sprint 21', 'Sprint 22', 'Sprint 23', 'Sprint 24', 'Sprint 25', 'Sprint 26', 'Sprint 27', 'Sprint 28', 'Sprint 29', 'Sprint 30', 'Sprint 31', 'Sprint 32', 'Sprint 33', 'Sprint 34', 'Sprint 35', 'Sprint 36', 'Sprint 37', 'Sprint 38', 'Sprint 39', 'Sprint 40', 'Sprint 41', 'Sprint 42', 'Sprint 43', 'Sprint 44', 'Sprint 45', 'Sprint 46', 'Sprint 47', 'Sprint 48', 'Sprint 49', 'Sprint 50', 'Sprint 51', 'Sprint 52', 'Sprint 53', 'Sprint 54', 'Sprint 55', 'Sprint 56', 'Sprint 57', 'Sprint 58', 'Sprint 59', 'Sprint 60'],
        'Numbers of bugs associated A':[total_number_bugs_count1, total_number_bugs_count2,	total_number_bugs_count3, total_number_bugs_count4, total_number_bugs_count5, total_number_bugs_count6, total_number_bugs_count7, total_number_bugs_count8, total_number_bugs_count9, total_number_bugs_count10, total_number_bugs_count11, total_number_bugs_count12, total_number_bugs_count13, total_number_bugs_count14, total_number_bugs_count15, total_number_bugs_count16, total_number_bugs_count17, total_number_bugs_count18, total_number_bugs_count19, total_number_bugs_count20, total_number_bugs_count21, total_number_bugs_count22, total_number_bugs_count23, total_number_bugs_count24, total_number_bugs_count25, total_number_bugs_count26, total_number_bugs_count27, total_number_bugs_count28, total_number_bugs_count29, total_number_bugs_count30, total_number_bugs_count31, total_number_bugs_count32, total_number_bugs_count33, total_number_bugs_count34, total_number_bugs_count35, total_number_bugs_count36, total_number_bugs_count37, total_number_bugs_count38, total_number_bugs_count39, total_number_bugs_count40, total_number_bugs_count41, total_number_bugs_count42, total_number_bugs_count43, total_number_bugs_count44, total_number_bugs_count45, total_number_bugs_count46, total_number_bugs_count47, total_number_bugs_count48, total_number_bugs_count49, total_number_bugs_count50, total_number_bugs_count51, total_number_bugs_count52, total_number_bugs_count53, total_number_bugs_count54, total_number_bugs_count55, total_number_bugs_count56, total_number_bugs_count57, total_number_bugs_count58, total_number_bugs_count59, total_number_bugs_count60],
        'total number of story points':[total_number_story_points1,	total_number_story_points2,	total_number_story_points3,	total_number_story_points4,	total_number_story_points5,	total_number_story_points6,	total_number_story_points7,	total_number_story_points8,	total_number_story_points9,	total_number_story_points10, total_number_story_points11, total_number_story_points12, total_number_story_points13,	total_number_story_points14, total_number_story_points15, total_number_story_points16, total_number_story_points17, total_number_story_points18, total_number_story_points19,	total_number_story_points20, total_number_story_points21, total_number_story_points22, total_number_story_points23,	total_number_story_points24, total_number_story_points25, total_number_story_points26, total_number_story_points27,	total_number_story_points28, total_number_story_points29, total_number_story_points30, total_number_story_points31,	total_number_story_points32, total_number_story_points33, total_number_story_points34, total_number_story_points35,	total_number_story_points36, total_number_story_points37, total_number_story_points38, total_number_story_points39,	total_number_story_points40, total_number_story_points41, total_number_story_points42, total_number_story_points43,	total_number_story_points44, total_number_story_points45, total_number_story_points46, total_number_story_points47,	total_number_story_points48, total_number_story_points49, total_number_story_points50, total_number_story_points51,	total_number_story_points52, total_number_story_points53, total_number_story_points54, total_number_story_points55,	total_number_story_points56, total_number_story_points57, total_number_story_points58, total_number_story_points59,	total_number_story_points60],
        'defect density':[d_d1,d_d2,d_d3,d_d4, d_d5, d_d6, d_d7,d_d8, d_d9, d_d10, d_d11, d_d12, d_d13, d_d14, d_d15, d_d16, d_d17, d_d18, d_d19, d_d20, d_d21, d_d22, d_d23, d_d24, d_d25, d_d26, d_d27, d_d28, d_d29, d_d30, d_d31, d_d32, d_d33, d_d34, d_d35, d_d36, d_d37, d_d38, d_d39, d_d40, d_d41, d_d42, d_d43, d_d44, d_d45, d_d46, d_d47, d_d48, d_d49, d_d50, d_d51, d_d52, d_d53, d_d54, d_d55, d_d56, d_d57, d_d58, d_d59, d_d60 ]}
        cod = pd.DataFrame.from_dict(nnn)
        st.table(cod)


    #mail = st.selectbox('DATA',('Select','MAIL'))

    #if mail=="MAIL":
    #    Subject=st.text_input('Please input a subject')
    #    #user="chandraprakash2194@gmail.com"
    #    recipient=st.text_input('Please input the email of recipient')
    #    #pwd="aosgdrvqphryqbde"
    #    upload=st.file_uploader('Please upload',type='csv')
    #    #

    #    if upload is not None:
    #        data=pd.read_csv(upload)
    #        d_html=data.to_html()
    #        dfp=MIMEText(d_html,'html')
    #        msg=MIMEMultipart('alternative')
    #        msg['Subject']=Subject
    #        msg['From']=user
    #        msg['To']=recipient
    #        msg.attach(dfp)

    #    try:
    #        if st.button('Send'):
    #            server=smtplib.SMTP("smtp.gmail.com",587)

    #            server.starttls()
    #            server.login(user,pwd)
    #            server.sendmail(user,recipient,msg.as_string())
    #            server.close()
    #            st.success("Sending successful")
    #    except Exception as e:
    #       st.error("error:")

    else:
        st.markdown('No file uploaded')
        
        
