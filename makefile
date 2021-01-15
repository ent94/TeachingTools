MODULENAME = TeachingTools

help:
	@echo ""
	@echo "Welcome to TeachingTools!!!"
	@echo "To get started create an environment using:"
	@echo "	make init"
	@echo "	conda activate ./envs"
	@echo ""
	@echo "To generate project documentation use:"
	@echo "	make docs"
	@echo "	source readtoind.sh"
	@echo ""
	@echo "To Lint the project use:"
	@echo "	make lint"
	@echo ""
	@echo "To run pydocstyle on the project use:"
	@echo "	make doclint"
	@echo ""
	@echo "To run unit tests use:"
	@echo "	make test"
	@echo ""
	

init:
	conda env create --prefix ./envs --file environment.yml

docs:
	bash ./readtoind.sh        	

lint:
	pylint $(MODULENAME)

doclint:
	pydocstyle $(MODULENAME)

test:
	pytest -v $(MODULENAME)

.PHONY: init docs lint test 
