<h1><strong>Chat-Based MCQ and Article Generation Model</strong></h1>
<p>This project is designed to interact with users, generate multiple-choice questions (MCQs), and summarize chat interactions into articles. The system uses the <strong>Hugging Face Transformers</strong> library to perform text summarization and <strong>WordNet</strong> for generating plausible distractors for the MCQs. It can also interact with the Gemini API to fetch bot responses during conversations.</p>

<h2><strong>Install Dependencies</strong></h2>
<p>Ensure that the required dependencies are installed. This project requires Python 3.7+.</p>
<p>You can install the dependencies using <strong>pip</strong>:</p>

<pre><code>pip install -r requirements.txt</code></pre>

<h2><strong>Set Up Environment Variables</strong></h2>
<p>Create a <strong>.env</strong> file in the root directory of the project and add your <strong>API Key</strong> and <strong>API URL</strong> for the Gemini API:</p>

<pre><code>
API_KEY=your_gemini_api_key_here
API_URL=your_gemini_api_url_here
</code></pre>

<h2><strong>Run the Application</strong></h2>
<p>To start the application, run the following command:</p>

<pre><code>python chat_mcq_generator.py</code></pre>

<h2><strong>Interact with the Chatbot</strong></h2>
<p>Once the application is running, you can begin interacting with the chatbot by providing user input. The bot will respond, and after 10 exchanges, the system will automatically generate:</p>
<ul>
    <li>MCQs based on the conversation.</li>
    <li>A concise article summarizing the chat history.</li>
</ul>

<h2><strong>View Generated MCQs and Article</strong></h2>
<p>Once the chat history is complete, the system will output:</p>
<ul>
    <li>A set of 3 MCQs with the correct answer and distractors.</li>
    <li>A summary article (200-300 words) based on the entire chat.</li>
</ul>

<h2><strong>Optional Features:</strong></h2>
<ul>
    <li>Fact-checking the article content.</li>
</ul>

<h2><strong>Dependencies</strong></h2>
<ul>
    <li>Python 3.7+</li>
    <li>Hugging Face Transformers</li>
    <li>NLTK (Natural Language Toolkit)</li>
    <li>Requests</li>
    <li>dotenv (for environment variable management)</li>
</ul>
