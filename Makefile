# Developer setup installs homebrew packages needed to develop.
.PHONY: setup
setup:
	brew update
	brew bundle install
	git lfs pull origin main
	poetry update && poetry install
	poetry run pre-commit install
	poetry run python -m spacy download en_core_web_sm


.PHONY: develop
ccda-dev:
	poetry install && poetry shell



.PHONY: notebook
notebook:
	poetry run jupyter notebook



.PHONY: checks 
checks:
	poetry run pre-commit run --all-files
	poetry run mypy .
	cd translator && poetry run pytest --cov=. tests
	cd ..