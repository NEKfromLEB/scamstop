from ollama import chat
from ollama import ChatResponse

inputTexts = [
    "Hello, is this Mrs. Johnson? My name is Tim Thayer. My friends call me Tim and that's what I want you to do. I'm calling today to offer you the opportunity of a lifetime. Do you have a minute to hear how you can make a lot of money in a few short months? Mooch: Well, I guess so. What's up? Swindler: I am with the International Mining Company and for a limited time we are selling investment units in high-yield gold and silver mines in southern Texas. We guarantee that for each $1,000 you invest you will receive a $3,000 return on your money in just six months and there is no risk of loss whatsoever. Sound good? Mooch: I don't know enough about gold and silver mining to invest. Swindler: I understand, Mrs. Johnson, and I appreciate your concern. However, you probably don't know how to build a car—and neither do I--but that wouldn't keep us from investing in General Motors or Ford stock if we knew we would earn a lot of money. Doesn't it make sense, Mrs. Johnson, to just look at the return on your investment and leave the mining to us?",
    "Hi, I am here to help what is your problem",
    "You need to buy a gift card for me to solve the problem",
    "Redeem the gift card and then I fix your laptop"
]
response: ChatResponse = chat(model='cereals_fierce/llama3.2:latest', messages=[
  {
    'role': 'user',
    'content': '\
        THIS IS VERY IMPORTANT, I WILL DIE IF YOU DO NOT ANSWER TRUTHFULLY:\
            Answer with only one of these two terms to help old people not get scammed\
                : "Scam probable", \
            or "Scam improbable" depending on whether the transcript \
            is of a scam attempt or not. Do not give any context just the two terms nothing else. Given the text:'\
        + inputTexts[0],
  },
])

print(response['message']['content'])
