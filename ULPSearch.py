import os
import time
import platform
import re
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

ART = f"""
{Fore.MAGENTA}██╗   ██╗██╗     ██████╗ 
{Fore.MAGENTA}██║   ██║██║     ██╔══██╗
{Fore.MAGENTA}██║   ██║██║     ██████╔╝
{Fore.MAGENTA}██║   ██║██║     ██╔═══╝ 
{Fore.MAGENTA}╚██████╔╝███████╗██║     
{Fore.MAGENTA} ╚═════╝ ╚══════╝╚═╝     
{Fore.CYAN}      Combo Filter 
"""

def loading_bar(duration=2):
    # nicer progress bar with percent and elapsed time
    width = 30
    start = time.time()
    for i in range(width + 1):
        percent = i / width
        filled = int(percent * width)
        empty = width - filled
        bar = f"{Fore.MAGENTA}{'█'*filled}{Fore.WHITE}{'░'*empty}"
        elapsed = time.time() - start
        print(f"\r{Fore.CYAN}Processing {Fore.CYAN}[{bar}{Fore.CYAN}] {Fore.WHITE}{percent*100:6.2f}% {Fore.CYAN}Elapsed: {elapsed:4.1f}s", end="", flush=True)
        time.sleep(max(0, duration / width))
    print(f"\n{Fore.GREEN}[+] Done!\n")

def main():
    clear_screen()
    
    print(ART)
    time.sleep(1)
    time.sleep(0.8)
    
    keywords_file = "keywords.txt"
    
    if not os.path.exists(keywords_file):
        print(f"{Fore.RED}[-] Error: 'keywords.txt' file not found in the folder!")
        input(f"\n{Fore.CYAN}Press ENTER to exit...")
        return
    
    with open(keywords_file, 'r', encoding='utf-8', errors='ignore') as f:
        keywords = [line.strip() for line in f if line.strip()]
    
    print(f"{Fore.GREEN}[+] {len(keywords)} keywords loaded from {Fore.WHITE}keywords.txt")
    for i, kw in enumerate(keywords[:10], 1):
        print(f"{Fore.CYAN}[{i}] {Fore.WHITE}{kw}")
    if len(keywords) > 10:
        print(f"{Fore.CYAN}... and {len(keywords)-10} more")
    print()
    
    combo_dir = "Combo Files"
    if not os.path.isdir(combo_dir):
        print(f"{Fore.RED}[-] Error: '{combo_dir}' folder not found in the folder!")
        input(f"\n{Fore.CYAN}Press ENTER to exit...")
        return

    txt_files = [os.path.join(combo_dir, f) for f in os.listdir(combo_dir)
                 if f.lower().endswith('.txt') and f != keywords_file and not any(f.startswith(kw + '.') for kw in keywords)]
    
    if not txt_files:
        print(f"{Fore.RED}[-] No combo .txt files found in (Combo Files) folder!")
        input(f"\n{Fore.CYAN}Press ENTER to exit...")
        return
    
    print(f"{Fore.GREEN}[+] Found {len(txt_files)} combo file(s):")
    for f in txt_files:
        print(f"{Fore.WHITE}{os.path.basename(f)}")
    print()
    
    loading_bar(1.5)
    
    total_processed = 0
    created_files_count = 0
    
    for keyword in keywords:
        results = set()
        keyword_lower = keyword.lower()
        
        for txt_file in txt_files:
            try:
                with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if keyword_lower in line.lower():
                            results.add(line.strip())
            except Exception as e:
                print(f"{Fore.RED}Error reading {txt_file}: {e}")
        
        def clean_line(line):
            line = line.strip()
            # Try to find an email:password pattern first
            m = re.search(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}:[^\s:]+', line)
            if m:
                return m.group(0)
            # Fallback: take the last two colon-separated parts
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    return parts[-2] + ':' + parts[-1]
            return line

        cleaned = {clean_line(l) for l in results if clean_line(l)}
        cleaned_sorted = sorted(cleaned)
        count = len(cleaned_sorted)
        # Prepare output directory: Output Files/<account_name>/
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', keyword)
        base_output_dir = os.path.join(os.getcwd(), "Output Files")
        account_dir = os.path.join(base_output_dir, safe_name)
        os.makedirs(account_dir, exist_ok=True)

        output_file = f"{safe_name}.txt"
        output_path = os.path.join(account_dir, output_file)

        with open(output_path, 'w', encoding='utf-8') as out:
            for line in cleaned_sorted:
                out.write(line + '\n')

        if os.path.exists(output_path):
            created_files_count += 1

        total_processed += count
        print(f"{Fore.GREEN}[+] {Fore.WHITE}{keyword:<15} → {Fore.CYAN}{count:>6} accounts")
    print()

    # === Parte final estilo da imagem ===
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████╗██╗   ██╗ ██████╗ ██████╗ ███████╗███████╗███████╗   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ██╔════╝██║   ██║██╔════╝██╔════╝ ██╔════╝██╔════╝██╔════╝   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████╗██║   ██║██║     ██║      █████╗  ███████╗███████╗   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ╚════██║██║   ██║██║     ██║      ██╔══╝  ╚════██║╚════██║   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████║╚██████╔╝╚██████╗╚██████╗ ███████╗███████║███████║   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝    {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.WHITE}{' '*18}FILTERING COMPLETED SUCCESSFULLY{' '*18}{Fore.MAGENTA}               ")
    print(f"{Fore.MAGENTA}{Fore.GREEN}        Total Keywords Processed: {Fore.WHITE}{len(keywords)}{Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.GREEN}        Total Accounts Extracted: {Fore.CYAN}{total_processed}{Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.YELLOW}        Output Files Created: {Fore.WHITE}{created_files_count}{Fore.MAGENTA}")

    print()

    print(f"{Fore.CYAN}                >>> All filtered files saved in this folder <<<\n")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}                        Thank you for using Combo Filter ")
    
    input(f"{Fore.CYAN}                               Press ENTER to exit...")

if __name__ == "__main__":
    main()