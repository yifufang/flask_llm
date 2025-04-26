from flask import Blueprint, render_template, request, jsonify
from .models import db, Messages, Summary
from flask import current_app
from .deepseek import Deepseek_llm
from .user import User
import json

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return jsonify({"message": "使用/ask接口进行提问"})


@main.route("/ask", methods=["POST"])
async def ask():
    """ 
    处理用户向AI的提问,并返回AI的回答
    接受的参数格式JSON:{"sender": "1","recipient": "bot","content": "内容"}
    返回的参数格式JSON:{"设定":"{'id': 1, 'name': '小明', 'age': 3, 'birthdate': datetime.datetime(2020, 1, 2, 0, 0), 'hobbies': '玩球', 'history': '对土豆过敏'}","记忆":"","response": "AI的回答"}
    """
    sender = request.json.get("sender")
    recipient = request.json.get("recipient", "bot")
    content = request.json.get("content")

    # 调用DeepSeek API 以及建立连接
    deepseek = Deepseek_llm(current_app.config['DEEPSEEK_API_KEY'])

    # 获取用户的设定和历史记录,生成上下文记忆内容,以及意图识别
    user = User(sender)
    memory = user.get_summary()
    baby_settings = json.dumps(user.get_baby_settings(), ensure_ascii=False)
    intents = user.purpose(content)
    
    # 调用DeepSeek API获取AI的回答
    response = await deepseek.get_response(content, memory, baby_settings, intents)
    if response is None:
        return jsonify({"error": "AI服务不可用"}), 500
    
    # 调用DeepSeek根据以往的记忆和用户的提问生成新的总结，方便下次提问的上下文记忆
    assistant = "将用户提供的内容进行总结,形成新的记忆,方便下次提问的上下文记忆"
    new_content = f"上下文记忆: {memory} \n用户提问: {content} \nAI回答: {response}"
    intent = "总结"
    summary = await deepseek.get_response(new_content, "", baby_settings, intent, assistant)
    if summary is None:
        return jsonify({"error": "AI服务不可用"}), 500
    
    # 关闭DeepSeeker API的连接
    deepseek.close()

    
    # 将AI的回答和用户提问存入数据库
    message = Messages(sender=sender, recipient=recipient, content=content)
    db.session.add(message)
    message = Messages(sender=recipient, recipient=sender, content=response)
    db.session.add(message)
    # 将AI的总结存入数据库
    summary_record = Summary.query.filter_by(user_id=sender).first()
    if summary_record is None:
        summary_record = Summary(user_id=sender, summary=summary)
        db.session.add(summary_record)
    else:
        summary_record.summary = summary
        summary_record.updated_at = db.func.now()
    db.session.commit()

  
    
    return jsonify({
        "设定": baby_settings,
        "记忆": memory,
        '意图': intents,
        "AI回复": response,
        "上下文总结": summary
    })