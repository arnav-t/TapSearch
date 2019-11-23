def gen_indices(indices, id, paragraph, delimiter):
	"""Split words and store them in an existing reverse index"""
	# Replace newline characters
	paragraph = paragraph.replace('\n', ' ')
	# Split words by delimiter
	words = [word.strip().lower() for word in paragraph.split(delimiter)]
	# Save number of occurences of word in a reverse index
	for word in words:
		if word:
			if word not in indices.keys():
				# Create new key if not present already
				indices[word] = {}
				indices[word][id] = 1
			else:
				# Increment if already present
				# Create paragraph id if not already present
				if id not in indices[word].keys():
					indices[word][id] = 1
				else:
					# Else just increment it
					indices[word][id] += 1