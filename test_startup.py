from modules.startup_manager import StartupManager

def main():
    sm = StartupManager()
    items = sm.get_all_startup_items()
    print("找到的启动项:")
    for item in items:
        print(f"名称: {item['name']}")
        print(f"命令: {item['command']}")
        print(f"位置: {item['location']}")
        print(f"类型: {item['type']}")
        print(f"启用状态: {'是' if item['enabled'] else '否'}")
        print("-" * 50)

if __name__ == "__main__":
    main() 