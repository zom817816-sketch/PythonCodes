# 迷宫搜索程序 - 使用递归和深度优先搜索

from turtle import Turtle, done, setup, setworldcoordinates, tracer

# 定义迷宫中的常量
OBSTACLE = "+"  # 墙
START = "S"  # 起点
TRIED = "."  # 已经尝试过的格子
PART_OF_PATH = "O"  # 路径的一部分
DEAD_END = "-"  # 死胡同


def searchFrom(maze, startRow, startColumn):
    """
    使用深度优先搜索算法在迷宫中寻找路径
    """
    # 首先检查是否越界
    if (
        startRow < 0
        or startRow >= maze.rowsInMaze
        or startColumn < 0
        or startColumn >= maze.columnsInMaze
    ):
        return False

    maze.updatePosition(startRow, startColumn)

    # 遇到墙
    if maze[startRow][startColumn] == OBSTACLE:
        return False

    # 遇到已经走过的格子
    if maze[startRow][startColumn] == TRIED:
        return False

    # 遇到死胡同标记
    if maze[startRow][startColumn] == DEAD_END:
        return False

    # 遇到出口（在边界上且不是起点）
    if maze.isExit(startRow, startColumn):
        if maze[startRow][startColumn] != START:
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
            return True

    # 标记当前位置为已尝试
    maze.updatePosition(startRow, startColumn, TRIED)

    # 递归尝试四个方向：北、南、西、东
    found = (
        searchFrom(maze, startRow - 1, startColumn)  # 北
        or searchFrom(maze, startRow + 1, startColumn)  # 南
        or searchFrom(maze, startRow, startColumn - 1)  # 西
        or searchFrom(maze, startRow, startColumn + 1)
    )  # 东

    # 根据搜索结果标记当前位置
    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)

    return found


class Maze:
    def __init__(self, mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []

        # 从文件读取迷宫 - 修复换行符处理
        with open(mazeFileName, "r") as mazeFile:
            lines = mazeFile.readlines()

        # 处理每一行，统一长度
        max_len = max(len(line.rstrip("\n").rstrip("\r")) for line in lines)

        for line in lines:
            # 修复：正确处理Windows和Unix换行符
            line = line.rstrip("\n").rstrip("\r")
            # 统一行长度，短行补空格
            if len(line) < max_len:
                line = line + " " * (max_len - len(line))
            rowList = list(line)
            col = 0
            for ch in rowList:
                if ch == START:
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze

        # 设置坐标转换
        self.xTranslate = -columnsInMaze / 2
        self.yTranslate = rowsInMaze / 2

        # 初始化乌龟图形
        self.t = Turtle(shape="turtle")
        setup(width=600, height=600)
        setworldcoordinates(
            -(columnsInMaze - 1) / 2 - 0.5,
            -(rowsInMaze - 1) / 2 - 0.5,
            (columnsInMaze - 1) / 2 + 0.5,
            (rowsInMaze - 1) / 2 + 0.5,
        )

    def drawMaze(self):
        """绘制迷宫的基本结构（只绘制墙）"""
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(
                        x + self.xTranslate, -y + self.yTranslate, "tan"
                    )
        self.t.color("black", "blue")

    def drawCenteredBox(self, x, y, color):
        """在指定位置绘制一个正方形（表示墙）"""
        tracer(0)
        self.t.up()
        self.t.goto(x - 0.5, y - 0.5)
        self.t.color("black", color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()
        tracer(1)

    def moveTurtle(self, col, row):  # 修复：明确参数是(col, row)
        """将乌龟移动到指定位置"""
        self.t.up()
        self.t.setheading(self.t.towards(col + self.xTranslate, -row + self.yTranslate))
        self.t.goto(col + self.xTranslate, -row + self.yTranslate)

    def dropBreadcrumb(self, color):
        """在当前位置放置一个彩色点（面包屑）"""
        self.t.dot(10, color)

    def updatePosition(self, row, col, val=None):
        """更新乌龟位置并标记格子状态"""
        if val:
            self.mazelist[row][col] = val
        self.moveTurtle(col, row)

        # 根据格子状态设置颜色
        if val == PART_OF_PATH:
            color = "green"
        elif val == TRIED:
            color = "black"
        elif val == DEAD_END:
            color = "red"
        elif val == OBSTACLE:
            color = "red"
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self, row, col):
        """检查指定位置是否为出口（在迷宫边界上且不是起点）"""
        return (
            row == 0
            or row == self.rowsInMaze - 1
            or col == 0
            or col == self.columnsInMaze - 1
        )

    def __getitem__(self, index):
        """支持使用maze[row][col]语法访问迷宫格子"""
        return self.mazelist[index]

    def printMaze(self):
        """打印迷宫的文本表示"""
        for row in self.mazelist:
            print("".join(row))


def create_sample_maze():
    """创建示例迷宫文件 - 修复：统一行长度，确保有出口"""
    maze_content = """++++++++++++++++++++++++
+   +   ++ ++        + O
+     +     +++++++ ++ O
+ +    ++  ++++ +++ ++ O
+ +   + + ++    +++  + O
+          ++  ++  + + O
+++++++ + +      ++  + +O
+++++++ +++  + +  ++   +O
+          + + S+ +  + O
+++++++ +  + + +     + O
++++++++++++++++++++++++"""
    with open("maze.txt", "w") as f:
        f.write(maze_content)
    print("已创建示例迷宫文件: maze.txt")


def main():
    """主函数"""
    print("=== 迷宫搜索程序（修复版）===")
    print()

    # 检查迷宫文件是否存在，如果不存在则创建
    try:
        with open("maze.txt", "r"):
            pass
    except FileNotFoundError:
        print("未找到迷宫文件，正在创建示例迷宫...")
        create_sample_maze()

    try:
        # 创建迷宫对象
        print("正在加载迷宫...")
        myMaze = Maze("maze.txt")

        # 绘制迷宫
        print("正在绘制迷宫...")
        myMaze.drawMaze()

        # 显示迷宫信息
        print(f"迷宫大小: {myMaze.rowsInMaze}行 × {myMaze.columnsInMaze}列")
        print(f"起点位置: ({myMaze.startRow}, {myMaze.startCol})")
        print()

        # 从起点开始搜索路径
        print("开始搜索迷宫路径...")
        print("搜索过程中:")
        print("  - 绿色点: 找到的路径")
        print("  - 黑色点: 尝试过的格子")
        print("  - 红色点: 死胡同")
        print()

        result = searchFrom(myMaze, myMaze.startRow, myMaze.startCol)

        print("=" * 40)
        if result:
            print("✓ 成功找到出口！")
        else:
            print("✗ 没有找到出口。")
        print("=" * 40)

        # 显示最终迷宫状态
        print("\n最终迷宫状态:")
        myMaze.printMaze()

        print("\n程序执行完成。")
        print("关闭图形窗口以退出程序。")

        done()  # 修复：添加done()保持窗口打开

    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
