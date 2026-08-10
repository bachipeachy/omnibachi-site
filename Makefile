.PHONY: preview build clean

# Local preview at http://localhost:1313 (includes drafts)
preview:
	hugo server -D --disableFastRender

# Production build into public/
build:
	hugo --minify

# Remove generated output
clean:
	rm -rf public resources/_gen