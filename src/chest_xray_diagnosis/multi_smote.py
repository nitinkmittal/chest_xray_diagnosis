"""
Multi label Synthetic Minority Oversampling Technique Approach
@author Theodoros Psallidas
TODO: Maybe i have to run the oversampling technique for all the feature space.
"""
import random
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from .utils import get_classes, get_sum_classes




class MultiSmote():
    """
    Multi Smote, is an extension of the Synthetic Minority Over Sampling Technique that
    supports multi label data. It get the samples of the minority class, sample that belongs
    in only one class are considered in order to generate data without affecting the other classes
    at the data augmentation process keeping the number of samples fixed.
    """

    def __init__(self):
        """
        Initializing multi smote algorithm
        """
        self.neighbors = 5
        self.class_bins = []  # contains the sum of the class instances

    @property
    def get_majority_index(self) -> int:
        """
        Get the index of the majority class
        Returns:
            int: The index of the majority class
        """
        return np.argmax(self.class_bins)

    @property
    def get_minority_index(self) -> int:
        """
        Get the index of the minority class
        Returns:
            int: The index of the minrity class
        """

        return np.argmin(self.class_bins)

    def get_majority_class(self) -> int:
        """
        Get the number of samples from the majority class
        Returns:
            int: The number of samples
        """

        return np.max(self.class_bins)

    @property
    def get_minority_class(self) -> int:
        """
        Get the number of samples from the minority class
        Returns:
            int: The number of samples
        """

        return np.min(self.class_bins)

    def get_minority_samples(self, x, y) -> tuple:
        """
        Get the samples and labels from the minority class
        Args:
            x : The Data
            y : The Labels
        Returns:
            tuple: [The minority's class samples, The minority class labels]
        """

        assert x.shape[0] == y.shape[0], "Samples and labels has not the same length"
        assert type(x) == type(y), "Data types of X and y does not match"

        index = int(self.get_minority_index)  # index of the minority class

        if isinstance(x, pd.DataFrame):
            #Dataframe support
            x_sub = []
            y_sub = []
            for row in range(x.shape[0]):
                if y.iloc[row].sum() == 1 and y.iloc[row, index] == 1:
                    x_sub.append(x.iloc[row])
                    y_sub.append(y.iloc[row])
            return pd.DataFrame(data=x_sub, index=None), pd.DataFrame(data=y_sub, index=None)

        #Numpy support
        x_sub = []
        y_sub = []
        for row in range(x.shape[0]):
            if y[row].sum() == 1 and y[row][index] == 1:
                x_sub.append(x[row])
                y_sub.append(y[row])
        return np.array(x_sub), np.array(y_sub)

    def nearest_neighbour(self, x) -> list:
        """
        Calculate the nearest Neighbors for the data
        Args:
            x : The samples from the minority class
        Returns:
            list: List of the nearest neighbors
        """

        nbs = NearestNeighbors(n_neighbors=self.neighbors,
                               metric='euclidean',
                               algorithm='kd_tree').fit(x)
        _, indices = nbs.kneighbors(x)
        return indices

    def resample(self, x, y):
        """
        The function that produces synthetic data from
         the representative samples of the minority class
        Args:
            x : Samples
            y : Labels
        Returns:
            list: [synthetic samples, synthetic's labels]
        """
        self.class_bins = get_sum_classes(y)  # Update the class bins.
        x_sub, y_sub = self.get_minority_samples(x, y)  # Get the minority samples
        if self.neighbors > len(x_sub) > 1:
            print('Number of Minority samples are less than the number of nearest neighbors,'
                  ' trying to resolve the conflict by decreasing the number of the neighbors')
            print("New k={0}".format(len(x_sub)))
            self.neighbors = len(x_sub)

        if len(x_sub) <= 1:
            print('The number of the unique samples from the minority class is small,'
                  ' cannot find neighbors for this minority class.\n'
                  'Aborting for class {}'.format(self.get_minority_index))
            return None, None

        indices = self.nearest_neighbour(x_sub)

        # num_samples: the number of synthetic samples
        num_samples = int(self.get_majority_class() - self.get_minority_class)

        gen_x = []  # Generated sampled
        gen_y = []  # labels for generated samples

        for _ in range(num_samples):
            n_n = random.randint(0, len(x_sub) - 1)
            # Random number from the neighbor's matrix
            neighbour = random.choice(indices[n_n, 1:])
            # A random neighbor from the neighbour's matrix.
            ratio = random.random()
            if isinstance(x_sub, pd.DataFrame):
                #pandas support
                gap = x_sub.iloc[n_n, :] - x_sub.iloc[neighbour, :]
                generated = np.array(x_sub.iloc[n_n, :] + ratio * gap)
                gen_x.append(generated)
                gen_y.append(y_sub.iloc[0])

            elif isinstance(y_sub, np.ndarray):
                #numpy support
                gap = x_sub[n_n, :] - x_sub[neighbour, :]
                generated = np.array(x_sub[n_n, :] + ratio * gap)
                gen_x.append(generated)
                gen_y.append(y_sub[0])

        if isinstance(x_sub, pd.DataFrame):
            return pd.DataFrame(data=gen_x, index=None), pd.DataFrame(data=gen_y, index=None)

        return np.array(gen_x), np.array(gen_y)

    def multi_smote(self, x, y) -> tuple:
        """
        The main function of multi label smote. The function resample
        data for all the classes of the data.
        The returned data will be balanced, only if the representative
        data of each class is greater than one instance.
        Args:
            x : Data
            y : Labels
        Returns:
            list: [Resampled Data, Resampled Labels]
        """
        if not isinstance(x, pd.DataFrame) and not isinstance(x, np.ndarray):
            print("Not supported type of the data.\n"
                  " Aborting")
            return None, None

        classes = get_classes(y)  # number of classes

        for _ in range(classes - 1):  # minus one, we exclude the majority class.
            x_new, y_new = self.resample(x, y)

            if x_new is not None and y_new is not None:
                if isinstance(x, pd.DataFrame):
                    #pandas support
                    x = pd.concat([x, x_new], axis=0)
                    y = pd.concat([y, y_new], axis=0)

                elif isinstance(y, np.ndarray):
                    #numpy support
                    x = np.concatenate((x, x_new))
                    y = np.concatenate((y, y_new))
        del x_new, y_new, classes
        return x, y

    def __str__(self):
        """
        str Method in order to change the printed message of the multilabel smote object
        Returns:
            message object.
        """
        return "Multi Label Smote Object. Default k is {0}".format(self.neighbors)