PYTHON ?= python
export PROJECT_ROOT := $(CURDIR)

all: simulate analyse

simulate:
	$(PYTHON) -m simulations.cli

analyse:
	Rscript analysis/performance.R
	Rscript analysis/exam_scores.R

test:
	$(PYTHON) -m pytest tests/

clean:
	rm -rf docs results build *.egg-info
	find . -name __pycache__ -type d -exec rm -rf {} +

.PHONY: all simulate analyse test clean
