local function valid_position(r, c, grid)
    return r > 0 and r <= #grid and c > 0 and c <= #grid[1]
end

local function part_1()
    local file = io.open("input.txt", "r")
    if not file then return nil end

    local grid = {}

    for line in file:lines() do
        local chars = {}
        for char in line:gmatch(".") do
            table.insert(chars, char)
        end
        table.insert(grid, chars)
    end

    local directions = {
        {-1,-1}, {-1,0}, {-1,1},
        {0,-1},          {0,1},
        {1,-1},  {1,0},  {1,1}
    }

    local result = 0

    for row = 1, #grid do
        for col = 1, #grid[1] do
            if grid[row][col] ~= "X" then goto continue end

            for _, dir in ipairs(directions) do
                local dr, dc = dir[1], dir[2]

                local r1, c1 = row + dr, col + dc
                local r2, c2 = row + 2 * dr, col + 2 * dc
                local r3, c3 = row + 3 * dr, col + 3 * dc

                if valid_position(r3, c3, grid) and
                   grid[r1][c1] == "M" and
                   grid[r2][c2] == "A" and
                   grid[r3][c3] == "S" then
                    result = result + 1
                end
            end

            ::continue::
        end
    end

    return result
end

local function part_2()
    local file = io.open("input.txt", "r")
    if not file then return nil end

    local grid = {}

    for line in file:lines() do
        local chars = {}
        for char in line:gmatch(".") do
            table.insert(chars, char)
        end
        table.insert(grid, chars)
    end

    local result = 0

    for row = 1, #grid do
        for col = 1, #grid[1] do
            if grid[row][col] ~= "A" then goto continue end

            if not valid_position(row + 1, col, grid) or not valid_position(row - 1, col, grid) then
                goto continue
            end

            if grid[row - 1][col - 1] == "M" and grid[row - 1][col + 1] == "S" and grid[row + 1][col - 1] == "M" and grid[row + 1][col + 1] == "S" then
                result = result + 1
            end

            if grid[row - 1][col - 1] == "M" and grid[row - 1][col + 1] == "M" and grid[row + 1][col - 1] == "S" and grid[row + 1][col + 1] == "S" then
                result = result + 1
            end

            if grid[row - 1][col - 1] == "S" and grid[row - 1][col + 1] == "M" and grid[row + 1][col - 1] == "S" and grid[row + 1][col + 1] == "M" then
                result = result + 1
            end

            if grid[row - 1][col - 1] == "S" and grid[row - 1][col + 1] == "S" and grid[row + 1][col - 1] == "M" and grid[row + 1][col + 1] == "M" then
                result = result + 1
            end

            ::continue::
        end
    end

    return result
end

local function run(fun)
    local start = os.clock()
    local result = fun()
    local duration = math.floor((os.clock() - start) * 1e9)
    print(string.format("(%d): %s", duration, result))
end

io.write("part_1 ")
run(part_1)
io.write("part_2 ")
run(part_2)
