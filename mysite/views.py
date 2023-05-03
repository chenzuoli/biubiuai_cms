# Create your views here.
from django.shortcuts import render
import openai
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging


def home(request):
    return render(request, 'home/home_page.html')


# add a url
def text_to_image(request):
    return render(request, 'home/text_to_image.html')

# add a request to openai api, and return the response, add a parameter: prompt


@csrf_exempt
def chenzuoli(request):
    # request to openai api to get response
    # get the parameter: prompt
    # Forbidden (CSRF cookie not set.): /chenzuoli/
    # https://stackoverflow.com/questions/40340595/django-csrf-cookie-not-set

    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    basePrefixPrompt = request.json.get('basePrefixPrompt')

    print(prompt)
    print(basePrefixPrompt)
    print(f"{basePrefixPrompt}\n\nYou:{prompt}\n\nAI:")

    openai.api_key = os.getenv("OPENAI_API_KEY")

    prePrefixPrompt = """
    我有许多个博客网站，一般在github pages上写的比较全\n
    另外csdn和知乎偶尔写一些，记录一些可能经常用到的东西，后面可以自己查看。\n
    https://chenzuoli.github.io/\n
    https://blog.csdn.net/chenzuoli\n
    https://www.zhihu.com/people/nihaoshijie709918\n
    我的微信公众号：程序员写书，里面最近记录的是关于商业的知识，欢迎关注👏🏻\n
    学习股票交易中，也在学习AIGC、ChatGPT，不想被AI替代\n
    最近在做AI相关的项目,想帮助那些恐惧AI的人,不被替代.\n
    最近做的AI项目：http://www.biubiuai.com/\n
    这是我的个人简历：https://chenzuoli.github.io/2021/09/27/%E4%B8%AA%E4%BA%BA%E7%AE%80%E5%8E%86/ 欢迎骚扰\n
    """

    res = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prePrefixPrompt}\n\n{basePrefixPrompt}\n\nYou:{prompt}\n\nAI:",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


@csrf_exempt
def chatgpt(request):
    # create a post request to openai api, and return the response, add a parameter: prompt
    # CSRF cookie set.
    # request to openai api to get response
    # get the parameter: message
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    basePrefixPrompt = request.json.get('basePrefixPrompt')

    prompt += ", 举个例子来详细说一下"

    openai.api_key = os.getenv("OPENAI_API_KEY")
    # print("openai.api_key:" + str(openai.api_key))
    logging.info("prompt:" + str(prompt))
    res = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{basePrefixPrompt}\n\nYou:{prompt}\n\nAI:",
        temperature=0.7,
        max_tokens=1024
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def qa_gpt(request):
    # request to openai api to get response
    # get the parameter: prompt
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    prefixPrompt = request.json.get('basePrefixPrompt')

    openai.api_key = os.getenv("OPENAI_API_KEY")

    basePrompt = """I am a highly intelligent question answering bot. 
            If you ask me a question that is rooted in truth, I will give you the answer. 
            If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with Unknown.\n\n
            Q: What is human life expectancy in the United States?\n
            A: Human life expectancy in the United States is 78 years.\n\n
            Q: Who was president of the United States in 1955?\n
            A: Dwight D. Eisenhower was president of the United States in 1955.\n\n
            Q: Which party did he belong to?\n
            A: He belonged to the Republican Party.\n\n
            Q: What is the square root of banana?\n
            A: Unknown\n\n
            Q: How does a telescope work?\n
            A: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\n
            Q: Where were the 1992 Olympics held?\n
            A: The 1992 Olympics were held in Barcelona, Spain.\n\n
            Q: How many squigs are in a bonk?\nA: Unknown\n\n
            Q: Where is the Valley of Kings?\nA:\n"""
    logging.info("prompt:" + str(prompt))
    if prefixPrompt:
        prompt = basePrompt + prefixPrompt + prompt
    else:
        prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def grammar_correction_gpt(request):
    # request to openai api to get response
    # get the parameter: prompt
    request.json = json.loads(request.body)
    prompt = request.json.get('message')

    openai.api_key = os.getenv("OPENAI_API_KEY")

    basePrompt = """
    Correct this to standard English:\n\n"""
    logging.info("prompt:" + str(prompt))

    prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def summarizer_gpt(request):
    """
    Summarize this for a second-grade student:
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    prefixPrompt = request.json.get('basePrefixPrompt')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
    "Summarize this for a second-grade student:\n\n\n"
    """

    if prefixPrompt:
        prompt = basePrompt + prefixPrompt + prompt
    else:
        prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def natural_lang_to_openai_api_gpt(request):
    """
    Create code to call to the OpenAI API using a natural language instruction.

    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    prefixPrompt = request.json.get('basePrefixPrompt')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
    "\"\"\"\nUtil exposes the following:\nutil.openai() -> authenticates & returns the openai module, which has the following functions:\nopenai.Completion.create(\n    prompt=\"<my prompt>\", # The prompt to start completing from\n   max_tokens=123, # The max number of tokens to generate\n    temperature=1.0 # A measure of randomness\n    echo=True, # Whether to return the prompt in addition to the generated completion\n)\n\"\"\"\nimport util\n\"\"\"\nCreate an OpenAI completion starting from the prompt \"Once upon an AI\", no more than 5 tokens. Does not include the prompt.\n\"\"\"\n"
    """

    if prefixPrompt:
        prompt = basePrompt + prefixPrompt + prompt
    else:
        prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )
    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def text_to_command(request):
    """
    Create a command from a natural language instruction.
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    prefixPrompt = request.json.get('basePrefixPrompt')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
        Convert this text to a programmatic command:\n\nExample: Ask Constance if we need some bread\nOutput: send-msg `find constance` Do we need some bread?\n
    """

    if prefixPrompt:
        prompt = basePrompt + prefixPrompt + prompt
    else:
        prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        # stop=["\n"]
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def translator(request):
    """
    Translate Chinese to English.
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
    Translate this into English:
    """

    prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def natural_lang_to_stripe_api_gpt(request):
    """
    Create code to call the Stripe API using natural language.
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')
    prefixPrompt = request.json.get('basePrefixPrompt')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
        \"\"\"\nUtil exposes the following:\n\nutil.stripe() -> authenticates & returns the stripe module; usable as stripe.Charge.create etc\n\"\"\"\nimport util\n\"\"\"\nCreate a Stripe token using the users credit card: 5555-4444-3333-2222, expiration date 12 / 28, cvc 521\n\"\"\"
    """

    if prefixPrompt:
        prompt = basePrompt + prefixPrompt + prompt
    else:
        prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def customer_gpt(request):
    """
    You are a customer service agent. You are given a customer's email address and a message. You need to respond to the customer.
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
    You are a customer service representative for a tech company and need to answer customer questions politely and confidently, conveying your professionalism and enthusiasm to the customer, and helping to resolve issues.:
    """

    prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response


def teacher_gpt(request):
    """
    You are a teacher
    """
    request.json = json.loads(request.body)
    prompt = request.json.get('message')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info("prompt:" + str(prompt))

    basePrompt = """
    \"\"\"You are a teacher. In your classroom, you patiently answer students' questions and carefully guide each student\"\"\""""

    prompt = basePrompt + prompt
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    logging.info("res.choices[0].text:" + str(res.choices[0].text))
    res = {"message": res.choices[0].text,
           "status_code": 200, "status": "success"}
    response = JsonResponse(res)
    response.status_code = 200
    return response
