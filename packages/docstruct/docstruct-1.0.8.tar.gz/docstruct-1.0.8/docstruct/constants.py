"""Constants for the docstruct package."""
PAGE_DELIMITER = "\f"
PARAGRAPH_DELIMITER = "\v"
LINE_DELIMITER = "\n"
WORD_DELIMITER = " "
PAGE = "PAGE"
LINE = "LINE"
WORD = "WORD"
BBOX_PATTERN = "\s*bbox\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)"

# The factor of which we'll multiply the paragraph bounding box when looking for intersections with other paragraphs.
PARAGRAPH_VERTICAL_SCALE = 1.3
PARAGRAPH_HORIZONTAL_SCALE = 1
