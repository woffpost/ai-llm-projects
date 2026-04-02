from dotenv import load_dotenv
import os
import anthropic
import json


load_dotenv("/Users/vladimirrusakov/Desktop/ai-llm-projects/06-agent/.env")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Загружаем каталог
with open("/Users/vladimirrusakov/Desktop/catalog.txt", "r", encoding="utf-8") as f:
    catalog = f.read()

# Определяем инструменты
tools = [
    {
        "name": "search_catalog",
        "description": "Поиск моделей в каталоге",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Поисковый запрос"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate_discount",
        "description": "Рассчитать цену со скидкой",
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "discount_percent": {"type": "number"}
            },
            "required": ["price", "discount_percent"]
        }
    }
]

def search_catalog(query):
    results = [line for line in catalog.split("\n") if query.lower() in line.lower()]
    return "\n".join(results) if results else "Ничего не найдено"

def calculate_discount(price, discount_percent):
    result = price * (1 - discount_percent / 100)
    return f"Цена со скидкой {discount_percent}%: {result:.2f}"

def run_agent(question):
    messages = [{"role": "user", "content": question}]
    
    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Если агент закончил — выводим ответ
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\nОтвет: {block.text}\n")
            break
        
        # Если агент хочет использовать инструмент
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Использую инструмент: {block.name} с параметрами {block.input}")
                    
                    if block.name == "search_catalog":
                        result = search_catalog(block.input["query"])
                    elif block.name == "calculate_discount":
                        result = calculate_discount(block.input["price"], block.input["discount_percent"])
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            messages.append({"role": "user", "content": tool_results})

while True:
    question = input("Вопрос: ")
    if question.lower() == "выход":
        break
    run_agent(question)