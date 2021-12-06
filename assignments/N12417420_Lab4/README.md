## Artificial Intelligence
### CSCI-GA.2560
#### [Lab 4](https://cs.nyu.edu/courses/fall21/CSCI-GA.2560-001/lab4.html)

### Algorithms:

- **K Nearest Neighbors:** The KNN classifier with options to customize distance measurements and voting weights.
- **K Means Clustering:** The unsupervised K Means clustering algorithm with options to customize distance measurements.

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
**NOTE: The code depends on the pandas and numpy python packages.**

The packages are present on the CIMS machines.

```console
$ pip3 list | grep pandas
pandas                             1.0.1
$ pip3 list | grep numpy
numpy                            1.19.5
```

However, they can be installed using:
```
$ pip3 install numpy pandas
```
Please make sure that the `pip3` corresponds to the `python3` that we use for executing the programs.

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
  -unitw UNITW  Whether to use unit voting weights or not. If not, we use 1/d as the voting strength of each neighbor. Defaults to False.
  -train TRAIN  Path to the training data file
  -test TEST    Path to the testing data file

Choose the nearest K neighbors
```

##### K Means Clustering

```console
usage: kmeans.py [-h] [-v] [-d D] -data DATA centroids [centroids ...]

K Means Classifier

positional arguments:
  centroids   Initial centroids for clustering.

optional arguments:
  -h, --help  show this help message and exit
  -v          Enable verbosity for program runs
  -d D        distance function to determine the closeness of points. Should be one of 'e2': euclidean squared, 'manh': manhattan. Defaults to 'e2'.
  -data DATA  A file containing the data to cluster.

Choose the best centroid!
```

#### Executing the programs

The learning algorithms can be used as follows:

```console
# Run the knn classifier with d='e2', voting=1/d and k=3 (default)
python3 knn.py -d e2 -train ../tests/train.txt -test ../tests/test.txt

# Run the knn classifier with d='manh', voting=unit and k=5
python3 knn.py -k 5 -unitw True -d manh -train ../tests/train.txt -test ../tests/test.txt

# Run the kmeans clustering algorithm with d='manh' and 3 centroids
python3 kmeans.py -d manh -data ../tests/data1.txt 0,0 200,200 500,500

# Run the kmeans clustering algorithm with d='e2' and 3 centroids
python3 kmeans.py -d e2 -data ../tests/data2.txt 0,0,0 200,200,200 500,500,500
```

**NOTE: The file paths given in the examples above are just for reference and have to be modified w.r.t proper test file paths**