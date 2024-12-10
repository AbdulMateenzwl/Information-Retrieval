DOCUMENTS = {
    "doc1": "Machine learning is a subset of AI focused on training models.",
    "doc2": "Data visualization helps to interpret complex datasets visually.",
    "doc3": "NASA has conducted many space missions over the years.",
    "doc4": "Astronauts undergo rigorous training for space exploration.",
    "doc5": "exams are realted to papers of student and information related to paper and there results"
}

# Enhanced graph where each word and its related words are bidirectional
RELATED_WORDS_GRAPH = {
    # Blog-related words
    "blog": ["website", "diary", "entries", "posts", "blog"],
    "website": ["blog", "diary", "entries", "posts", "website"],
    "diary": ["blog", "website", "entries", "posts", "diary"],
    "entries": ["blog", "website", "diary", "posts", "entries"],
    "posts": ["blog", "website", "diary", "entries", "posts"],
    
    # Exams-related words
    "exams": ["papers", "students", "results", "information", "exams"],
    "papers": ["exams", "students", "results", "information", "papers"],
    "students": ["exams", "papers", "results", "information", "students"],
    "results": ["exams", "papers", "students", "information", "results"],
    "information": ["exams", "papers", "students", "results", "information"],
    
    # Flash ROM-related words
    "flash": ["ROM", "device", "product", "data", "flash"],
    "ROM": ["flash", "device", "product", "data", "ROM"],
    "device": ["flash", "ROM", "product", "data", "device"],
    "product": ["flash", "ROM", "device", "data", "product"],
    "data": ["flash", "ROM", "device", "product", "data"],
}

