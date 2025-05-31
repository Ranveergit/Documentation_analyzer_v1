# import streamlit as st
# from langchain_core.messages import AIMessage, HumanMessage
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.prompts import PromptTemplate
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from bs4 import BeautifulSoup
# import requests
# from langchain.schema import Document


# import os
# import json

# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")

# # def load_and_chunk_document(url):
# #     # get the text in document form
# #     loader = WebBaseLoader(url)
# #     document = loader.load()
    
# #     # split the document into chunks
# #     text_splitter = RecursiveCharacterTextSplitter()
# #     chunks = text_splitter.split_documents(document)
    
# #     # create a vectorstore from the chunks
# #     # vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())
# #     full_text = "\n\n".join(chunk.page_content for chunk in chunks)
# #     return full_text, url


# #     # return vector_store




# # def load_and_chunk_document(url):
# #     # Step 1: Fetch HTML content using requests
# #     headers = {"User-Agent": "Mozilla/5.0"}
# #     response = requests.get(url, headers=headers)
# #     soup = BeautifulSoup(response.text, "html.parser")

# #     # Step 2: Remove non-text elements
# #     for tag in soup(["script", "style", "img", "video", "nav", "footer", "header", "noscript"]):
# #         tag.decompose()

# #     # Step 3: Extract and clean text
# #     text = soup.get_text(separator="\n")
# #     cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

# #     # Step 4: Split into chunks
# #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# #     docs = text_splitter.create_documents([cleaned_text])
    
# #     # Step 5: Join and return only plain text
# #     full_text = "\n\n".join(chunk.page_content for chunk in docs)
# #     return full_text, url


# import requests
# from bs4 import BeautifulSoup

# def load_and_chunk_document(url):
#     # Step 1: Fetch HTML content using requests
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Step 2: Remove non-text elements
#     for tag in soup(["script", "style", "img", "video", "nav", "footer", "header", "noscript"]):
#         tag.decompose()

#     # Step 3: Extract and clean plain text
#     text = soup.get_text(separator="\n")
#     cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

#     return cleaned_text



# # 2. Prompt for single chunk analysis
# def get_chunk_prompt():
#     return PromptTemplate.from_template(
#         """
# You are an assistant helping improve documentation articles.

# Analyze the following chunk from a MoEngage documentation article. Evaluate it based on:

# 1. Readability for marketers.
# 2. Structure and flow.
# 3. Completeness and examples.
# 4. Adherence to simple style guidelines (Microsoft Style Guide).

# For each section, give:
# - A brief assessment
# - One or two actionable improvement suggestions

# Return result in plain markdown format.

# --- CHUNK START ---
# {text}
# --- CHUNK END ---
# """
#     )



# def analyze_chunks(chunks):
#     llm = ChatOpenAI(model="gpt-4", temperature=0,openai_api_key=api_key)
#     prompt = get_chunk_prompt()
#     chunks = chunks[:10]
#     results = []
#     for i, chunk in enumerate(chunks):
#         print(f"🔎 Analyzing chunk {i+1}/{len(chunks)}...")
#         input_text = prompt.format(text=chunk)
#         response = llm.invoke(input_text)
#         results.append({
#             "chunk_index": i,
#             "content": chunk,
#             "analysis": response.content
#         })
#     return results



# def analyze_documentation_by_chunk(url):
#     chunks, source_url = load_and_chunk_document(url)
#     analyses = analyze_chunks(chunks)

#     return {
#         "url": source_url,
#         "total_chunks": len(chunks),
#         "chunk_reports": analyses
#     }



# if __name__ == "__main__":
#     # url = "https://help.moengage.com/hc/en-us/articles/33508135433236-Migrate-or-Transfer-Push-Tokens"
#     url = "https://python.langchain.com/api_reference/openai/llms/langchain_openai.llms.base.OpenAI.html"
#     print(f"📄 Analyzing URL: {url}\n")
    
#     # report = analyze_documentation_by_chunk(url)
#     text = load_and_chunk_document(url)


#     # print(f"✅ Total Chunks Analyzed: {report['total_chunks']}\n")
#     # for chunk in report['chunk_reports'][:10]:
#     #     print(f"🧩 Chunk {chunk['chunk_index'] + 1} Analysis:\n")
#     #     print(chunk['analysis'])
#     #     print("\n" + "-" * 80 + "\n")
    
