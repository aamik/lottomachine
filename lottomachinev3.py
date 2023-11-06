# VAIHDA TÄSTÄ MONTAKO NUMEROA (7) MONESTAKO NUMEROSTA ARVOTAAN (40) 
NUM_LOTTERY_NUMBERS = 7 # Ns. lottorivi, kuinka monta numeroa kaikista vaihtoehdoista voidaan valita, vakiomuuttujat isoin kirjaimin
RANGE_OF_NUMBERS = 40 # Lottokoneen sisältämät numerot, eli kaikki vaihtoehdot


# Tuodaan ensimmäisenä tarvittavat moduulit
import random
import math
import time
from unittest import result # ?????????????????
import tkinter as tk
import os
from tkinter import filedialog
from matplotlib.lines import lineStyles # ??????????????????
import matplotlib.pyplot as plt # numpya ei tällä datalla tarvita

# Määritellään matplotlibin muuttujat
plt.ion()

# Tuodaan oma moduuli animaatiolle harjoitusmielessä
import lotto_animation


all_results = []


#Luokka Lottery sisältää tarvittavat määritelmät NUM_LOTTERY_NUMBERS/RANGE_OF_NUMBERS tyyppisen loton lukujen arvontaan
class Lottery:
    def __init__(self):
        self.lottery_numbers = set()

# Tässä käytetään pythonin random-moduulin sisäänrakennettua random.sample -funktiota
    def draw_numbers(self):
        self.lottery_numbers = set(random.sample(range(1, RANGE_OF_NUMBERS + 1), NUM_LOTTERY_NUMBERS))

    def check_results(self, user_numbers):
        matched_numbers = user_numbers.intersection(self.lottery_numbers)
        num_matched = len(matched_numbers)
        return num_matched, matched_numbers


# Matemaattisia kombinaatioita eli loton todennäköisyyksiä voi laskea suoraan math-moduulin math.comb-funktiolla
def calculate_probability(num_matched):
    total_combinations = math.comb(RANGE_OF_NUMBERS, NUM_LOTTERY_NUMBERS)       
    favorable_outcomes = math.comb(NUM_LOTTERY_NUMBERS, num_matched) * math.comb(RANGE_OF_NUMBERS - NUM_LOTTERY_NUMBERS, NUM_LOTTERY_NUMBERS - num_matched) 
    probability = favorable_outcomes / total_combinations
    results = (num_matched, probability)
    all_results.append(results)
    return probability
    

# Jokaista lottoriviä voi myös ajatella itsenäisenä todennäköisyytenä, mutta lasketaan monen yrityksen kumuloituva todennäköisyys
# Kumuloituva todennäköisyys on laskettu todennäköisyys voitolle (kullekin lottoriville) ** yritysten lukumäärä
# Piirretään tämä todennäköisyys matplotlibillä
def plot_cumulative_probability(num_tries):
    
    probabilities = [1 - (1 - calculate_probability(i))**num_tries for i in range(0, 8)]
    plt.plot(range(0, 8), probabilities, label=f"Try {num_tries}", linestyle="-", alpha=0.6)

    plt.xlabel("Number of Matches")
    plt.ylabel("Cumulative Probability after {} tries".format(num_tries))
    plt.title("Cumulative Probability of Getting 0-7 matches in {} tries".format(num_tries))
    plt.legend(loc="upper right")
      
    
    plt.show()

# Käyttäjän valitsemat luvut joiden lukumäärä = NUM_LOTTERY_NUMBERS
def get_user_numbers():
    while True:
        try:
            user_numbers = input(f"Enter your {NUM_LOTTERY_NUMBERS} lottery numbers between 1 and {RANGE_OF_NUMBERS}, separated by spaces: ").split()
            user_numbers = [int(number) for number in user_numbers]
            if len(user_numbers) != NUM_LOTTERY_NUMBERS or any(number < 1 or number > RANGE_OF_NUMBERS for number in user_numbers):
                print(f"Please enter {NUM_LOTTERY_NUMBERS} unique numbers between 1 and {RANGE_OF_NUMBERS}.")
            else:
                return set(user_numbers)
        except ValueError:
            print("Invalid input. Please enter numbers only.")



