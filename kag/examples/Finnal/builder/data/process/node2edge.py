import json

import json 
file_path = "./disease_kb_sample.json"

with open(file_path, "r") as file:
    datas = json.load(file)
    
# 全局
result = []


# 原始 JSON 数据
def process_data(data):
    node_id = data["id"]
    from_name = data["name"]
    from_type = "EntityType"
    to_type = "EntityType"

    # 处理顶层属性（除了 properties）
    for key in ["id", "name", "label"]:
        if key in data:
            result.append({
                "id": node_id,
                "from": from_name,
                "fromType": from_type,
                "to": data[key],
                "toType": to_type,
                "label": key,
                "properties": {}
            })

    # 处理 properties 下的属性
    for key, value in data["properties"].items():
        if isinstance(value, list):
            # 对于列表值，逐个创建关系
            for item in value:
                result.append({
                    "id": node_id,
                    "from": from_name,
                    "fromType": from_type,
                    "to": item,
                    "toType": to_type,
                    "label": key,
                    "properties": {}
                })
        else:
            # 对于非列表值，直接创建关系
            result.append({
                "id": node_id,
                "from": from_name,
                "fromType": from_type,
                "to": value,
                "toType": to_type,
                "label": key,
                "properties": {}
            })


for data in datas:
    process_data(data)

with open("transformed_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)