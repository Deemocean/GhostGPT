import tiktoken

def token_est(history):
  total_token=0
  encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
  for chat in history:
    content= chat["content"]
    num_tokens = len(encoding.encode(content))
    total_token+=num_tokens
    
  return total_token