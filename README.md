# Introduction

This is an experiment to optimize CSS classes (for production -- you wouldn't use this in development) using linear programming.
This is inspired by the demo found on https://css-blocks.com (which surely uses heuristics).

This experiment failed miserably. There's simply to many constraints required to try to solve this problem with naive LP.
This is also some of the worst, hackiest code I've ever written.

Enjoy!

# Installation

This was a PITA to get working. I ended up just running it in an Ubuntu box because I couldn't figure out how to compile it on OS X.


```bash
sudo add-apt-repository -y ppa:george-edison55/cmake-3.x
sudo apt-get update
sudo apt-get install build-essential cmake python-dev python-pip

wget http://scip.zib.de/download/release/scipoptsuite-4.0.1.tgz
tar -xzf scipoptsuite-4.0.1.tgz
cd scipoptsuite-4.0.1

# Build SoPlex
cd soplex
mkdir build
cd build
cmake ..
make
cd ..

# Build SCIP
cd scip
mkdir build
cd build
cmake .. -DSOPLEX_DIR=/home/vagrant/scipoptsuite-4.0.1/soplex/build
make
make check # (Optional) Run a simple test to make sure everything installed correctly
sudo make install

# Install Python dependencies
cd /vagrant
sudo pip install Cython
sudo pip install pyscipopt

LD_LIBRARY_PATH=/usr/local/lib python optimize.py
```

Check sample_output.txt for an example session to see how the CSS would be optimized.
