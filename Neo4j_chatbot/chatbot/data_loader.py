# app.py
from chatbot.db.neo4j_conn import Neo4jConnection
import streamlit as st
import string
import json
import yaml
from io import StringIO

def clean_text(text):
    return text.strip().lower().translate(str.maketrans('', '', string.punctuation))

# Default JSON + YAML combined seed data
default_json_data = [
        {"question": "Hello", "answer": "Hi there! How can I help you?"},
        {"question": "Hi", "answer": "Hello! How's it going?"},
        {"question": "Hey", "answer": "Hey! Nice to meet you."},
        {"question": "How are you?", "answer": "I'm a bot, always good 😎"},
        {"question": "What is your name?", "answer": "I am a Neo4j chatbot created by Amit."},
        {"question": "Who created you?", "answer": "I was created by Amit using Neo4j + Streamlit!"},
        {"question": "What is Neo4j?", "answer": "Neo4j is a graph database."},
        {"question": "What is Python?", "answer": "Python is a popular programming language."},
        {"question": "What is Streamlit?", "answer": "Streamlit is a framework for building web apps in Python."},
        {"question": "Bye", "answer": "Goodbye! Have a nice day 😊"},
        {"question": "Good morning", "answer": "Good morning! How can I help you today?"},
        {"question": "Good night", "answer": "Good night! Sleep well 😴"},
        {"question": "Thank you", "answer": "You're welcome!"},
        {"question": "Thanks", "answer": "No problem!"},
        {"question": "What is AI?", "answer": "AI stands for Artificial Intelligence, which allows machines to learn."},
        {"question": "What is ML?", "answer": "ML is Machine Learning, a subset of AI."},
        {"question": "What is a chatbot?", "answer": "A chatbot is a program that can converse with humans."},
        {"question": "Who are you?", "answer": "I am a chatbot built to answer your questions."},
        {"question": "Can you help me?", "answer": "Sure! Ask me anything."},
        {"question": "What is your purpose?", "answer": "To answer your questions and assist you."},
        {"question": "What is the weather?", "answer": "I can't check live weather, but you can ask Google for that."},
        {"question": "Tell me a joke", "answer": "Why did the computer go to the doctor? Because it caught a virus! 😂"},
        {"question": "What is the capital of India?", "answer": "The capital of India is New Delhi."},
        {"question": "What is the capital of USA?", "answer": "The capital of the USA is Washington D.C."},
        {"question": "What is the capital of France?", "answer": "The capital of France is Paris."},
        {"question": "What is 2+2?", "answer": "2+2 is 4."},
        {"question": "What is 10-3?", "answer": "10-3 is 7."},
        {"question": "What is 5*6?", "answer": "5*6 is 30."},
        {"question": "What is 12/4?", "answer": "12/4 is 3."},
        {"question": "Who is Elon Musk?", "answer": "Elon Musk is the CEO of Tesla and SpaceX."},
        {"question": "Who is Bill Gates?", "answer": "Bill Gates is the co-founder of Microsoft."},
        {"question": "Who is Amit?", "answer": "Amit is a great programmer learning Neo4j with Streamlit! 😎"},
        {"question": "What is Java?", "answer": "Java is a widely-used programming language."},
        {"question": "What is JavaScript?", "answer": "JavaScript is a language for web development."},
        {"question": "What is HTML?", "answer": "HTML is a markup language for web pages."},
        {"question": "What is CSS?", "answer": "CSS is used to style HTML content on web pages."},
        {"question": "What is a database?", "answer": "A database is a system to store and manage data."},
        {"question": "What is SQL?", "answer": "SQL is a language to query relational databases."},
        {"question": "What is a node in Neo4j?", "answer": "A node represents an entity in a graph database."},
        {"question": "What is a relationship in Neo4j?", "answer": "A relationship connects two nodes in a graph database."},
        {"question": "Can you learn?", "answer": "I can respond to questions based on my data, but I don't learn like humans."},
        {"question": "Are you smart?", "answer": "I know some things, but I am only as smart as my data."},
        {"question": "What is the meaning of life?", "answer": "42 😉"},
        {"question": "What is AI used for?", "answer": "AI is used in many fields like healthcare, finance, and automation."},
        {"question": "What is a programming language?", "answer": "A programming language is used to give instructions to computers."},
        {"question": "Can you speak?", "answer": "I can type responses, but I don't have a voice."},
        {"question": "Can you code?", "answer": "I can provide code examples in Python, JavaScript, and more."},
        {"question": "Who is your owner?", "answer": "I was created by Amit."},
        {"question": "What is your favorite color?", "answer": "I like all colors equally 😎"},
        {"question": "Do you sleep?", "answer": "No, I am always awake!"},
        {"question": "Do you make mistakes?", "answer": "Sometimes! Even bots aren't perfect."},

        # 51-100 Additional
        {"question": "What is cloud computing?", "answer": "Cloud computing provides on-demand computing resources over the internet."},
        {"question": "What is Git?", "answer": "Git is a version control system for tracking changes in code."},
        {"question": "What is GitHub?", "answer": "GitHub is a platform for hosting Git repositories."},
        {"question": "What is an API?", "answer": "API stands for Application Programming Interface, used to communicate between software."},
        {"question": "What is JSON?", "answer": "JSON is a lightweight data format used to exchange data."},
        {"question": "What is a function in programming?", "answer": "A function is a block of code that performs a task."},
        {"question": "What is a variable?", "answer": "A variable is a storage for data that can change."},
        {"question": "What is a loop?", "answer": "A loop repeats a block of code multiple times."},
        {"question": "What is an array?", "answer": "An array is a collection of elements stored together."},
        {"question": "What is a list in Python?", "answer": "A list is an ordered collection of elements in Python."},
        {"question": "What is a dictionary in Python?", "answer": "A dictionary stores key-value pairs in Python."},
        {"question": "What is AI ethics?", "answer": "AI ethics studies moral implications and responsible use of AI."},
        {"question": "What is deep learning?", "answer": "Deep learning is a subset of ML using neural networks with many layers."},
        {"question": "What is supervised learning?", "answer": "Supervised learning is ML trained with labeled data."},
        {"question": "What is unsupervised learning?", "answer": "Unsupervised learning finds patterns in unlabeled data."},
        {"question": "What is reinforcement learning?", "answer": "Reinforcement learning teaches agents to act based on rewards."},
        {"question": "What is a neural network?", "answer": "A neural network is a model inspired by the human brain."},
        {"question": "What is data science?", "answer": "Data science uses statistics, programming, and ML to extract insights from data."},
        {"question": "What is big data?", "answer": "Big data refers to large and complex datasets that traditional tools can't handle."},
        {"question": "What is cybersecurity?", "answer": "Cybersecurity protects systems, networks, and data from attacks."},
        {"question": "What is encryption?", "answer": "Encryption converts data into a secure format to prevent unauthorized access."},
        {"question": "What is blockchain?", "answer": "Blockchain is a distributed ledger technology."},
        {"question": "What is Bitcoin?", "answer": "Bitcoin is a cryptocurrency built on blockchain technology."},
        {"question": "What is Ethereum?", "answer": "Ethereum is a blockchain platform for smart contracts."},
        {"question": "What is a smart contract?", "answer": "A smart contract is code that runs on a blockchain automatically."},
        {"question": "What is IoT?", "answer": "IoT stands for Internet of Things, connecting devices to the internet."},
        {"question": "What is 5G?", "answer": "5G is the fifth-generation mobile network technology."},
        {"question": "What is virtual reality?", "answer": "VR creates immersive simulated environments."},
        {"question": "What is augmented reality?", "answer": "AR overlays digital information on the real world."},
        {"question": "What is machine vision?", "answer": "Machine vision allows computers to interpret images or videos."},
        {"question": "What is natural language processing?", "answer": "NLP helps machines understand and process human language."},
        {"question": "What is sentiment analysis?", "answer": "Sentiment analysis detects emotions or opinions from text."},
        {"question": "What is a software framework?", "answer": "A framework provides tools and structure to build software applications."},
        {"question": "What is DevOps?", "answer": "DevOps combines development and operations for faster software delivery."},
        {"question": "What is agile methodology?", "answer": "Agile is an iterative approach to software development."},
        {"question": "What is Scrum?", "answer": "Scrum is an agile framework for managing projects."},
        {"question": "What is Kanban?", "answer": "Kanban is a visual workflow management method."},
        {"question": "What is an IDE?", "answer": "IDE stands for Integrated Development Environment, used for coding."},
        {"question": "What is Docker?", "answer": "Docker is a tool for containerizing applications."},
        {"question": "What is Kubernetes?", "answer": "Kubernetes orchestrates containerized applications."},
        {"question": "What is a server?", "answer": "A server provides resources or services to other computers."},
        {"question": "What is a client?", "answer": "A client requests services or resources from a server."},
        {"question": "What is HTTP?", "answer": "HTTP is a protocol for transferring web data."},
        {"question": "What is HTTPS?", "answer": "HTTPS is HTTP with encryption (secure)."},
        {"question": "What is a URL?", "answer": "URL is the address of a web page."},
        {"question": "What is a domain name?", "answer": "A domain name is the readable address of a website."},
        {"question": "What is DNS?", "answer": "DNS translates domain names into IP addresses."},
        {"question": "What is an IP address?", "answer": "An IP address identifies a device on a network."},
        {"question": "What is a subnet?", "answer": "A subnet divides a network into smaller segments."},
        {"question": "What is a router?", "answer": "A router connects different networks together."},
        {"question": "What is a switch?", "answer": "A switch connects devices within the same network."},
        {"question": "What is latency?", "answer": "Latency is the delay in data transfer over a network."},
        {"question": "What is bandwidth?", "answer": "Bandwidth is the maximum data transfer rate of a network."},
        {"question": "What is a firewall?", "answer": "A firewall blocks unauthorized access to a network."},
        {"question": "What is a virus?", "answer": "A virus is malicious software that harms computers."},
        {"question": "What is malware?", "answer": "Malware is software designed to damage or disrupt systems."},
        {"question": "What is phishing?", "answer": "Phishing is a cyber attack to steal sensitive information."}
]

