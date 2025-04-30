import pygame
import time
from slime_volleyball import SlimeVolleyball
from algorithms import GameAI

def main():
    # Initialize game
    env = SlimeVolleyball()
    ai = GameAI(env)
    
    # Game loop
    running = True
    clock = pygame.time.Clock()
    
    # Record games
    env.start_recording()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Get current state
        state = env.get_state()
        
        # Get AI actions
        player_action = ai.get_best_action(state, use_alpha_beta=True)  # Use alpha-beta for player
        opponent_action = ai.get_best_action(state, use_alpha_beta=False)  # Use minimax for opponent
        
        # Apply actions
        env.apply_action(player_action, is_player=True)
        env.apply_action(opponent_action, is_player=False)
        
        # Update game state
        env.update()
        
        # Render
        env.render()
        
        # Control game speed
        clock.tick(60)
        
        # Check if game should end
        if env.score[0] >= 5 or env.score[1] >= 5:
            time.sleep(2)  # Pause to show final score
            env.reset()
            
    # Stop recording and save video
    env.stop_recording("slime_volleyball_gameplay.mp4")
    env.close()
    
if __name__ == "__main__":
    main() 