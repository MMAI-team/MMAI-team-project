import csv
import random


def load_data(negative_samples=True, samples_per_whale=None, table_path='train.csv',
              images_directory='train', seed=None):
    """
        Load data for a whale identification task.

        Parameters:
        - negative_samples (bool): If True, include negative samples (pairs of images from different whales) in the data.
        - samples_per_whale (int or None): Number of positive samples to include for each whale. If None, include all possible
          positive samples. Default is None.
        - table_path (str): Path to the CSV file containing the mapping of image filenames to whale IDs. Default is 'train.csv'.
        - images_directory (str): Directory where the whale images are stored. Default is 'train'.
        - seed (int or None): Seed for random number generation to ensure reproducibility. If None, no seed is set. Default is None.

        Returns:
        - data (list): A list of tuples, each containing a pair of image file paths and a label (1 for positive, 0 for negative).
        """

    if seed is not None:
        random.seed(seed)

    if samples_per_whale is None:
        samples_per_whale = float('inf')
    # if type(samples_per_whale) != int:
    #     raise TypeError('Type of samples_per_whale should be int')
    elif samples_per_whale <= 0:
        raise ValueError('samples_per_whale should be greater then 0')

    ind_dict = {}
    whales_images = []
    with open(table_path) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        k = 0
        for row in reader:
            filename, whale_id = row
            if whale_id == 'new_whale':
                continue
            if ind_dict.get(whale_id) is None:
                ind_dict[whale_id] = k
                k += 1
                whales_images.append([])

            whales_images[ind_dict[whale_id]].append(filename)

    whale_count = len(whales_images) - 1

    positive_data = []
    negative_data = []

    for whale in whales_images:
        whale_added = 0
        for i, el in enumerate(whale):
            n = len(whale)
            if n == 1:
                continue
            if i < n - 1 and whale_added < samples_per_whale:
                positive_data.append(((f'{images_directory}/{el}', f'{images_directory}/{whale[i + 1]}'), 1))
                random_whale = random.randint(0, whale_count)
                if negative_samples:
                    negative_data.append(
                        ((f'{images_directory}/{el}', f'{images_directory}/{whales_images[random_whale][0]}'), 0))
                whale_added += 1

    data = positive_data + negative_data

    return data
