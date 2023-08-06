cd ../
pip install 'twine>=1.5.0'
rmdir /S /Q dist
python setup.py sdist bdist_wheel
twine upload dist/*