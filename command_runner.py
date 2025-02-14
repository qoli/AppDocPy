import subprocess

def run_command(command):
    """執行命令並返回輸出"""
    try:
        result = subprocess.run(command, 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"錯誤: {e.stderr.strip()}")
        return None

if __name__ == "__main__":
    # 示例：執行 git status
    output = run_command("git status")
    if output:
        print(output)