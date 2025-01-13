import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound playback
pygame.mixer.init()

# Load the sound files
tick_sound = pygame.mixer.Sound('tick.wav')
minute_sound = pygame.mixer.Sound('min.wav')
hour_sound = pygame.mixer.Sound('hour.wav')

# Load the background image (dsclock.png)
background = pygame.image.load('dsclock.png')

# Set up the display to be resizable
size = 97  # Fixed dimensions (width and height)
screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)
pygame.display.set_caption("Analog Clock")

# Clock parameters (relative proportions)
hour_hand_length_ratio = 0.216  # 21px of 97px (width) for the hour hand
minute_hand_length_ratio = 0.289  # 28px of 97px for the minute hand
second_hand_length_ratio = 0.34  # 33px of 97px for the second hand
alarm_hand_length = 16  # Length of the alarm hand in pixels
hand_width = 2  # All hands are 2 pixels wide
center_square_size_ratio = 0.0412  # 4px of 97px for the central square

# Colors
second_hand_color = (0, 89, 243)  # #0059f3 color for second hand
hand_color = (121, 121, 121)  # #797979 color for hour and minute hands
alarm_hand_color = (251, 89, 113)  # #fb5971 color for the alarm hand
center_color = (73, 73, 73)  # #494949 color for the central square

# Initialize alarm time
alarm_hour = None
alarm_minute = None

# Prompt for alarm input
while True:
    alarm_time_input = input("Enter alarm time (HH:MM in 24-hour format): ")
    try:
        alarm_hour, alarm_minute = map(int, alarm_time_input.split(':'))
        if 0 <= alarm_hour < 24 and 0 <= alarm_minute < 60:
            break
        else:
            print("Invalid input. Please enter values within the specified ranges (HH:MM).")
    except ValueError:
        print("Invalid input format. Please use HH:MM (e.g., 23:59).")

# Helper function to calculate the hand positions
def get_hand_position(center, length, angle):
    rad = math.radians(angle)
    x = center[0] + length * math.sin(rad)
    y = center[1] - length * math.cos(rad)
    return int(x), int(y)

# Function to draw the clock
def draw_clock(screen, size, hour, minute, second, alarm_hour, alarm_minute):
    # Scale the background image to the current window size
    background_scaled = pygame.transform.scale(background, (size, size))
    screen.blit(background_scaled, (0, 0))

    # Recalculate the center and hand lengths based on the new window size
    center = (size // 2, size // 2)
    hour_hand_length = int((hour_hand_length_ratio * size))
    minute_hand_length = int((minute_hand_length_ratio * size))
    second_hand_length = int((second_hand_length_ratio * size))
    center_square_size = int(center_square_size_ratio * size)

    # Calculate angles for the hands
    second_angle = 360 * (second / 60)
    minute_angle = 360 * (minute / 60) + (second / 60) * 6
    hour_angle = 360 * (hour % 12 / 12) + (minute / 60) * 30
    alarm_angle = 360 * (alarm_hour % 12 / 12) + (alarm_minute / 60) * 30

    # Draw the alarm hand first (below all other hands)
    pygame.draw.line(screen, alarm_hand_color, center, get_hand_position(center, alarm_hand_length, alarm_angle), hand_width)  # Alarm hand

    # Draw the hour and minute hands with #797979 color
    pygame.draw.line(screen, hand_color, center, get_hand_position(center, hour_hand_length, hour_angle), hand_width)  # Hour hand
    pygame.draw.line(screen, hand_color, center, get_hand_position(center, minute_hand_length, minute_angle), hand_width)  # Minute hand

    # Draw the second hand last to layer it on top, with #0059f3 color
    pygame.draw.line(screen, second_hand_color, center, get_hand_position(center, second_hand_length, second_angle), hand_width)  # Second hand

    # Draw the central square with color #494949
    pygame.draw.rect(screen, center_color, pygame.Rect(center[0] - center_square_size // 2, center[1] - center_square_size // 2, center_square_size, center_square_size))

# Get current time to initialize the last time values
t = time.localtime()
last_second = t.tm_sec  # Start with the current second
last_minute = t.tm_min  # Start with the current minute
last_hour = t.tm_hour   # Start with the current hour

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:  # Handle window resizing
            new_size = min(event.w, event.h)  # Maintain square aspect ratio
            size = max(new_size, 97)  # Ensure a minimum size
            screen = pygame.display.set_mode((size, size), pygame.RESIZABLE)

    # Get current time
    t = time.localtime()
    hour, minute, second = t.tm_hour, t.tm_min, t.tm_sec

    # Play the second sound (tick.wav) if a new second occurs
    if second != last_second:
        tick_sound.play()
        last_second = second

    # Play the minute sound (min.wav) if a new minute occurs
    if minute != last_minute:
        minute_sound.play()
        last_minute = minute

    # Play the hour sound (hour.wav) if a new hour occurs
    if hour != last_hour:
        hour_sound.play()
        last_hour = hour

    # Draw the clock with the current size
    draw_clock(screen, size, hour, minute, second, alarm_hour, alarm_minute)

    # Update display
    pygame.display.flip()

    # Control the frame rate (1 frame per second)
    pygame.time.wait(1000)

# Quit Pygame
pygame.quit()
