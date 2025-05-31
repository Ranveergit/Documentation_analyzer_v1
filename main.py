import requests
from bs4 import BeautifulSoup
import textstat
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Configuration ---
load_dotenv()

# --- Helper Functions ---
# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of the article from the URL."""
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
#     }
#     try:
#         response = requests.get(url,headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#          # --- Inspect the page manually to find the correct containers ---
#         # # Try a broader search first, then refine
#         # article_body = soup.find('div', class_='article-body') # Your current attempt
#         # if not article_body:
#         #     article_body = soup.find('main') # Your current attempt
#         # if not article_body:
#         #     # Look for common article content containers in help centers
#         #     article_body = soup.find('article')
#         # if not article_body:
#         #     # Sometimes it's within a div that contains the entire content section
#         #     article_body = soup.find('div', class_='article-container') # Or a similar class name
#         # if not article_body:
#         #     article_body = soup.find('div', class_='section-tree-entry-content') # Specific to Zendesk-like help centers
#         # if not article_body:
#         #     # As a last resort, try getting content from the body, but this will include sidebar, footer, etc.
#         #     return soup.body.get_text(separator='\n', strip=True) if soup.body else "Error: Could not find main article content."

#     #     if article_body:
#     #         return article_body.get_text(separator='\n', strip=True)
#     #     else:
#     #         return "Error: Could not find main article content after trying various tags."
#     # except requests.exceptions.RequestException as e:
#     #     return f"Error fetching URL: {e}"
#     # except Exception as e:
#     #     return f"Error parsing content: {e}"

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



# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of the article from the URL."""
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # First, try to find the <main> tag
#         main_tag = soup.find('main', role="main") # Use role="main" for precision if present

#         if main_tag:
#             # Then, look for the div with class="article-page" inside the main tag
#             article_body_container = main_tag.find('div', class_='article-page')

#             if article_body_container:
#                 return article_body_container.get_text(separator='\n', strip=True)
#             else:
#                 # If 'article-page' div is not found within main,
#                 # you might want a fallback or simply indicate failure for this specific target
#                 return "Error: Could not find 'article-page' div within the main content area."
#         else:
#             # Fallback for pages that might not use <main> or use a different structure
#             # This keeps some of your previous broader search logic as a backup
#             article_body_container = soup.find('div', class_='article-body')
#             if article_body_container:
#                 return article_body_container.get_text(separator='\n', strip=True)
#             else:
#                 # If neither main > article-page nor article-body div are found, try broader main
#                 main_content = soup.find('main')
#                 if main_content:
#                     return main_content.get_text(separator='\n', strip=True)
                
#                 # You can add more fallbacks here if you know other common structures
#                 # For example:
#                 # article_container = soup.find('div', class_='article-container')
#                 # if article_container:
#                 #     return article_container.get_text(separator='\n', strip=True)
                
#                 return "Error: Could not find main article content using any known selectors."

#     except requests.exceptions.RequestException as e:
#         return f"Error fetching URL: {e}"
#     except Exception as e:
#         return f"Error parsing content: {e}"




# -- main updated code  part 1 ------



# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of a JavaScript-rendered article from the URL using Selenium."""
#     options = Options()
#     options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--window-size=1920,1080')
#     options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36')

#     # Use webdriver-manager to handle ChromeDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     try:
#         driver.get(url)
#         time.sleep(5)  # Let JavaScript render the page

#         soup = BeautifulSoup(driver.page_source, 'html.parser')

#         # Attempt to extract using common structures
#         main_tag = soup.find('main', role="main") or soup.find('main')
#         if main_tag:
#             article_body_container = main_tag.find('div', class_='article-page') or \
#                                      main_tag.find('div', class_='article-body') or \
#                                      main_tag.find('article')
#             if article_body_container:
#                 return article_body_container.get_text(separator='\n', strip=True)
#             else:
#                 return "Error: Could not find 'article-page' or 'article-body' within <main>."
        
#         # Fallbacks
#         article_body_container = soup.find('div', class_='article-body') or \
#                                  soup.find('div', class_='container') or \
#                                  soup.find('article')
#         if article_body_container:
#             return article_body_container.get_text(separator='\n', strip=True)

#         return "Error: Could not find main article content using any known selectors."

#     except Exception as e:
#         return f"Error: {e}"

#     finally:
#         driver.quit()




# -- main updated code  part 1 ------




#----------------------------main updated code part2 ------------------------------------


