import numpy as np
import itertools
import math

from mrjob.job import MRJob
from itertools import combinations, permutations

from scipy.stats.stats import pearsonr


class RestaurantSimilarities(MRJob):

    def steps(self):
        "the steps in the map-reduce process"
        thesteps = [
            self.mr(mapper=self.line_mapper, reducer=self.users_items_collector),
            self.mr(mapper=self.pair_items_mapper, reducer=self.calc_sim_collector)
        ]
        return thesteps

    def line_mapper(self,_,line):
        "this is the complete implementation"
        user_id,business_id,stars,business_avg,user_avg=line.split(',')
        yield user_id, (business_id,stars,business_avg,user_avg)


    def users_items_collector(self, user_id, values):
        """
        #iterate over the list of tuples yielded in the previous mapper
        #and append them to an array of rating information
        """
        yield user_id, list(values)  #pass on user_id and values in a list


    def pair_items_mapper(self, user_id, values):
        """
        ignoring the user_id key, take all combinations of business pairs
        and yield as key the pair id, and as value the pair rating information
        """
	values_dict={}   #empty dictionary
		
        #goes over the list of values and assign business id as key and ratings as values to a dictionary
        for x in values:   
            values_dict[x[0]]=x[1:]
         
        #makes all possible combinations of business ids, puts them in dictionary where 
        #keys are pairs of business id and values are ratings for those pairs
        pair_dict=map(dict,itertools.combinations(values_dict.iteritems(),2))
        
        #loops over dictionary to remove duplicates, compares the pairs in keys and if it 
        #appears again in backward order, it will skip over it
        for i in pair_dict:
            if i.keys()[0]>i.keys()[1]:
            #yield passes on pairs and ratings as lists
                yield (i.keys()[0],i.keys()[1]), i.values()   
            else:
                yield (i.keys()[1],i.keys()[0]), i.values()                  
            

        

    def calc_sim_collector(self, key, values):
        """
        Pick up the information from the previous yield as shown. Compute
        the pearson correlation and yield the final information as in the
        last line here.
        """

        (rest1, rest2), common_ratings = key, values
	
        n_common=0   #sets the n_common to 0
        rest1_diff=np.array([])   #empty arrays
        rest2_diff=np.array([]) 
        for i in list(common_ratings):   #loops over the ratings of business ids
            rest1_stars=i[0][0]    #gets the rating for business1
            rest1_uavg=i[0][2]    #gets the user average for business1
            rest2_stars=i[1][0]  #gets the rating for business2
            rest2_uavg=i[1][2]    #gets the user average for business2
            
            #gets difference between actual rating and user average
            diff1=float(rest1_stars)-float(rest1_uavg)  
            diff2=float(rest2_stars)-float(rest2_uavg)

            #puts all the differences for diff values in an array
            rest1_diff=np.append(rest1_diff,diff1)
            rest2_diff=np.append(rest2_diff,diff2)
            
            n_common+=1  #calculates the n_common
     
        #calculates the similarity using pearson  
        rho=pearsonr(rest1_diff,rest2_diff)[0] 
        
        #if similarity is NaN then sets it to zero 
        if math.isnan(rho): rho = 0
        yield (rest1, rest2), (rho, n_common)  #outputs final results


#Below MUST be there for things to work
if __name__ == '__main__':
    RestaurantSimilarities.run()