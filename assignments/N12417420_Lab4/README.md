## Artificial Intelligence
### CSCI-GA.2560
#### [Lab 4](https://cs.nyu.edu/courses/fall21/CSCI-GA.2560-001/lab4.html)

### Algorithms:

- **K Nearest Neighbors:** The KNN classifier with options to customize distance measurements and voting weights
- **K Means Clustering:** The unsuperviced K Means clustering algorithm with options to customize distance measurements

### Python coding style

The assignment is written in python3 and alligns with the
[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)

The `.pylintrc` file has been referenced directly from the [Tensorflow project](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/ci_build/pylintrc), with
a slight modification w.r.t `max-line-length`. To install `pylint` and check all files with `pylint` against TensorFlow's custom style definition:

```bash
pip3 install pylint
pylint --rcfile=./.pylintrc ./*.py
```

### Running the code

The code is written in `python3` can be executed using the `python>=3.6` interpreters.

#### Help with executions

##### K Nearest Neighbors Classifier

```console
usage: knn.py [-h] [-v] [-k K] [-d D] [-unitw UNITW] -train TRAIN -test TEST

K Nearest Neighbor Classifier

optional arguments:
  -h, --help    show this help message and exit
  -v            Enable verbosity for program runs
  -k K          Number of nearest neighbors needed to determine the class. Defaults to 3.
  -d D          distance function to determine the closeness of neighbors. Should be one of 'e2': euclidean squared, 'manh': manhattan. Defaults to 'e2'.
  -unitw UNITW  Whether to use unit voring weights or not. If not, we use 1/d as the voting strength of each neighbor. Defaults to False.
  -train TRAIN  Path to the training data file
  -test TEST    Path to the testing data file

Choose the nearest K neighbors
```

##### K Means Clustering

```console
usage: kmeans.py [-h] [-v] [-d D] -data DATA centroids [centroids ...]

K Means Classifier

positional arguments:
  centroids   Path to the testing data file

optional arguments:
  -h, --help  show this help message and exit
  -v          Enable verbosity for program runs
  -d D        distance function to determine the closeness of points. Should be one of 'e2': euclidean squared, 'manh': manhattan. Defaults to 'e2'.
  -data DATA  Path to the clustering data file

Choose the best centroid!
```

#### Executing the programs

The learning algorithms can be used as follows:

#TODO
```console

```