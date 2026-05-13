def split_text_by_period(text):
    """
    按中文的：；。！等需要断开的地方分割长文本
    
    Args:
        text: 要分割的长文本
    
    Returns:
        list: 分割后的文本列表
    """
    # 定义需要分割的标点符号
    separators = ['。', '！', '；', '：', '？']
    
    # 首先将所有分隔符统一替换为句号，方便后续处理
    for sep in separators:
        text = text.replace(sep, '。')
    
    # 按中文句号分割文本
    sentences = text.split('。')
    
    # 过滤空字符串，并在每个句子末尾添加句号
    result = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            result.append(sentence + '。')
    
    return result

if __name__ == "__main__":
    # 测试文本分割功能
    test_text = "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也！然侍卫之臣不懈于内：忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也；诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。"
    sentences = split_text_by_period(test_text)
    print("分割后的文本:")
    for i, sentence in enumerate(sentences):
        print(f"{i+1}. {sentence}")
