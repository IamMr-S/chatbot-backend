import openai

client = openai.OpenAI(api_key="")
try:
  response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
      {'role': 'system', 'content': '英語で考え、日本語で返答してください。'},
      {'role': 'user', 'content': 'こんにちは'}
    ]
  )
  print(response.choices[0].message.content)
except openai.OpenAIError as e:
  error_message = str(e)
  if "Error code:" in error_message:
      error_code = int(error_message.split("Error code:")[1][:4])
      error_info = error_message.split("Error code:")[1][7:]
      print("エラーコード:", error_code)
      print(error_info)