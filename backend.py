import os
import textwrap
import time
from InstructorEmbedding import INSTRUCTOR
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import HuggingFaceHub
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from config import HUGGING_FACE_API_TOKEN

os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGING_FACE_API_TOKEN

class CFG:
    #Параметры модели
    model_name = 'mistralai/Mistral-7B-Instruct-v0.1'
    temperature = 0.5
    top_p = 0.8
    repetition_penalty = 1.11
    do_sample = True
    max_new_tokens = 200
    num_return_sequences=1

    #Деление на чанки
    split_chunk_size = 900
    split_overlap = 0
    embeddings_model_repo = 'sentence-transformers/all-MiniLM-L6-v2'
    k = 3

    #Пути
    Embeddings_path =  r'ML_book_analyzer/vector_db/faiss_index_hp'



def get_llm():
    llm = HuggingFaceHub(
        repo_id = CFG.model_name,
        model_kwargs={
            "max_new_tokens": CFG.max_new_tokens,
            "temperature": CFG.temperature,
            "top_p": CFG.top_p,
            "repetition_penalty": CFG.repetition_penalty,
            "do_sample": CFG.do_sample,
            "num_return_sequences": CFG.num_return_sequences,
            "device": "cuda"
        }
    )
    return llm

#download embedding model
def dowland_model():
    embeddings = HuggingFaceInstructEmbeddings(
        model_name=CFG.embeddings_model_repo,
        model_kwargs = {"device": "cuda"}
    )

    #load vector db
    vectordb = FAISS.load_local(
        r'D:\ML_book_analyzer\vector_db\faiss_index_hp',
        embeddings
    )
    print("TYPE = ", type(vectordb))
    return vectordb


def get_llm_chain(llm):
    #generate promt
    prompt_template = """<s>[INST] {question}\n{context} [/INST]"""
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["question", "context"]
    )
    llm_chain = LLMChain(prompt=PROMPT, llm=llm)
    return llm_chain,PROMPT

def get_qa_chain(vectordb, llm, PROMPT):
    retriever = vectordb.as_retriever(search_kwargs={"k": CFG.k, "search_type": "similarity"})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        verbose=False
    )
    return qa_chain

def wrap_text_preserve_newlines(text, width=700):
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response):
    ans = wrap_text_preserve_newlines(llm_response['result'])
    sources_used = ' \n'.join(
        [
            source.metadata['source'].split('/')[-1][:-4] + ' - page: ' + str(source.metadata['page'])
            for source in llm_response['source_documents']
        ]
    )
    ans = ans + '\n\nSources: \n' + sources_used
    return ans


def llm_ans(query, qa_chain):
    start = time.time()
    llm_response = qa_chain(query)
    ans = process_llm_response(llm_response)
    end = time.time()

    time_elapsed = int(round(end - start, 0))
    time_elapsed_str = f'\n\nTime elapsed: {time_elapsed} s'
    return ans.strip() + time_elapsed_str


#Должна запускаться 1 раз при запуске бота, собирая всё вместе
def main_point_for_answers():
    vectordb = dowland_model()
    llm = get_llm()
    llm_chain, PROMPT = get_llm_chain(llm)
    qa_chain = get_qa_chain(vectordb, llm, PROMPT)
    return qa_chain

def message_answer(query, qa_chain):
    answer = llm_ans(query, qa_chain)
    return answer


if __name__ == '__main__':
    qa_chain = main_point_for_answers()
    # dowland_model()
    print(message_answer('Who is Harry Potter ?', qa_chain))
