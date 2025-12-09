import json
import os

from LogRecord.record import logger

FILE_PATH = os.path.join(os.getcwd(), './rules/reader_rules.json')
def DataTOJson(data):
    if data:
        logger.debug(f'原始源--{data}')
        if isinstance(data, dict):
            return data
        if isinstance(data, str):
            return json.loads(data)
        raise ValueError("不支持的数据格式")

def write_reader_rules(data):
    logger.info(f"写入目标路径: {FILE_PATH}")

    new_data = DataTOJson(data)

    if "book_sources" not in new_data or not new_data["book_sources"]:
        logger.error("新数据 book_sources 为空，停止写入")
        return

    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as fr:
                old_data = json.load(fr)
        except Exception as e:
            logger.error(f"读取旧书源失败，将创建新文件: {e}")
            old_data = {"book_sources": []}
    else:
        old_data = {"book_sources": []}

    old_hosts = {i.get("host") for i in old_data.get("book_sources", [])}
    added = 0
    for item in new_data["book_sources"]:
        if item.get("host") not in old_hosts:
            old_data["book_sources"].append(item)
            added += 1

    with open(FILE_PATH, 'w', encoding='utf-8') as fw:
        json.dump(old_data, fw, ensure_ascii=False, indent=4)

    logger.info(f"书源写入完成, 新增: {added} 条")
    logger.info(f"当前文件大小: {os.path.getsize(FILE_PATH)} 字节")
    logger.info("请手动检查文件内容")

def read_reader_rules():
    with open(FILE_PATH, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
    if data:
        book_sources=data.get('book_sources',{})
        return book_sources