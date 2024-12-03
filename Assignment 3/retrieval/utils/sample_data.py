DOCUMENTS = {
    "doc1": "Machine learning is a subset of AI focused on training models.",
    "doc2": "Data visualization helps to interpret complex datasets visually.",
    "doc3": "NASA has conducted many space missions over the years.",
    "doc4": "Astronauts undergo rigorous training for space exploration.",
    "doc5": "Data visualization and machine learning often go hand in hand."
}

# Enhanced graph where each word and its related words are bidirectional
RELATED_WORDS_GRAPH = {
    "NASA": ["space", "exploration", "missions", "astronauts","NASA"],
    "space": ["NASA", "missions", "exploration", "astronauts","space"],
    "exploration": ["space", "NASA", "missions", "astronauts","exploration"],
    "missions": ["NASA", "space", "exploration", "astronauts","missions"],
    "astronauts": ["NASA", "space", "exploration", "missions","astronauts"],
    
    "machine learning": ["AI", "models", "data", "training","machine learning"],
    "AI": ["machine learning", "models", "data", "training","AI"],
    "models": ["machine learning", "AI", "data", "training","models"],
    "data": ["machine learning", "AI", "models", "training","data"],
    "training": ["machine learning", "AI", "models", "data","training"],
    
    "data visualization": ["charts", "graphs", "datasets", "visual","data visualization"],
    "charts": ["data visualization", "graphs", "datasets", "visual","charts"],
    "graphs": ["data visualization", "charts", "datasets", "visual","graphs"],
    "datasets": ["data visualization", "charts", "graphs", "visual","datasets"],
    "visual": ["data visualization", "charts", "graphs", "datasets","visual"]
}
