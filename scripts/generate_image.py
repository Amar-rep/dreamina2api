#!/usr/bin/env python3
"""
Dreamina 图片生成脚本

使用方法：
    python generate_image.py --prompt "画一个苹果" --token "YOUR_SESSION_ID"
    python generate_image.py --prompt "画一个苹果" --token "YOUR_SESSION_ID" --ratio "16:9"
    
可选参数：
    --prompt    图片描述 (必填)
    --token     Dreamina session ID (必填)
    --ratio     图片比例，支持: 1:1, 3:4, 4:3, 9:16, 16:9, 2:3, 3:2, 21:9 (默认: 1:1)
    --output    输出目录 (默认: 当前目录)
    --api       API地址 (默认: http://localhost:5200)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


def parse_args():
    parser = argparse.ArgumentParser(description="Dreamina 图片生成脚本")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述")
    parser.add_argument("--token", "-t", required=True, help="Dreamina session ID")
    parser.add_argument("--ratio", "-r", default="1:1", 
                       choices=["1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2", "21:9"],
                       help="图片比例 (默认: 1:1)")
    parser.add_argument("--output", "-o", default=".", help="输出目录 (默认: 当前目录)")
    parser.add_argument("--api", default="http://localhost:5200", help="API地址")
    return parser.parse_args()


def generate_images(api_url: str, token: str, prompt: str, ratio: str) -> list:
    """调用生成API"""
    url = f"{api_url}/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "prompt": prompt,
        "ratio": ratio,
        "response_format": "url"
    }
    
    print(f"[生成] 正在提交生成请求...")
    print(f"  Prompt: {prompt}")
    print(f"  Ratio: {ratio}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=600)
        response.raise_for_status()
        result = response.json()
        
        if "data" in result:
            urls = [item.get("url") for item in result["data"] if item.get("url")]
            print(f"[生成] 成功! 获得 {len(urls)} 张图片")
            return urls
        else:
            print(f"[错误] 响应格式异常: {result}")
            return []
            
    except requests.exceptions.Timeout:
        print("[错误] 请求超时 (10分钟)")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[错误] 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"  详情: {json.dumps(error_detail, ensure_ascii=False, indent=2)}")
            except:
                print(f"  响应: {e.response.text[:500]}")
        return []


def download_image(url: str, output_dir: Path, index: int) -> str:
    """下载单张图片"""
    try:
        # 从URL提取文件扩展名
        parsed = urlparse(url)
        path = parsed.path
        
        # 尝试从URL获取格式
        if "format=.jpeg" in url or "format=.jpg" in url:
            ext = "jpg"
        elif "format=.png" in url:
            ext = "png"
        elif "format=.webp" in url:
            ext = "webp"
        else:
            # 从路径获取
            ext = Path(path).suffix.lstrip('.') or "jpg"
        
        # 生成文件名
        timestamp = int(time.time())
        filename = f"dreamina_{timestamp}_{index:02d}.{ext}"
        filepath = output_dir / filename
        
        print(f"  [{index+1}] 下载中... ", end="", flush=True)
        
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        file_size = filepath.stat().st_size
        print(f"完成 ({file_size / 1024:.1f} KB) -> {filepath.name}")
        return str(filepath)
        
    except Exception as e:
        print(f"失败: {e}")
        return ""


def main():
    args = parse_args()
    
    # 确保输出目录存在
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Dreamina 图片生成")
    print("=" * 60)
    print(f"API: {args.api}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 生成图片
    start_time = time.time()
    image_urls = generate_images(args.api, args.token, args.prompt, args.ratio)
    generation_time = time.time() - start_time
    
    if not image_urls:
        print("\n[失败] 未能生成图片")
        return 1
    
    print(f"\n[耗时] 生成用时: {generation_time:.1f} 秒")
    
    # 下载图片
    print(f"\n[下载] 开始下载 {len(image_urls)} 张图片...")
    downloaded = []
    
    for i, url in enumerate(image_urls):
        filepath = download_image(url, output_dir, i)
        if filepath:
            downloaded.append(filepath)
    
    # 总结
    print()
    print("=" * 60)
    print(f"[完成] 成功下载 {len(downloaded)}/{len(image_urls)} 张图片")
    print(f"[位置] {output_dir}")
    print("=" * 60)
    
    if downloaded:
        print("\n生成的图片:")
        for path in downloaded:
            print(f"  - {path}")
    
    return 0 if downloaded else 1


if __name__ == "__main__":
    sys.exit(main())
