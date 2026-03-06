import pygame

# 1. Sozlamalar
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8
COLORS = [pygame.Color(235, 235, 208), pygame.Color(119, 148, 85)] 

UNICODE_PIECES = {
    'wK': '♚', 'wQ': '♛', 'wR': '♜', 'wB': '♝', 'wN': '♞', 'wP': '♟',
    'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟'
}

board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--"]*8, ["--"]*8, ["--"]*8, ["--"]*8,
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

def is_path_clear(start, end, cur_board):
    r1, c1 = start; r2, c2 = end
    dr = 1 if r2 > r1 else (-1 if r2 < r1 else 0)
    dc = 1 if c2 > c1 else (-1 if c2 < c1 else 0)
    curr_r, curr_c = r1 + dr, c1 + dc
    while (curr_r, curr_c) != (r2, c2):
        if cur_board[curr_r][curr_c] != "--": return False
        curr_r += dr; curr_c += dc
    return True

def is_valid_move_logic(p, start, end, cur_board):
    r1, c1 = start; r2, c2 = end
    if cur_board[r2][c2] != "--" and cur_board[r2][c2][0] == p[0]: return False
    type = p[1]
    if type == 'P':
        dir = -1 if p[0] == 'w' else 1
        if c1 == c2 and cur_board[r2][c2] == "--":
            if r2 == r1 + dir: return True
            if ((r1==6 and p[0]=='w') or (r1==1 and p[0]=='b')) and r2==r1+2*dir:
                return cur_board[r1+dir][c1] == "--"
        if abs(c1-c2) == 1 and r2 == r1 + dir and cur_board[r2][c2] != "--": return True
    elif type == 'N': return (abs(r1-r2), abs(c1-c2)) in [(2,1), (1,2)]
    elif type == 'R':
        if r1 == r2 or c1 == c2: return is_path_clear(start, end, cur_board)
    elif type == 'B':
        if abs(r1-r2) == abs(c1-c2): return is_path_clear(start, end, cur_board)
    elif type == 'Q':
        if r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2): return is_path_clear(start, end, cur_board)
    elif type == 'K': return abs(r1-r2) <= 1 and abs(c1-c2) <= 1
    return False

def get_king_pos(color, cur_board):
    for r in range(8):
        for c in range(8):
            if cur_board[r][c] == color + 'K': return (r, c)
    return None

def is_in_check(color, cur_board):
    king_pos = get_king_pos(color, cur_board)
    if not king_pos: return False
    opp = 'b' if color == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            if cur_board[r][c].startswith(opp):
                if is_valid_move_logic(cur_board[r][c], (r, c), king_pos, cur_board): return True
    return False

def check_for_checkmate(color):
    for r in range(8):
        for c in range(8):
            if board[r][c].startswith(color):
                for tr in range(8):
                    for tc in range(8):
                        if is_valid_move_logic(board[r][c], (r, c), (tr, tc), board):
                            old = board[tr][tc]; board[tr][tc] = board[r][c]; board[r][c] = "--"
                            safe = not is_in_check(color, board)
                            board[r][c] = board[tr][tc]; board[tr][tc] = old
                            if safe: return False 
    return True 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gemini Chess - Final Masterpiece")
    font = pygame.font.SysFont("Segoe UI Symbol", 65)
    msg_font = pygame.font.SysFont("Arial", 45, bold=True)
    
    selected_sq = (); player_clicks = []; white_to_move = True
    game_over = False; winner_text = ""
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); return
            elif e.type == pygame.MOUSEBUTTONDOWN and not game_over:
                c, r = e.pos[0] // SQ_SIZE, e.pos[1] // SQ_SIZE
                if selected_sq == (r, c): selected_sq = (); player_clicks = []
                else:
                    if not player_clicks:
                        if board[r][c] != "--" and board[r][c][0] == ('w' if white_to_move else 'b'):
                            selected_sq = (r, c); player_clicks.append(selected_sq)
                    else:
                        r1, c1 = player_clicks[0]
                        if is_valid_move_logic(board[r1][c1], (r1, c1), (r, c), board):
                            temp_target = board[r][c]
                            board[r][c] = board[r1][c1]; board[r1][c1] = "--"
                            if not is_in_check('w' if white_to_move else 'b', board):
                                white_to_move = not white_to_move
                                if check_for_checkmate('w' if white_to_move else 'b'):
                                    game_over = True
                                    winner_text = "QORALAR YUTDI!" if white_to_move else "OQLAR YUTDI!"
                            else:
                                board[r1][c1] = board[r][c]; board[r][c] = temp_target
                        selected_sq = (); player_clicks = []

        # Chizish qismi - DIQQAT: OQLAR UCHUN KONTUR SHU YERDA!
        for r in range(8):
            for c in range(8):
                pygame.draw.rect(screen, COLORS[(r+c)%2], (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                if selected_sq == (r, c): pygame.draw.rect(screen, (255, 255, 0), (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)
                if board[r][c] != "--":
                    piece_text = UNICODE_PIECES[board[r][c]]
                    center_pos = (c*SQ_SIZE+SQ_SIZE//2, r*SQ_SIZE+SQ_SIZE//2)
                    if board[r][c][0] == 'w':
                        # 4 tomonga qora kontur chizamiz
                        for dx, dy in [(-1,-1), (1,1), (-1,1), (1,-1)]:
                            out_txt = font.render(piece_text, True, (0,0,0))
                            screen.blit(out_txt, out_txt.get_rect(center=(center_pos[0]+dx, center_pos[1]+dy)))
                        p_color = (255, 255, 255)
                    else:
                        p_color = (0, 0, 0)
                    txt = font.render(piece_text, True, p_color)
                    screen.blit(txt, txt.get_rect(center=center_pos))
        
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)); screen.blit(overlay, (0,0))
            txt_surf = msg_font.render(winner_text, True, (255, 215, 0))
            screen.blit(txt_surf, txt_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()

if __name__ == "__main__": main()