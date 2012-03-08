import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16
LINE_THICKNESS = 3

# Load sounds
def load_sound(sound_name):
	try:
		sound = pygame.mixer.Sound(sound_name)
	except pygame.error, message:
		print "Can't load sound: " + sound_name
		raise SystemExit, message
	return sound

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Opponent's paddle vertically centered on the right side
opp_paddle_rect = pygame.Rect((SCREEN_WIDTH - 2*PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball
score = 0
opp_score = 0 # Opponent's score

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:

	# Win conditions	
	if score >= 11:
		pygame.time.delay(1000) # So we can see the score a little longer
		screen.fill((255, 255, 255))
		win_message = font.render(str("Left player has won! Press SPACE to play again."), True, (0, 0, 0))
		screen.blit(win_message, ((SCREEN_WIDTH / 2) - font.size(str("Left player has won! Press SPACE to play again."))[0] / 2, SCREEN_HEIGHT/2))
		pygame.display.flip()
		wait = True
		while wait == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
				    pygame.quit()
				    sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						score = 0
						opp_score = 0
						wait = False
			pygame.time.delay(20)
	if opp_score >= 11:
		pygame.time.delay(1000) # So we can see the score a little longer
		screen.fill((255, 255, 255))
		win_message = font.render(str("Right player has won! Press SPACE to play again."), True, (0, 0, 0))
		screen.blit(win_message, ((SCREEN_WIDTH / 2) - font.size(str("Right player has won! Press SPACE to play again."))[0] / 2, SCREEN_HEIGHT/2))
		pygame.display.flip()
		wait = True
		while wait == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
				    pygame.quit()
				    sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						score = 0
						opp_score = 0
						wait = False
			pygame.time.delay(20)

	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
		
	# If W or S keys pressed, move opponent's paddle
	elif pygame.key.get_pressed()[pygame.K_w] and opp_paddle_rect.top > 0:
		opp_paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and opp_paddle_rect.bottom < SCREEN_HEIGHT:
		opp_paddle_rect.top += BALL_SPEED
		
	# If ESC pressed, quit
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with top/bottom rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	
	# Ball collision with walls (scoring)
	if ball_rect.right >= SCREEN_WIDTH:
		pygame.time.delay(1000) # If ball hits opponent's wall, pause for a second, then put the ball back in center
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
		score += 1 # You score a point!
	if ball_rect.left <= 0:
		pygame.time.delay(1000) # If ball hits opponent's wall, pause for a second, then put the ball back in center
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
		opp_score += 1 # Opponent scores a point :(

	# Test if the ball is hit by the paddle; if yes reverse speed and play sound
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		sound = load_sound("pong1.wav")
		sound.play()
	if opp_paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		sound = load_sound("pong2.wav")
		sound.play()
	
	# Clear screen
	screen.fill((255, 255, 255))

	# Draw the middle line
	pygame.draw.line(screen, (255, 0, 0), (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), LINE_THICKNESS)

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), opp_paddle_rect) # Opponent's paddle
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text = font.render(str(score), True, (0, 0, 0))
	opp_score_text = font.render(str(opp_score), True, (0, 0, 0))
	screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # Your score
	screen.blit(opp_score_text, ((SCREEN_WIDTH * 3/4) - font.size(str(opp_score))[0] / 2, 5)) # Opponent's score
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)