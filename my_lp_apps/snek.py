#!/usr/bin/env python
#
# Attempting to create a snake game on the launchpad

import sys
import random
from pygame import time
from collections import deque

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad.py")



bounds = {7, 7}

def main():

	mode = None

	lp = launchpad.LaunchpadLPX()
	if lp.Open( 1, "lpx" ):
		print("Launchpad X")
		mode = "Pro"


	butLast  = -1
	butCount = 0

	board = Board(lp)
	snake = Snake(0, 0)

	while True:
		buts = lp.ButtonStateRaw()


class LP_int:
	#Interface between game logic and launchpad

	def __init__(self,lp):
		self.lp = lp

	def clear(self):
		#todo
		#clear all lights on board

	def illuminate(self, coords, color):
		#todo
		#light up a specific square with white
		#this will have to translate game friendly coordinates to launchpad friendly pad values




class Snake:
	body = deque()
	direction = "right"

	def __init__(self, x, y):
		self.head = [x, y]
		self.body.append(self.head)

	def change_dir(self,direction):
		self.direction = direction

	def move(self, is_eating):
		if self.direction == "up":
			self.head[1] = self.head[1] - 1
			if self.head[1] == -1:
				self.head[1] = 7
		elif self.direction == "down":
			self.head[1] = (self.head[1] + 1) % 8
		elif self.direction == "left":
			self.head[0] = self.head[0] - 1
			if self.head[0] == -1:
				self.head[0] = 7
		elif self.direction == "right":
			self.head[0] = (self.head[0] + 1) % 8
		else:
			print("invalid direction passed")

		#removes the last piece from the tail of the snake unless the snake is eating,
		#in which case the new head is added, but the tail does not shorten, making the snake grow
		if not is_eating:
			self.body.popleft()

		#adds our new head to the snake body
		self.body.append(self.head)



class Board:
	apple = [7, 7]
	snake = Snake(0, 0)
	lp_int =  LP_int()


	def place_apple(self):
		#place apple in a random location
		x = random.randint(0, 7)
		y = random.randint(0, 7)
		self.apple = [x, y]

		#if apple happens to fall within the snake body, this function will call itself again until it does not.
		for i in self.snake.body:
			if i == self.apple:
				self.place_apple()

	def draw(self):
		#clear the board
		self.lp_int.clear()

		#light up snake body and apple
		for i in self.snake.body:
			self.lp_int.illuminate(i, "green")
		self.lp_int.illuminate(self.apple, "white")


	def check_eating(self):
		#if head and apple are in the same place, return true
		if self.snake.head == self.apple:
			return True
		else:
			return False

	def check_collision(self):
		#if head is in the same place as another body part, return true
		for i in range(len(self.snake.body)-1):
			if self.snake.head == self.snake.body[i]:
				return True
		return False

	def disp_game_over(self):
		for x in range(7):
			for y in range(7):
				self.lp_int.illuminate([x,y], "red")

main()