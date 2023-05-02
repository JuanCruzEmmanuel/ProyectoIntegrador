import pygame

pygame.init()

print_message = pygame.USEREVENT + 0
pygame.time.set_timer(print_message, 10)

while True:
    for event in pygame.event.get():
        if event.type == print_message:
            print("Hello World")