def fetch_article_content(url: str) -> str:
    """Fetches cleaned article content and headings from a JavaScript-rendered page using Selenium."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Let JavaScript render

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Try to extract article content from known containers
        main_tag = soup.find('main', role="main") or soup.find('main')
        article_container = None
        if main_tag:
            article_container = main_tag.find('div', class_='article-page') or \
                                main_tag.find('div', class_='article-body') or \
                                main_tag.find('article')

        if not article_container:
            article_container = soup.find('div', class_='article-body') or \
                                soup.find('div', class_='container') or \
                                soup.find('article') or soup.body

        if not article_container:
            return "Error: Could not locate main article container."

        # Get cleaned text content
        content = article_container.get_text(separator='\n', strip=True)

        # Extract headings
        headings = []
        for level in range(1, 5):
            for header in article_container.find_all(f'h{level}'):
                heading_text = header.get_text(separator=" ", strip=True).replace("link", "").strip()
                if heading_text:
                    headings.append({
                        "level": level,
                        "text": heading_text
                    })

        # Optionally print or return both
        structured_output = "\n\n".join([f"{'#' * h['level']} {h['text']}" for h in headings])
        full_output = f"{structured_output}\n\n{content}"

        return full_output

    except Exception as e:
        return f"Error: {e}"

    finally:
        driver.quit()




#----------------------------main updated code part2 ------------------------------------

# import requests
# from bs4 import BeautifulSoup

# def fetch_article_content(url: str) -> str:
#     """Fetches the main content of the article from the URL."""
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Try to find the <main> tag first
#         main_tag = soup.find('main', role="main") # Using role="main" if it's consistently there

#         if main_tag:
#             # Now, specifically look for the div with class "article__body" INSIDE the main tag
#             article_body_container = main_tag.find('div', class_='article__body')

#             if article_body_container:
#                 return article_body_container.get_text(separator='\n', strip=True)
#             else:
#                 # If article__body is not found within main
#                 return "Error: Could not find 'article__body' div within the main content area."
#         else:
#             # Fallback if the <main> tag itself is not found
#             # (Less likely for this specific site given your info, but good for robustness)
#             return "Error: Could not find the main content area (<main> tag)."

#     except requests.exceptions.RequestException as e:
#         return f"Error fetching URL: {e}"
#     except Exception as e:
#         return f"Error parsing content: {e}"



## --------------- update getheading function 1 -----------------------------------------

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


## ----------------------------- update getheading function 1--------------------------------------------



## ------------------------------------update getheading function 2----------------------------------


def get_headings_structure(url: str) -> list:
    """Uses Selenium to extract heading structure (h1-h4) from JavaScript-rendered web pages."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Let JS render

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        article_body = soup.find('div', class_='article-body') or soup.find('main') or soup.find('body')
        if not article_body:
            return []

        headings_list = []
        for i in range(1, 5):
            for header in article_body.find_all(f'h{i}'):
                text = header.get_text(strip=True)
                if text:
                    headings_list.append({'level': i, 'text': text})

        return headings_list

    except Exception as e:
        print(f"Error while fetching headings: {e}")
        return []

    finally:
        driver.quit()



## ------------------------------------update getheading function 2----------------------------------

