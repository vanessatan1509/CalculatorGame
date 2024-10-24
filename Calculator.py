import pygame
import sys
import math
from decimal import Decimal, getcontext

# Set precision for Decimal operations
getcontext().prec = 10  # You can adjust this value for more precision if needed

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 590, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font settings
FONT = pygame.font.Font(None, 48)

# Calculator state
input_string = ""
result_string = ""

# Button layout values
button_values = [
    "7", "8", "9", "/", "√",
    "4", "5", "6", "*", "^",
    "1", "2", "3", "-", "Del",
    "0", ".", "=", "+", "C"
]

# Create buttons with coordinates
buttons = [(button_values[i], 50 + (i % 5) * 100, 150 + (i // 5) * 100) for i in range(len(button_values))]

def format_number(number):
    """Format number for better readability."""
    if number < 0.0001:
        return f"{number:.2e}"  # Format as scientific notation
    else:
        return f"{number:.5f}"  # Format with five decimal places

def evaluate_expression(expression):
    try:
        # Replace "^" with "**" for power calculations
        expression = expression.replace("^", "**")
        
        # Handle square root
        if "√" in expression:
            parts = expression.split("√")
            if len(parts) > 1:
                root_value = Decimal(parts[1])  # Use Decimal
                if root_value < 0:
                    return "Error"  # Handle negative root
                result = root_value.sqrt()
                return format_number(result)  # Return formatted result

        # Evaluate the expression with Decimal
        result = eval(expression)
        decimal_result = Decimal(result)

        return format_number(decimal_result)  # Return formatted result
    except Exception:
        return "Error"
    
def draw_buttons():
    for (text, x, y) in buttons:
        pygame.draw.rect(screen, GRAY, (x, y, 80, 80))
        text_surface = FONT.render(text, True, BLACK)
        screen.blit(text_surface, (x + 10, y + 25))  # Adjusted for center alignment

def button_clicked(pos):
    global input_string, result_string
    for (text, x, y) in buttons:
        if x < pos[0] < x + 80 and y < pos[1] < y + 80:
            if text == 'C':
                input_string = ""
                result_string = ""
            elif text == 'Del':
                input_string = input_string[:-1]  # Remove last character
            elif text == '=':
                result_string = evaluate_expression(input_string)
                input_string = ""
            else:
                input_string += text

# Main game loop
while True:
    screen.fill(WHITE)
    draw_buttons()

    # Display the current input and result
    input_surface = FONT.render(input_string, True, BLACK)
    result_surface = FONT.render(result_string, True, BLACK)
    
    # Display positions
    screen.blit(input_surface, (50, 50))
    screen.blit(result_surface, (50, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                button_clicked(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.unicode.isdigit() or event.unicode in "+-*/^√.":
                input_string += event.unicode
            elif event.key == pygame.K_BACKSPACE:  # Handle backspace for deleting
                input_string = input_string[:-1]

    pygame.display.flip()
