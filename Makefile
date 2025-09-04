# Makefile to automate some tools
SHELL=/bin/bash
PATH := $(shell python -c "import sysconfig; print(sysconfig.get_path('scripts'))"):$(PATH)

PY_PLATFORM := $(shell python -c "import sysconfig; print(sysconfig.get_platform())")
PRE_COMMIT_OPTIONS := --show-diff-on-failure --color=always --all-files --hook-stage=manual

COV_TMPDIR := $(shell mktemp -d)

.PHONY: all
all: install

.PHONY: pre-commit
pre-commit: install
	@(pre-commit run $(PRE_COMMIT_OPTIONS) || true) | more
	@pre-commit gc

.PHONY: clean
clean:
	@rm -f .coverage* || true
	@rm -rf build dist wheelhouse

.PHONY: install
install:
	./ci/install-tools.sh --dev
	if ! [ -f .git/hooks/pre-commit ]; then\
		pre-commit install --install-hooks --overwrite -t pre-commit;\
	fi

.PHONY: uninstall
uninstall:
	@if [ -f .git/hooks/pre-commit ]; then\
		pre-commit clean;\
		pre-commit uninstall;\
		rm -f .git/hooks/pre-commit;\
	fi

.PHONY: upgrade
upgrade: uninstall clean install
	pre-commit autoupdate
	$(MAKE) pre-commit

.PHONY: tests
tests:
	./ci/install-tools.sh --tests
	./ci/build-wheel.sh
	cp pyproject.toml $(COV_TMPDIR)/
	cp -a tests/ $(COV_TMPDIR)/
	cd $(COV_TMPDIR) && pytest -nauto -v || true

.PHONY: cov
cov:
	./ci/install-tools.sh --tests
	./ci/build-wheel.sh
	@rm -rf build/coverage_html_report
	cp pyproject.toml $(COV_TMPDIR)/
	cp -a tests/ $(COV_TMPDIR)/
	cd $(COV_TMPDIR) && coverage run || true
	coverage combine --keep --quiet -a $(COV_TMPDIR)/
	coverage report
	coverage html

.PHONY: release
release:
	bump-my-version show-bump 2>/dev/null
	@echo "Run:"
	@echo "  bump-my-version bump <option>"
	@echo "--or--"
	@echo "  bump-my-version bump patch --new-version=X.XX.X"
	@echo "--then--"
	@echo "  git push origin `git branch --show-current` --tags"

.PHONY: release-dev
release-dev:
	if (grep "current_version" pyproject.toml | grep -q "\-dev"); then\
		bump-my-version bump --allow-dirty --no-tag build;\
	else\
		bump-my-version bump --allow-dirty --no-tag minor;\
	fi
	git log -1