#     # Optional: Save to file
#     with open("chunk_analysis_report.json", "w", encoding="utf-8") as f:
#         json.dump(text, f, indent=2)

# # def get_context_retriever_chain(vector_store):
# #     llm = ChatOpenAI()
    
# #     retriever = vector_store.as_retriever()
    
# #     prompt = ChatPromptTemplate.from_messages([
# #       MessagesPlaceholder(variable_name="chat_history"),
# #       ("user", "{input}"),
# #       ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
# #     ])
    
# #     retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
# #     return retriever_chain
    
# # def get_conversational_rag_chain(retriever_chain): 
    
# #     llm = ChatOpenAI()
    
# #     prompt = ChatPromptTemplate.from_messages([
# #       ("system", "Answer the user's questions based on the below context:\n\n{context}"),
# #       MessagesPlaceholder(variable_name="chat_history"),
# #       ("user", "{input}"),
# #     ])
    
# #     stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
# #     return create_retrieval_chain(retriever_chain, stuff_documents_chain)

# # def get_response(user_input):
# #     retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
# #     conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
# #     response = conversation_rag_chain.invoke({
# #         "chat_history": st.session_state.chat_history,
# #         "input": user_input
# #     })
    
# #     return response['answer']

# # app config
# # st.set_page_config(page_title="Chat with websites", page_icon="🤖")
# # st.title("Chat with websites")

# # # sidebar
# # with st.sidebar:
# #     st.header("Settings")
# #     website_url = st.text_input("Website URL")

# # if website_url is None or website_url == "":
# #     st.info("Please enter a website URL")

# # else:
# #     # session state
# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = [
# #             AIMessage(content="Hello, I am a bot. How can I help you?"),
# #         ]
# #     if "vector_store" not in st.session_state:
# #         st.session_state.vector_store = get_vectorstore_from_url(website_url)    

# #     # user input
# #     user_query = st.chat_input("Type your message here...")
# #     if user_query is not None and user_query != "":
# #         response = get_response(user_query)
# #         st.session_state.chat_history.append(HumanMessage(content=user_query))
# #         st.session_state.chat_history.append(AIMessage(content=response))
        
       

# #     # conversation
# #     for message in st.session_state.chat_history:
# #         if isinstance(message, AIMessage):
# #             with st.chat_message("AI"):
# #                 st.write(message.content)
# #         elif isinstance(message, HumanMessage):
# #             with st.chat_message("Human"):
# #                 st.write(message.content)






















# import requests
# from bs4 import BeautifulSoup
# import textstat
# import os # For environment variables
# from dotenv import load_dotenv # To load .env file
# from openai import OpenAI # OpenAI library

# # --- Configuration ---
# load_dotenv() # Load variables from .env file into environment variables

# # --- Helper Functions (fetch_article_content, get_headings_structure) ---
# # These remain the same as in the previous response. I'll omit them here for brevity
# # but they should be included in your final script.

# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of the article from the URL."""
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         article_body = soup.find('div', class_='article-body')
#         if article_body:
#             return article_body.get_text(separator='\n', strip=True)
#         else:
#             main_content = soup.find('main')
#             if main_content:
#                 return main_content.get_text(separator='\n', strip=True)
#             return "Error: Could not find main article content."
#     except requests.exceptions.RequestException as e:
#         return f"Error fetching URL: {e}"
#     except Exception as e:
#         return f"Error parsing content: {e}"

# def get_headings_structure(url: str) -> list:
#     """Fetches headings (h1-h4) to understand structure."""
#     headings_list = []
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         article_body = soup.find('div', class_='article-body')
#         if not article_body:
#             article_body = soup.find('main')

#         if article_body:
#             for i in range(1, 5):
#                 for header in article_body.find_all(f'h{i}'):
#                     headings_list.append({'level': i, 'text': header.get_text(strip=True)})
#         return headings_list
#     except Exception:
#         return []

# # --- Main Analyzer Agent ---
# class DocumentationAnalyzerAgent:
#     def __init__(self, openai_api_key: str = None):
#         self.openai_client = None
#         self.llm_available = False
#         actual_api_key = openai_api_key if openai_api_key else os.getenv("OPENAI_API_KEY")

