
import cv2
import mediapipe as mp
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CHARACTER_WIDTH = 40
CHARACTER_HEIGHT = 70
OBSTACLE_IMAGE_PATH="iceberg.jpg"
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 80
BACKGROUND_COLOR = (173, 216, 230)
BACKGROUND__IMAGE_PATH="BACKGROUND.jpeg"
SIDEBAR_COLOR = (255, 255, 255)
TEXT_COLOR = (0,0,0)
CHARACTER_IMAGE_PATH = "penguin-clip-art-penguin-png-image.jpg"  # Path to your image file
OBSTACLE_COLOR = (255, 0, 0)
background_image = pygame.image.load(BACKGROUND__IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture-Based Recovery Game")

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# Fonts
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

# Game variables
score = 0
obstacles = []
game_over = False

# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(CHARACTER_IMAGE_PATH)  # Load character image
        self.image = pygame.transform.scale(self.image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))  # Scale image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - CHARACTER_HEIGHT

        # Initialize jumping attributes
        self.is_jumping = False
        self.jump_count = 10  # Controls how high the character jumps

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 13  # Reset jump count for each new jump

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.3 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.rect.y = HEIGHT - CHARACTER_HEIGHT  # Reset position to ground

    def reset(self):
        self.rect.y = HEIGHT - CHARACTER_HEIGHT


# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(OBSTACLE_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Scale image to fit
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - OBSTACLE_HEIGHT

    def update(self):
        self.rect.x -= 5
        if self.rect.x < 0:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - OBSTACLE_HEIGHT
            global score
            score += 1


# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    fingers_raised = 0

    # Loop through each finger to check if it's raised
    for tip in finger_tips:
        # If the tip is above the knuckle, the finger is raised
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_raised += 1

    return fingers_raised


# Function to detect gesture
def detect_gesture(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Count raised fingers
            fingers_raised = count_raised_fingers(hand_landmarks)

            # Gesture based on number of raised fingers
            if fingers_raised == 1:
                return "walking"
            elif fingers_raised == 2:
                return "running"
            elif fingers_raised == 3:
                return "jumping"
            else:
                return "None"
    return "None"


# Draw sidebar
def draw_sidebar():
    pygame.draw.rect(screen, SIDEBAR_COLOR, (0, 0, 200, HEIGHT))
    instructions = [
        "Use hand gestures:",
        "Closed fist: Walking",
        "One fingers raised: Run",
        "Two finger raised: Jump",
    ]
    y_offset = 50
    for line in instructions:
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (10, y_offset))
        y_offset += 30


# Game loop
def game_loop():
    global game_over, score
    clock = pygame.time.Clock()
    character = Character()
    all_sprites = pygame.sprite.Group(character)
    obstacles_group = pygame.sprite.Group()
    score = 0
    game_over = False

    # Create obstacles
    for _ in range(5):
        obstacle = Obstacle()
        obstacles_group.add(obstacle)
        all_sprites.add(obstacle)

    cap = cv2.VideoCapture(0)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get the webcam feed
        ret, frame = cap.read()
        if not ret:
            break

        # Detect gestures
        gesture = detect_gesture(frame)

        # Handle actions based on gesture
        if gesture == "jumping":
            character.jump()
        elif gesture == "running":
            for obstacle in obstacles_group:
                obstacle.rect.x -= 10
        elif gesture == "walking":
            for obstacle in obstacles_group:
                obstacle.rect.x -= 5

        # Update character and obstacles
        all_sprites.update()

        # Collision check
        if pygame.sprite.spritecollideany(character, obstacles_group):
            game_over = True

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw the background image
        draw_sidebar()
        all_sprites.draw(screen)
        pygame.display.flip()

        # Display webcam feed in the right section
        webcam_surface = pygame.surfarray.make_surface(cv2.flip(frame, 1).swapaxes(0, 1))
        screen.blit(pygame.transform.scale(webcam_surface, (200, 150)), (800, 20))

        pygame.display.flip()

        # Show the webcam feed with gesture and landmarks
        cv2.imshow('Hand Gesture Monitor', frame)

        clock.tick(30)

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print(f"Game Over! Your final score is: {score}")


if __name__ == "__main__":
    game_loop()
