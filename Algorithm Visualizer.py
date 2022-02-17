import pygame
import random

#used TechWithTim Source code + Video for some things/reference
#https://www.youtube.com/watch?v=twRidO-_vqQ&t=3925s
pygame.init()

class Button():
	#Class to handle buttons, modified from 
	#https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py

	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.text_input = text_input
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.text = self.font.render(self.text_input, True, self.base_color)
		# if we are not using an image for button, the image is the text
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

			#renders the image if we are using an image, and text on top of the image, or
			#just renders the text.
	def render(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

		#returns true if cursor is hovering, and sets colour of text to hovering color
		#returns false if not hovering, sets text color to base color
	def isHovering(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
			return True
		else: 
			self.text = self.font.render(self.text_input, True, self.base_color)
			return False

	
class VisualInfo:
	BGCOLOR = (255, 255, 255) #white
	SIDEPAD = 50 #pad for bars and side of window
	TOPPAD = 200 #pad for bars and top of window

	BLOCKCOLORS = [
		#(255,0,0),
		(255,125,0),
		#(255,255,0),
		(125,255,0),
		(0,255,0),
		(0,255,125),
		(0,255,255),
		#(0,125,255),
		#(0,0,255),
		#(125,0,255),
		#(255,0,255),
		#(255,0,125),
	]


	def __init__(self, width, height, arr):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width,height))
		pygame.display.set_caption("Sorting Algorithm Visualizer")

		self.set_arr(arr)

	def set_arr(self, arr):
		self.arr = arr
		self.max_val = max(arr)
		self.min_val = min(arr)

		self.bar_width = int((self.width - self.SIDEPAD) / len(arr))
		self.height_scale = int((self.height - self.TOPPAD) / self.max_val)

def get_font(size):
	return pygame.font.SysFont('freesansbold.ttf', size)

sortButton = Button(image=None, pos=(100,40), text_input="Sort", font=get_font(70),
		base_color="#000000", hovering_color="#0040c9")
resetButton = Button(image=None, pos=(100,90), text_input="Reset", font=get_font(70),
		base_color="#000000", hovering_color="#0040c9")
bubbleButton = Button(image=None, pos=(1130,85), text_input="Bubble Sort",
		font=get_font(40), base_color="#000000", hovering_color="#0040c9")
insertionButton = Button(image=None, pos=(1130,45), text_input="Insertion Sort",
		font=get_font(40), base_color="#000000", hovering_color="#0040c9")



def generate_array(n, minimum, maximum):
	arr = []

	for _ in range(n):
		temp = random.randint(minimum, maximum)
		arr.append(temp)

	return arr

def draw(visual_info):
	visual_info.window.fill(visual_info.BGCOLOR)


	draw_list(visual_info)
	pygame.display.update()

def draw_buttons(visual_info):
	#DRAW BUTTONS
	mouse_pos = pygame.mouse.get_pos()

	for Button in [sortButton, bubbleButton, insertionButton, resetButton]:
		Button.isHovering(mouse_pos)
		Button.render(visual_info.window)
	pygame.display.update()

def draw_list(visual_info, current_positions={}, isSorting=False):
	arr = visual_info.arr

	if isSorting:
		list_drawing_area_rect = (visual_info.SIDEPAD, visual_info.TOPPAD, visual_info.width - visual_info.SIDEPAD, visual_info.height)
		pygame.draw.rect(visual_info.window, visual_info.BGCOLOR, list_drawing_area_rect)

	for i, val in enumerate(arr):
		#rectangles draw from top left corner, width wide and height high.
		xpos = visual_info.SIDEPAD + i * visual_info.bar_width
		ypos = visual_info.height - (visual_info.height_scale * val)

		#color = visual_info.BLOCKCOLORS[i % 5]
		colorVal = int(val / visual_info.max_val * 200) + 55
		color = (20,colorVal,colorVal/2)

		if i in current_positions:
			color = current_positions[i]
		pygame.draw.rect(visual_info.window, color, (xpos, ypos, visual_info.bar_width, visual_info.height))

	if isSorting:
		pygame.display.update()

def bubble_sort(visual_info):
	arr = visual_info.arr
	n = len(arr)
	for i in range(n -1):
		for j in range(n - 1 - i):
			if (arr[j] > arr[j+1]):
				#swap if j > j+1
				tmp = arr[j+1]
				arr[j+1] = arr[j]
				arr[j] = tmp
				#two lines below from video, shows progress/steps of algorithm
				draw_list(visual_info, {j: (255,0,0), j+1: (0,0,255)}, True)
				yield True  #effectively pauses our function, and then resume it at the same spot
							#this allows us to draw our current
	return arr

def insertion_sort(visual_info):
	arr = visual_info.arr
	n = len(arr)

	for i in range(1, n):
		curr = arr[i]
		j = i -1
		while j >= 0 and curr < arr[j]:
			arr[j+1] = arr[j]
			j-=1
			draw_list(visual_info, {j-1: (255,0,0), j: (0,0,255)}, True)
			yield True
		arr[j+1] = curr
	return arr
					


def main():
	running = True
	clock = pygame.time.Clock()

	n = 125
	min_val = 0
	max_val = 500
	isSorting = False

	algo = bubble_sort
	algo_name = "Bubble Sort"
	algo_generator = None

	numList = generate_array(n, min_val, max_val)
	visual_info = VisualInfo(1280, 720, numList)
	draw(visual_info)
	while running:
		clock.tick(100)
		draw_buttons(visual_info)
		mouse_pos = pygame.mouse.get_pos()

		#from video
		if isSorting:
			try:
				next(algo_generator)
			except StopIteration:
				isSorting = False
			#else: 
				draw_list(visual_info)

		
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if sortButton.isHovering(mouse_pos) and not isSorting:
					isSorting = True
					algo_generator = algo(visual_info)
				if resetButton.isHovering(mouse_pos):
					isSorting = False
					numList = generate_array(n, min_val, max_val)
					visual_info = VisualInfo(1280,720, numList)
					draw(visual_info)
				if bubbleButton.isHovering(mouse_pos):
					algo = bubble_sort
					algo_name = "Bubble Sort"
				if insertionButton.isHovering(mouse_pos):
					algo = insertion_sort
					algo_name = "Insertion Sort"

				


if __name__ == "__main__":
	main()
