from learningmap_hardcoding import *
import matplotlib.patches as mpatches



# Collection of objects for the learning map.

##########
#
# KSA object.  Store all the necessary information.
#
##########

class KSA:

    def __init__(self, idn, name, description):
        # ID Number
        self.id = idn 

        # KSA name
        self.name = name

        # Description
        self.description = description
        
        # Strata number
        self.strata = -1

        # Grade level
        self.gradelevel = -1
        
        # Things this KSA Depends on
        self.depend_on_list=[]

        #Things this KSA is a Dependant of
        self.dependant_of=[]

        # The design pattern this is associated with
        self.dp = -1
        self.dptitle = -1
        self.pattern_id = -1

        # The Domain this is associated with
        self.domain = -1
        self.domain_name = ''

        # Apparently, there's a subdomain.
        self.subdomain = -1
        self.subdomain_name = ''

        # The position on a unit square grid
        self.x = -1
        self.y = -1


##########
#
# This manages all of the sub domain links, and the 
# design pattern links as well.
#
##########

class SubdomainLinkManager:

    # set up the dicts...
    def __init__(self, list_of_subdomains, list_of_patternids, list_of_gradelevels):

        self.sd_d = {}
        self.pattern_d = {}
        self.subdomain_gradelevel_patternlist={}

        self.patternlist = list_of_patternids
        self.gradelevels = list_of_gradelevels

        for isd in list_of_subdomains:
            self.subdomain_gradelevel_patternlist[isd]={}

            self.sd_d[isd]={}
            for jsd in list_of_subdomains:
                self.sd_d[isd][jsd]=0
        #
        for i, ipattern in enumerate(list_of_patternids):
            
            self.add_sd_gradelevel(get_subdomain(ipattern),list_of_gradelevels[i],ipattern)
            self.pattern_d[ipattern]={}
            for jpattern in list_of_patternids:
                self.pattern_d[ipattern][jpattern]=0
        

    # add a design pattern with the associated subdomain, grade level
    def add_sd_gradelevel(self, sd,gl,patternid):
        if gl not in self.subdomain_gradelevel_patternlist[sd].keys():
            self.subdomain_gradelevel_patternlist[sd][gl]=[]
        self.subdomain_gradelevel_patternlist[sd][gl].append(patternid)

    # Return the grade level given a pattern
    def get_gradelevel(self, pattern):
        if pattern in self.patternlist:
            return self.gradelevels[self.patternlist.index(pattern)]

        
    # add a link
    def add_link(self, isd, jsd, ipattern, jpattern):
        self.sd_d[isd][jsd]+=1
        self.sd_d[jsd][isd]+=1
        self.pattern_d[ipattern][jpattern]+=1
        self.pattern_d[jpattern][ipattern]+=1
        

    # get number of links given the patterns
    def get_pattern_link(self,  ipattern, jpattern):
        return self.pattern_d[ipattern][jpattern]


    # get the number of links given the subdomains
    def get_sd_links(self, isd, jsd):
        return self.sd_d[isd][jsd]
    
    
    # Calculate the "Diagonal-ness figure of merit".
    # in this case, we're organizing the columns of
    # the interaction matrix such that we maximize
    # the correlation coeff.  I think that's right.  
    
    def calc_link_fom(self, sd_order):
        c = (len(sd_order)*1.)/2.
        total = 0
        denom = 0
        for i, isd in enumerate(sd_order):
            
            for j, jsd in enumerate(sd_order):
                denom += self.sd_d[isd][jsd]*(i-c)*(i-c)
                total+=self.sd_d[isd][jsd]*(i-c)*(j-c)

        
        return (total*1.)/(denom*1.)

##########
#
##########
