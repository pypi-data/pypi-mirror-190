python3.8 setup.py sdist bdist_wheel
twine upload dist/*
rm -r ./build ./dist ./*.egg-info
