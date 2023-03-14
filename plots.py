import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns 
import os 
import json 

'''




'''
path_to_results = 'C:/source/Results-for-paper'


    

class loader():
    
    def __init__(self, path_to_results):
        '''
        the init will set up all the items that are needed for the loading 


        '''

        self.results_base_path = path_to_results
        self.list_of_envs = [

            'Foraging-10x10-3p-3f',
            'Foraging-2s-10x10-3p-3f',
            'Foraging-8x8-2p-2f-coop',
            'Foraging-2s-8x8-2p-2f-coop'
            ]
        
        self.reward_type = [
            'LBF',
            'CLBF'
        ]
        self.step_number = [

            '25step',
            '50step'
            ]

        self.list_of_algs = [
            'ia2c'
            ]   
        
        
        self.dataframes = {

        }
        
        # long format lists: 
        self.data_steps = []
        self.data_values = []
        self.alg_values = []
        self.episode_length = []
        self.reward_types = []
        
    def load_files(self):
        # for each of the algorithms i will have to build the env type: 
        env_type = self.list_of_algs[0]+ '_LBF_' + self.step_number[0]
        
        # self.mystring = '/'.join([self.results_base_path,self.list_of_algs[0],self.reward_type[0], env_type,self.list_of_envs[0]]) + '/'

        # self.create_lists(self.mystring)
        
        for alg in self.list_of_algs:
            for step_number in self.step_number:
                for reward in self.reward_type:
                    env_type = '_'.join([alg,reward,step_number])
                    # print(env_type)
                    for env in self.list_of_envs:
                        path_string = '/'.join([self.results_base_path,alg, reward,env_type,env]) + '/'
                        # print(path_string)
                        self.create_lists(path_string,step_number,alg, reward)

        print(len(self.data_values))
        print(len(self.data_steps))
        print(len(self.alg_values))
        print(len(self.episode_length))
        print(len(self.reward_types))

        


        # this should be out in the main function 
        # print('starting the plotting process')
        # DF = pd.DataFrame(data_dict)
        
        
        # self.plotter = plotter(DF)
        # self.plotter.plot_lineplot("steps","values","run", show=True)
       
    
    def create_lists(self,terminal_directory_path, episode_length, algorithm, reward_type):
        data_steps = []
        data_values = []
        alg_values = []
        

        for dir in os.listdir(terminal_directory_path):
            # add the run number to the string & metrics 
            metrics_path = terminal_directory_path + dir + '/' + 'metrics.json'
            # print(episode_length, algorithm, reward_type)
            # print(metrics_path)

            with open(metrics_path) as f: 
                # load the data 
                loaded_dict = json.load(f)
                # create the new indes
                new_index = range(len(loaded_dict['return_mean']['steps']))
                # create categorical values 
                algorithm_name = [algorithm]*len(loaded_dict['return_mean']['steps'])
                episode_length = [episode_length]*len(loaded_dict['return_mean']['steps'])
                reward_ = [reward_type]* len(loaded_dict['return_mean']['steps'])
                # print(len(reward_))
                # extend the existing lists with the new information 
                self.data_values.extend(loaded_dict['return_mean']['values'])
                self.data_steps.extend(new_index)
                self.alg_values.extend(algorithm_name)
                self.episode_length.extend(episode_length)
                self.reward_types.extend(reward_)
                
            
    

    




        
        

class plotter():
    '''
    The plotter is expecting a long format dataframe of all the data, 
    '''
    def __init__(self, data):
        '''
        
        '''
        self.data_for_plotting = data
    
    def plot_lineplot(self, x, y, hue, show = False ):
        '''
        This function uses seaborn to plot a lineplot that is given too it. 
        '''
        print("Starting the plotting")
        sns.lineplot(data= self.data_for_plotting, x=x, y=y, hue=hue)

        if show: 
            plt.show()
    
    





def _main():
    lder = loader(path_to_results)
    lder.load_files()

    datadict={
        'steps':lder.data_steps,
        'values':lder.data_values,
        'reward' : lder.reward_types,
        'algorithm': lder.alg_values,
        'episode length' : lder.episode_length
    }
    print(datadict.keys())
    data_frame = pd.DataFrame(data=datadict)
    print('data frame loaded')
    plotr = plotter(data_frame)
    plotr.plot_lineplot('steps','reward', 'episode length', show=True)

if __name__ == "__main__":
    _main()