# --- Main Analyzer Agent ---
class DocumentationAnalyzerAgent:
    def __init__(self, openai_api_key: str = None):
        self.openai_client = None
        self.llm_available = False
        actual_api_key = openai_api_key if openai_api_key else os.getenv("OPENAI_API_KEY")

        if actual_api_key:
            try:
                self.openai_client = OpenAI(api_key=actual_api_key)
                self.llm_available = True
                st.success("OpenAI client initialized successfully.")
            except Exception as e:
                st.warning(f"Failed to initialize OpenAI client: {e}. Proceeding without LLM.")
        else:
            st.warning("OpenAI API key not found. Proceeding without LLM.")

    def _llm_analyze(self, prompt_messages: list) -> str:
        """
        Helper to call OpenAI LLM or return placeholder if not available.
        OpenAI prefers a list of messages (system, user, assistant).
        """
        if not self.llm_available or not self.openai_client:
            user_content_for_placeholder = ""
            for msg in reversed(prompt_messages):
                if msg.get("role") == "user":
                    user_content_for_placeholder = msg.get("content", "")
                    break
            return self.call_placeholder_llm_analysis(user_content_for_placeholder)

        try:
            completion = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=prompt_messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error during OpenAI API call: {e}")
            return "LLM analysis failed due to an API error."

    def call_placeholder_llm_analysis(self, user_prompt_content: str) -> str:
        """
        This is the placeholder function from your original example,
        triggered if the actual LLM call isn't possible.
        It uses the content of the user's message to decide which placeholder to return.
        """
        if "Readability for a Marketer" in user_prompt_content:
            return """
            Assessment: (Placeholder) The text appears moderately complex for a non-technical marketer.
            Suggestions:
            1. (Placeholder) Sentence "The synergistic amalgamation..." is too complex. Consider: "Our system uses smart algorithms..."
            2. (Placeholder) Explain 'API endpoint' or link to a glossary.
            """
        elif "Structure and Flow" in user_prompt_content:
            return """
            Assessment: (Placeholder) Decent heading structure, but some long paragraphs.
            Suggestions:
            1. (Placeholder) Section under 'Advanced Configuration' has long paragraphs. Break them down.
            2. (Placeholder) Use bullet points for 'Setup Process'.
            """
        elif "Completeness of Information & Examples" in user_prompt_content:
            return """
            Assessment: (Placeholder) Covers basics but lacks depth in examples.
            Suggestions:
            1. (Placeholder) Add a code snippet for API usage in 'Integration Details'.
            2. (Placeholder) Include diverse examples for 'Targeting Rules'.
            """
        elif "Style Guidelines" in user_prompt_content:
            return """
            Assessment: (Placeholder) Tone is professional but could be more customer-focused.
            Suggestions:
            1. (Placeholder) Voice/Tone: Change "The system allows users to..." to "You can use the system to...".
            2. (Placeholder) Clarity: Simplify "It is imperative for the configuration..." to "Important: Validate your configuration...".
            """
        return "(Placeholder) LLM analysis placeholder: No specific suggestions generated for this section."

    def analyze_readability(self, article_text: str) -> dict:
        flesch_reading_ease = textstat.flesch_reading_ease(article_text)
        gunning_fog = textstat.gunning_fog(article_text)

        score_explanation = ""
        if flesch_reading_ease > 60:
            score_explanation = "The Flesch Reading Ease score suggests the text is relatively easy to read."
        elif 30 <= flesch_reading_ease <= 60:
            score_explanation = "The Flesch Reading Ease score suggests the text is somewhat difficult to read."
        else:
            score_explanation = "The Flesch Reading Ease score suggests the text is very difficult to read."
        assessment = f"Flesch Reading Ease: {flesch_reading_ease:.2f}. Gunning Fog Index: {gunning_fog:.2f}.\n{score_explanation}"

        system_message = "You are an AI assistant helping to improve technical documentation for a non-technical marketer audience."
        user_prompt = (
            f"Analyze the following documentation article excerpt for readability from the perspective of a non-technical marketer. "
            f"The Flesch Reading Ease score is {flesch_reading_ease:.2f} and Gunning Fog is {gunning_fog:.2f}. "
            f"Explain why it might be easy or difficult for this persona to understand. "
            f"Provide specific, actionable suggestions for improvement (e.g., 'Sentence X is too long...', 'Term Y is jargon...'). "
            f"Focus on providing concrete examples of how to rephrase sentences or explain terms if needed.\n\n"
            f"Article Text:\n{article_text}"
        )
        llm_suggestions = self._llm_analyze([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ])
        return {"assessment": assessment, "suggestions": llm_suggestions}

    def analyze_structure_and_flow(self, article_text: str, headings: list) -> dict:
        headings_summary = "No headings found or extracted."
        if headings:
            headings_summary = "Headings structure:\n" + "\n".join([f"{'    ' * (h['level']-1)}- H{h['level']}: {h['text']}" for h in headings])

        system_message = "You are an AI assistant evaluating the structure and flow of technical documentation."
        user_prompt = (
            f"Analyze the structure and flow of the following documentation article. "
            f"Consider the use of headings (structure provided below), paragraph length, use of lists, and logical progression. "
            f"Is it easy to navigate and find specific information? "
            f"Provide specific, actionable suggestions for improvement (e.g., 'Section X could benefit from subheadings like A, B, C...', 'Paragraph Y (provide first few words) is too dense; split it into smaller paragraphs focusing on Z.').\n\n"
            f"Headings Structure:\n{headings_summary}\n\n"
            f"Article Text:\n{article_text}"
        )
        llm_suggestions = self._llm_analyze([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ])
        return {
            "assessment": f"Article structure based on headings:\n{headings_summary}\nFurther assessment on flow and navigability provided by LLM.",
            "suggestions": llm_suggestions
        }

    def analyze_completeness_and_examples(self, article_text: str) -> dict:
        system_message = "You are an AI assistant evaluating the completeness and clarity of examples in technical documentation."
        user_prompt = (
            f"Evaluate the completeness of information and the use of examples in this documentation article. "
            f"Does it provide enough detail for a user to understand and implement the feature or concept? "
            f"Are there sufficient, clear, and relevant examples? "
            f"If not, suggest specific areas where examples could be added or existing ones improved (e.g., 'After explaining concept A, an example illustrating its use would be beneficial. Specifically, show how to configure X for scenario Y.' or 'The example for feature B is unclear; clarify by showing the expected output.').\n\n"
            f"Article Text:\n{article_text}"
        )
        llm_suggestions = self._llm_analyze([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ])
        return {
            "assessment": "LLM will assess if the article provides enough detail and relevant examples.",
            "suggestions": llm_suggestions
        }

    def analyze_style_guidelines(self, article_text: str) -> dict:
        style_principles = """
        1. Voice and Tone: Is it customer-focused (e.g., uses "you" and "your"), friendly, supportive, and professional? Avoids overly technical or aloof language.
        2. Clarity and Conciseness: Are sentences and paragraphs generally short? Is jargon avoided or clearly explained? Does it get straight to the point?
        3. Action-oriented language: Does it use strong verbs for instructions? Does it clearly guide the user on what to do (e.g., "Click Save," "Enter your campaign name," "To create a segment, follow these steps:")?
        """
        system_message = "You are an AI assistant analyzing documentation against specific style guidelines."
        user_prompt = (
            "Analyze this documentation article based on the following simplified style guidelines (inspired by Microsoft Style Guide):\n"
            f"{style_principles}\n"
            "Identify specific sentences or phrases (quote them) that deviate from these principles and suggest concrete changes "
            "(e.g., 'The sentence \"The system allows users to...\" should be \"You can use the system to...\" for a more customer-focused voice.' or 'The term \"idiosyncratic variable\" is jargon; explain it or simplify to \"unique setting\".').\n\n"
            "Article Text:\n{article_text}"
        )
        llm_suggestions = self._llm_analyze([
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt.format(article_text=article_text)}
        ])
        return {
            "assessment": f"LLM will assess adherence to: {style_principles.strip()}",
            "suggestions": llm_suggestions
        }

    def run_analysis(self, url: str) -> dict:
        st.info(f"Analyzing URL: {url}")
        article_text = fetch_article_content(url)
        headings = get_headings_structure(url)

        if article_text.startswith("Error:"):
            st.error(article_text)
            return {"url": url, "error": article_text, "analysis": {}}
        if not article_text.strip():
            st.warning("Fetched empty content.")
            return {"url": url, "error": "Fetched empty content.", "analysis": {}}

        st.success(f"Fetched {len(article_text)} characters for analysis.")

        report = {
            "url": url,
            "analysis": {
                "readability_for_marketer": self.analyze_readability(article_text),
                "structure_and_flow": self.analyze_structure_and_flow(article_text, headings),
                "completeness_of_information_and_examples": self.analyze_completeness_and_examples(article_text),
                "style_guidelines_adherence": self.analyze_style_guidelines(article_text),
            }
        }
        return report

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Documentation Analyzer")

