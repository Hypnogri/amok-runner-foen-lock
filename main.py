import asyncio
import pygame
import time
import random

async def main():
    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    FONT_SIZE = 32

    # Initialize Pygame
    pygame.init()

    # Set up the display window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('4 Number Lock')

    # Set up the font for rendering text
    font = pygame.font.Font(None, FONT_SIZE)

    # Set up the current cursor position
    cursor_pos = 0

    # Set up the start time
    start_time = time.time()

    # state of the lock
    solved = False
    # Set up the game loop
    running = True

    # all possibilities
    two_letters = ['ON', 'NF', 'NO', 'FO', 'FN']
    two_letter_code = [[5, 8, 6, 1], [8, 1, 6, 5], [8, 5, 6, 1], [1, 5, 6, 8], [1, 8, 5, 6]]

    # Set up the lock code
    letters = random.choice(two_letters)
    lock_code = two_letter_code[two_letters.index(letters)]

    # Set up the current guess (starting position)
    guess = [0, 0, 0, 0]

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    guess = [0, 0, 0, 0]
                    cursor_pos = 0
                    solved = False
                    letters = random.choice(two_letters)
                    lock_code = two_letter_code[two_letters.index(letters)]
                    start_time = time.time()
                elif event.key == pygame.K_s:
                    # Increment the current guess at the cursor position
                    guess[cursor_pos] = (guess[cursor_pos] + 1) % 10
                    if guess == lock_code:
                        solved = True
                elif event.key == pygame.K_w:
                    # Decrement the current guess at the cursor position
                    guess[cursor_pos] = (guess[cursor_pos] - 1) % 10
                    if guess == lock_code:
                        solved = True
                elif event.key == pygame.K_d:
                    # Move the cursor to the right
                    cursor_pos = (cursor_pos + 1) % 4
                elif event.key == pygame.K_a:
                    # Move the cursor to the left
                    cursor_pos = (cursor_pos - 1) % 4

        # Clear the screen
        screen.fill((255, 255, 255))

        # Render the current guess
        for i, g in enumerate(guess):
            text = font.render(str(g), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH * (i + 1) / 5, SCREEN_HEIGHT / 2)
            screen.blit(text, text_rect)

        # Render the numbers above the current guess
        for i, g in enumerate(guess):
            above_number = (g - 1) % 10
            above_text = font.render(str(above_number), True, (192, 192, 192))
            above_text_rect = above_text.get_rect()
            above_text_rect.center = (SCREEN_WIDTH * (i + 1) / 5, SCREEN_HEIGHT / 2 - FONT_SIZE)
            screen.blit(above_text, above_text_rect)

        # Render the numbers below the current guess
        for i, g in enumerate(guess):
            below_number = (g + 1) % 10
            below_text = font.render(str(below_number), True, (192, 192, 192))
            below_text_rect = below_text.get_rect()
            below_text_rect.center = (SCREEN_WIDTH * (i + 1) / 5, SCREEN_HEIGHT / 2 + FONT_SIZE)
            screen.blit(below_text, below_text_rect)

        # Render the cursor
        cursor_width = SCREEN_WIDTH / 5
        cursor_height = FONT_SIZE * 3
        cursor_x = SCREEN_WIDTH * (cursor_pos + 1) / 5 - cursor_width / 2
        cursor_y = SCREEN_HEIGHT / 2 - FONT_SIZE * 1.5
        pygame.draw.rect(screen, (0, 0, 0), (cursor_x, cursor_y, cursor_width, cursor_height), 2)

        # Render "ESC to reset" text
        reset_text = font.render("ON - 5861, NF - 8165, NO - 8561, FO - 1568, FN - 1856", True, (0, 0, 0))
        reset_text_rect = reset_text.get_rect()
        reset_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8)
        screen.blit(reset_text, reset_text_rect)

        # Render the timer
        if not solved:
            elapsed_time = time.time() - start_time
            timer_text = font.render('Timer: {:.1f}'.format(elapsed_time), True, (0, 0, 0))
        else:
            timer_text = font.render('Final Time: {:.1f}   (ESC or ENTER or SPACE to reset)'.format(elapsed_time), True, (0, 0, 0))
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8)
        screen.blit(timer_text, timer_text_rect)

        # letters below timer
        letters_text = font.render('{}'.format(letters), True, (0, 0, 0))
        letters_text_rect = letters_text.get_rect()
        letters_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8 + FONT_SIZE)
        screen.blit(letters_text, letters_text_rect)

        # Update the display
        pygame.display.update()

        # Frame rate limit
        time.sleep(1 / 60)
        await asyncio.sleep(0)

    if not running:
        pygame.quit()
        return

asyncio.run(main())