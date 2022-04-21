import pygame
ora = [60, 60, 60]
pygame.init()
screen = pygame.display.set_mode()
x, y = screen.get_size()
running = True
text = '$'
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 50)
def seecl(n1):
    global b
    while pygame.mouse.get_pressed()[0]:
        pass
    n2 = pygame.mouse.get_pos()
    x, y = n1[0] - n2[0], n1[1] - n2[1]
    d = 1.5
    if y < 0 and abs(x) < abs(d * y):
        return 'v'
    elif y > 0 and abs(x) < abs(d * y):
        return 'u'
    elif x > 0 and abs(x) > abs(d * y):
        return '<'
    elif x < 0 and abs(x) > abs(d * y):
        return '>'
    else:
        return f'{x} {y}'
while running:
    screen.fill(ora)
    for event in pygame.event.get():
    	pos = pygame.mouse.get_pos()
    	if event.type == pygame.MOUSEBUTTONDOWN:
    	    text = seecl(pos)
    texte = font.render(text, True, [100, 255, 100])
    textpose = (50, 810)
    screen.blit(texte, textpose)
    pygame.display.flip()