st.sidebar.title("Analyze Documentation")
url_input = st.sidebar.text_input("Enter Article URL", "")
analyze_button = st.sidebar.button("Analyze")

st.title("Documentation Analysis Report")

# Use session state to store the analysis report
if 'analysis_report' not in st.session_state:
    st.session_state.analysis_report = None

if analyze_button and url_input:
    analyzer = DocumentationAnalyzerAgent()
    with st.spinner("Analyzing... This may take a moment."):
        st.session_state.analysis_report = analyzer.run_analysis(url_input)
elif analyze_button and not url_input:
    st.sidebar.error("Please enter a URL to analyze.")

# Display the report using the new UI structure
report_data = st.session_state.analysis_report
if report_data:
    st.header("Analyzed URL")
    if report_data.get("url"):
        st.markdown(f"[{report_data['url']}]({report_data['url']})")
    else:
        st.warning("URL not found in the JSON data.")

    if "analysis" in report_data and isinstance(report_data["analysis"], dict):
        st.divider()
        st.header("Analysis Details")

        for criterion, details in report_data["analysis"].items():
            # Make the criterion name more presentable
            criterion_title = criterion.replace("_", " ").title()

            with st.expander(f"📊 {criterion_title}", expanded=False):
                if isinstance(details, dict):
                    if "assessment" in details:
                        st.subheader("📋 Assessment")
                        st.markdown(details["assessment"]) # Use markdown to render formatting

                    if "suggestions" in details:
                        st.subheader("💡 Suggestions for Improvement")
                        st.markdown(details["suggestions"]) # Use markdown for suggestions
                    
                    if not "assessment" in details and not "suggestions" in details:
                        st.write("No assessment or suggestions found for this criterion.")
                else:
                    st.write(f"Details for {criterion_title} are not in the expected format.")
    else:
        st.warning("No 'analysis' section found or it's not in the expected format in the JSON data.")

    # Download button for JSON - moved outside the analysis display block
    if report_data and "error" not in report_data: # Only show download if analysis was successful
        report_json_string = json.dumps(report_data, indent=2)
        st.download_button(
            label="Download Full Analysis Report (JSON)",
            data=report_json_string,
            file_name="documentation_analysis_report.json",
            mime="application/json"
        )
    elif report_data and "error" in report_data:
        st.error("Cannot download report due to analysis error.")

st.markdown(
    """
    ---
    This application helps you analyze documentation articles for various aspects like readability, structure, completeness, and adherence to style guidelines.
    Enter a URL in the sidebar and click 'Analyze' to get a detailed report.
    """
)