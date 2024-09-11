import csv
import sys

def count(fichier_csv):
    try:
        with open(fichier_csv, mode='r', encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier)
            total = 0
            OK = 0
            FalsePositive = 0
            Missedattack = 0
            BadAddress = 0
            OutOfContext = 0
            
            for ligne in lecteur:
                analyse = ligne.get('analyse')
                if analyse == 'OK +5':
                    OK += 1
                elif analyse == 'False positive -5':
                    FalsePositive += 1
                elif analyse == 'LLM missed an attack -1':
                    Missedattack += 1
                elif analyse == 'Bad IP attack -3':
                    BadAddress += 1
                elif analyse == 'Out of context':
                    OutOfContext += 1
                total += 1
            print(f"{OK} OK on {total} requests: {OK/total*100:.2f}%")
            print(f"{FalsePositive} false positive on {total} requests: {FalsePositive/total*100:.2f}%")
            print(f"{Missedattack} undetected attacks on {total} requests: {Missedattack/total*100:.2f}%")
            print(f"{BadAddress} wrong address detected on {total} requests: {BadAddress/total*100:.2f}%")
            print(f"{OutOfContext}  Out of context on {total} requests: {OutOfContext/total*100:.2f}%")

    except FileNotFoundError:
        print("The specified file cannot be found.")
    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 CountScore.py <csv_file_path>")
    else:
        fichier = sys.argv[1]
        llm = fichier.split('_')
        print(f"results for {llm[0]}:")
        count(fichier)