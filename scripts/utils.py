import pygame

def draw_text(screen, text, left, top, color, font):
    text_generate = font.render(text, True, color)
    text_generate_rect = text_generate.get_rect(midtop = (left, top))

    screen.blit(text_generate, text_generate_rect)