#         if actual_api_key:
#             try:
#                 self.openai_client = OpenAI(api_key=actual_api_key)
#                 self.llm_available = True
#                 print("OpenAI client initialized successfully.")
#             except Exception as e:
#                 print(f"Failed to initialize OpenAI client: {e}. Proceeding without LLM.")
#         else:
#             print("OpenAI API key not found. Proceeding without LLM.")

#     def _llm_analyze(self, prompt_messages: list) -> str:
#         """
#         Helper to call OpenAI LLM or return placeholder if not available.
#         OpenAI prefers a list of messages (system, user, assistant).
#         """
#         if not self.llm_available or not self.openai_client:
#             # Fallback to the placeholder if LLM is not set up
#             # This part uses the content of the last user message for the old placeholder logic
#             user_content_for_placeholder = ""
#             for msg in reversed(prompt_messages):
#                 if msg.get("role") == "user":
#                     # A bit of a hack to extract context for the old placeholder
#                     user_content_for_placeholder = msg.get("content", "")
#                     break
#             return self.call_placeholder_llm_analysis(user_content_for_placeholder)

#         try:
#             # print(f"\n--- OpenAI LLM Call ---")
#             # print(f"Messages: {prompt_messages}")
#             completion = self.openai_client.chat.completions.create(
#                 model="gpt-3.5-turbo", # Or "gpt-4" if you have access and prefer it
#                 messages=prompt_messages
#             )
#             # print(f"Response: {completion.choices[0].message.content}")
#             # print(f"--- End OpenAI LLM Call ---\n")
#             return completion.choices[0].message.content
#         except Exception as e:
#             print(f"Error during OpenAI API call: {e}")
#             return "LLM analysis failed due to an API error."

#     def call_placeholder_llm_analysis(self, user_prompt_content: str) -> str:
#         """
#         This is the placeholder function from your original example,
#         triggered if the actual LLM call isn't possible.
#         It uses the content of the user's message to decide which placeholder to return.
#         """
#         # print(f"\n--- Placeholder LLM Called With User Content Snippet ---\n{user_prompt_content[:200]}...\n---")
#         if "Readability for a Marketer" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) The text appears moderately complex for a non-technical marketer.
#             Suggestions:
#             1. (Placeholder) Sentence "The synergistic amalgamation..." is too complex. Consider: "Our system uses smart algorithms..."
#             2. (Placeholder) Explain 'API endpoint' or link to a glossary.
#             """
#         elif "Structure and Flow" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Decent heading structure, but some long paragraphs.
#             Suggestions:
#             1. (Placeholder) Section under 'Advanced Configuration' has long paragraphs. Break them down.
#             2. (Placeholder) Use bullet points for 'Setup Process'.
#             """
#         elif "Completeness of Information & Examples" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Covers basics but lacks depth in examples.
#             Suggestions:
#             1. (Placeholder) Add a code snippet for API usage in 'Integration Details'.
#             2. (Placeholder) Include diverse examples for 'Targeting Rules'.
#             """
#         elif "Style Guidelines" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Tone is professional but could be more customer-focused.
#             Suggestions:
#             1. (Placeholder) Voice/Tone: Change "The system allows users to..." to "You can use the system to...".
#             2. (Placeholder) Clarity: Simplify "It is imperative for the configuration..." to "Important: Validate your configuration...".
#             """
#         return "(Placeholder) LLM analysis placeholder: No specific suggestions generated for this section."

#     def analyze_readability(self, article_text: str) -> dict:
#         flesch_reading_ease = textstat.flesch_reading_ease(article_text)
#         gunning_fog = textstat.gunning_fog(article_text)

#         score_explanation = ""
#         if flesch_reading_ease > 60:
#             score_explanation = "The Flesch Reading Ease score suggests the text is relatively easy to read."
#         elif 30 <= flesch_reading_ease <= 60:
#             score_explanation = "The Flesch Reading Ease score suggests the text is somewhat difficult to read."
#         else:
#             score_explanation = "The Flesch Reading Ease score suggests the text is very difficult to read."
#         assessment = f"Flesch Reading Ease: {flesch_reading_ease:.2f}. Gunning Fog Index: {gunning_fog:.2f}.\n{score_explanation}"

