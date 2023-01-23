import pygame
pygame.font.init()

#setting up the screen
width = 800
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Wars!")


#setting up variables with their specific colour codes
White = (255, 255, 255)
Blue = (0, 0, 255)
Red = (255, 0, 0)

#the boundary in the middle of the screen that would separate the ships from each other
boundary = pygame.Rect(width//2 - 13, 0, 10, height)

#the variables to show the winner and health fonts
health_font = pygame.font.SysFont('timesnewroman', 30)
win_font = pygame.font.SysFont('timesnewroman', 100)

fps = 60
vel = 5
laser_vel = 7
max_laser = 3
ship_width = 70
ship_height = 55

white_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

#loading up the white ship image and rotating it to face the direction of the red ship
white_ship_img = pygame.image.load('white1.png')
white_ship = pygame.transform.rotate(pygame.transform.scale(white_ship_img, (ship_width, ship_height)), 270)

#loading up the red ship image and rotating it to face the direction of the white ship
red_ship_img = pygame.image.load('redred.png')
red_ship = pygame.transform.rotate(pygame.transform.scale(red_ship_img, (ship_width, ship_height)), 270)

#loading up the space background
space_bg = pygame.image.load('space1.png')

#creating a function to draw the window of the game. Using the blit function, the background image and the other two ships are loaded in the same window. 
def window(red, white, red_laser, white_laser, red_health, white_health):
  screen.blit(space_bg, (0, 0))
  pygame.draw.rect(screen, Blue, boundary)
  
  #setting up the string for the ships health and their positioning in the screen.
  red_health_txt = health_font.render("Red Health: " + str(red_health), 2, Red)
  white_health_txt = health_font.render("White Health: " + str(white_health), 2, White)
  
  screen.blit(red_health_txt, (width - red_health_txt.get_width() - 85, 2))
  screen.blit(white_health_txt, (70, 2))

  screen.blit(white_ship, (white.x, white.y))
  screen.blit(red_ship, (red.x, red.y))

  for laser in red_laser:
    pygame.draw.rect(screen, Red, laser)

  for laser in white_laser:
    pygame.draw.rect(screen, White, laser)

  pygame.display.update()

# creating a function for the white ship to move using the keys AWSD for the movement
def white_ctrls(pressed_keys, white):
  if pressed_keys[pygame.K_a] and white.x - vel > 0:  # LEFT
    white.x -= vel
  if pressed_keys[pygame.K_d] and white.x + vel + white.width < boundary.x:  # RIGHT
    white.x += vel
  if pressed_keys[pygame.K_w] and white.y - vel > 0:  # UP
    white.y -= vel
  if pressed_keys[pygame.K_s] and white.y + vel + white.height < height - 15:  # DOWN
    white.y += vel


# creating a function for the red ship to move using the ARROWS for the movement
def red_ctrls(pressed_keys, red):
  if pressed_keys[pygame.K_LEFT] and red.x - vel > boundary.x + boundary.width:  # LEFT
    red.x -= vel
  if pressed_keys[pygame.K_RIGHT] and red.x + vel + red.width < width:  # RIGHT
    red.x += vel
  if pressed_keys[pygame.K_UP] and red.y - vel > 0:  # UP
    red.y -= vel
  if pressed_keys[pygame.K_DOWN] and red.y + vel + red.height < height - 15:  # DOWN
    red.y += vel

#creating a function so that when either laser hit the ship, the laser will be deleted as it would show the ship was hit. 
def lasers(white_laser, red_laser, white, red):
  for laser in white_laser:
      laser.x += laser_vel
      if red.colliderect(laser):
        pygame.event.post(pygame.event.Event(red_hit))
        white_laser.remove(laser)
      elif laser.x > width:
        white_laser.remove(laser)

  for laser in red_laser:
      laser.x -= laser_vel
      if white.colliderect(laser):
        pygame.event.post(pygame.event.Event(white_hit))
        red_laser.remove(laser)
      elif laser.x < 0:
        red_laser.remove(laser)

#creating a function for the winner of the game. If either one of the players win, big words will pop up in the screen to announce the winner and a delay will also be called to reset the game.
def winner(text):
  draw_text = win_font.render(text, 1, White)
  screen.blit(draw_text, (width/2 - draw_text.get_width() / 2, height/2 - draw_text.get_height()/2))
  pygame.display.update()
  pygame.time.delay(5000)

#creating the last function to call on the other functions and variables.
def main():
  red = pygame.Rect(655, 230, ship_width, ship_height)
  white = pygame.Rect(100, 230, ship_width, ship_height)
  
  red_laser = []
  white_laser = []

  #variables for the ship's health
  red_health = 15
  white_health = 15

  #a while loop to make the window stay open until the user manually closes the program and without it, the progpram will constantly keep on closing.
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(fps)
    for event in pygame.event.get():  
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()

      #if the user presses the space button, the white ship will fire and if the number of laser fired is less than the maxiumum ammo, the ship will reload. The moment either ship hits each other, a quick reload will happen.
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(white_laser) < max_laser:
          laser = pygame.Rect(white.x + white.width, white.y + white.height//2 - 2, 10, 5)
          white_laser.append(laser)

        #if the user presses the right shift button, the red ship will fire and if the number of laser fired is less than the maxiumum ammo, the ship will reload.
        if event.key == pygame.K_RSHIFT and len(red_laser) < max_laser:
          laser = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
          red_laser.append(laser)

      #an if statement for the health to go down by 1 everytime either ships get hit.
      if event.type == red_hit:
        red_health -= 1

      if event.type == white_hit:
        white_health -= 1

    #an if statement to call the winner of the game if one of the ship's health reaches 0.
    winner_text = ""
    if red_health <= 0:
      winner_text = "White Wins!"

    if white_health <= 0:
      winner_text = "Red Wins!"

    if winner_text != "":
        winner(winner_text)
        break

    #calling all the functions that was created.
    pressed_keys = pygame.key.get_pressed()
    white_ctrls(pressed_keys, white)
    red_ctrls(pressed_keys, red)

    lasers(white_laser, red_laser, white, red)

    window(red, white, red_laser, white_laser, red_health, white_health)

  main()


if __name__ == "__main__":
    main()