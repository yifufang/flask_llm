from .models import db, Summary, BabySettings

INTENT_KEYWORDS = {
    "喂食建议": [
        "吃饭", "蔬菜", "喂养", "母乳", "奶粉"
    ],
    "睡眠建议": [
        "入睡", "午睡", "睡觉", "醒来", "失眠"
    ],
    "健康建议": [
        "发烧", "健康", "过敏", "拉肚子", "疫苗"
    ],
    "查看": [
        "查询", "查看", "读出", "上次", "历史"
    ],
    "打招呼": [
        "你好", "早上好", "下午好", "晚上好", "你好"
    ],
}


class User():
    """
    用户类, 用于处理用户的基本信息
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def get_summary(self):
        """
        获取用户和AI交互的历史概括
        """
        summary = Summary.query.filter_by(user_id=self.user_id).first()
        if summary is None:
            return ""
        return summary.summary

    def get_baby_settings(self):
        """
        获取宝宝的设定
        """
        settings = BabySettings.query.filter_by(user_id=self.user_id).first()
        if settings is None:
            return ""
        return settings.to_dict()

    def purpose(self, content):
        """
        简易rule based关键词匹配，用户的意图识别
        """

        for intent, keywords in INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content:
                    return intent
        return "其他"
