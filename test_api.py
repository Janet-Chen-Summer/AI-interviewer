#!/usr/bin/env python
"""
test_api_fixed.py - 正确处理 reasoning_content
"""

import os
import time
from dotenv import load_dotenv
from zhipuai import ZhipuAI

def test_api():
    print("=" * 50)
    print("🔑 测试智谱API (正确处理reasoning_content)")
    print("=" * 50)
    
    load_dotenv()
    api_key = os.getenv("ZHIPUAI_API_KEY")
    
    if not api_key:
        print("❌ 未找到API Key")
        return False
    
    masked_key = api_key[:6] + "..." + api_key[-4:]
    print(f"📌 API Key: {masked_key}")
    
    try:
        client = ZhipuAI(api_key=api_key)
        
        # 修改提示词，避免触发reasoning模式
        response = client.chat.completions.create(
            model="glm-4.7-flash",
            messages=[
                {"role": "user", "content": "你叫什么名字?"}
            ],
            temperature=0.8,
            max_tokens=50
        )
        
        print("✅ 调用成功！")
        
        # 检查各种可能的返回字段
        if response.choices and len(response.choices) > 0:
            message = response.choices[0].message
            
            # 尝试获取content
            content = getattr(message, 'content', '')
            if content:
                print(f"📝 content: {content}")
            
            # 尝试获取reasoning_content
            reasoning = getattr(message, 'reasoning_content', '')
            if reasoning:
                print(f"🧠 reasoning: {reasoning}")
            
            # 如果有content就用content，否则用reasoning
            final_response = content if content else reasoning
            if final_response:
                print(f"🤖 最终回复: {final_response}")
            else:
                print("⚠️ 两个字段都为空")
        
        print(f"📊 Token使用: {response.usage}")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    test_api()