#         system_message = "You are an AI assistant helping to improve technical documentation for a non-technical marketer audience."
#         user_prompt = (
#             f"Analyze the following documentation article excerpt for readability from the perspective of a non-technical marketer. "
#             f"The Flesch Reading Ease score is {flesch_reading_ease:.2f} and Gunning Fog is {gunning_fog:.2f}. "
#             f"Explain why it might be easy or difficult for this persona to understand. "
#             f"Provide specific, actionable suggestions for improvement (e.g., 'Sentence X is too long...', 'Term Y is jargon...'). "
#             f"Focus on providing concrete examples of how to rephrase sentences or explain terms if needed.\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {"assessment": assessment, "suggestions": llm_suggestions}

#     def analyze_structure_and_flow(self, article_text: str, headings: list) -> dict:
#         headings_summary = "No headings found or extracted."
#         if headings:
#             headings_summary = "Headings structure:\n" + "\n".join([f"{'  ' * (h['level']-1)}- H{h['level']}: {h['text']}" for h in headings])

#         system_message = "You are an AI assistant evaluating the structure and flow of technical documentation."
#         user_prompt = (
#             f"Analyze the structure and flow of the following documentation article. "
#             f"Consider the use of headings (structure provided below), paragraph length, use of lists, and logical progression. "
#             f"Is it easy to navigate and find specific information? "
#             f"Provide specific, actionable suggestions for improvement (e.g., 'Section X could benefit from subheadings like A, B, C...', 'Paragraph Y (provide first few words) is too dense; split it into smaller paragraphs focusing on Z.').\n\n"
#             f"Headings Structure:\n{headings_summary}\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {
#             "assessment": f"Article structure based on headings:\n{headings_summary}\nFurther assessment on flow and navigability provided by LLM.",
#             "suggestions": llm_suggestions
#         }

#     def analyze_completeness_and_examples(self, article_text: str) -> dict:
#         system_message = "You are an AI assistant evaluating the completeness and clarity of examples in technical documentation."
#         user_prompt = (
#             f"Evaluate the completeness of information and the use of examples in this documentation article. "
#             f"Does it provide enough detail for a user to understand and implement the feature or concept? "
#             f"Are there sufficient, clear, and relevant examples? "
#             f"If not, suggest specific areas where examples could be added or existing ones improved (e.g., 'After explaining concept A, an example illustrating its use would be beneficial. Specifically, show how to configure X for scenario Y.' or 'The example for feature B is unclear; clarify by showing the expected output.').\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {
#             "assessment": "LLM will assess if the article provides enough detail and relevant examples.",
#             "suggestions": llm_suggestions
#         }

#     def analyze_style_guidelines(self, article_text: str) -> dict:
#         style_principles = """
#         1. Voice and Tone: Is it customer-focused (e.g., uses "you" and "your"), friendly, supportive, and professional? Avoids overly technical or aloof language.
#         2. Clarity and Conciseness: Are sentences and paragraphs generally short? Is jargon avoided or clearly explained? Does it get straight to the point?
#         3. Action-oriented language: Does it use strong verbs for instructions? Does it clearly guide the user on what to do (e.g., "Click Save," "Enter your campaign name," "To create a segment, follow these steps:")?
#         """
#         system_message = "You are an AI assistant analyzing documentation against specific style guidelines."
#         user_prompt = (
#             "Analyze this documentation article based on the following simplified style guidelines (inspired by Microsoft Style Guide):\n"
#             f"{style_principles}\n"
#             "Identify specific sentences or phrases (quote them) that deviate from these principles and suggest concrete changes "
#             "(e.g., 'The sentence \"The system allows users to...\" should be \"You can use the system to...\" for a more customer-focused voice.' or 'The term \"idiosyncratic variable\" is jargon; explain it or simplify to \"unique setting\".').\n\n"
#             "Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt.format(article_text=article_text)} # Ensure article_text is correctly passed
#         ])
#         return {
#             "assessment": f"LLM will assess adherence to: {style_principles.strip()}",
#             "suggestions": llm_suggestions
#         }

#     def run_analysis(self, url: str) -> dict:
#         print(f"Analyzing URL: {url}")
#         article_text = fetch_article_content(url)
#         headings = get_headings_structure(url)

#         if article_text.startswith("Error:"):
#             return {"url": url, "error": article_text, "analysis": {}}
#         if not article_text.strip():
#              return {"url": url, "error": "Fetched empty content.", "analysis": {}}


#         print(f"Fetched {len(article_text)} characters for analysis.")