# Pääfunktio jossa kaikki muu ajetaan
def main():
    print("Welcome to the Lottery Machine!")
    play_again = "y"
    num_tries = 1 # "Yritys 0" kuulostaisi oudolta

    
    best_result = (0, 0.0)


    print(f"Here you can choose {NUM_LOTTERY_NUMBERS} numbers out of {RANGE_OF_NUMBERS} possible lottery numbers")
    user_numbers = get_user_numbers()  # Tallennetaan käyttäjän numerot valmiiksi, eikä loopata valintaprosessia
    plt.figure(figsize=(10, 6))



    # Uudestaanpeluu-looppi
    while play_again.lower() == "y" or "p":
        try:                    
            lottery = Lottery()
            lottery.draw_numbers()

            # Näytetään animaatio vain ensimmäisellä kerralla
            if num_tries == 1:
                lotto_animation.rolling_drum_animation()
                lotto_animation.ending_animation()

            # Tauko käyttäjän lukuajalle ja dramaattisen efektin takia
            time.sleep(0.8)
            
            num_matched, matched_numbers = lottery.check_results(user_numbers)
            print(f"You matched {num_matched} {"number" if num_matched == 1 else "numbers"}: {matched_numbers if matched_numbers else ""}")   
            
            probability = calculate_probability(num_matched)
            print(f"Probability of matching {num_matched} {"number" if num_matched == 1 else "numbers"}: {probability:.6f}")

            # Otetaan ylös kaikkien ajojen paras tulos
            if num_matched > best_result[0]:
                best_result = (num_matched, probability)

            
            
            if num_tries == 1:
                time.sleep(0.8)
                print("Let's plot the results")
           
                       
       # Kaikki main()-funktion mahdolliset poikkeukset samassa
        except Exception as e:
            print(f"An error occurred: {e}")
            
        finally:
            # Piirretään kumulatiivisen todennäköisyyden kuvaaja
            plot_cumulative_probability(num_tries)

            # Uudestaanpeluu-looppi
            print("Your cumulative probability changes according to the number of matches you get in subsequent runs.")
            play_again = input("Would you like to play again using your inputted numbers? \n (y=yes, n=no (exit), p=plot 10 runs, s=save results): ")
            if play_again.lower() == "y":
                num_tries += 1

            elif play_again.lower() == "p":
                for _ in range(10):
                    num_tries += 1
                    plot_cumulative_probability(num_tries)
                
                    plt.pause(0.2) # Ehkäistään matplotlibin kaatuminen käyttämällä tauotusta


            
            
            # Haluaako käyttäjä tallentaa tulokset tekstitiedostoon, a = append
            elif play_again.lower() == "s":
                try:
                    root = tk.Tk()
                    root.withdraw()  # Piilotetaan tk-ikkuna

                    # Kysytään käyttäjältä mihin kansioon tiedosto tallennetaan
                    print("Select a folder (where admin rights are not needed)")
                    folder_selected = filedialog.askdirectory()

                    # Jos kansio on valittu, tallenetaan ajojen tiedot
                    if folder_selected:
                        with open(os.path.join(folder_selected, "lottoresults.txt"), "w") as file:
                            num_matched, probability = best_result
                            file.write(f"Best Result: {num_matched} matches with probability {probability:.6f} in {num_tries} tries\n")
                        print(f"The best result has been saved to {folder_selected} as lottoresults.txt")
                    else:
                        print("No folder selected.")


                except PermissionError:
                    print("Error: Permission denied. Unable to save the results.")
                except OSError as e:
                    print(f"Error occurred while saving results: {e}")
                except Exception as ee:
                    print(f"Unexpected error: {ee}")
      
                
                    
            elif play_again.lower() == "n":
                print("Hopefully you enjoyed the game, please come again!")
                exit()

            else:
                print("You should answer y/n/s/p, closing the program")
                exit()
                


# Tässä main() ajetaan vain, jos Pythonin kääntäjä on nimennyt tiedoston "__main__", joka tarkoittaa, että main-funktiota ollaan ajamassa suoraan
if __name__ == "__main__":
    main()



