VERSION := $(shell grep version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

.PHONY: style
style:
	pylama --ignore=E501,E301,E302,E265,E266 z2/*.py | less -XR

.PHONY: pypi
pypi:
	make clean
	poetry build
	poetry publish -vvv

.PHONY: repo-push
repo-push:
	-git remote remove origin
	git remote add origin "git@github.com:mpenning/z2"
	git push git@github.com:mpenning/z2.git
	git push origin +main

.PHONY: repo-push-tag
repo-push-tag:
	-git remote remove origin
	git remote add origin "git@github.com:mpenning/z2"
	git tag -a ${VERSION} -m "Tag with ${VERSION}"
	git push --tags git@github.com:mpenning/z2.git
	git push --tags origin +main
	git push --tags origin ${VERSION}

.PHONY: repo-push-force
repo-push-force:
	-git remote remove origin
	git remote add origin "git@github.com:mpenning/z2"
	git push --force-with-lease git@github.com:mpenning/z2.git
	git push --force-with-lease origin +main

.PHONY: repo-push-tag-force
repo-push-tag-force:
	-git remote remove origin
	git remote add origin "git@github.com:mpenning/z2"
	git tag -a ${VERSION} -m "Tag with ${VERSION}"
	git push git@github.com:mpenning/z2.git
	git push --force-with-lease origin +main
	git push --force-with-lease --tags origin ${VERSION}

.PHONY: test
test:
	# Run the doc tests and unit tests
	cd tests; ./runtests.sh

.PHONY: clean
clean:
	find ./* -name '*.pyc' -exec rm {} \;
	find ./* -name '*.so' -exec rm {} \;
	find ./* -name '*.coverage' -exec rm {} \;
	@# A minus sign prefixing the line means it ignores the return value
	-find ./* -path '*__pycache__' -exec rm -rf {} \;
	-rm -rf .pytest_cache/
	-rm -rf .eggs/
	-rm -rf .cache/
	-rm -rf build/ dist/ z2.egg-info/ setuptools*