#         report = {
#             "url": url,
#             "analysis": {
#                 "readability_for_marketer": self.analyze_readability(article_text),
#                 "structure_and_flow": self.analyze_structure_and_flow(article_text, headings),
#                 "completeness_of_information_and_examples": self.analyze_completeness_and_examples(article_text),
#                 "style_guidelines_adherence": self.analyze_style_guidelines(article_text),
#             }
#         }
#         return report

# # --- Main Execution ---
# if __name__ == "__main__":
#     # The OpenAI API key is loaded from the .env file by load_dotenv()
#     # and then picked up by os.getenv("OPENAI_API_KEY") in the agent's constructor.
#     # You can also pass it directly: analyzer = DocumentationAnalyzerAgent(openai_api_key="sk-...")
#     analyzer = DocumentationAnalyzerAgent()

#     test_url = "https://python.langchain.com/docs/tutorials/agents/"
#     # test_url = "https://help.moengage.com/hc/en-us/articles/12998826037140-Generative-Content-BETA-"


#     if not test_url:
#         print("Please set a test_url to analyze.")
#     else:
#         analysis_report = analyzer.run_analysis(test_url)

#         import json
#         report_json = json.dumps(analysis_report, indent=2)
#         print("\n\n--- Analysis Report ---")
#         print(report_json)

#         with open("documentation_analysis_report1.json", "w") as f:
#             f.write(report_json)
#         print("\nReport saved to documentation_analysis_report.json")


# import requests
# from bs4 import BeautifulSoup
# import textstat
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# import streamlit as st
# import json

# # --- Configuration ---
# load_dotenv()

# # --- Helper Functions ---
# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of the article from the URL."""
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         article_body = soup.find('div', class_='article-body')
#         if article_body:
#             return article_body.get_text(separator='\n', strip=True)
#         else:
#             main_content = soup.find('main')
#             if main_content:
#                 return main_content.get_text(separator='\n', strip=True)
#             return "Error: Could not find main article content."
#     except requests.exceptions.RequestException as e:
#         return f"Error fetching URL: {e}"
#     except Exception as e:
#         return f"Error parsing content: {e}"

# def get_headings_structure(url: str) -> list:
#     """Fetches headings (h1-h4) to understand structure."""
#     headings_list = []
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         article_body = soup.find('div', class_='article-body')
#         if not article_body:
#             article_body = soup.find('main')

#         if article_body:
#             for i in range(1, 5):
#                 for header in article_body.find_all(f'h{i}'):
#                     headings_list.append({'level': i, 'text': header.get_text(strip=True)})
#         return headings_list
#     except Exception:
#         return []

# # --- Main Analyzer Agent ---
# class DocumentationAnalyzerAgent:
#     def __init__(self, openai_api_key: str = None):
#         self.openai_client = None
#         self.llm_available = False
#         actual_api_key = openai_api_key if openai_api_key else os.getenv("OPENAI_API_KEY")

#         if actual_api_key:
#             try:
#                 self.openai_client = OpenAI(api_key=actual_api_key)
#                 self.llm_available = True
#                 st.success("OpenAI client initialized successfully.")
#             except Exception as e:
#                 st.warning(f"Failed to initialize OpenAI client: {e}. Proceeding without LLM.")
#         else:
#             st.warning("OpenAI API key not found. Proceeding without LLM.")

#     def _llm_analyze(self, prompt_messages: list) -> str:
#         """
#         Helper to call OpenAI LLM or return placeholder if not available.
#         OpenAI prefers a list of messages (system, user, assistant).
#         """
#         if not self.llm_available or not self.openai_client:
#             user_content_for_placeholder = ""
#             for msg in reversed(prompt_messages):
#                 if msg.get("role") == "user":
#                     user_content_for_placeholder = msg.get("content", "")
#                     break
#             return self.call_placeholder_llm_analysis(user_content_for_placeholder)

#         try:
#             completion = self.openai_client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=prompt_messages
#             )
#             return completion.choices[0].message.content
#         except Exception as e:
#             st.error(f"Error during OpenAI API call: {e}")
#             return "LLM analysis failed due to an API error."

