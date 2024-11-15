#!/usr/bin/python3
#
# Copyright (c) 2020 Wade Brainerd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pygame
pygame.font.init()
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

RADIUS = 100


class TestGame:

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.paused = False
        # Quiz specific attributes
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "correct": 1
            },
            {
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Mars", "Mercury", "Jupiter"],
                "correct": 2
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            }
        ]
        self.current_question = 0
        self.score = 0
        self.selected_option = None
        self.font = pygame.font.Font(None, 36)
    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    def handle_click(self, pos):
        if self.current_question >= len(self.questions):
            return
    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()
        width = screen.get_width()
        height = screen.get_height()

        dirty = []
        dirty.append(pygame.draw.rect(screen, (255, 255, 255),
                                      pygame.Rect(0, 0, width, height)))
        pygame.display.update(dirty)

        while self.running:
            dirty = []

            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    width = screen.get_width()
                    height = screen.get_height()
                    dirty.append(pygame.draw.rect(screen, (255, 255, 255),
                                                  pygame.Rect(0, 0,
                                                              width, height)))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            # Clear screen
            screen.fill((255, 255, 255))
            

            self.draw_question(screen)

            pygame.display.flip()
            self.clock.tick(30)
            # Update Display
    def draw_question(self, screen):
        question = self.questions[self.current_question]
        
        # Draw question
        question_surface = self.font.render(question["question"], True, (0, 0, 0))
        screen.blit(question_surface, (50, 50))
        
        # Draw options
        for i, option in enumerate(question["options"]):
            color = (200, 200, 200) if i == self.selected_option else (150, 150, 150)
            pygame.draw.rect(screen, color, (50, 150 + i * 60, 400, 40))
            option_surface = self.font.render(option, True, (0, 0, 0))
            screen.blit(option_surface, (60, 160 + i * 60))
# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = TestGame()
    game.run()


if __name__ == '__main__':
    main()
