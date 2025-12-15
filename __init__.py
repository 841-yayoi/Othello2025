# Generation ID: Hutch_1765783050952_vxkyyec4j (前半)

def OthelloAI(board, Color):
    """
    オセロAIのメイン関数
    ゲーム木を使ってミニマックスアルゴリズムで最適な手を探索
    """
    
    def is_valid_move(b, col, row, color):
        if b[row][col] != 0:
            return False
        
        opponent = 3 - color
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dx, dy in directions:
            x, y = col + dx, row + dy
            found_opponent = False
            
            while 0 <= x < len(b) and 0 <= y < len(b):
                if b[y][x] == 0:
                    break
                if b[y][x] == opponent:
                    found_opponent = True
                elif b[y][x] == color:
                    if found_opponent:
                        return True
                    break
                x += dx
                y += dy
        
        return False
    
    def get_valid_moves(b, color):
        moves = []
        for row in range(len(b)):
            for col in range(len(b[0])):
                if is_valid_move(b, col, row, color):
                    moves.append((col, row))
        return moves
    
    def apply_move(b, col, row, color):
        new_board = [row[:] for row in b]
        new_board[row][col] = color
        opponent = 3 - color
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dx, dy in directions:
            x, y = col + dx, row + dy
            flip_list = []
            
            while 0 <= x < len(new_board) and 0 <= y < len(new_board):
                if new_board[y][x] == 0:
                    break
                if new_board[y][x] == opponent:
                    flip_list.append((x, y))
                elif new_board[y][x] == color:
                    for fx, fy in flip_list:
                        new_board[fy][fx] = color
                    break
                x += dx
                y += dy
        
        return new_board
    
    def evaluate(b, color):
        ai_count = sum(row.count(color) for row in b)
        opponent_count = sum(row.count(3 - color) for row in b)
        
        corner_weight = 25
        edge_weight = 5
        corners = [(0,0), (0,len(b)-1), (len(b)-1,0), (len(b)-1,len(b)-1)]
        
        score = ai_count - opponent_count
        
        for c, r in corners:
            if b[r][c] == color:
                score += corner_weight
            elif b[r][c] == 3 - color:
                score -= corner_weight
        
        return score
    
    def minimax(b, depth, is_maximizing, alpha, beta, color):
        if depth == 0:
            return evaluate(b, color), None
        
        opponent = 3 - color
        current_player = color if is_maximizing else opponent
        valid_moves = get_valid_moves(b, current_player)
        
        if not valid_moves:
            opponent_moves = get_valid_moves(b, opponent)
            if not opponent_moves:
                return evaluate(b, color), None
            return minimax(b, depth - 1, not is_maximizing, alpha, beta, color)
        
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            for col, row in valid_moves:
                new_board = apply_move(b, col, row, current_player)
                eval_score, _ = minimax(new_board, depth - 1, False, alpha, beta, color)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (col, row)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for col, row in valid_moves:
                new_board = apply_move(b, col, row, current_player)
                eval_score, _ = minimax(new_board, depth - 1, True, alpha, beta, color)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (col, row)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    valid_moves = get_valid_moves(board, Color)
    if not valid_moves:
        return None
    
    search_depth = 6 if len(board) == 6 else 5
    _, best_move = minimax(board, search_depth, True, float('-inf'), float('inf'), Color)
    
    return best_move

# Generation ID: Hutch_1765783050952_vxkyyec4j (後半)

