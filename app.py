from flask import Flask, jsonify, render_template, request
from gen_indices import gen_indices
from os import environ

API_ENDPOINT = 'api'
PARAGRAPH_DELIMITER = '\n\n'
WORD_DELIMITER = ' '

app = Flask(__name__, template_folder='./templates')		# Start flask app

paragraphs = []		# Paragraphs list
reverseIndices = {}		# Reverse indices for the paragraphs
indexed = set()		# Set of indexed paragraphs 

@app.route('/')
def home():
	"""Return the homepage."""
	return render_template('home.html')

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

@app.route(f'/{API_ENDPOINT}/search')
def search():
	"""Search and return top paragraphs for the given word."""
	word = request.args.get('query')
	if word is None:
		return 'Missing parameter', 400
	word = word.strip().lower()
	# Return empty list if word is not found
	if word not in reverseIndices.keys():
		return jsonify([])
	# Sort in descending order and return paragraphs
	indices = sorted(reverseIndices[word], key=reverseIndices[word].get, reverse=True)
	results = [paragraphs[idx] for idx in indices]
	return jsonify(results)

if __name__ == '__main__':
	port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)