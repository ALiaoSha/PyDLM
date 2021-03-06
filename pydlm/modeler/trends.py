"""
=========================================================================

Code for the trend component

=========================================================================

This piece of code provide one building block for the dynamic linear model.
It decribes a latent polynomial trending in the time series data

"""
import numpy as np
from component import component
import pydlm.base.tools as tl

# create trend component
# We create the trend using the component class

class trend(component):
    """
    The trend component that features the polynomial trending. It implements
    an abstract component class and override all the abstractmethod.
    
    Members:
        d: the degree of the polynomial trend
        componentType: the type of the component, in this case, 'trend'
        name: the name of the trend component, to be supplied by user
              used in modeling and result extraction
        discount: the discount factor for this component. Details please refer
                  to the @kalmanFilter
        evaluation: the evaluation matrix for this component
        transition: the transition matrix for this component
        covPrior: the prior guess of the covariance matrix of the latent states
        meanPrior: the prior guess of the latent states
    
    Methods:
        createEvaluation: create the initial evaluation matrix
        createTransition: create the initial transition matrix
        createCovPrior: create a simple prior covariance matrix
        createMeanPrior: create a simple prior latent state
        checkDimensions: if user supplies their own covPrior and meanPrior, this can 
                         be used to check if the dimension matches

    Examples:
          # create a constant trend:
        > ctrend = trend(degree = 1, name = 'Const', discount = 0.99)
          # change the ctrend to have covariance with diagonals are 2 and state 1
        > ctrend.createCovPrior(cov = 2)
        > ctrend.createMeanPrior(mean = 1)
    
    """

    # class variable specify the component type
    componentType = 'trend'
    
    def __init__(self, degree = 1, discount = 0.99, name = 'trend'):
        if degree <= 0:
            raise NameError('degree has to be positive')
        self.d = degree
        self.name = name
        self.discount = np.ones(self.d) * discount
        
        # Initialize all basic quantities
        self.evaluation = None
        self.transition = None
        self.covPrior = None
        self.meanPrior = None

        # create all basic quantities
        self.createEvaluation()
        self.createTransition()
        self.createCovPrior()
        self.createMeanPrior()

    def createEvaluation(self):
        self.evaluation = np.matrix(np.zeros((1, self.d)))
        self.evaluation[0, 0] = 1

    def createTransition(self):
        """
        According Hurrison and West (1999), the transition matrix of trend takes
        a form of 

        [1 1 1 1]
        [0 1 1 1]
        [0 0 1 1]
        [0 0 0 1]

        """
        self.transition = np.matrix(np.zeros((self.d, self.d)))
        self.transition[np.triu_indices(self.d)] = 1
        
    def createCovPrior(self, cov = 1):
        self.covPrior = np.matrix(np.eye(self.d)) * cov

    def createMeanPrior(self, mean = 0):
        self.meanPrior = np.matrix(np.ones((self.d, 1))) * mean

    def checkDimensions(self):
        tl.checker.checkVectorDimension(self.meanPrior, self.covPrior)
        print 'The dimesnion looks good!'