#     def call_placeholder_llm_analysis(self, user_prompt_content: str) -> str:
#         """
#         This is the placeholder function from your original example,
#         triggered if the actual LLM call isn't possible.
#         It uses the content of the user's message to decide which placeholder to return.
#         """
#         if "Readability for a Marketer" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) The text appears moderately complex for a non-technical marketer.
#             Suggestions:
#             1. (Placeholder) Sentence "The synergistic amalgamation..." is too complex. Consider: "Our system uses smart algorithms..."
#             2. (Placeholder) Explain 'API endpoint' or link to a glossary.
#             """
#         elif "Structure and Flow" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Decent heading structure, but some long paragraphs.
#             Suggestions:
#             1. (Placeholder) Section under 'Advanced Configuration' has long paragraphs. Break them down.
#             2. (Placeholder) Use bullet points for 'Setup Process'.
#             """
#         elif "Completeness of Information & Examples" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Covers basics but lacks depth in examples.
#             Suggestions:
#             1. (Placeholder) Add a code snippet for API usage in 'Integration Details'.
#             2. (Placeholder) Include diverse examples for 'Targeting Rules'.
#             """
#         elif "Style Guidelines" in user_prompt_content:
#             return """
#             Assessment: (Placeholder) Tone is professional but could be more customer-focused.
#             Suggestions:
#             1. (Placeholder) Voice/Tone: Change "The system allows users to..." to "You can use the system to...".
#             2. (Placeholder) Clarity: Simplify "It is imperative for the configuration..." to "Important: Validate your configuration...".
#             """
#         return "(Placeholder) LLM analysis placeholder: No specific suggestions generated for this section."

#     def analyze_readability(self, article_text: str) -> dict:
#         flesch_reading_ease = textstat.flesch_reading_ease(article_text)
#         gunning_fog = textstat.gunning_fog(article_text)

#         score_explanation = ""
#         if flesch_reading_ease > 60:
#             score_explanation = "The Flesch Reading Ease score suggests the text is relatively easy to read."
#         elif 30 <= flesch_reading_ease <= 60:
#             score_explanation = "The Flesch Reading Ease score suggests the text is somewhat difficult to read."
#         else:
#             score_explanation = "The Flesch Reading Ease score suggests the text is very difficult to read."
#         assessment = f"Flesch Reading Ease: {flesch_reading_ease:.2f}. Gunning Fog Index: {gunning_fog:.2f}.\n{score_explanation}"

#         system_message = "You are an AI assistant helping to improve technical documentation for a non-technical marketer audience."
#         user_prompt = (
#             f"Analyze the following documentation article excerpt for readability from the perspective of a non-technical marketer. "
#             f"The Flesch Reading Ease score is {flesch_reading_ease:.2f} and Gunning Fog is {gunning_fog:.2f}. "
#             f"Explain why it might be easy or difficult for this persona to understand. "
#             f"Provide specific, actionable suggestions for improvement (e.g., 'Sentence X is too long...', 'Term Y is jargon...'). "
#             f"Focus on providing concrete examples of how to rephrase sentences or explain terms if needed.\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {"assessment": assessment, "suggestions": llm_suggestions}

#     def analyze_structure_and_flow(self, article_text: str, headings: list) -> dict:
#         headings_summary = "No headings found or extracted."
#         if headings:
#             headings_summary = "Headings structure:\n" + "\n".join([f"{'    ' * (h['level']-1)}- H{h['level']}: {h['text']}" for h in headings])

#         system_message = "You are an AI assistant evaluating the structure and flow of technical documentation."
#         user_prompt = (
#             f"Analyze the structure and flow of the following documentation article. "
#             f"Consider the use of headings (structure provided below), paragraph length, use of lists, and logical progression. "
#             f"Is it easy to navigate and find specific information? "
#             f"Provide specific, actionable suggestions for improvement (e.g., 'Section X could benefit from subheadings like A, B, C...', 'Paragraph Y (provide first few words) is too dense; split it into smaller paragraphs focusing on Z.').\n\n"
#             f"Headings Structure:\n{headings_summary}\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {
#             "assessment": f"Article structure based on headings:\n{headings_summary}\nFurther assessment on flow and navigability provided by LLM.",
#             "suggestions": llm_suggestions
#         }

