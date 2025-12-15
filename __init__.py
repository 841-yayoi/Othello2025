# Generation ID: Hutch_1764572450193_s8obrz7mb (前半)

def myai(board, Color):
    """
    オセロAIの主関数
    board: ゲーム盤の状態(2次元配列)
    Color: AIの色(2=白)
    return: (column, row)の形式で最適な手を返す
    """
    size = len(board)
    best_move = None
    best_score = float('-inf')

    # 合法手をすべて列挙
    for row in range(size):
        for col in range(size):
            if is_legal_move(board, row, col, Color):
                # 手を試す
                new_board = apply_move(board, row, col, Color)
                # ゲーム木を探索(深さ6)
                score = minimax(new_board, 6, False, Color, float('-inf'), float('inf'))

                if score > best_score:
                    best_score = score
                    best_move = (col, row)

    return best_move if best_move else (0, 0)


def minimax(board, depth, is_maximizing, ai_color, alpha, beta):
    """
    ゲーム木探索(アルファベータ枝刈り)
    """
    size = len(board)
    opponent_color = 3 - ai_color  # 1なら2、2なら1

    # 終了条件
    if depth == 0:
        return evaluate_board(board, ai_color)

    if is_maximizing:
        max_eval = float('-inf')
        has_move = False

        for row in range(size):
            for col in range(size):
                if is_legal_move(board, row, col, ai_color):
                    has_move = True
                    new_board = apply_move(board, row, col, ai_color)
                    eval_score = minimax(new_board, depth - 1, False, ai_color, alpha, beta)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        return max_eval

        return max_eval if has_move else evaluate_board(board, ai_color)

    else:
        min_eval = float('inf')
        has_move = False

        for row in range(size):
            for col in range(size):
                if is_legal_move(board, row, col, opponent_color):
                    has_move = True
                    new_board = apply_move(board, row, col, opponent_color)
                    eval_score = minimax(new_board, depth - 1, True, ai_color, alpha, beta)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        return min_eval

        return min_eval if has_move else evaluate_board(board, ai_color)


def is_legal_move(board, row, col, color):
    """合法手かチェック"""
    size = len(board)
    if board[row][col] != 0:
        return False

    opponent = 3 - color
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < size and 0 <= c < size:
            if board[r][c] == 0:
                break
            if board[r][c] == opponent:
                found_opponent = True
            elif board[r][c] == color and found_opponent:
                return True
            else:
                break
            r += dr
            c += dc

    return False


def apply_move(board, row, col, color):
    """手を適用して新しい盤を返す"""
    size = len(board)
    new_board = [row[:] for row in board]
    new_board[row][col] = color

    opponent = 3 - color
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flip_list = []

        while 0 <= r < size and 0 <= c < size and new_board[r][c] == opponent:
            flip_list.append((r, c))
            r += dr
            c += dc

        if 0 <= r < size and 0 <= c < size and new_board[r][c] == color and flip_list:
            for fr, fc in flip_list:
                new_board[fr][fc] = color

    return new_board


def evaluate_board(board, ai_color):
    """盤面を評価"""
    size = len(board)
    ai_count = sum(row.count(ai_color) for row in board)
    opponent_count = sum(row.count(3 - ai_color) for row in board)

    # 隅の価値が高い
    corner_bonus = 0
    for r, c in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
        if board[r][c] == ai_color:
            corner_bonus += 10
        elif board[r][c] == 3 - ai_color:
            corner_bonus -= 10

    return (ai_count - opponent_count) * 10 + corner_bonus

# Generation ID: Hutch_1764572450193_s8obrz7mb (後半)
