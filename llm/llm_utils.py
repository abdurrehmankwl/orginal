from groq import Groq
from .vector_utils import get_similar_docs
import os

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key="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")

def generate_answer(question):
    
    docs = get_similar_docs(question)
    
    context = "\n".join([doc.page_content for doc in docs]) if docs else ""
    
    if context:
        prompt = (
            f"You are a plant disease detection expert AI.\n"
            f"Provide clear and concise explanations and recommendations based on context.\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer with explanation and any recommendations if needed:"
        )
    else:
       
        prompt = (
            f"You are a plant disease detection expert AI.\n"
            f"Provide an expert explanation and recommendations based on your knowledge.\n"
            f"Question: {question}\n"
            f"Answer with explanation and any recommendations if needed:"
        )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    return response.choices[0].message.content.strip()
