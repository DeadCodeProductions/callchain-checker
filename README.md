`ccc` is the callchain checker used in [DEAD](https://github.com/DeadCodeProductions/dead).


#### To build just the clang tool

Prerequisites: `cmake`, `make`, `clang/llvm` 13/14.

```
mkdir build
cd build
cmake .. 
cmake --build . [--parallel]
cmake --install . --prefix=/where/to/install/
```

#### Usage
```
cat test.c
int bar();
int foo(){
    return bar();
}

./build/bin/ccc test.c --from=foo --to=bar --
call chain exists between foo -> bar
```

#### Python wrapper

`pip install callchain-checker`


To use the checker in python import `from callchain_checker.callchain_checker import callchain_exists`: 
`callchain_exists(program: diopter.SourceProgram, source_function: str, target_function:str) -> bool`


#### Building the python wrapper

##### Local build

```
./build_python_wheel_local.sh #this will build the current branch
pip install .
```

#### Docker based build

```
docker run --rm -e REVISION=REV -v `pwd`:/io theodort/manylinux-with-llvm:latest /io/build_python_wheel_docker.sh
```

This will build multiple wheels for `REV` with multiple python versions.
The output is stored in the `wheelhouse` directory.
The docker image is based on https://github.com/thetheodor/manylinux-with-llvm.
