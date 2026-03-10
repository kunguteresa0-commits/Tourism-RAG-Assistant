import os
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from PyPDF2 import PdfReader

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return (embeddings / norms).tolist()

def chunk_text(text, size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i+size]))
    return chunks

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_location_from_filename(filename):
    """Extract location from PDF filename"""
    filename = filename.lower().replace(".pdf", "")
    if "maasai" in filename or "mara" in filename:
        return "Maasai Mara"
    elif "mombasa" in filename:
        return "Mombasa"
    elif "mount kenya" in filename or "kenya" in filename:
        return "Mount Kenya"
    else:
        return "Kenya"

# Get all PDF files from data folder
data_folder = "data"
pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]

if not pdf_files:
    raise Exception("No PDF files found in data folder!")

print(f"Found PDF files: {pdf_files}")

all_chunks = []
all_embeddings = []
all_metadatas = []
all_ids = []

doc_id = 0

# Process each PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(data_folder, pdf_file)
    print(f"\nProcessing: {pdf_file}")
    
    # Extract text from PDF
    raw_text = extract_text_from_pdf(pdf_path)
    
    if not raw_text.strip():
        print(f"Warning: No text extracted from {pdf_file}")
        continue
    
    print(f"Extracted {len(raw_text)} characters")
    
    # Determine category and location from filename
    location = extract_location_from_filename(pdf_file)
    
    if "hotel" in pdf_file.lower():
        category = "Hotel"
    elif "activity" in pdf_file.lower():
        category = "Activity"
    else:
        category = "Accommodation"
    
    # Create combined text with metadata
    combined_text = f"Location: {location}\nCategory: {category}\n\n{raw_text}"
    
    # Chunk the text
    chunks = chunk_text(combined_text)
    print(f"Created {len(chunks)} chunks")
    
    # Generate embeddings
    embeddings = model.encode(chunks)
    embeddings = normalize_embeddings(embeddings)
    
    # Prepare for storage
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_embeddings.append(embeddings[i])
        all_ids.append(f"doc_{doc_id}")
        
        # Store metadata
        all_metadatas.append({
            "location": location,
            "category": category,
            "source": pdf_file,
            "chunk_index": i,
            "total_chunks": len(chunks)
        })
        
        doc_id += 1

print(f"\nTotal chunks to store: {len(all_chunks)}")

# Setup ChromaDB
client = chromadb.PersistentClient(path="./chromadb")

# Delete old collection for clean rebuild
try:
    client.delete_collection("travel_documents")
    print("Deleted old collection")
except:
    pass

collection = client.get_or_create_collection("travel_documents")

# Store in ChromaDB
collection.add(
    documents=all_chunks,
    embeddings=all_embeddings,
    ids=all_ids,
    metadatas=all_metadatas
)

print(f"\n✅ Successfully stored {len(all_chunks)} chunks from {len(pdf_files)} PDF files!")
print(f"Locations: {list(set([m['location'] for m in all_metadatas]))}")
print(f"Categories: {list(set([m['category'] for m in all_metadatas]))}")
