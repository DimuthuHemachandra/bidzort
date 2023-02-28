import pandas as pd
import os
import shutil

bids_dir = '/home/dimuthu1/projects/ctb-akhanf/ext-bids/ppmi/ppmi-bids-smk/bids_workflow/subj_bids/PPMI_CTRL_DTI_MRI_3T'

def do_ls(current_dir, kind):
    if kind == 'None':
        return [dir for dir in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, dir))]
    else:
        return [dir for dir in os.listdir(current_dir) if kind in dir]


def get_summary(df):

	unique_sessions = df['session'].unique()
	
	ses_dict_list=[]
	
	ses_df_list=[]

	for ses in unique_sessions:
	
		summary_dict={'session': ses}
		ses_df = df[df['session']==ses]
		

		#get t1 sum
		if 'yes' in ses_df['t1'].values:
			counts = ses_df['t1'].value_counts()
			summary_dict['Total T1s'] = counts['yes']
		else:
			summary_dict['Total T1s'] = 0 
			
		#get t2 sum
		if 'yes' in ses_df['t2'].values:
			counts = ses_df['t2'].value_counts()
			summary_dict['Total T2s'] = counts['yes']
		else:
			summary_dict['Total T2s'] = 0

		#get dwi sum
		if 'yes' in ses_df['dwi'].values:
			counts = ses_df['dwi'].value_counts()
			summary_dict['Total dwis'] = counts['yes']
		else:
			summary_dict['Total dwis'] = 0
			
		#get func sum
		if 'yes' in ses_df['func'].values:
			counts = ses_df['func'].value_counts()
			summary_dict['Total funcs'] = counts['yes']
		else:
			summary_dict['Total funcs'] = 0

		#get func sum
		t1_dwi_df = ses_df[(ses_df['t1']=='yes') & (ses_df['dwi']=='yes')]
		t1_dwi_count = t1_dwi_df ['ID'].unique()
		summary_dict['Total T1 and DWI'] = len(t1_dwi_count)
		summary_dict['subjects that have T1 and DWI'] = t1_dwi_count


		ses_dict_list.append(summary_dict)
		ses_df_list.append(ses_df)
		
		
	#print(ses_dict_list)
	session_df = pd.DataFrame(ses_dict_list)
	session_df.to_csv('sorted_bids_session_data.csv', sep=',', index=False)
	
		
    



directories = do_ls(bids_dir, 'sub')

dict_list = []
for i, subj in enumerate(directories):
    content = do_ls(bids_dir + '/' + subj, 'None')
    session = any('ses' in item for item in content)
    
    if session:
        for ses in content:
            mods = do_ls(bids_dir + '/' + subj + '/' + ses, 'None')
            sub_dict = {'Number': i, 'ID': subj, 'session': ses}
            t1_count = 0
            t2_count = 0
            dwi_count = 0
            func_count = 0
            
            for mod in mods:
                if mod == 'anat':
                    T1 = do_ls(bids_dir + '/' + subj + '/' + ses + '/' + mod, 'T1w.nii')
                    t1_count = len(T1)
                    sub_dict['t1'] = 'yes'
                    sub_dict['t1_runs'] = t1_count
                    
                    T2 = do_ls(bids_dir + '/' + subj + '/' + ses + '/' + mod, 'T2w.nii')
                    t2_count = len(T2)
                    sub_dict['t2'] = 'yes'
                    sub_dict['t2_runs'] = t2_count
                    
                elif mod == 'dwi':
                    dwi = do_ls(bids_dir + '/' + subj + '/' + ses + '/' + mod, 'dwi.nii')
                    dwi_count = len(dwi)
                    sub_dict['dwi'] = 'yes'
                    sub_dict['dwi_runs'] = dwi_count	
            
                elif mod == 'func':
                    func = do_ls(bids_dir + '/' + subj + '/' + ses + '/' + mod, 'bold.nii')
                    func_count = len(func)
                    sub_dict['func'] = 'yes'
                    sub_dict['func_runs'] = func_count	
            
            if t1_count == 0:
                sub_dict['t1'] = 'No'
                sub_dict['t1_runs'] = 'None'

            if t2_count == 0:
                sub_dict['t2'] = 'No'
                sub_dict['t2_runs'] = 'None'
        
            if dwi_count == 0:
                sub_dict['dwi'] = 'No'
                sub_dict['dwi_runs'] = 'None'

            if func_count == 0:
                sub_dict['func'] = 'No'
                sub_dict['func_runs'] = 'None'
                    
            #print(sub_dict)
            dict_list.append(sub_dict)
        
    else:
        sub_dict['session'] = None
        mods = do_ls(bids_dir + '/' + subj + '/' + content)
        
df = pd.DataFrame(dict_list)
df.to_csv('sorted_bids_data.csv', sep=',', index=False)

get_summary(df)



