# Lucas Reicher 2021
# Written over several days during vacation

import random

class Solitaire:
	def __init__(self):
		self.restart()

	def restart(self):
		random_deck = self.get_random_deck()
		self.board = [ [(None, -1)] * 19 for i in range(7)]
		self.completed = [[] for i in range(4)]
		self.has_won = False
		self.can_win = False
		self.num_moves = 0

		# Initialize starting setup
		for n in range(7):
			for i in range(n+1):
				card = random_deck.pop()
				self.board[n][i] = (card, 1) if n == i else (card, 0)

		# Store remaining cards in deck and begin game loop
		self.deck = random_deck
		self.deck_index = 0
		self.loop_until_end()


	def loop_until_end(self):
		playing = True
		while playing:
			self.print_board()
			if self.check_for_soft_win():
				self.can_win = True
				result = self.handle_move(input("Enter Move (auto-win 'a'): "))
			else: result = self.handle_move(input("Enter Move: "))
			if result == 0:
				print("Move Failed")
			elif result == 1:
				self.num_moves += 1
				print("Move Successful")
			elif result == -1:
				print("Good Bye")
				quit()
			self.update_board()
			if self.check_for_win():
				print("You won!")
				playing = False
		print("Game Over")
		self.restart()


	def print_board(self):
		print("   0     1     2     3     4     5     6")
		print("_" * 43)
		for i in range(19):
			row = ""
			for n in range(7):
				if self.board[n][i][1] == 1:
					card = self.get_card_string(self.board[n][i][0])
					row += ("| " + card + " ")
				elif self.board[n][i][1] == 0:
					row += "| /?/ "
				else:
					row += "|     "
			row += "|  " + str(i)
			if i == 0:
				row += "         Deck Card:"
			elif i == 1:
				if len(self.deck) > 0:
					deck_card = self.get_card_string(self.deck[self.deck_index])
					deck_length = len(self.deck)
					cards_left = deck_length - (self.deck_index + 1)
				else:
					deck_card = "XXX"
					deck_length = 0
					cards_left = 0
				row += "      " + deck_card + " - /?/ (" + str(self.deck_index + 1) + "/" + str(deck_length) + ")"
			elif i == 4:
				row += "		 Stacks"
			elif i == 5:
				if len(self.completed[0]) > 0:
					row += "	   	 q. " + self.get_card_string(self.completed[0][-1])
				else:
					row += "	   	 q. 00\u2664"
			elif i == 6:
				if len(self.completed[1]) > 0:
					row += "	   	 w. " + self.get_card_string(self.completed[1][-1])
				else:
					row += "	   	 w. 00\u2665" 
			elif i == 7:
				if len(self.completed[2]) > 0:
					row += "	   	 e. " + self.get_card_string(self.completed[2][-1])
				else:
					row += "	   	 e. 00\u2667"
			elif i == 8:
				if len(self.completed[3]) > 0:
					row += "	   	 r. " + self.get_card_string(self.completed[3][-1])
				else:
					row += "	   	 r. 00\u2666"
			elif i == 11:
				row += "		 Moves"
			elif i == 12:
				row += "		   " + str(self.num_moves)
			elif i == 15:
				row += "       Instructions"
			elif i == 16:
				row += "		  '?'"
			elif i == 18:
				row += "       Restart: 'r'\n" + "\u203E" * 43
			print(row)


	def handle_move(self, move):
		if ":" in move:
			instructions = move.split(":")
			if len(instructions[1]) > 1:
				return 0
			if "d" in instructions[0]:
				if instructions[1] == "":
					return self.deck_to_completed()
				elif instructions[1].isnumeric() and (0 <= int(instructions[1]) <= 6):
					return self.deck_to_board(instructions)
				else:
					return 0
			elif instructions[1] == "" and instructions[0].isnumeric() and (0 <= int(instructions[0]) <= 6):
				return self.board_to_completed(instructions)
			elif "," in instructions[0]:
				column,row = instructions[0].split(",")
				if column.isnumeric() and row.isnumeric() and (0<= int(column) <= 6) and (0 <= int(row) <= 18):
					from_column = self.board[int(column)]
					to_column = self.board[int(instructions[1])]
					return self.board_to_board_multiple(column, row, to_column)
				else:
					return 0
			elif not instructions[0].isnumeric() and instructions[1].isnumeric() and (0 <= int(instructions[1]) <= 6):
				return self.completed_to_board(instructions)
			elif instructions[0].isnumeric() and instructions[1].isnumeric() and (0 <= int(instructions[0]) <= 6) and (0 <= int(instructions[1]) <= 6):
				return self.board_to_board_single(instructions)
			else:
				return 0
		elif move == "d" and len(self.deck) > 0:
			self.deck_index = ((self.deck_index+1) % len(self.deck))
			return 1
		elif move == "r":
			self.restart()
		elif move == "?":
			self.display_instructions()
		elif move == "a" and self.can_win:
			self.has_won = True
		elif move == "quit":
			return -1
		else: return 0


	def update_board(self):
		for n in range(7):
			for i in range(n):
				card = self.board[n][i]
				if card[1] == 0 and self.board[n][i+1][1] == -1:
					card = (card[0],1)
					self.board[n][i] = card


	def get_card_string(self, card):
		suits = ['\u2664','\u2665','\u2667','\u2666']
		cards = [" A", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K"]
		card = cards[card[0]-1] + suits[card[1]]
		return card


	def get_random_deck(self):
		deck = [(x,y) for x in range(1,14) for y in range(4)]
		random.shuffle(deck)
		return deck				


	def get_top_card(self, column):
		top_index = -1
		top_card = None
		for i in range(len(column)):
			if column[i][1] == 1:
				top_index = i
				top_card = column[i][0]
				return top_index, top_card
		return top_index,top_card


	def get_bottom_card(self, column):
		bottom_index = -1
		bottom_card = None
		for i in range(len(column)):
			if column[i][1] == -1:
				bottom_index = i - 1
				if bottom_index >= 0:
					bottom_card = column[bottom_index][0]
				return bottom_index, bottom_card
		return bottom_index, bottom_card


	def get_column_stack(self, column, row=None):
		cards = []
		for i in range(len(column)):
			if row is not None:
				if i >= row and column[i][1] > 0:
					cards.append(column[i])
			else:
				if column[i][1] > 0:
					cards.append(column[i])
		return cards


	def board_to_board_multiple(self, instructions):
		from_card = from_column[from_index]
		# check that this card is visible
		if from_card[1] != 1:
			return 0
		else: from_card = from_card[0]
		to_index, to_card = self.get_bottom_card(to_column)
		cards_to_move = self.get_column_stack(from_column, from_index)
		if self.valid_move(to_card, from_card):
			for i in range(len(cards_to_move)):
				to_column[to_index+i+1] = cards_to_move[i]
				from_column[from_index+i] = (None, -1)
			return 1
		else: return 0


	def board_to_board_single(self, instructions):
		# All cards lower than selected card to lowest position
		from_column = self.board[int(instructions[0])]
		to_column = self.board[int(instructions[1])]
		from_index, from_card = self.get_top_card(from_column)
		to_index, to_card = self.get_bottom_card(to_column)
		cards_to_move = self.get_column_stack(from_column)
		if self.valid_move(to_card, from_card):
			for i in range(len(cards_to_move)):
				to_column[to_index+i+1] = cards_to_move[i]
				from_column[from_index+i] = (None, -1)
			return 1
		else: return 0


	def board_to_completed(self, instructions):
		from_column = self.board[int(instructions[0])]
		# Single Lowest Card
		from_index, from_card = self.get_bottom_card(from_column)
		from_suit = from_card[1]
		if self.valid_stack(from_card):
			self.completed[from_suit].append(from_card)
			from_column[from_index] = (None, -1)
			return 1
		else: return 0


	def deck_to_board(self, instructions):
		# Single Card to Lowest Position
		to_column = self.board[int(instructions[1])]
		if len(self.deck) <= 0:
			return 0
		from_card = self.deck[self.deck_index]
		to_index, to_card = self.get_bottom_card(to_column)
		if self.valid_move(to_card, from_card):
			to_column[to_index+1] = (from_card, 1)
			self.deck.remove(from_card)
			if len(self.deck) > 0:
				self.deck_index = ((self.deck_index-1) % len(self.deck))
			else: self.deck_index = -1
			return 1
		else: return 0
		

	def deck_to_completed(self):
		# Single Card to Lowest Position
		if len(self.deck) <= 0:
			return 0
		from_card = self.deck[self.deck_index]
		from_suit = from_card[1]
		if self.valid_stack(from_card):
			self.completed[from_suit].append(from_card)
			self.deck.remove(from_card)
			if len(self.deck) > 0:
				self.deck_index = ((self.deck_index-1) % len(self.deck))
			else: self.deck_index = -1
			return 1
		else: return 0


	def completed_to_board(self, instructions):
		# Single Card to Lowest Position
		keys = {"q":0, "w":1, "e":2, "r":3}
		to_column = self.board[int(instructions[1])]
		suit = keys.get(instructions[0])
		if suit is None or len(self.completed[suit]) <= 0:
			return 0
		from_card = self.completed[suit][-1]
		to_index, to_card = self.get_bottom_card(to_column)
		if self.valid_move(to_card, from_card):
			to_column[to_index+1] = (from_card, 1)
			self.completed[suit].pop()
			return 1
		else: return 0


	def valid_move(self, bottom_card, top_card):
		# if bottom card is empty and top card is a King it is a valid move
		if bottom_card is None:
			return top_card[0] == 13
		# if bottom card value is +1 and suit is not same color it is a valid move
		return (bottom_card[0] == top_card[0] + 1) and (bottom_card[1]%2 != top_card[1]%2)


	def valid_stack(self, card):
		suit = card[1]
		if len(self.completed[suit]) > 0:
			return self.completed[suit][-1][0] + 1 == card[0]
		else:
			return card[0] == 1


	def check_for_win(self):
		if self.has_won:
			return 1
		for completes in self.completed:
			if len(completes) != 13:
				return 0
		return 1


	def check_for_soft_win(self):
		for column in self.board:
			for card in column:
				if card[1] == 0:
					return 0
		return 1


	def display_instructions(self):
		print("Instructions...")
		print("Moves are denoted by the form: from:to")
		print("")
		print("                     -from-")
		print("")
		print("Use 0-6 to denote columns. Specify specific rows using a comma.")
		print("    - i.e. 3:    -> top card in column-3 and below")
		print("    - i.e. 3,2:  -> column-3 row-2 and below")
		print("Use d to denote the deck")
		print("    - i.e. d:2   -> deck card to bottom card of column 2")
		print("Use q,w,e,r to denote the stacks")
		print("    - i.e. q:4   -> top of spades stack to column 4")
		print("")
		print("                      -to-")
		print("")
		print("Use 0-6 to denote columns like before.")
		print("    - i.e. 3:4   -> top card in column-3 to bottom card in column-4")
		print("    - i.e. 3,2:4 -> column-3 row-2 and below to botom card in column 4")
		print("Ommitting 'to' attempts to move card to stacks")
		print("    - i.e. 3:    -> bottom card in column-3 to stack of same suit")
		print("    - i.e. d:    -> deck card to stack of same suit")
		print("")
		input("Press Enter to Exit Instructions")
		print("")


if __name__ == '__main__':
	Solitaire = Solitaire()