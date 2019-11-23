from flask import Flask, jsonify, request
from gen_indices import gen_indices

API_ENDPOINT = 'api'
PARAGRAPH_DELIMITER = '\n\n'
WORD_DELIMITER = ' '

app = Flask(__name__)		# Start flask app

paragraphs = []		# Paragraphs list
reverseIndices = {}		# Reverse indices for the paragraphs
indexed = set()		# Set of indexed paragraphs 

@app.route(f'/{API_ENDPOINT}/get')
def get_paragraphs():
	"""Return all paragraphs."""
	return jsonify(paragraphs)

@app.route(f'/{API_ENDPOINT}/add', methods=['POST'])
def add_paragraphs():
	"""Add paragraphs to memory and return all paragraphs."""
	newParagraphs = request.get_json(force=True)['data']
	newParagraphs = newParagraphs.split(PARAGRAPH_DELIMITER)
	# Remove empty paragraphs
	newParagraphs = list(filter(None, newParagraphs))
	# Split by delimiter and add to list
	paragraphs.extend(newParagraphs)
	return jsonify(paragraphs)

@app.route(f'/{API_ENDPOINT}/index')
def index_paragraph():
	"""Index a given paragraph from given id otherwise index all and return generated indices."""
	id = request.args.get('id')
	if id is None:
		# Index all paragraphs
		for id, paragraph in enumerate(paragraphs):
			# Verify if not already indexed
			if id not in indexed:
				gen_indices(reverseIndices, id, paragraph, WORD_DELIMITER)
				indexed.add(id)
	else:
		try:
			# Convert id to integer
			id = int(id)
		except ValueError:
			# Invalid id given
			return 'Invalid id', 400
		# Check for bounds
		if id < 0 or id >= len(paragraphs):
			return 'Not Found', 404
		# Verify if not already indexed
		if id not in indexed:
			gen_indices(reverseIndices, id, paragraphs[id], WORD_DELIMITER)
			indexed.add(id)
	return jsonify(reverseIndices)

@app.route(f'/{API_ENDPOINT}/clear')
def clear():
	"""Flush all paragraphs and indices from memory."""
	del paragraphs[:]
	reverseIndices.clear()
	indexed.clear()
	return 'Success', 200