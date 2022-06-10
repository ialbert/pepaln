
all:
	echo "make test devel upload"

test:
	python -m pepaln -m data/fragments.txt -r data/sequence.fa
	cat output.txt

push:
	git commit -am 'update'
	git push

devel:
	python setup.py develop

upload:
	rm -rf dist
	python setup.py sdist bdist_wheel
	#python -m twine upload --repository testpypi dist/*
	python -m twine upload --repository pypi dist/*




