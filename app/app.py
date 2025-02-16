import os
import openai
import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# OpenAI API Key (Replace with your key)
openai.api_key = "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"

# PostgreSQL Database Configuration
DB_HOST = "database-1.c9scia20gbq0.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Allvy1234"

def convert_nl_to_sql(user_question):
    """Uses GPT to convert natural language to SQL"""
    prompt = f"Convert this question into a SQL query for PostgreSQL:\nQ: {user_question}\nSQL:"
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100
    )
    
    sql_query = response["choices"][0]["text"].strip()
    return sql_query

def execute_sql_query(query):
    """Executes SQL query and returns result"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return str(e)

@app.route("/")
def home():
    """Renders the chat page"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot API requests"""
    data = request.json
    user_question = data.get("message", "")

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # Convert natural language to SQL
    sql_query = convert_nl_to_sql(user_question)

    # Fetch result from the database
    query_result = execute_sql_query(sql_query)

    return jsonify({"sql_query": sql_query, "result": query_result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
