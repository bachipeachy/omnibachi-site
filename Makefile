.PHONY: ingest preview build clean serve-drafts

# Pull canonical markdown from pgs_workspace into content/ + static/
ingest:
	python3 scripts/ingest.py --config ingest.config.yaml

# Local preview at http://localhost:1313
preview:
	hugo server -D --disableFastRender

# Production build into public/
build:
	hugo --minify

# Remove generated output
clean:
	rm -rf public resources/_gen