#     def analyze_completeness_and_examples(self, article_text: str) -> dict:
#         system_message = "You are an AI assistant evaluating the completeness and clarity of examples in technical documentation."
#         user_prompt = (
#             f"Evaluate the completeness of information and the use of examples in this documentation article. "
#             f"Does it provide enough detail for a user to understand and implement the feature or concept? "
#             f"Are there sufficient, clear, and relevant examples? "
#             f"If not, suggest specific areas where examples could be added or existing ones improved (e.g., 'After explaining concept A, an example illustrating its use would be beneficial. Specifically, show how to configure X for scenario Y.' or 'The example for feature B is unclear; clarify by showing the expected output.').\n\n"
#             f"Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt}
#         ])
#         return {
#             "assessment": "LLM will assess if the article provides enough detail and relevant examples.",
#             "suggestions": llm_suggestions
#         }

#     def analyze_style_guidelines(self, article_text: str) -> dict:
#         style_principles = """
#         1. Voice and Tone: Is it customer-focused (e.g., uses "you" and "your"), friendly, supportive, and professional? Avoids overly technical or aloof language.
#         2. Clarity and Conciseness: Are sentences and paragraphs generally short? Is jargon avoided or clearly explained? Does it get straight to the point?
#         3. Action-oriented language: Does it use strong verbs for instructions? Does it clearly guide the user on what to do (e.g., "Click Save," "Enter your campaign name," "To create a segment, follow these steps:")?
#         """
#         system_message = "You are an AI assistant analyzing documentation against specific style guidelines."
#         user_prompt = (
#             "Analyze this documentation article based on the following simplified style guidelines (inspired by Microsoft Style Guide):\n"
#             f"{style_principles}\n"
#             "Identify specific sentences or phrases (quote them) that deviate from these principles and suggest concrete changes "
#             "(e.g., 'The sentence \"The system allows users to...\" should be \"You can use the system to...\" for a more customer-focused voice.' or 'The term \"idiosyncratic variable\" is jargon; explain it or simplify to \"unique setting\".').\n\n"
#             "Article Text:\n{article_text}"
#         )
#         llm_suggestions = self._llm_analyze([
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_prompt.format(article_text=article_text)}
#         ])
#         return {
#             "assessment": f"LLM will assess adherence to: {style_principles.strip()}",
#             "suggestions": llm_suggestions
#         }

#     def run_analysis(self, url: str) -> dict:
#         st.info(f"Analyzing URL: {url}")
#         article_text = fetch_article_content(url)
#         headings = get_headings_structure(url)

#         if article_text.startswith("Error:"):
#             st.error(article_text)
#             return {"url": url, "error": article_text, "analysis": {}}
#         if not article_text.strip():
#             st.warning("Fetched empty content.")
#             return {"url": url, "error": "Fetched empty content.", "analysis": {}}

#         st.success(f"Fetched {len(article_text)} characters for analysis.")

#         report = {
#             "url": url,
#             "analysis": {
#                 "readability_for_marketer": self.analyze_readability(article_text),
#                 "structure_and_flow": self.analyze_structure_and_flow(article_text, headings),
#                 "completeness_of_information_and_examples": self.analyze_completeness_and_examples(article_text),
#                 "style_guidelines_adherence": self.analyze_style_guidelines(article_text),
#             }
#         }
#         return report

# # --- Streamlit UI ---
# st.set_page_config(layout="wide", page_title="Documentation Analyzer")

# st.sidebar.title("Analyze Documentation")
# url_input = st.sidebar.text_input("Enter Article URL", "")
# analyze_button = st.sidebar.button("Analyze")

# st.title("Documentation Analysis Report")

# if analyze_button and url_input:
#     analyzer = DocumentationAnalyzerAgent()
#     with st.spinner("Analyzing... This may take a moment."):
#         analysis_report = analyzer.run_analysis(url_input)

#     st.subheader("Analysis Results")
#     if "error" in analysis_report:
#         st.error(f"Error during analysis: {analysis_report['error']}")
#     else:
#         st.json(analysis_report) # Display the JSON report

#         # Download button for JSON
#         report_json_string = json.dumps(analysis_report, indent=2)
#         st.download_button(
#             label="Download Analysis Report (JSON)",
#             data=report_json_string,
#             file_name="documentation_analysis_report.json",
#             mime="application/json"
#         )
# elif analyze_button and not url_input:
#     st.sidebar.error("Please enter a URL to analyze.")

# st.markdown(
#     """
#     ---
#     This application helps you analyze documentation articles for various aspects like readability, structure, completeness, and adherence to style guidelines.
#     Enter a URL in the sidebar and click 'Analyze' to get a detailed report.
#     """
# )