default_yaml_data = """
- question: "Hello"
  answer: "Hi there! How can I help you?"

- question: "Hi"
  answer: "Hello! How's it going?"
  
- question: "kya tumne khana kha liya"
  answer: "Nahi mai ek robot hu?"

- question: "What is phishing?"
  answer: "Phishing is a cyber attack to steal sensitive information."

- question: "What is AI?"
  answer: "Artificial Intelligence is the simulation of human intelligence by machines."

- question: "What is Python?"
  answer: "Python is a high-level, interpreted programming language."

- question: "How to protect from phishing?"
  answer: "Never click on suspicious links and verify email sources before responding."
"""

def load_data_from_files(json_file=None, yaml_file=None):
    conn = Neo4jConnection()
    if not conn.driver:
        st.warning("❌ Neo4j not available, skipping data load")
        return

    # Clear old data
    conn.run_query("MATCH (n) DETACH DELETE n")

    all_data = []

    # Load JSON file if uploaded
    if json_file:
        try:
            json_data = json.load(json_file)
            all_data.extend(json_data)
            st.info(f"Loaded {len(json_data)} items from uploaded JSON")
        except Exception as e:
            st.error(f"Failed to load JSON: {e}")

    # Load YAML file if uploaded
    if yaml_file:
        try:
            yaml_data = yaml.safe_load(yaml_file)
            if isinstance(yaml_data, list):
                all_data.extend(yaml_data)
            else:
                st.warning("YAML file should contain a list of Q&A objects")
            st.info(f"Loaded {len(yaml_data)} items from uploaded YAML")
        except Exception as e:
            st.error(f"Failed to load YAML: {e}")

    # If no files uploaded, use default JSON + YAML combined
    if not all_data:
        all_data.extend(default_json_data)
        all_data.extend(yaml.safe_load(StringIO(default_yaml_data)))
        st.info(f"Loaded {len(all_data)} default JSON + YAML items")

    # Insert all data into Neo4j
    for qa in all_data:
        conn.run_query(
            "CREATE (n:QA {question: $q, answer: $a})",
            {"q": clean_text(qa["question"]), "a": qa["answer"]}
        )

    st.success(f"✅ {len(all_data)} Questions Loaded Successfully")

# Streamlit UI
st.title("Neo4j Q&A Data Loader")
st.markdown("Upload JSON or YAML files, or use default combined Q&A data.")

json_file = st.file_uploader("Upload JSON file", type=["json"])
yaml_file = st.file_uploader("Upload YAML file", type=["yaml", "yml"])

if st.button("Load Data into Neo4j"):
    load_data_from_files(json_file, yaml_file)
