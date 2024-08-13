import pandas as pd
import csv
import requests
import json

# 定义调用本地API的函数
def get_completion(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": prompt}
    try:
        response = requests.post(url='http://127.0.0.1:6006', headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"错误: 响应码 {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"错误: {str(e)}"

# 读取CSV文件
df = pd.read_csv('../test.csv')
input_texts = df.iloc[:, 0].tolist()  # 根据需要调整列索引

# 准备输出的CSV文件
with open('qwen1k5.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['原始文本', '任务模板', 'API响应'])
    i=1

    # 处理输入数据的每一行
    for text in input_texts:
        task_template = {
            "instruction": "你是专门进行事件提取的专家。请从input中抽取出符合schema定义的事件，不存在的事件返回空列表，不存在的论元返回NAN，如果论元存在多值请返回列表。请按照JSON字符串的格式回答。",
            "schema": [
        {
            "event_type": "交通出行",
            "trigger": True,
            "arguments": [
                "所在城市",
                "出发地",
                "目的地",
                "起始车站/机场/码头",
                "途经地点/车站/机场/码头",
                "到达车站/机场/码头",
                "进站口",
                "出站口",
                "交通工具/方式",
                "所在景区（注：此参数仅在交通工具为景区内部交通时抽取）",
                "线路/车次名称",
                "出发时间",
                "到达时间",
                "耗时",
                "发车间隔/频率",
                "花费金额",
                "购票地点",
                "交通出行体验",
                "注意事项与建议",
                "停车信息",
                "路况与安全",
                "高速信息",
                "路线与导航",
                "运营信息",
                "发车时间信息",
                "票价与支付信息",
                "路线与站点信息",
                "推荐与评价信息",
                "其他交通出行经验"
            ]
        }
    ],
            "input": text
        }
        # 将任务模板转换为JSON字符串
        task_template_str = json.dumps(task_template, indent=4, ensure_ascii=False)
        print(i)
        i=i+1
        # 获取API响应
        api_response = get_completion(task_template_str)
        print(api_response)
        # 将结果写入到输出文件
        writer.writerow([text, task_template_str, api_response])

print("数据处理完成并已保存到 'local_api_responses.csv'。")
