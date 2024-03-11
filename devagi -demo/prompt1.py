import os
from openai import OpenAI

# 这是用大模型+数据控制的方式来实现问答

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 基于prompt生成文本
def get_completion(prompt,model="gpt-3.5-turbo"):
    messages = [{"role":"user","content":prompt}]   #将prompt作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content      #返回模型生成的文本

# 实现一个NLU
# 任务描述
instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。
每种流量套餐产品包含三个属性：名称(name)，月费价格(price)，月流量(data)。
根据用户输入，识别用户在上述三种属性上每一种的需求。
"""

# 用户输入
input_text = "办个最便宜的套餐。"

# 约定输出格式
output_format = """
以 JSON 格式输出。
1、name字段的取值为string类型,取值必须为以下之一：经济套餐 畅游套餐 无线套餐 校园套餐 或者 null

2、price字段的取值为一个结构体 或者 null ，包含两个字段：
(1)operator,string类型,取值范围：'<='(小于等于),'>='(大于等于),'=='(等于)
(2)value,int类型

3、data字段的取值为一个结构体 或者 null,包含两个字段
(1)operator,string类型,取值范围：'<='(小于等于),'>='(大于等于),'=='(等于)
(2)value,int类型或者string类型,string类型智能是'无上限'

4、用户意图可以包含按照price或者data排序,以sort字段标识,取值为一个结构体
(1)结构体中以"ordering"="descend"表示按降序排序,以"value"字段存储待排序的字段
(2)结构体中以"ordering"="ascend"表示按升序排序,以"value"字段存储待排序的字段

输出中只包含用户提及的字段,不要猜测任何用户未提及的字段,不要输出值为null的字段。
"""

# prompt模板
prompt = f"""
{instruction}

{output_format}

用户输入：
{input_text}
"""

response = get_completion(prompt)
print(response)


