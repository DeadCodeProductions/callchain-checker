#!/usr/bin/env bash
set -e -x

dnf install boost-devel -y


cd /root
git clone https://github.com/DeadCodeProductions/callchain-checker.git
cd callchain-checker
git checkout "$REVISION"
mkdir build
cd build
cmake -G Ninja .. -DCMAKE_BUILD_TYPE=Release \
                  -DCMAKE_CXX_FLAGS="-static-libgcc -static-libstdc++ -fPIC" \
                  -DCMAKE_EXE_LINKER_FLAGS="-static-libgcc -static-libstdc++" \
                  -DCMAKE_SHARED_LINKER_FLAGS="-static-libgcc -static-libstdc++"
ninja 
cd ..
cp build/bin/ccc python_src/callchain_checker
cp setup.py.in setup.py
sed -i "s~THIS_DIR~$(pwd)~g" setup.py

"/opt/python/cp310-cp310/bin/python" -m build -w -o wheelhouse
"/opt/python/cp311-cp311/bin/python" -m build -w -o wheelhouse


function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" -w /io/wheelhouse/
    fi
}


for whl in wheelhouse/*.whl; do
    repair_wheel "$whl"
done

rm setup.py
