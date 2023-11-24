import pygame
import simulation
import entities
import level

from collections import defaultdict

def count_character_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        if 'A' <= char <= 'z':
            frequency[char] += 1
    return frequency

if __name__ == "__main__":
    input_text = input("Wprowadź tekst: ")
    character_frequency = count_character_frequency(input_text)
    
    for char, count in character_frequency.items():
        print(f"Litera '{char}' wystąpiła {count} razy.")


print("Zmiana wprowadzona przez Konrada!")

