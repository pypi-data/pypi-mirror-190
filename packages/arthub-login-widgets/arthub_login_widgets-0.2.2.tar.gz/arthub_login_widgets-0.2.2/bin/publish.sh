cd ../
pip install 'twine>=1.5.0'
rm -vr dist
python setup.py sdist bdist_wheel
twine upload dist/*