all:

clean:
	rm -rf htmlcov
	find . -iname __pycache__ -o -iname '*.pyc' | xargs rm -rf
	rm -f .coverage
	rm -rf *.egg-info build dist

# sudo apt install python3-wheel twine
publish: build
	twine upload dist/*

build: clean
	python3 setup.py sdist bdist_wheel

veryclean: clean
	rm -rf pyenv

pull-protocols:
	git subtree pull -P syndicate/protocols \
		-m 'Merge latest changes from the syndicate-protocols repository' \
		git@git.syndicate-lang.org:syndicate-lang/syndicate-protocols \
		main

chat.bin: chat.prs
	preserves-schemac .:chat.prs > $@
