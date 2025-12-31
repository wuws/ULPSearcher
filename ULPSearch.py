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
    print(f"{Fore.CYAN}[{Fore.WHITE}*{Fore.CYAN}] Processing", end="")
    for _ in range(20):
        time.sleep(duration / 20)
        print(f"{Fore.MAGENTA}█", end="", flush=True)
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
    
    txt_files = [f for f in os.listdir('.') if f.lower().endswith('.txt') 
                 and f != keywords_file and not any(f.startswith(kw + '.') for kw in keywords)]
    
    if not txt_files:
        print(f"{Fore.RED}[-] No combo .txt files found in the folder!")
        input(f"\n{Fore.CYAN}Press ENTER to exit...")
        return
    
    print(f"{Fore.GREEN}[+] Found {len(txt_files)} combo file(s):")
    for f in txt_files:
        print(f"    {Fore.WHITE}{f}")
    print()
    
    loading_bar(1.5)
    
    total_processed = 0
    
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
        output_file = f"{keyword}.txt"

        with open(output_file, 'w', encoding='utf-8') as out:
            for line in cleaned_sorted:
                out.write(line + '\n')

        total_processed += count
        print(f"{Fore.GREEN}[+] {Fore.WHITE}{keyword:<15} → {Fore.CYAN}{count:>6} accounts → {Fore.WHITE}{output_file}")
    print()

    # === Parte final estilo da imagem ===
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████╗██╗   ██╗ ██████╗ ██████╗ ███████╗███████╗███████╗   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ██╔════╝██║   ██║██╔════╝██╔════╝ ██╔════╝██╔════╝██╔════╝   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████╗██║   ██║██║     ██║      █████╗  ███████╗███████╗   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ╚════██║██║   ██║██║     ██║      ██╔══╝  ╚════██║╚════██║   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ███████║╚██████╔╝╚██████╗╚██████╗ ███████╗███████║███████║   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.CYAN}   ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝    {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.WHITE}{' '*18}FILTERING COMPLETED SUCCESSFULLY{' '*18}{Fore.MAGENTA}               ")
    print(f"{Fore.MAGENTA}{Fore.GREEN}        Total Keywords Processed: {Fore.WHITE}{len(keywords):>8}    {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.GREEN}        Total Accounts Extracted: {Fore.CYAN}{total_processed:>8}   {Fore.MAGENTA}")
    print(f"{Fore.MAGENTA}{Fore.YELLOW}        Output Files Created:     {Fore.WHITE}{len([k for k in keywords if os.path.exists(f'{k}.txt')]):>8}{Fore.MAGENTA}")

    print()

    print(f"{Fore.CYAN}                >>> All filtered files saved in this folder <<<\n")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}                        Thank you for using Combo Filter ")
    
    input(f"{Fore.CYAN}                                 Press ENTER to exit...")

if __name__ == "__main__":
    main()